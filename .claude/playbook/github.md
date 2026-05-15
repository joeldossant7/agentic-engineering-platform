# Playbook: GitHub Integration

## Overview

How agents interact with GitHub for repository operations, PR management, and issue tracking. Uses the GitHub REST API v3 and GitHub CLI (`gh`).

## Authentication

```bash
# Required environment variables
GITHUB_TOKEN=<YOUR_PAT_OR_APP_TOKEN>  # Personal Access Token or GitHub App token
GITHUB_ORG=your-org
GITHUB_REPO=your-repo
```

Token scopes required: `repo`, `read:org`, `write:issues`, `pull_requests`.

## Common operations

### List open PRs

```bash
gh pr list --repo $GITHUB_ORG/$GITHUB_REPO --state open --json number,title,author,createdAt
```

### Create an issue from a ticket draft

```bash
gh issue create \
  --repo $GITHUB_ORG/$GITHUB_REPO \
  --title "Story: <title>" \
  --body "<description>\n\n## Acceptance Criteria\n- [ ] <criterion>" \
  --label "story" \
  --milestone "<milestone name>"
```

### Search issues

```bash
gh issue list --repo $GITHUB_ORG/$GITHUB_REPO \
  --search "label:epic state:open" \
  --json number,title,labels,milestone
```

### Link a PR to an issue

Include in the PR body: `Closes #<issue-number>` — GitHub auto-closes the issue on merge.

## Branch naming conventions

Agents must use the following branch naming pattern when creating branches:

```
<type>/<ticket-id>-<short-description>
# Examples:
feat/SPEC-2026-001-user-auth
fix/SPEC-2026-002-token-expiry
chore/SPEC-2026-003-update-deps
```

## Issue to PR workflow

```
Epic issue (label: epic)
  └── Story issues (label: story, linked to epic via "part of #N" in body)
        └── PRs (closes story issue on merge)
```

## Rate limits

GitHub REST API: 5,000 requests/hour per authenticated user. GraphQL API: 5,000 points/hour. Agents must check `X-RateLimit-Remaining` header and pause if < 100.

## Setup checklist

- [ ] PAT or GitHub App token created with correct scopes
- [ ] Token stored in `GITHUB_TOKEN` environment variable
- [ ] `gh` CLI installed and authenticated (`gh auth login`)
- [ ] Milestone created in the repo for the current initiative
- [ ] Labels created: `epic`, `story`, `task`, `blocked`
