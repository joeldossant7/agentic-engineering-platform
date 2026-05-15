# Skill: Project Management

**Description:** Produces roadmaps, milestone plans, risk registers, and sprint structures from approved specs.

**When to use:** Inject when an agent needs to organize work into phases, assign priorities, or produce planning artifacts. Used primarily by the Planner Agent.

---

## Injectable prompt block

```
When producing project management output, apply the following structure:

PRIORITIZATION — Use MoSCoW:
  Must have: required for the initiative to deliver value
  Should have: important but not blocking
  Could have: desirable if time permits
  Won't have (this cycle): explicitly deferred

PHASING — Group work into phases:
  - Each phase should deliver a testable, deployable increment
  - Phases should not exceed 4–6 weeks unless justified
  - Define a clear entry condition and exit condition for each phase

MILESTONES — For each phase, define:
  - A milestone name (e.g., "Alpha release", "Data pipeline live")
  - Success criteria (measurable)
  - Owner (team or agent responsible)

RISKS — Identify top 3 risks:
  | Risk | Likelihood | Impact | Mitigation |
  |------|-----------|--------|-----------|
  | ... | H/M/L | H/M/L | ... |

ASSUMPTIONS — List explicit assumptions the plan depends on.
  If any assumption is invalidated, the plan must be revisited.

OUTPUT FORMAT:
  Use markdown with clear headers.
  Use checkboxes [ ] for milestones and deliverables.
  Do not use Gantt charts — use phase tables instead.
```
