# Spec-Driven Development (SDD)

## What It Is

Spec-Driven Development is a systematic, multi-phase operational framework for translating raw ideas or requests into shipped code. It imposes a structured pipeline — from ambiguous input to committed branch — that works **across and independently of any specific task or goal**. The same flow applies whether you're building a new feature, fixing a system, or overhauling architecture.

At its core, SDD is an AI-augmented assembly line where human developers hold veto power at every critical transition point. No phase advances without human sign-off.

---

## What It Solves

| Problem | How SDD addresses it |
|---|---|
| Ambiguous requirements reaching developers | Clarification Node catches underspecified inputs before any work begins |
| Specs written in isolation without codebase context | Product Owner Agent queries a Vector DB of existing knowledge and ENGRAM memory for past-related context |
| Developers building to wrong spec | HITL checkpoints enforce approval before moving downstream |
| Tickets that don't reflect agreed specs | Jira Agent generates tickets *from* approved specs, not from memory |
| Coding agents working blind | Coding Agents read both the repo and the tickets before touching code |
| No traceability from idea to commit | Every artifact (specs → docs → tickets → commits) is linked in sequence |

---

## Architecture Overview

The system is divided into **3 phases**, each with its own agents, tools, and human checkpoints.

```
Input/Basket
    │
    ▼
[Phase 1] Documentation + Specs Generation
    │
    ▼
[Phase 2] Planning
    │
    ▼
[Phase 3] Execution
    │
    ▼
  GitHub (push branch)
```

---

## Phase 1: Documentation + Specs Generation

**Purpose:** Turn a raw request into a reviewed, approved specification and supporting documentation.

### Nodes

#### Input / Basket
The entry point for any request — a feature idea, a bug report, a strategic goal. Can be free-text or structured (document, image, and file read/upload --> OCR).

#### Clarification Node *(red circle)*
The first filter. Before any agent does real work, this node evaluates the input for ambiguity across four dimensions: scope, acceptance criteria, ownership, and contradictions.

- If clear → passes through to Product Owner Agent
- If unclear → asks targeted questions (max 3 per round, max 3 rounds) before proceeding

See: [`.claude/skills/clarification.md`](../.claude/skills/clarification.md) and [`.claude/prompts/clarification_node.md`](../.claude/prompts/clarification_node.md)

#### Product Owner Agent
Receives the clarified input and orchestrates research. Queries the **Vector DB** to retrieve existing context: past decisions, architecture notes, similar features, current roadmap state.

See: [`.claude/prompts/po_agent.md`](../.claude/prompts/po_agent.md)

#### Vector DB Search
A knowledge retrieval layer. Provides the PO Agent with grounded context so specs are written against *reality*, not assumptions.

See: [`.claude/playbook/vector_db.md`](../.claude/playbook/vector_db.md)

#### Research Specs *(document node)*
The output of the PO Agent's research pass: a draft specification. At this stage, specialized sub-agents may contribute in parallel:

- **Coding Skill Agent** — implementation angle
- **Systems Design Skill Agent** — architecture angle
- **Infra Skill Agent** — deployment/infrastructure angle
- **Project Management Agent** — timeline, dependencies, risk angle
- *(Optional: Crew AI or multi-agent framework for parallel contribution)*

#### HITL Checkpoint — Approve/Edit Specs *(yellow circle)*
Developers review the draft spec. This is a **hard stop**: the pipeline does not continue until a human approves, edits, or rejects. Multiple developers can participate.

**Hold condition:** Waiting on developer review.
**Outputs on approval:** Finalized spec passes to documentation assembly.

#### Vision, Roadmap + TODO + Ticket Assembly Draft *(document stack)*
From the approved spec, and using skills like systems_design, read_specs, ticket_assembly, read_data, project_management and more, the system assembles:
- Current state vs. target vision
- Definitive roadmap
- TODO breakdown
- Draft tickets (pre-Jira)

#### HITL Checkpoint — Approve/Edit Docs *(yellow circle)*
Second human gate within Phase 1. Developers review the full documentation package before it exits the phase.

**Hold condition:** Waiting on developer review of assembled docs.

---

## Phase 2: Planning

**Purpose:** Convert approved documentation into trackable, actionable tickets in the project management system.

### Nodes

#### Developers Team
The handoff point between Phase 1 and Phase 2. The dev team receives approved specs and docs as the authoritative source of truth for all subsequent planning.

#### Jira Agent
An agent specialized in creating well-formed Jira tickets from the spec artifacts. It reads the approved documentation and translates requirements into structured tickets.

See: [`.claude/prompts/jira_agent.md`](../.claude/prompts/jira_agent.md) and [`.claude/playbook/jira.md`](../.claude/playbook/jira.md)

> **Note (open decision):** *"ver si es necesario → Opcion de reemplazar Jira x ticketera de specs"* — there is an open architectural decision about whether to replace Jira with a native spec-ticketing system. Jira is the current default.

