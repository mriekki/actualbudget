---
name: start-work
description: Assess requirement readiness and implementation risk, then guide direct Agent work or native planning for the configured work item.
argument-hint: "<work-item ID, external key, or concise change>"
user-invocable: true
disable-model-invocation: true
---

# Start Work

## 1. Resolve the requested work

Read `.github/project-forge-workspace.json` when present.

Resolve only the context needed:
- authoritative work-item source,
- parent/grouping context when actually available,
- optional Product/Feature/Enabler briefs according to configured authority,
- local detailed requirements when permitted/present,
- relevant decisions/ADRs/architecture/standards,
- current code/tests and branch/diff when relevant.

Do not require local briefs when the repository uses Jira/Issues. Do not invent external content.

## 2. Check requirement readiness before planning

Assess:
- outcome clarity,
- acceptance criteria/validation expectations,
- material domain/engineering rules,
- dependencies/cross-work-item context,
- unresolved human decisions,
- requirement authority/status.

Ask:

```text
Does detailed precision matter?
Does the authoritative source contain enough detail?
If local requirements exist, are they DRAFT or APPROVED?
Are material decisions unresolved?
```

If detailed precision is warranted but incomplete, recommend `/refine-requirements` or `/grill-me` rather than silently inventing behavior. `/grill-me` may remain read-only or, when the human selects its session-level reconciliation option, write resolved decisions into permitted authorities.

If local requirements are DRAFT and carry material behavior, human approval is the gate before substantive planning/implementation.

If requirements are already sufficient/approved under the configured model, do not force another refinement cycle.

### CI/policy evidence is not a start-work gate

When requirements say CI/checks must pass before a later merge, release, or deployment action, use repository-configured workflows/checks plus observable repository policy/mergeability as the planning evidence available now.

Do not interpret words such as `required CI` or `required checks` as a mandate to discover GitHub branch-protection/ruleset admin settings before implementation can begin. Those settings may provide additional evidence later when they are observable, but inability to read them is not by itself a blocker.

Do not ask the human to open GitHub Settings and transcribe required-check names merely to proceed with `/start-work`. Stop and ask only when actual evidence conflicts or missing policy information creates a concrete unresolved decision that materially affects implementation or the later consequential action.

## 3. Classify risk

### LIGHT

Tiny, obvious, low-risk; no meaningful schema/security/concurrency/deployment/major-UX implications.

```text
Agent
→ relevant checks
→ human meaningful-diff review
```

No formal plan or detailed requirements are required.

### STANDARD

Meaningful multi-file work.

```text
requirements ready as needed
→ native plan
→ HUMAN PLAN APPROVAL
→ short-lived work branch setup
→ Agent implementation
→ checks
→ Reviewer
→ human meaningful-diff acceptance
```

### ELEVATED

Use for:
- schema/data-loss risk,
- authentication/security,
- concurrency/transactions,
- release/deployment/recovery,
- significant architecture,
- broad cross-layer changes,
- hard-to-reverse decisions.

```text
detailed approved requirements / ADR as needed
→ native plan
→ Reviewer challenges plan
→ HUMAN PLAN APPROVAL
→ short-lived work branch setup
→ implementation in small slices
→ stronger verification
→ Reviewer
→ human acceptance
```

Explain why the level was chosen.

## 4. Optional learning checkpoint

For STANDARD/ELEVATED work, once requirements are ready, coaching may be offered but is never required. When the human needs to choose, render a **single-select structured choice** through the host UI when available; in VS Code use the native question surface such as `vscode_askQuestions`.

Relevant choices are:
- `Continue without coaching` — `RECOMMENDED` default;
- `/coach` for a short pre-build concept review;
- `/grill-me` for challenge rather than teaching;
- `Stop`.

Use a numbered text list only when structured choice UI is unavailable. For LIGHT work, do not interrupt with coaching unless requested.

## 5. Planning rules

For STANDARD/ELEVATED work:
- use the editor's current native planning capability,
- plan approach, affected areas, key decisions, risks, and verification,
- require human plan approval before implementation,
- do not auto-launch subagents,
- do not create mandatory `spec.md` or `tasks.md`,
- save a durable plan only when it is useful across sessions or for genuinely complex/risky work.

## 6. Working branch setup

Once implementation is authorized to begin, establish the repository-appropriate short-lived work branch as routine setup before substantive edits.

Do not ask a separate branch-creation permission when all of the following are true:
- the current branch is the default/integration branch and repository policy expects short-lived work branches,
- the work-item boundary is clear,
- the target branch name is unambiguous under repository convention or the Project Forge fallback below,
- creating/switching branches does not require history rewriting or discarding work.

Branch naming order:
1. repository/team convention when defined,
2. an already-existing branch clearly tied to the work item,
3. Project Forge fallback: `<lowercase-work-item-id>-<concise-slug>` for ID-backed work, or `work/<concise-slug>` for a concise ad hoc change.

Examples of the fallback shape are conceptual only; never invent a consumer-specific work-item ID in Core documentation or behavior.

If scoped uncommitted changes already exist on the default branch and clearly belong to this work item, preserve them while creating/switching to the short-lived branch when Git can do so safely. Verify that the worktree diff is unchanged after the branch switch.

Stop and ask only when branch policy/naming is materially ambiguous, the intended branch already exists with divergent work, unrelated changes are present, or the operation would require stash/reset/rebase/force/history rewriting.

For LIGHT work, branch setup is part of the human-selected implementation action. For STANDARD/ELEVATED work, it is part of the approved implementation start after plan approval. Merely inspecting `/start-work` does not authorize implementation before its required gate.

## 7. Deployment enabler

When a work item owns release/deployment engineering or environment enablement, classify it ELEVATED when the change materially affects deployment/recovery/security behavior.

Environment readiness may begin early with the normal state-driven interface:

```text
/deployment-readiness <environment>
```

It begins with existing local/repository configuration, shows simple known machine facts for confirmation, and continues only as far as current engineering/evidence safely allows. It does not authorize application deployment.

After implementation review/local acceptance, use `/deliver`. After `/deliver` reports the merge, default-branch CI, and applicable repository-policy evidence satisfied, return to the same state-driven readiness command for the selected environment:

```text
/deployment-readiness <environment>
```

The workflow re-discovers state and continues from the furthest safe point; do not require the human to switch from a discovery mode to an enable mode.

Production remains a role with stronger policy and deployment authorization; it does not use a separate readiness workflow.

## 8. Guided ending

Return:
- CURRENT STATE,
- risk level and why,
- requirement readiness,
- branch state / expected short-lived branch when implementation is about to begin,
- RECOMMENDED NEXT STEP,
- a small set of relevant action choices.

Render mutually exclusive next actions through the host's **single-select structured choice UI** when available, following `INTERACTIVE_SESSION_GUIDE.md`. In VS Code, use the native question surface such as `vscode_askQuestions`. Make the recommended action visible when evidence supports one, include `Other / specify` or free-text only when the action set may be incomplete, and use a numbered text menu only as the no-structured-UI fallback.

Do not skip an unresolved requirement/plan gate merely because implementation is technically possible. Once implementation is selected/approved, do not insert a separate ceremonial branch-creation gate when the branch setup is safe and deterministic.
