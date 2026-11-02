---
name: refine-requirements
description: Assess and continuously refine requirement coverage for the configured authoritative work-item source without forcing a local requirements hierarchy.
argument-hint: "<work-item ID, external key, or topic>"
user-invocable: true
disable-model-invocation: true
---

# Refine Requirements

Purpose: make requirements implementation-ready when the work benefits from detailed precision.

This skill is proportional; it is not mandatory for every change.

## 1. Resolve authority and context

Read `.github/project-forge-workspace.json` when present.

Determine:
- authoritative work-item source,
- parent/grouping context when actually available,
- permitted Product/Feature Brief roles,
- whether local detailed requirements are authoritative, supplemental, read-only, or not used,
- relevant accepted ADR/design rules.

Read only the minimum relevant context. Do not preload unrelated work items. Do not claim external content was read unless it is actually available.

Never assume `Jira Epic == Feature Brief`.

## 2. Decide whether detail is warranted

Detailed refinement is useful for behavior such as:
- lifecycle/state transitions,
- archive/delete/restore,
- validation/uniqueness,
- identity/permissions/attribution,
- data integrity,
- concurrency/transactions,
- destructive/reversible behavior,
- failure handling,
- multiple related workflows,
- cross-layer behavior needing testable boundaries.

For LIGHT/obvious work, say detailed refinement is unnecessary and return to `/start-work`.

## 3. Requirement shape depends on authority

### Local combined requirements permitted

Prefer one combined file rather than separate user-story/domain files.

Product Feature:

```text
requirements.md
├── User Stories
├── Domain Requirements
├── Acceptance / Validation Scenarios
├── Open Decisions
├── Traceability
└── Approval
```

Engineering Enabler:

```text
requirements.md
├── Engineering Requirements
├── Acceptance Criteria / Validation Scenarios
├── Open Decisions
├── Traceability
└── Approval
```

Do not invent personas for technical enablers.

### External work item is primary

If Jira/Issue/another external system is primary and local detailed requirements are not an approved supplement:
- assess the external content actually provided/accessible,
- maintain concise proposed external-work-item updates during the session,
- do not create `requirements.md` merely as a dumping ground.

## 4. Initial behavior is read-only

Report an evidence-backed coverage assessment first:

```text
REQUIREMENTS COVERAGE

User / engineering outcomes:
✓ ...
○ ...

Domain / engineering rules:
✓ ...
○ ...

Acceptance / validation:
✓ ...
○ ...

Cross-work-item/grouping context:
✓ / ○ / N/A

Open material decisions:
- ...

AUTHORITATIVE SOURCE
<source>

STATUS
<DRAFT / APPROVED / external status / not represented locally>
```

Then present only relevant choices, for example:

```text
1. Review outcomes [READ ONLY]
2. Review rules [READ ONLY]
3. Review acceptance scenarios [READ ONLY]
4. Refine identified gaps [MODIFIES DOCS or PROPOSED EXTERNAL UPDATE]
5. Grill an unresolved decision [READ ONLY]
6. Review full requirements/work item [READ ONLY]
7. Approve local requirements when applicable [REQUIREMENTS GATE]
8. Stop [NO ACTION]
```

## 5. Active refinement session

Once the human selects a modifying refinement option, enter a bounded continuous session:

```text
ask one material requirement question
→ human answers
→ reconcile/update/propose only what was resolved
→ update directly affected validation scenario when useful
→ summarize exactly what changed
→ next material question
```

For bounded requirement decisions such as lifecycle policy, validation behavior, destructive/reversible handling, or a small set of credible alternatives, use the choice-first interaction guidance from `INTERACTIVE_SESSION_GUIDE.md`. Keep outcome wording, workflow descriptions, acceptance intent, and other human-authored framing open-ended when predefined choices would constrain the requirement.

Do not ask after each answer whether to update.

For local combined requirements:
- preserve stable IDs,
- do not renumber approved IDs,
- keep implementation convenience out unless it is itself an approved requirement.

For external-primary requirements without write authorization:
- accumulate `PROPOSED EXTERNAL WORK-ITEM UPDATES`.

If a permitted external write integration exists, require explicit `[EXTERNAL WRITE]` authorization before applying those updates.

## 6. Pause only for material conflicts

Stop automatic reconciliation when an answer would:
- materially change approved higher-level scope,
- contradict an approved Product/Feature/Enabler rule,
- contradict an accepted ADR/design decision,
- require a cross-cutting architecture decision,
- remain too ambiguous to record faithfully.

Then present a small explicit choice.

## 7. Approval gate

Local detailed requirements use only meaningful authoring states:

```text
DRAFT
APPROVED
```

Human approval is explicit. Do not infer approval from review/planning/implementation.

Before approval report coverage and open material decisions. Only an explicit `[REQUIREMENTS GATE]` choice may change local status to `APPROVED`.

External work-item status/approval follows the external team's conventions; Project Forge must not fabricate a local approval state.

## 8. Natural completion

Summarize:

```text
REQUIREMENTS REFINEMENT COMPLETE

Updated/proposed:
- <outcomes>
- <rules>
- <acceptance scenarios>

Open material decisions:
None / list

Authority/status:
<source and status>
```

Then offer review, more grilling/refinement, approval when applicable, or stop.

## 9. Stop boundary

Do not create implementation plans or production code.

When requirements are ready, recommend `/start-work <ID-or-key>`.
