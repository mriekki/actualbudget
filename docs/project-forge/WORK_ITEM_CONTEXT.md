# Work-Item Context

Project Forge reads `.github/project-forge-workspace.json` to learn how this repository organizes
work.

Supported sources:

```text
Jira Story / Epic
GitHub Issue
local docs
hybrid
```

## Jira Epics

Epics are first-class context but are not automatically Feature Briefs.

## Briefs

Product/Feature Brief modes can be:

```text
not-used
read-existing
supplemental-experimental
authoritative
suggest-complex
```

If supplemental/experimental, label them clearly and do not replace the primary
Jira/Issue authority.
