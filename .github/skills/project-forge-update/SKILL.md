---
name: project-forge-update
description: Guided, fail-closed update of already-installed Project Forge Adoption Kit capabilities to the exact accepted Adoption Kit target.
user-invocable: true
disable-model-invocation: true
---

# Project Forge Update

`/project-forge-update` guides an already-adopted repository through a deterministic Project Forge Adoption Kit update without silently changing capabilities or delivering the resulting diff.

The deterministic update engine owns classification, file mutation, baseline refresh, and post-write verification. This skill owns the human interaction around that engine and the post-apply validation/recovery flow.

Invocation starts read-only.

## 1. Confirm this repository is update-capable

Inspect the target repository and require:

- a Git worktree;
- `.github/project-forge-adoption-baseline.json`;
- `.github/project-forge-workspace.json` when present to remain repository-owned and untouched;
- no merge, rebase, cherry-pick, or similar interrupted Git operation; and
- enough repository context to identify the target root unambiguously.

Read the adoption baseline and report the installed Adoption Kit commit, Core commit, and installed capability set.

Do not infer or add capabilities that are absent from `installedCapabilities`.
Do not reconstruct a missing adoption baseline during `/project-forge-update`; a valid recorded baseline is required.

If the repository is already on a `chore/project-forge-update-<sha>` branch with an advanced adoption baseline and a preserved update diff from a prior validation failure, do not rerun apply. Resolve the exact Adoption Kit commit recorded in that baseline and continue with the validation-only recovery path in section 7.

## 2. Resolve a trusted updater source

The updater must come from the exact Adoption Kit commit accepted by authoritative `mriekki/project-forge-adoption-kit` `main` through `ADOPTION_UPDATE_TARGET.json`.

Never execute `installer/update.ps1`, `installer/update.sh`, `installer/validate-update.ps1`, or `installer/validate-update.sh` directly from arbitrary current working-tree bytes.

Source resolution:

1. consider only an explicitly known or nearby local `project-forge-adoption-kit` Git repository; do not perform a broad filesystem scan;
2. use that local repository only when its `origin` resolves to the expected repository, its worktree is clean, no Git operation is in progress, and its current branch/upstream state is not ahead or diverged;
3. if the local repository is dirty, ahead, diverged, ambiguous, or otherwise unsafe, preserve it exactly as-is and obtain the source from GitHub rather than repairing or normalizing it;
4. for a safe local source, refresh/read authoritative `origin/main` without resetting, rebasing, cleaning, stashing, switching, or pulling the local checkout;
5. read `ADOPTION_UPDATE_TARGET.json` from authoritative `main`, resolve its exact `adoptionKitCommit`, and materialize that exact commit into a temporary detached worktree/checkout; or
6. when no usable safe local repository exists, obtain the Adoption Kit from GitHub into temporary state and materialize the same exact accepted commit.

The local repository is only an optimization for obtaining trusted Git objects. It is never update authority and its current working-tree bytes are never executable updater authority.

Do not require the Control Plane.

If authoritative `main`, the accepted commit, or the exact updater script cannot be resolved safely, stop without changing the target repository.

## 3. Run deterministic preview

From the materialized accepted Adoption Kit commit, run the platform-appropriate preview against the target repository:

```powershell
./installer/update.ps1 <target-repository-path>
```

or:

```bash
./installer/update.sh <target-repository-path>
```

The engine owns provenance validation, ancestor validation, candidate construction, and the complete three-way plan.

Present the engine classifications without reinterpreting them:

- `UNCHANGED`
- `UPDATE`
- `ADD`
- `RETIRE`
- `LOCAL_DRIFT`
- `CONFLICT`
- `LOCAL_MISSING`

If preview returns any blocking state or nonzero failure, stop. Do not offer an overwrite/force option and do not modify the target repository.

## 4. Apply gate

Only after a successful complete preview, present one explicit gate:

```text
PROJECT FORGE UPDATE READY

Baseline: <old Adoption Kit SHA>
Accepted target: <accepted Adoption Kit SHA>
Capabilities: <installed capability set>
Plan: <counts for UPDATE / ADD / RETIRE / UNCHANGED>
Blocking states: NONE

1. Apply update [WRITE] — create the Project Forge update branch and apply this exact plan
2. Stop [NO ACTION]
```

The human must explicitly choose the apply action. A preview request alone never authorizes mutation.

If relevant evidence changes after preview—accepted target, target branch/worktree state, baseline bytes, or candidate source—discard the old approval, rerun preview, and present a renewed gate.

