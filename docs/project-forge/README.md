# Project Forge Existing-Repository Additions

This directory documents the Project Forge capabilities adopted into this repository.

The root README, CI, PR template, branch conventions, and existing requirements
system remain authoritative unless explicitly changed by the team.

Configuration:

```text
.github/project-forge-workspace.json
```

Read:

- `WORK_ITEM_CONTEXT.md`
- `ADOPTION_WORKFLOW.md`
- `JIRA_ACCESS_GUIDE.md`

For maintenance of already-installed Project Forge capabilities, use `/project-forge-update`. It previews the exact accepted Adoption Kit update first, requires an explicit apply gate, and stops after producing a validated local diff for normal Reviewer → `/deliver` handling.

The Project Forge package does not imply this repo uses Product Briefs, Feature Briefs, or
local work-item folders.
