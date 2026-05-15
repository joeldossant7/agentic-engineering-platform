# Operational Rules

Rules govern how the agentic workflow operates — the sequencing, handoffs, escalations, and human-in-the-loop moments defined in the SDD diagram.

## Workflow rules

### R-01 — Clarification before action
The Clarification Node must run before the Product Owner Agent when the input is ambiguous. Ambiguity is defined as: missing scope, missing acceptance criteria, or contradictory requirements. Claude must ask at most 3 clarifying questions per input, grouped in a single message.

### R-02 — Specs are the source of truth
Research Specs (the output of the PO Agent) are the authoritative input for all downstream agents. No agent may act on informal conversation context that contradicts the current spec document.

### R-03 — HITL on spec approval
After the PO Agent produces Research Specs, execution must pause. Claude must present the specs in a structured summary and request explicit human approval (`approve` / `edit` / `reject`) before routing to specialist agents.

### R-04 — HITL on doc approval
After specialist agents produce the Vision + Roadmap + Ticket Draft, execution must pause again. Claude must present a diff-style summary of changes and request approval before finalizing.

### R-05 — Vector DB is read-only during sessions
Claude may query the Vector DB for context retrieval. Claude must never write to or update the Vector DB directly during a session — writes require a dedicated indexing pipeline run.

### R-06 — Ticket assembly requires spec approval
The Ticket Assembly skill must not run unless R-03 has been completed with an `approve` response. If specs are in `edit` or `reject` state, Claude must loop back to the PO Agent.

## Agent routing rules

### R-07 — Specialist agent selection
The following agents are available after HITL spec approval. Claude must select the appropriate subset based on the task:

| Task type | Agent |
|---|---|
| Code architecture, implementation | coding-skill agent |
| System design, diagrams, ADRs | systems-design-skill agent |
| Infrastructure, deployment, environments | infra-skill agent |
| Ticket creation, sprint planning, roadmaps | project-management agent |

Claude must not route to an agent whose skill is not registered in `skills/`.

### R-08 — No agent self-selection
Agents must not decide their own follow-up actions. All routing decisions must surface to the session (HITL or explicit user instruction).

## Communication rules

### R-09 — Use contracts for inter-agent messages
Any data passed from one agent to another must conform to the schema defined in `contracts/<sender>_to_<receiver>.json`. Unvalidated free-text handoffs between agents are not allowed.

### R-10 — Audit trail
Every agent action that modifies a spec, ticket, or document must be logged with: timestamp, agent name, action type, and input hash. Log to `.claude/audit.log` during sessions.
