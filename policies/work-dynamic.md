# Work Dynamic

How humans and agents collaborate in sessions. This document defines the expected interaction patterns, roles, and escalation paths.

## Session roles

| Role | Responsibility |
|---|---|
| **Human (Product Owner)** | Provides input, approves specs, approves final docs, defines priorities |
| **Clarification Node** | Resolves ambiguous inputs before they reach the PO Agent |
| **PO Agent** | Transforms clarified input into structured Research Specs |
| **Specialist Agents** | Produce technical artifacts (vision, roadmap, tickets, ADRs) |
| **Claude (orchestrator)** | Routes between agents, enforces HITL checkpoints, surfaces decisions |

## Interaction patterns

### Pattern 1 — Happy path
```
Human input → Clarification Node → PO Agent → [HITL: approve specs]
→ Specialist Agents → [HITL: approve docs] → Final artifacts
```

### Pattern 2 — Clarification loop
```
Human input → Clarification Node → asks questions → Human answers
→ (repeat up to 3 rounds) → PO Agent → ...
```

### Pattern 3 — Spec edit loop
```
... → [HITL: edit specs] → Human provides edits → PO Agent revises
→ [HITL: approve specs] → ...
```

### Pattern 4 — Spec rejection
```
... → [HITL: reject specs] → Claude asks for new input → restart
```

## HITL checkpoint format

When Claude reaches a HITL checkpoint, it must present:

```
--- CHECKPOINT: [CHECKPOINT NAME] ---
Summary: <1-3 sentence summary of what was produced>

[Structured output: specs, docs, or ticket list]

Action required:
  approve  — proceed to next stage
  edit     — provide inline edits, Claude will revise
  reject   — discard and restart from input
```

Claude must wait for a response before continuing. It must not infer approval from silence or a partial answer.

## Escalation

If after 3 clarification rounds the input remains ambiguous, Claude must escalate by stating: "I cannot proceed without a clear [scope / acceptance criteria / owner]. Please provide this before we continue."

Claude must not fabricate missing information to unblock itself.
