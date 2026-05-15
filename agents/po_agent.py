"""
Product Owner Agent — entry point.

Receives clarified input from the Clarification Node, queries the Vector DB,
produces a Research Spec, and pauses for HITL approval before routing downstream.
"""

import json
from pathlib import Path
import anthropic

REPO_ROOT = Path(__file__).parent.parent
AGENT_CONFIG = REPO_ROOT / "agents" / "po_agent" / "config.json"
PROMPT_FILE = REPO_ROOT / "prompts" / "po_agent.md"
SKILL_FILES = [
    REPO_ROOT / "skills" / "read_specs.md",
    REPO_ROOT / "skills" / "read_data.md",
    REPO_ROOT / "skills" / "systems_design.md",
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


def run_hitl_checkpoint(spec_text: str) -> str:
    print("\n" + "=" * 60)
    print("CHECKPOINT: SPEC APPROVAL")
    print("=" * 60)
    print(spec_text)
    print("\n" + "=" * 60)
    print("Action required: approve / edit / reject")
    return input("> ").strip().lower()


def run_po_agent(clarified_input: dict) -> dict:
    config = load_config()
    model_cfg = config["model"]

    client = anthropic.Anthropic()
    system_prompt = load_system_prompt()

    user_message = f"""
Clarified input received from Clarification Node:

{json.dumps(clarified_input, indent=2)}

Produce the Research Spec now.
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

    spec_text = next(
        block.text for block in response.content if block.type == "text"
    )

    action = run_hitl_checkpoint(spec_text)

    if action == "approve":
        return {"status": "approved", "spec": spec_text, "routed_to": "planner_agent"}
    elif action == "edit":
        edits = input("Provide your edits: ").strip()
        return {"status": "edited", "spec": spec_text, "edits": edits, "action": "revise"}
    else:
        return {"status": "rejected", "action": "restart"}


if __name__ == "__main__":
    sample_input = {
        "original_input": "We need to redesign how users log in",
        "clarifications": [],
        "resolved_scope": "Redesign the authentication flow for web app users.",
        "confidence": "high",
        "routed_to": "po_agent"
    }
    result = run_po_agent(sample_input)
    print(json.dumps(result, indent=2))
