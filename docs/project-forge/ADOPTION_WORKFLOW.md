# Project Forge Workflow in an Existing Repository

Typical meaningful work:

```text
authoritative Jira/Issue/local work item
→ optional /grill-me
→ optional /refine-requirements
→ /start-work
→ native plan when warranted
→ human plan approval
→ implementation
→ tests/checks
→ Reviewer
→ human meaningful-diff review
→ optional /code-walkthrough, /learning-review, or /coach
→ /deliver
→ PR/CI
→ final human PR review
→ explicit merge
```

`/code-walkthrough`, `/learning-review`, and `/coach` are optional learning tools and never engineering delivery gates. A useful project-first learning sequence after stable implementation is `/code-walkthrough` → `/learning-review` → targeted `/coach` follow-up.

LIGHT work can skip most ceremony.

Existing team policy always wins.

## Updating adopted Project Forge capabilities

Repositories adopted with Team-Safe Core include `/project-forge-update` to synchronize managed capabilities to the exact accepted Adoption Kit target.

The maintenance lifecycle is:

```text
/project-forge-update
→ read-only discovery + deterministic preview
→ Apply update [HUMAN GATE]
→ deterministic apply
→ post-apply validation
→ meaningful local diff
→ STOP

Reviewer
→ human meaningful-diff acceptance
→ /deliver
```

Normal `/project-forge-update` updates only capabilities already recorded in `.github/project-forge-adoption-baseline.json`. It does not silently add/remove capabilities, overwrite repository-owned `.github/project-forge-workspace.json`, commit, push, open a PR, or merge.

Post-apply validation checks the installed baseline against the exact accepted Adoption Kit/Core provenance, accepted capability manifests, managed-path hashes, and Project Forge adoption readiness. No arbitrary application test suite is inferred.

A repository can explicitly add platform-specific update validation through a repository-owned hook:

```text
.github/project-forge-update-validate.ps1
.github/project-forge-update-validate.sh
```

The matching hook is run only when present and must be read-only with respect to the Git worktree/index.

If post-apply validation fails, `/project-forge-update` preserves the update branch, diff, and candidate-aligned adoption baseline and stops before Reviewer or `/deliver`. After the cause is addressed, validation can be rerun from the exact Adoption Kit commit recorded in the baseline without reapplying the update.

If the updater reports local drift, conflict, missing managed files, divergent provenance, or another blocking state, the update stops fail-closed for explicit diagnosis.
