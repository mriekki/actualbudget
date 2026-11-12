#!/usr/bin/env python3
"""Project Forge catalog-bound workstation updates. Status/preview never mutate."""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

TOOL_ID = re.compile(r"^[a-z0-9][a-z0-9-]*$")
VERSION = re.compile(r"(?<!\d)(\d+\.\d+\.\d+)(?!\d)")
PACKAGE_ID = re.compile(r"^[a-zA-Z0-9_.@/+:-]+$")
# Catalog identities alone do not authorize broad workstation upgrades.
SAFE_MANAGER_UPDATE_IDS = frozenset({"rtk", "github-cli", "git", "fnm"})


def platform() -> str:
    return "windows" if sys.platform == "win32" else "macos" if sys.platform == "darwin" else "linux" if sys.platform.startswith("linux") else "unsupported"


def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected object in {path}")
    return value


def run(argv: list[str], timeout: int = 15) -> tuple[int, str]:
    try:
        result = subprocess.run(argv, capture_output=True, text=True, errors="replace", timeout=timeout, check=False)
        return result.returncode, (result.stdout + "\n" + result.stderr).strip()[:1000]
    except (OSError, subprocess.TimeoutExpired) as error:
        return 127, type(error).__name__


def semver(s: str | None) -> tuple[int, int, int] | None:
    match = VERSION.search(s or "")
    return tuple(map(int, match.group(1).split("."))) if match else None


def inventory(root: Path) -> list[dict]:
    env = load(root / "DEV_ENVIRONMENT.json")
    if env.get("schemaVersion") != 1:
        raise ValueError("unsupported DEV_ENVIRONMENT.json schema")
    values: list[dict] = []
    seen = set()
    for item in env.get("tools", []):
        name = item.get("id")
        if not isinstance(name, str) or not TOOL_ID.fullmatch(name) or name in seen:
            raise ValueError(f"unsafe or duplicate declared tool: {name}")
        seen.add(name)
        src = root / "tools/dev-environment/catalog" / (name + ".json")
        if not src.is_file():
            values.append({"id": name, "status": "CATALOG_MISSING", "update": "MANUAL_REVIEW"})
            continue
        data = load(src)
        if data.get("id") != name:
            raise ValueError(f"tool catalog identity mismatch: {name}")
        executable = data.get("command")
        verify = data.get("verifyArgs", ["--version"])
        if not isinstance(executable, str) or not isinstance(verify, list) or not all(isinstance(v, str) for v in verify):
            raise ValueError(f"invalid verification command for {name}")
        path = shutil.which(executable)
        rc, output = run([path, *verify]) if path else (127, "")
        installed = semver(output) if rc == 0 else None
        spec = data.get("install", {}).get(platform(), {})
        spec = spec if isinstance(spec, dict) else {}
        manager = spec.get("manager")
        package = spec.get("package")
        pin = item.get("version")
        update = "MANUAL_REVIEW"
        if pin:
            update = "PROJECT_PINNED"
        elif (rc == 0 and name in SAFE_MANAGER_UPDATE_IDS and
              data.get("category") in ("machine-tool", "runtime-manager") and
              manager in ("winget", "brew") and isinstance(package, str) and PACKAGE_ID.fullmatch(package)):
            update = "MANAGER_CHECK"
        elif rc == 0 and manager == "project-forge-pinned-release":
            expected = semver(spec.get("version"))
            update = "APPROVED_PIN_CURRENT" if installed == expected and expected else (
                "PINNED_RELEASE_UPGRADE" if installed and expected and installed < expected and name == "rtk" else "MANUAL_REVIEW"
            )
        values.append({"id": name, "status": "INSTALLED" if rc == 0 else "NOT_INSTALLED",
                       "installedVersion": ".".join(map(str, installed)) if installed else None,
                       "projectPin": pin, "update": update, "manager": manager, "package": package,
                       "approvedVersion": spec.get("version") if manager == "project-forge-pinned-release" else None})
    return values


def make_plan(root: Path, selected: list[str]) -> dict:
    items = inventory(root)
    candidates = {x["id"]: x for x in items}
    if not selected:
        selected = [v["id"] for v in items if v["update"] in ("MANAGER_CHECK", "PINNED_RELEASE_UPGRADE")]
    if len(selected) != len(set(selected)):
        raise ValueError("duplicate requested tool")
    ops = []
    for name in sorted(selected):
        if name not in candidates:
            raise ValueError(f"undeclared tool {name}")
        item = candidates[name]
        if item["update"] == "MANAGER_CHECK":
            manager = item["manager"]
            if not shutil.which(manager):
                raise ValueError(f"package manager {manager} is missing")
            cmd = ["brew", "upgrade", item["package"]] if manager == "brew" else [
                "winget", "upgrade", "--id", item["package"], "--exact",
                "--accept-source-agreements", "--accept-package-agreements"
            ]
        elif item["update"] == "PINNED_RELEASE_UPGRADE":
            launcher = root / "scripts/setup.sh"
            if platform() != "linux" or not launcher.is_file() or "--update-rtk" not in launcher.read_text(encoding="utf-8"):
                raise ValueError("approved pinned RTK update launcher unavailable; use an updated Bootstrap setup script")
            cmd = ["bash", str(launcher), "--update-rtk"]
        else:
            raise ValueError(f"{name} cannot be automatically updated: {item['update']}")
        ops.append({"id": name, "command": cmd, "fromVersion": item["installedVersion"],
                    "approvedVersion": item["approvedVersion"]})
    plan = {"schemaVersion": 1, "platform": platform(), "operations": ops}
    digest = hashlib.sha256(json.dumps(plan, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return {"plan": plan, "sha256": digest}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["status", "update"])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--tool", action="append", default=[])
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--plan-sha256")
    parser.add_argument("--record-check", action="store_true")
    args = parser.parse_args()
    if args.action == "status" and (args.tool or args.apply or args.plan_sha256):
        parser.error("status is read-only and cannot accept update controls")
    if args.action == "update" and args.record_check:
        parser.error("--record-check applies only to status")
    if args.apply != bool(args.plan_sha256):
        parser.error("apply requires a reviewed --plan-sha256 and vice versa")
    root = args.root.resolve()
    try:
        if args.action == "status":
            result = {"platform": platform(), "tools": inventory(root)}
            marker = root / ".project-forge/setup-maintenance/last-check.json"
            if marker.is_file():
                result["previousCheckUtc"] = load(marker).get("checkedAtUtc")
            if args.record_check:
                marker.parent.mkdir(parents=True, exist_ok=True)
                marker.write_text(json.dumps({"checkedAtUtc": dt.datetime.now(dt.timezone.utc).isoformat()}) + "\n", encoding="utf-8")
            print(json.dumps(result, indent=2))
            return 0
        result = make_plan(root, args.tool)
        if not args.apply:
            print(json.dumps({"mode": "PREVIEW", **result}, indent=2))
            return 0
        if args.plan_sha256 != result["sha256"]:
            raise ValueError("update plan changed; re-preview and reapprove")
        applied = []
        for op in result["plan"]["operations"]:
            code, _ = run(op["command"], timeout=900)
            applied.append({"id": op["id"], "exitCode": code})
            if code:
                print(json.dumps({"mode": "PARTIAL_FAILURE", "applied": applied}, indent=2))
                return 2
        print(json.dumps({"mode": "APPLIED", "applied": applied, "after": inventory(root)}, indent=2))
        return 0
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
