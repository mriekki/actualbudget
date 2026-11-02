---
applyTo: "**"
---

# Project Forge Agentic Workflow

Read `.github/project-forge-workspace.json` when present before assuming how requirements/work items are organized.

Existing team conventions outrank Project Forge defaults.

Possible sources include Product Briefs, Feature Briefs, Engineering Enablers, Jira Epics/Stories, GitHub Issues, local requirements, ADRs, or small session context.

Use proportional rigor: `LIGHT`, `STANDARD`, `ELEVATED`.

Keep explicit human gates for material requirements, substantive plans, meaningful implementation acceptance, the final merge/delivery decision, and production deployment.

Once a bounded action is authorized, routine mechanics inside that scope should proceed without repeated ceremonial confirmation.

For implementation, establish the repository-appropriate short-lived work branch as routine setup once implementation itself is authorized; do not add a separate branch-creation gate when branch policy/naming and scope are clear.

Continuous modes such as `/grill-me`, `/refine-requirements`, `/coach`, `/learning-review`, and `/deployment-readiness` continue until stopped or naturally complete.

During interactive questioning, prefer concise choice-first options for genuinely bounded human decisions, including `Other / specify` and `Not sure — recommend one` when appropriate. When the host exposes native structured question controls, use them instead of a plain numbered chat list. In VS Code, use the host's structured question surface such as `vscode_askQuestions` when available: single-select for mutually exclusive decisions/actions and multi-select only when several simultaneous selections are valid. A textual numbered menu is only the fallback when structured choice UI is unavailable.

Make a recommendation only when current evidence, repository policy, or a clear engineering tradeoff supports one. Mark exactly one supported choice with the host's `recommended` indicator when available and give a brief rationale. If no option is clearly better, do not mark any option recommended. A recommendation is advice, not approval: record only the human's selected/confirmed answer. If the human asks for no recommendation on one decision, honor that for that decision only; later questions may still include evidence-backed recommendations.

Keep factual/environment-specific values and questions intended to elicit the human's own framing, reasoning, debugging approach, design rationale, or understanding open-ended unless options are later useful as scaffolding.

`/grill-me` is the single adversarial-questioning entry point. It begins read-only and may, after one explicit session-level choice, reconcile resolved decisions into permitted local authorities or proposed external updates. Do not create a second documentation-aware grilling command.

`/setup` is the single workstation/environment preparation entry point. It owns status, repair, verified local runtime convergence, remote-enabled capability preparation, and named-environment setup/proof. Do not create a second developer-environment-mode command. `/deployment-readiness <environment>` remains the later exact-environment pre-deploy verification step.

For deployment readiness, inspect existing non-secret configuration before asking setup questions. Show already-known simple machine facts such as hostname/address, deployment user, port, and target OS for confirmation. Ask only for missing or conflicting facts. Keep deployment-tool implementation identifiers such as logical target names, `targetName`, SSH aliases, profile paths, and trust-file paths internal unless troubleshooting or genuine ambiguity requires them.

Shared managed code keeps its canonical owner. When a consumer contains `CORE_BASELINE.json` or `DEPLOYMENT_BASELINE.json`, treat those baselines as ownership evidence. A temporary edit to a shared-managed consumer file may be used to diagnose or prove a reusable defect, but it is not the canonical deliverable.

Before consumer delivery, run available managed-baseline integrity checks. If Core- or Deployment-Kit-managed files have unexplained local drift, stop before staging/commit/push and route the reusable change through `/upstream-fix`. Fix the owning canonical repository, deliver/merge it there under normal gates, then adopt the exact accepted shared commit back into the consumer through the appropriate update boundary and retest in consumer context.

Package-managed generated Projects use `/project-forge-update`. Direct `/core-sync` remains only for component-only Core consumers without `PROJECT_FORGE_BASELINE.json` and is not part of the normal greenfield Project command surface.

Do not manually preserve a private consumer fork of shared managed code merely because the consumer exposed the bug. Consumer-owned product/application files remain normal consumer implementation scope.

After implementation review and local human acceptance, manually invoking `/deliver` authorizes routine short-lived-branch recovery/setup as needed, selective stage/commit/push, PR creation/update, and PR-CI inspection. `/deliver` then stops once for the explicit `Merge and finalize delivery` decision. When the PR still exactly matches the accepted implementation, that one choice combines final PR acceptance, merge authorization, post-merge CI observation, and safe delivered-branch finalization.

Changed PR evidence re-opens the relevant review gate. Merge never implies production-deployment authorization.

## Post-delivery documentation and learning handoff

After engineering delivery is complete, documentation impact and learning are **non-blocking follow-ups**, not new delivery states or gates.

Use the accepted work-item/PR diff conservatively to classify likely documentation impact. Examples:

- public API/contract changes may affect architecture/runtime/API narrative;
- services, dependencies, messaging, caches, auth, observability, deployment topology, or failure handling may affect System evidence;
- entities, migrations, schema/DDL, ORM, queries, constraints, or indexes may affect DB evidence;
- environment/deployment changes may affect operations docs;
- durable developer/test workflow changes may affect engineering docs;
- a consequential architectural tradeoff may deserve an ADR recommendation.

A changed file proves relevant evidence was touched; it does not by itself prove a runtime or physical-schema change.

When the relevant tools exist and prerequisites are safe, `/deliver` may best-effort prepare **disposable** evidence/site projections under:

```text
.project-forge/docs-cache/system/
.project-forge/docs-cache/database/
.project-forge/docs-site/
```

System evidence may be reconstructed from the current repository. Database evidence may be generated automatically only when a safe local development/test database path is already explicit; never guess a path merely to populate docs.

If `tools/project-forge-docs/docs-site.py` exists, a build of the local documentation projection may follow safe lab preparation. Failure to build docs or a lab projection does not change `DELIVERY COMPLETE`.

Do not silently rewrite project-owned narrative or approve/create an ADR solely because implementation evidence changed. Instead surface a compact `DOCUMENTATION IMPACT` handoff, for example:

```text
DOCUMENTATION IMPACT

✓ Project brief: no material change detected
★ System evidence: changed; current projection prepared
★ Database evidence: changed; /db-lab recommended
○ ADR consideration: new synchronous external dependency introduced

/docs — explore the current project documentation
```

Use only claims supported by observed evidence. Keep `/docs`, `/db-lab`, `/system-lab`, `/code-walkthrough`, and `/learning-review` visible when useful, but never require them solely to complete engineering delivery.

Do not pin or automatically escalate models.
