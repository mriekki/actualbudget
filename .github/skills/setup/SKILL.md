---
name: setup
description: "Guide and execute setup for this workstation/workspace instance, including verified local runtime convergence, optional remote-enabled capability, named deployment-environment onboarding, and disposable deployment-path proof."
argument-hint: "[status|repair|local|remote|<environment>]"
user-invocable: true
disable-model-invocation: true
---

# Setup

Purpose: give the developer one obvious entry point after cloning/opening a Project Forge workspace and whenever this workstation later needs local or remote environment preparation.

Normal first use is simply:

```text
/setup
```

Supported focused forms include:

```text
/setup status
/setup repair
/setup local
/setup remote
/setup <environment>
```

`/setup` is the conversational/orchestration layer. Repository-local setup scripts and Deployment Kit commands remain the deterministic machine implementations. Do not duplicate installer, SSH, Docker, deployment, or profile mechanics in the skill when the repository already provides them.

The governing readiness invariant is:

```text
REQUESTED MODE != ready state
READY = verified operational evidence
```

A requested local/remote capability becomes ready only after its applicable readiness contract passes. Preserve the prior ready state when convergence fails.

## 1. Resolve this workspace instance

From the repository root inspect only what is needed:

- `DEV_ENVIRONMENT.json`;
- `DEPLOYMENT_TOPOLOGY.json` when present;
- `PROJECT_BOOTSTRAP.json` as generation/provenance and initial topology fallback;
- `SCAFFOLD_PLAN.json` when present;
- `.github/project-forge-workspace.json` and Project Forge/component baselines when present;
- `scripts/setup.ps1` on Windows or `scripts/setup.sh` on macOS;
- current Git branch/status/upstream evidence so setup does not overwrite unrelated work;
- workstation-local setup/readiness evidence when present;
- actual workstation OS/platform and machine-local identity needed to describe this workspace instance.

If package-managed Project Forge files are drifted, route that problem to `/project-forge-update`; do not silently replace managed files during setup.

A **workspace instance** is one checkout of one Project Forge project on one developer workstation. Multiple workstations may work on the same project concurrently, and multiple workspace instances are normal.

When project provenance/configuration exists but this computer has no local readiness evidence for the checkout, treat the situation as:

```text
EXISTING PROJECT — NEW WORKSTATION
```

Do not require another workstation to be online and do not treat another computer as the project's primary machine.

Detect the current OS automatically. Do not ask the developer which setup launcher to use when the platform can be observed.

A workspace instance owns machine-local state such as local runtime/data, SSH private keys/trust, credential-manager entries, Docker state, and repository-scoped readiness evidence. Git/GitHub is the shared source-code coordination boundary. Never invent a central workstation registry merely to coordinate another computer.

## 2. `status` is read-only

`/setup status` performs no setup writes. Inspect current workstation evidence and live prerequisites, then report local workspace/runtime readiness plus any configured remote capabilities.

Prefer a compact result such as:

```text
SETUP STATUS

Workspace ......... READY / NOT CONFIGURED / BLOCKED
Local runtime ..... READY / STALE / NOT APPLICABLE
Build/tests ....... READY / STALE / BLOCKED
Local data ........ READY / NOT APPLICABLE / BLOCKED
Personal profile .. READY / DEFERRED / BLOCKED
Remote capability . READY / PARTIAL / NOT CONFIGURED

NEXT
/setup local | /setup remote | /setup <environment> | /next-step
```

Do not silently repair state during `status`.

## 3. Run generated workstation setup

Select the launcher for the actual workstation OS:

```text
Windows  -> .\scripts\setup.ps1
macOS    -> ./scripts/setup.sh
```

For normal setup, run the launcher with repository restore enabled when supported:

```text
setup --restore
```

For a read-only generated setup check, use the script's check mode when supported:

```text
setup --check
```

A manually invoked `/setup` authorizes routine, bounded, non-destructive local setup that the generated script already owns: supported tool installation, VS Code extension installation, dependency restore, personal Project Forge profile initialization, and other declared workstation preparation.

Stop before destructive replacement, unrelated machine mutation, secret disclosure, or repair outside the declared setup contract.

## 4. `/setup local` converges verified local development readiness

