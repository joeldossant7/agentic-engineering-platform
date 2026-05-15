# Agentic Engineering Platform — Corporate Brain

This repository is **not a project**. It is the organization's shared knowledge base, operational doctrine, and engineering governance layer for Claude Code sessions.

## What this repo is

- Reusable agent configurations and system prompts
- Operational policies that govern Claude's behavior across all sessions
- Skill fragments ready to inject into agent prompts
- Integration playbooks for external tools (Jira, GitHub, Vector DB)
- Inter-agent communication contracts

## How Claude must behave in this repo

1. **Never treat this as a feature repo.** Do not add product logic, business rules, or project-specific code.
2. **Respect the folder contract.** Each directory has a single responsibility (see folder guide below).
3. **Prompts and skills must be in English.** Documentation and READMEs may be in Spanish.
4. **HITL checkpoints are mandatory.** When the workflow diagram calls for human approval, Claude must pause and present a clear summary before proceeding.
5. **Model selection follows the agent config.** Do not default to a single model; read the agent's `config.json`.

## Folder responsibilities

| Folder | Responsibility |
|---|---|
| `agents/` | Agent identity: role, model config, tool list, persona |
| `contracts/` | Input/output schemas for inter-agent messages |
| `llm/` | LLM node implementations (clarification, routing, etc.) |
| `playbook/` | External tool integrations (Jira, GitHub, Vector DB, RAG) |
| `policies/` | Behavioral constraints and rules for Claude sessions |
| `prompts/` | Full system prompts per agent |
| `skills/` | Reusable prompt fragments injected into agent calls |

## Policies in force

All files under `policies/` are active and binding for any Claude Code session opened in this repo or any project that imports from it. See `policies/README.es.md` for the full list.

## Session startup checklist

When Claude Code starts a session in a project that uses this platform:

1. Read the relevant agent's `agents/<name>/config.json`
2. Load the agent's system prompt from `prompts/<name>.md`
3. Apply all constraints from `policies/constraints.md`
4. Load required skills from `skills/` as specified in the agent config
5. Confirm HITL checkpoints are enabled if the workflow requires them
