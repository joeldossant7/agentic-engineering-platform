"""
Jira Agent — entry point.

Receives approved ticket drafts and creates the corresponding
Epic → Story → Task hierarchy in Jira. Requires HITL approval
before any write operation.
"""

import json
import os
import time
import base64
from pathlib import Path
import urllib.request
import urllib.error

REPO_ROOT = Path(__file__).parent.parent
AGENT_CONFIG = REPO_ROOT / "agents" / "jira_agent" / "config.json"


def load_config() -> dict:
    with open(AGENT_CONFIG) as f:
        return json.load(f)


def get_auth_headers() -> dict:
    email = os.environ["JIRA_USER_EMAIL"]
    token = os.environ["JIRA_API_TOKEN"]
    credentials = base64.b64encode(f"{email}:{token}".encode()).decode()
    return {
        "Authorization": f"Basic {credentials}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }


def jira_request(method: str, path: str, body: dict | None = None) -> dict:
    base_url = os.environ["JIRA_BASE_URL"].rstrip("/")
    url = f"{base_url}/rest/api/3{path}"
    headers = get_auth_headers()

    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)

    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        raise RuntimeError(f"Jira API error {e.code}: {error_body}")


def create_issue(project_key: str, ticket: dict, parent_jira_id: str | None = None) -> str:
    issue_type_map = {"epic": "Epic", "story": "Story", "task": "Subtask"}
    estimate_map = {"S": 1, "M": 3, "L": 5, "XL": 8}

    fields = {
        "project": {"key": project_key},
        "issuetype": {"name": issue_type_map[ticket["type"]]},
        "summary": ticket["title"],
        "description": {
            "type": "doc",
            "version": 1,
            "content": [{"type": "paragraph", "content": [{"type": "text", "text": ticket.get("description", "")}]}]
        },
    }

    if ticket.get("estimate"):
        fields["story_points"] = estimate_map.get(ticket["estimate"], 1)

    if ticket.get("labels"):
        fields["labels"] = ticket["labels"]

    # Link to parent epic for stories
    if parent_jira_id and ticket["type"] == "story":
        fields["customfield_10014"] = parent_jira_id  # Epic Link — adjust per instance

    # Link to parent story for tasks
    if parent_jira_id and ticket["type"] == "task":
        fields["parent"] = {"key": parent_jira_id}

    result = jira_request("POST", "/issue", {"fields": fields})
    return result["key"]


def run_jira_agent(approved_draft: dict) -> dict:
    project_key = approved_draft["ticket_draft"]["project_key"]
    tickets = approved_draft["ticket_draft"]["tickets"]

    created = []
    failed = []
    title_to_jira_id = {}

    # Create in order: epics → stories → tasks
    for issue_type in ("epic", "story", "task"):
        for ticket in [t for t in tickets if t["type"] == issue_type]:
            parent_jira_id = title_to_jira_id.get(ticket.get("parent_ref"))
            try:
                jira_id = create_issue(project_key, ticket, parent_jira_id)
                title_to_jira_id[ticket["title"]] = jira_id
                created.append({"type": ticket["type"], "title": ticket["title"], "jira_id": jira_id})
                print(f"[Jira Agent] Created {issue_type}: {jira_id} — {ticket['title']}")
                time.sleep(0.2)  # Rate limit buffer for large batches
            except RuntimeError as e:
                failed.append({"title": ticket["title"], "error": str(e)})
                print(f"[Jira Agent] FAILED {issue_type}: {ticket['title']} — {e}")

    return {
        "status": "complete",
        "project_key": project_key,
        "created": created,
        "failed": failed,
        "total_created": len(created),
        "total_failed": len(failed)
    }


if __name__ == "__main__":
    sample_draft = {
        "ticket_draft": {
            "project_key": "PROJ",
            "tickets": [
                {"type": "epic", "title": "[EPIC] Auth Redesign", "description": "Full auth overhaul"},
                {"type": "story", "title": "Implement JWT login", "description": "...", "parent_ref": "[EPIC] Auth Redesign", "estimate": "M"},
                {"type": "task", "title": "Write JWT middleware", "description": "...", "parent_ref": "Implement JWT login", "estimate": "S"}
            ]
        }
    }
    result = run_jira_agent(sample_draft)
    print(json.dumps(result, indent=2))