The first success target is:

```text
LOCAL WORKSPACE READY
```

Remote environments must not block local setup unless the approved project explicitly requires a remote dependency for local development.

If application scaffolding is intentionally deferred by `SCAFFOLD_PLAN.json` or approved work-item state, local workspace readiness may be valid without an application runtime. Do not invent source/runtime work merely to make local setup look complete.

When application source/runtime exists, converge only the repository-owned local development contract.

### A. Prerequisites and restore

Verify supported tools/versions using repository setup/doctor tooling when present. Run repository-defined dependency restore/setup commands when missing or stale. Preserve pinned versions and project conventions.

### B. Local persistence

For SQLite local development, resolve the project-owned database path and migration/initialization contract from repository evidence. Prefer installed Deployment Kit local SQLite ensure/status primitives when available.

When the database is absent, creating the owned local SQLite file/directory and running normal forward initialization/migrations may be routine setup.

If an existing database is corrupt, incompatible, has unexpected ownership/schema state, or recovery would be destructive, stop. **Never delete, replace, reset, or migrate destructively** merely to make setup pass. Other persistence engines require their own explicit repository-owned setup contract.

Each workstation normally owns independent local development data; do not silently copy mutable local databases or runtime state from another computer.

### C. Build and tests

Run the repository's required local build and test commands. A missing/stale build is a normal convergence condition; rebuild it. If required build/tests fail, report:

```text
LOCAL MODE NOT READY
```

and do not record local runtime readiness.

### D. Local immutable runtime artifact

When local execution is Docker-based, build/acquire the application image through repository-owned commands and resolve an immutable identity. A repository-supported workstation adapter may accept an exact registry digest or a local Docker image ID (`sha256:<64 hex>`) for workstation-only execution. Never treat a mutable tag as final runtime identity.

### E. Local runtime and health

Converge the project-owned local application runtime through the repository-distributed workstation adapter when available. Current reusable workstation-container topology remains loopback-only:

```text
placement: workstation
isolation: container
exposure: loopback
```

Mount only project-owned local persistence as required. Verify the declared health endpoint/smoke check when the project defines one. Do not resolve SSH targets, publish images, create public routes, or deploy Staging/Production while preparing local development.

Only after applicable prerequisites, persistence, build/tests, runtime, and health checks pass should local readiness be recorded as ready.

## 5. Establish/sync the personal Project Forge profile

When installed Deployment Kit exposes personal-profile operations, `/setup` should establish the authenticated developer's portable non-secret profile as routine setup state. This repo is per developer, not per Project or workstation.

If the expected private profile repository is missing, explain the intended creation before writing. It stores only non-secret target definitions/preferences. SSH private keys, passwords, PATs, known-host contents, mutable local databases, Docker credentials, and machine-local readiness remain local.

Use repository-provided deterministic profile operations when supported. If GitHub is unavailable, otherwise-ready local development remains valid; report profile portability as `DEFERRED`.

Never ask the developer to paste credentials into chat.

## 6. Present guided environment setup selection

After local readiness/profile state is understood, show the environments this workstation can be prepared to use.

This is an intentionally **multi-select** decision because preparing the workstation for several environments in one setup session is valid. When the host exposes structured choice UI, use native multi-select; in VS Code use a question surface such as `vscode_askQuestions`.

Conceptual choices are:
- `Local development`;
- each existing project-defined environment from current topology;
- `Other / define another environment`.

Recommend/select `Local development` by default only because Project Forge is local-first. Do not automatically recommend additional environments without project-specific evidence.

Rules:
- existing names come from `DEPLOYMENT_TOPOLOGY.json`, falling back to Bootstrap topology only for the initial topology;
- selecting an environment means **prepare this workstation for that environment**, not deploy the project application;
- do not force every environment to be configured in one session;
- the recorded setup scope comes from the developer's actual selections;
- later environment changes belong in mutable project topology, not casual rewrites of Bootstrap provenance.

### Define another environment

For `Other / define another environment`, collect only material durable facts, normally:

```text
Name ............ demo
Purpose ......... demo / staging / production / development
Placement ....... workstation / remote-target / managed-service / deferred
Target .......... <when placement requires one>
Isolation ....... <project/catalog-supported option>
Exposure ........ <project/catalog-supported option>
```