## 5. Apply the exact accepted plan

After explicit approval, run the same accepted updater source with apply enabled:

```powershell
./installer/update.ps1 <target-repository-path> -Apply
```

or:

```bash
./installer/update.sh --apply <target-repository-path>
```

Do not manually reproduce the engine's file-copy/delete logic.
Do not bypass a clean-worktree requirement.
Do not create a different branch name or alter the baseline by hand.

The engine is expected to create `chore/project-forge-update-<accepted-sha>`, apply safe `UPDATE`/`ADD`/`RETIRE` operations, refresh `.github/project-forge-adoption-baseline.json`, and verify resulting managed-path hashes.

## 6. Run post-apply validation

After apply succeeds, run the validation-only runner from the same exact accepted Adoption Kit snapshot:

```powershell
./installer/validate-update.ps1 <target-repository-path>
```

or:

```bash
./installer/validate-update.sh <target-repository-path>
```

The validation runner must confirm:

- the current branch is `chore/project-forge-update-<accepted-sha>`;
- the adoption baseline records this exact accepted Adoption Kit commit and its exact Core commit;
- the standard Project Forge adoption validator passes, including baseline schema/integrity and managed-path hashes;
- `.github/project-forge-workspace.json` remains unchanged;
- the resulting installed Project Forge capability surface is present and valid; and
- repository-native validation is run only when the repository explicitly provides the platform-specific hook `.github/project-forge-update-validate.ps1` or `.github/project-forge-update-validate.sh`.

Repository-owned validation hooks are not Adoption Kit-managed files. Run them from the repository root, require a successful exit, and require them to be read-only: if a hook changes the worktree/index, validation fails and the changed state is preserved for diagnosis.

Do not invent an application test command when no hook exists. Report repository-native validation as `NOT CONFIGURED` and continue using the Project Forge validation evidence only.

## 7. Validation failure and recovery

If apply or validation fails, preserve the update branch and exact diff. Do not auto-revert, reset, clean, reapply, commit, push, or continue to delivery.

When file application completed and `.github/project-forge-adoption-baseline.json` already records the accepted candidate, that baseline must remain aligned with the candidate files actually written even if a later validation step fails.

A post-apply validation failure is recoverable without reapplying the update:

1. diagnose/fix only the cause of the failed validation as a separate human-authorized change when needed;
2. materialize the exact Adoption Kit commit recorded in `.github/project-forge-adoption-baseline.json`;
3. rerun only `installer/validate-update.ps1 <target>` or `installer/validate-update.sh <target>` from that exact snapshot; and
4. repeat until validation passes or the human abandons the update branch.

Validation-only recovery does not need a second Apply update gate because it performs no Project Forge file application or baseline advancement.

Do not treat a failed validation as a successful update and do not proceed to Reviewer or `/deliver` until validation passes.

## 8. Stop at meaningful-diff review

After validation passes, inspect and report:

```text
git status --short --branch
git --no-pager diff
```

Use:

```text
PROJECT FORGE UPDATE APPLIED

Branch: <branch>
Baseline: <old Adoption Kit SHA> -> <accepted Adoption Kit SHA>
Plan applied: <UPDATE / ADD / RETIRE counts>
Validation: PASS
Delivery: NOT STARTED

Next: Reviewer -> human meaningful-diff acceptance -> /deliver
```

Do not commit, push, open/update a PR, merge, publish, or deploy as part of `/project-forge-update`.

`/deliver` remains the separate delivery workflow after Reviewer and human meaningful-diff acceptance.

## 9. Boundaries

`/project-forge-update` never:

- reconstructs or backfills missing adoption provenance;
- adds or removes capabilities;
- synchronizes directly from Core to the target repository;
- uses the Control Plane as a prerequisite;
- performs a downgrade or update from divergent Adoption Kit history;
- overwrites `LOCAL_DRIFT`, `CONFLICT`, or `LOCAL_MISSING` states;
- rewrites `.github/project-forge-workspace.json`;
- runs arbitrary full application test suites without an explicit repository-owned update validation hook;
- commits, pushes, opens PRs, merges, releases, or deploys.

The intended lifecycle is:

```text
/project-forge-update
-> read-only discovery + deterministic preview
-> Apply update [HUMAN GATE]
-> deterministic apply
-> post-apply validation
-> if validation fails: preserve branch/diff -> validation-only recovery
-> meaningful local diff
-> STOP

Reviewer
-> human meaningful-diff acceptance
-> /deliver
```
