# Skill: Ticket Assembly

**Description:** Converts planning artifacts into a structured Epic → Story → Task ticket hierarchy ready for Jira or Linear import.

**When to use:** Inject as the final step of the Planner Agent's output, or standalone when converting an approved spec into tickets.

---

## Injectable prompt block

```
When assembling tickets, apply the following rules:

HIERARCHY:
  Epic  → represents a feature or major initiative (weeks to months)
  Story → represents a user-facing capability within an epic (days to 1 week)
  Task  → represents a single technical unit of work within a story (hours to 1 day)

EPIC FORMAT:
  Title: [EPIC] <Feature name>
  Description: <What this epic delivers. Business value.>
  Acceptance criteria: <How we know the epic is complete>
  Labels: [epic, <domain>]

STORY FORMAT:
  Title: <Action verb> <capability> for <user type>
  User story: As a [user type] I want [goal] so that [benefit]
  Acceptance criteria:
    - Given [context], when [action], then [outcome]
    - (minimum 2 criteria per story)
  Estimate: S (1pt) | M (3pt) | L (5pt) | XL (8pt)
  Labels: [story, <domain>]

TASK FORMAT:
  Title: <Technical action> — <specific component>
  Description: <What needs to be done technically>
  Estimate: S | M | L
  Labels: [task, <component>]

RULES:
  - Every story must belong to an epic.
  - Every task must belong to a story.
  - No orphan tickets.
  - Do not create tickets for open questions — list them separately under "Blocked by open questions."
  - Acceptance criteria must be testable (Given/When/Then format preferred).
  - Estimates are relative, not hour-based.
```