#### Jira Tool — Write *(diamond)*
The actual write operation to Jira. The agent uses this tool to create/update tickets. Marked as a tool (not an agent) — it has no autonomy, only executes writes.

#### HITL Checkpoint — Approve/Edit Tickets *(yellow circle)*
Developers review and edit the generated tickets before they become official work items.

**Hold condition:** Waiting on ticket sign-off.
**Outputs on approval:** Final tickets in Jira, ready for engineering pickup.

---

## Phase 3: Execution

**Purpose:** Implement the work defined in approved tickets, with human oversight before code lands.

### Nodes

#### Coding Agents
AI agents assigned to implement tickets. Before writing any code, they ground themselves with two read skills:

- **`read_repo` skill** — reads the current codebase state, understands structure, conventions, and existing patterns
- **`read_jira` skill** — reads the assigned ticket for exact scope, acceptance criteria, and constraints

This prevents agents from hallucinating requirements or misunderstanding the codebase.

See: [`.claude/skills/read_specs.md`](../.claude/skills/read_specs.md)

#### HITL Checkpoint — Approve/Edit Code *(yellow circle)*
Developers review the code produced by Coding Agents before it is committed. This is the last human gate before code enters version control.

**Hold condition:** Waiting on code review.
**On approval:** triggers commit to branch on GitHub.

#### GitHub (commit branch / push branch)
The final output of the pipeline. Code is committed to a feature branch and pushed. No direct commits to main — the branch then enters the standard PR/merge process outside this pipeline.

See: [`.claude/playbook/github.md`](../.claude/playbook/github.md)

---

## End-to-End Flow

```
1.  Input/Basket receives request
2.  Clarification Node evaluates ambiguity
    ├─ Unclear → ask questions (max 3 rounds) → loop back
    └─ Clear → continue
3.  Product Owner Agent + Vector DB → Research Specs
4.  Sub-agents (coding, systems, infra, PM) contribute to spec draft
5.  [HITL] Developers approve/edit specs
6.  System assembles Vision + Roadmap + TODO + Ticket Draft
7.  [HITL] Developers approve/edit documentation
8.  Developers Team receives approved docs
9.  Jira Agent reads docs → generates tickets via Jira Tool
10. [HITL] Developers approve/edit tickets
11. Coding Agents read repo + tickets → implement
12. [HITL] Developers approve/edit code
13. Commit branch → push to GitHub
```

---

## HITL Checkpoints Summary

| Checkpoint | Phase | What's reviewed | Hold condition |
|---|---|---|---|
| Approve/Edit Specs | 1 | Draft specification from research | Dev review pending |
| Approve/Edit Docs | 1 | Vision, roadmap, TODO, ticket draft | Dev review pending |
| Approve/Edit Tickets | 2 | Jira tickets generated from specs | Dev review pending |
| Approve/Edit Code | 3 | Code produced by Coding Agents | Dev review pending |

All checkpoints are **hard stops** — the pipeline is blocked until a human acts. There is no timeout-based auto-approval.

---

## Interruptions and Dev Holds

The pipeline can be interrupted at three levels:

1. **Clarification loop** — Phase 1 entry is gated by the Clarification Node. The pipeline loops until the input is unambiguous or escalates after 3 rounds.
2. **HITL holds** — Any of the four checkpoints puts the pipeline in a waiting state. Developers can: approve (advance), edit (re-run the generating agent with corrections), or reject (return to an earlier phase).
3. **Phase boundary holds** — The Developers Team handoff between Phase 1 and Phase 2 is an implicit hold — planning doesn't start until the team has reviewed the Phase 1 artifacts.

---

## Iterations

SDD supports iteration at multiple granularities:

### Within-phase iteration
At each HITL checkpoint, a developer can **edit and re-run** rather than approve. This sends corrected input back to the generating agent (PO Agent, Jira Agent, or Coding Agent) for a revised pass — without restarting the full pipeline.

### Phase-level rollback
If a downstream phase surfaces a problem traceable to an earlier artifact (e.g., tickets reveal a spec gap), the pipeline can return to the relevant phase's input and re-run from that point.

### Full pipeline re-entry
New inputs or significant scope changes re-enter at the Clarification Node, ensuring ambiguity is re-evaluated before any new work is committed.

---

## Key Design Principles

- **Human veto at every gate.** Agents propose; humans decide. No phase transition is autonomous.
- **Grounded generation.** Agents don't write from scratch — they read existing context (Vector DB, repo, tickets) before producing artifacts.
- **Sequential fidelity.** Each phase's output is the input for the next. Specs drive tickets. Tickets drive code. Nothing is written in a vacuum.
- **Separation of concerns.** Documentation, planning, and execution are distinct phases with distinct agent roles. Coding agents don't touch specs; the PO Agent doesn't write code.
- **Tool vs. Agent distinction.** Write operations to external systems (Jira Tool) are explicitly marked as tools — bounded, non-autonomous execution — as opposed to agents with reasoning loops.
