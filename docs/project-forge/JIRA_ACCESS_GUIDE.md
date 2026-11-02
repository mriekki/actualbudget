# Jira Access Guide

Project Forge supports several Jira access modes because corporate environments differ.

## Mode 1 — Browser-Assisted

Use when Jira API and MCP are not permitted.

Recommended workflow:

1. Open Jira in an authenticated browser.
2. In current VS Code desktop versions that support the integrated browser, use:
   `Browser: Open Integrated Browser`.
3. Navigate to the Story/Epic.
4. Provide the relevant Story/Epic/Acceptance Criteria to Copilot Chat using
   available browser-to-chat context features, or paste the relevant text.
5. Invoke Project Forge against the Jira key, for example:

```text
/start-work ABC-1234
/grill-me ABC-1234
/refine-requirements ABC-1234
```

Important:

- Browser-assisted mode does not imply silent Jira scraping.
- The agent must not claim it read Jira unless Jira content is actually available
  in chat/tool context.
- Writes back to Jira should be proposed as copyable text unless a permitted
  write-capable integration is available.

## Mode 2 — Jira API

Use only when organization policy permits.

The Adoption Kit includes read-only connectivity tests.

Secrets are read from process environment variables and are not written into
`.github/project-forge-workspace.json`.

Supported test patterns:

### Jira Cloud

```text
JIRA_BASE_URL
JIRA_EMAIL
JIRA_API_TOKEN
```

### Jira Data Center / PAT-style

```text
JIRA_BASE_URL
JIRA_PAT
```

The test tries a `/myself` endpoint and performs no write.

## Mode 3 — MCP

Current VS Code/Copilot installations can configure MCP at workspace or user
scope.

The Adoption Kit looks for:

```text
.vscode/mcp.json
.mcp.json
~/.copilot/mcp-config.json
```

Detection does not prove that the Jira MCP server is correctly authenticated or
that the current agent has permission to use it.

Use the generated read-only runtime prompt:

```text
Use the configured Jira MCP server to read <ISSUE-KEY>.
Return only:
- key
- title/summary
- issue type
- status
- parent Epic if present

Do not modify Jira.
```

If that succeeds, choose MCP mode in the generated workspace config.

## Mode 4 — API + MCP

Useful when:

- API is available for deterministic read/write operations,
- MCP is useful interactively from Copilot.

The workspace may record both as available, but each operation should still use
the least-powerful appropriate mechanism.

## Authority vs Access

These are separate concepts.

Example:

```text
Jira Story:
  authority = primary
  access = browser-assisted

Feature Brief:
  authority = supplemental
  access = repository file
```

The fact that Jira is browser-only does not reduce its authority.
