# Skill: Systems Design

**Description:** Produces structured systems design artifacts — component diagrams, data flow descriptions, API contracts, and architectural decision records (ADRs).

**When to use:** Inject when an agent needs to reason about architecture, system boundaries, integrations, or technical trade-offs. Used by the PO Agent (to understand system context) and by the systems-design specialist agent (to produce formal design output).

---

## Injectable prompt block

```
When producing systems design output, structure your thinking as follows:

1. COMPONENTS — Identify the main system components involved. For each, state:
   - Name and responsibility (one sentence)
   - Owner (team or agent)
   - Interface type (API, event, file, DB)

2. DATA FLOW — Describe how data moves between components:
   - Trigger: what initiates the flow
   - Steps: numbered sequence of operations
   - Output: what is produced and where it goes

3. BOUNDARIES — State what is inside and outside the system:
   - In scope: components you will design or modify
   - Out of scope: components you depend on but will not change

4. TRADE-OFFS — For any significant design choice, document:
   - Option A vs Option B
   - Decision: which was chosen
   - Reason: why (performance, cost, team capability, existing patterns)

5. ADR (if a significant decision is made):
   ```
   # ADR-[NUMBER]: [Decision Title]
   Status: Proposed | Accepted | Deprecated
   Context: <Why this decision was needed>
   Decision: <What was decided>
   Consequences: <What this means going forward>
   ```

Use diagrams in Mermaid syntax when helpful:
  graph LR
    A[Component A] --> B[Component B]
```
