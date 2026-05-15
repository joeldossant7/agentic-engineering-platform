"""
Planner Agent — entry point.

Receives approved Research Specs and produces Vision, Roadmap,
and Ticket Draft artifacts. Pauses for final HITL approval.
"""

import json
from pathlib import Path
import anthropic

REPO_ROOT = Path(__file__).parent.parent
AGENT_CONFIG = REPO_ROOT / "agents" / "planner_agent" / "config.json"
PROMPT_FILE = REPO_ROOT / "prompts" / "planner_agent.md"
SKILL_FILES = [
    REPO_ROOT / "skills" / "systems_design.md",
    REPO_ROOT / "skills" / "project_management.md",
    REPO_ROOT / "skills" / "ticket_assembly.md",
]


def load_config() -> dict:
    with open(AGENT_CONFIG) as f:
        return json.load(f)


def load_system_prompt() -> str:
    parts = [PROMPT_FILE.read_text()]
    for skill_path in SKILL_FILES:
        parts.append(f"\n\n---\n# Injected Skill: {skill_path.name}\n")
        parts.append(skill_path.read_text())
    return "\n".join(parts)


def run_hitl_checkpoint(output_text: str) -> str:
    print("\n" + "=" * 60)
    print("CHECKPOINT: VISION + ROADMAP + TICKET DRAFT APPROVAL")
    print("=" * 60)
    print(output_text)
    print("\n" + "=" * 60)
    print("Action required: approve / edit / reject")
    return input("> ").strip().lower()


def run_planner_agent(approved_spec: dict) -> dict:
    config = load_config()
    model_cfg = config["model"]

    client = anthropic.Anthropic()
    system_prompt = load_system_prompt()

    user_message = f"""
Approved Research Spec received:

{json.dumps(approved_spec, indent=2)}

Produce the Vision Document, Definitive Roadmap, and Ticket Assembly Draft.
"""

    thinking_config = {}
    if model_cfg.get("thinking", {}).get("enabled"):
        thinking_config = {
            "thinking": {
                "type": "enabled",
                "budget_tokens": model_cfg["thinking"]["budget_tokens"]
            }
        }

    response = client.messages.create(
        model=model_cfg["id"],
        max_tokens=model_cfg["max_tokens"],
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
        **thinking_config
    )

    output_text = next(
        block.text for block in response.content if block.type == "text"
    )

    action = run_hitl_checkpoint(output_text)

    if action == "approve":
        return {"status": "approved", "output": output_text, "routed_to": "jira_agent"}
    elif action == "edit":
        edits = input("Provide your edits: ").strip()
        return {"status": "edited", "output": output_text, "edits": edits, "action": "revise"}
    else:
        return {"status": "rejected", "action": "restart"}


if __name__ == "__main__":
    sample_spec = {
        "spec_id": "SPEC-2026-001",
        "spec_version": 1,
        "approved_at": "2026-05-14T10:00:00Z",
        "approved_by": "Joel",
        "content": {
            "title": "User Authentication Redesign",
            "context": "Current auth is legacy and non-compliant.",
            "scope": {"included": ["web app auth"], "excluded": ["mobile app"]},
            "current_state": "Session tokens stored insecurely.",
            "desired_state": "JWT-based auth with refresh tokens."
        }
    }
    result = run_planner_agent(sample_spec)
    print(json.dumps(result, indent=2))