Use structured single-select controls for bounded mutually exclusive fields when available. Keep names/targets open-ended. Persist the approved logical environment definition before claiming it is configured.

Normal commands then use that exact name, for example:

```text
/setup demo
/deployment-readiness demo
/deploy demo
/tear-down demo
```

Do not create an environment whose required placement/adapter is unsupported; report the concrete `CATALOG GAP` or deferred state instead.

## 7. `/setup remote` and `/setup <environment>` prepare remote-enabled capability

Remote setup proves that this workstation can later work with the configured non-Production or Production-class environment under its normal safety contract. It does **not** publish an artifact or deploy the real application.

Verify as applicable:
- local developer prerequisites still needed to build/test;
- project topology contains the selected non-deferred environment;
- exact target/provider binding exists when required;
- workstation-to-target identity/trust/access is valid;
- target OS/runtime/platform prerequisites are valid;
- persistence/readiness prerequisites can be inspected safely;
- GitHub/registry access needed for a later release/publish step is available;
- repository deployment tooling/baselines are coherent.

For remote SSH preserve strict host identity. Unknown/changed host identity is a stop condition. Never copy SSH private keys/trust from another workstation and never fall back to another target/provider simply to make setup pass.

Remote readiness does not require configuring Production when the selected environment is non-Production. Production classification remains project topology/policy, not a literal-name check.

## 8. Prove supported remote mechanics with a disposable Project Forge probe

When the installed Deployment Kit exposes environment proof operations, a selected remote environment should normally be taken through an end-to-end **environment proof deployment** during setup.

The proof is not the Project application. It is a tiny disposable Project Forge-owned probe:

```text
acquire a stable probe image locally
→ resolve exact immutable digest
→ transfer using the real workstation-mediated path
→ deploy under reserved probe identity
→ verify runtime/HTTP health
→ remove probe
→ verify cleanup
```

Use the actual installed command/help contract. Never claim the Project application is deployed because the probe succeeds.

Preferred evidence:

```text
Environment ........... demo
Target/access ......... READY
Host platform ......... READY
Deployment path ....... PROVEN
Project application ... NOT YET DEPLOYED
```

For a Production-class environment, keep the proof explicitly labeled as a **PRODUCTION ENVIRONMENT PROOF** only when topology says the selected environment is Production-class. The disposable proof still does not authorize real Production deployment.

If cleanup fails, report `PROOF PASSED — CLEANUP ACTION NEEDED`; do not claim a clean setup.

## 9. `repair` is bounded and fail-closed

`/setup repair` may re-run safe deterministic setup/readiness operations after classifying the blocker. It may create missing local directories/caches, restore dependencies, rebuild outputs, create a new owned local database, run normal forward initialization, or recreate an owned disposable/local runtime when the repository contract permits those actions.

Stop for a separate explicit decision before:
- deleting/resetting an existing database;
- destructive migration or rollback;
- replacing unexplained persistent data;
- deleting unrelated containers/images/volumes;
- publishing an artifact remotely;
- rebinding a target;
- weakening host verification;
- changing public/LAN exposure;
- deploying Staging or Production.

## 10. Relationship to deployment readiness

`/setup` establishes workstation/workspace capability and may prove reusable environment mechanics.

`/deployment-readiness <environment>` remains the later pre-deployment check for one exact environment. It reuses fresh setup-time proof where valid, then verifies application-specific prerequisites for the real deployment.

`/setup` never implies `/deploy`. A successful setup/proof does not authorize a remote or Production application write.

## 11. Completion and handoff

After setup, report evidence rather than inferring human acceptance.

A generated setup/doctor/proof success is machine evidence. Human workspace acceptance remains distinct.

Useful next actions include:
- `/next-step` — one sensible next action after current evidence is known;
- `/start-work <ID>` — implementation authorization after workspace acceptance;
- `/deployment-readiness <environment>` — final pre-deploy evidence for a prepared environment;
- `/deploy <environment>` — only after readiness and its own authorization contract;
- `/tear-down <scope>` — destructive cleanup under its separate gate.

Do not create a second top-level developer-environment-mode workflow. Local/remote workstation convergence belongs here.
