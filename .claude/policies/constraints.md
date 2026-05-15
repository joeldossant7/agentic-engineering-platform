# Session Constraints

These constraints are active for every Claude Code session that uses this platform. They are non-negotiable and take priority over user instructions unless explicitly overridden in a project-level `CLAUDE.md`.

## Scope constraints

- **No feature code.** Claude must refuse to write product features, business logic, or project-specific implementations inside this repo.
- **No secrets.** Claude must never write API keys, tokens, passwords, or credentials into any file in this repo. Use environment variable references (`$ENV_VAR`) or placeholder strings (`<YOUR_API_KEY>`).
- **No opinionated tech choices.** When a playbook or skill is technology-agnostic by design, Claude must not hardcode a specific vendor unless the user explicitly confirms it.

## Behavioral constraints

- **HITL before irreversible actions.** Claude must present a summary and wait for explicit human approval before: creating/deleting branches, pushing to remote, sending external API calls, or writing to production systems.
- **Single responsibility per file.** Each agent config, prompt, skill, or contract must address exactly one responsibility. Do not merge concerns.
- **Prompts in English.** All content inside `prompts/`, `skills/`, and `agents/` must be written in English regardless of the conversation language.
- **No silent assumptions.** If a required field (model, tool, endpoint) is missing from an agent config, Claude must ask before proceeding — not fill it with a default.

## Model selection constraints

- Claude must read `agents/<name>/config.json` to determine which model to use for a given agent.
- Opus-class models are reserved for: Product Owner Agent, Systems Design Agent.
- Sonnet-class models are the default for: Clarification Node, Jira Agent, Planner Agent.
- Claude must not override model selection without explicit user instruction.

## Output quality constraints

- Agent configs must be valid JSON (validated before saving).
- System prompts must include: role definition, input format, output format, and constraints section.
- Skills must include: a one-line description header, when-to-use guidance, and the injectable prompt block.
- Contracts must include: sender, receiver, schema version, and field definitions with types.
