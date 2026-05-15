# Playbook: Jira Integration

## Overview

How the Jira Agent connects to and operates on Jira Cloud or Jira Data Center. This playbook covers authentication, field mapping, issue hierarchy, and error patterns.

## Authentication

```bash
# Required environment variables — never hardcode
JIRA_BASE_URL=https://your-org.atlassian.net
JIRA_USER_EMAIL=your-service-account@org.com
JIRA_API_TOKEN=<YOUR_API_TOKEN>   # Generate at id.atlassian.com/manage-profile/security/api-tokens
```

Authentication method: HTTP Basic Auth with email + API token.

```python
import base64, os

credentials = base64.b64encode(
    f"{os.environ['JIRA_USER_EMAIL']}:{os.environ['JIRA_API_TOKEN']}".encode()
).decode()

headers = {
    "Authorization": f"Basic {credentials}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}
```

## Issue hierarchy

```
Epic
  └── Story (Epic Link → Epic)
        └── Subtask / Task (Parent → Story)
```

Epic Link is a custom field in most Jira configurations. Its field ID varies by instance. Retrieve it:

```bash
curl -H "Authorization: Basic <credentials>" \
  "$JIRA_BASE_URL/rest/api/3/field" | jq '.[] | select(.name=="Epic Link") | .id'
```

## Common API calls

### Create an issue

```
POST /rest/api/3/issue
{
  "fields": {
    "project": { "key": "PROJECT_KEY" },
    "issuetype": { "name": "Story" },
    "summary": "Issue title",
    "description": {
      "type": "doc", "version": 1,
      "content": [{ "type": "paragraph", "content": [{ "type": "text", "text": "Description" }] }]
    },
    "story_points_field_id": 3,
    "customfield_10014": "EPIC-KEY"   // Epic Link — adjust field ID per instance
  }
}
```

### Search issues

```
GET /rest/api/3/search?jql=project=PROJECT_KEY+AND+issuetype=Epic&maxResults=50
```

### Update an issue

```
PUT /rest/api/3/issue/{issueIdOrKey}
{ "fields": { "summary": "Updated title" } }
```

## Field mapping reference

| Ticket Draft field | Jira field | Notes |
|---|---|---|
| `title` | `summary` | Required |
| `description` | `description` | ADF format for Cloud |
| `acceptance_criteria` | `description` append or custom field | Depends on Jira config |
| `estimate: S` | `story_points: 1` | Map: S=1, M=3, L=5, XL=8 |
| `estimate: M` | `story_points: 3` | |
| `estimate: L` | `story_points: 5` | |
| `estimate: XL` | `story_points: 8` | |
| `labels` | `labels` | Array of strings |
| `parent_ref` | `customfield_10014` (Epic Link) | For stories under epics |

## Error patterns

| HTTP Status | Meaning | Action |
|---|---|---|
| 400 | Invalid field or value | Log the field, report to human |
| 401 | Bad credentials | Check env vars |
| 403 | Permission denied | Verify service account permissions |
| 404 | Project or issue not found | Verify project key |
| 429 | Rate limited | Wait 60s, retry once, then report |

## Rate limits

Jira Cloud: ~300 requests / minute per API token. The Jira Agent must insert a 200ms delay between sequential issue creates when batch size > 10.

## Setup checklist

- [ ] Service account created with "Create Issues" and "Edit Issues" permissions
- [ ] API token generated and stored in environment variables
- [ ] Project key confirmed
- [ ] Epic Link field ID retrieved for the target Jira instance
- [ ] Story Points field ID retrieved (often `customfield_10016`)
