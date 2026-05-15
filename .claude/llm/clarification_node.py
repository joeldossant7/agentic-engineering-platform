"""
Clarification Node — LLM implementation.

Reads the clarification_node agent config, loads the system prompt,
and runs a clarification conversation loop before routing to the PO Agent.
"""

import json
import re
import os
from pathlib import Path
import anthropic

REPO_ROOT = Path(__file__).parent.parent
AGENT_CONFIG = REPO_ROOT / "agents" / "clarification_node" / "config.json"
PROMPT_FILE = REPO_ROOT / "prompts" / "clarification_node.md"
SKILL_FILES = [
    REPO_ROOT / "skills" / "clarification.md",
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


def run_clarification(user_input: str) -> dict:
    config = load_config()
    model = config["model"]
    max_rounds = config.get("max_clarification_rounds", 3)

    client = anthropic.Anthropic()
    system_prompt = load_system_prompt()

    messages = [{"role": "user", "content": user_input}]
    clarifications = []
    round_count = 0

    while round_count < max_rounds:
        response = client.messages.create(
            model=model["id"],
            max_tokens=model["max_tokens"],
            system=system_prompt,
            messages=messages,
        )

        assistant_text = response.content[0].text
        messages.append({"role": "assistant", "content": assistant_text})

        # If the model produced a resolved_scope JSON block, we're done
        if "resolved_scope" in assistant_text and "routed_to" in assistant_text:
            match = re.search(r"```json\n(.*?)\n```", assistant_text, re.DOTALL)
            if match:
                return json.loads(match.group(1))

        # Otherwise, it asked questions — prompt the human
        print("\n[Clarification Node]\n")
        print(assistant_text)
        human_answer = input("\nYour answer: ").strip()

        clarifications.append({
            "round": round_count + 1,
            "question": assistant_text,
            "answer": human_answer
        })
        messages.append({"role": "user", "content": human_answer})
        round_count += 1

    # Max rounds exceeded — escalate
    print("\n[Clarification Node] Max clarification rounds reached. Escalating.")
    return {"error": "max_rounds_exceeded", "clarifications": clarifications}


if __name__ == "__main__":
    user_input = input("Input/basket: ").strip()
    result = run_clarification(user_input)
    print("\n[Output to PO Agent]")
    print(json.dumps(result, indent=2))
