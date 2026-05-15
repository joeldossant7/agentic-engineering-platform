# Skill: Read Data

**Description:** Retrieves structured data (metrics, schemas, usage stats) relevant to the current task from available data sources.

**When to use:** Inject when an agent needs factual data to inform a spec, roadmap, or design decision — rather than relying on assumptions or hallucinated numbers.

---

## Injectable prompt block

```
If factual data is needed to support this task, retrieve it before making claims:

Data sources available (use whichever apply):
- Vector DB: organizational knowledge, prior analyses, documented metrics
- Provided files: any files attached to this session
- User-provided context: data stated explicitly in the conversation

When referencing data:
- Cite the source: "According to [source], ..."
- If data is unavailable, state the assumption explicitly: "Assuming X (unverified) — please confirm."
- Do not fabricate metrics, user counts, performance figures, or dates.

If no data is available and data is required to proceed, ask the human:
  "To proceed accurately, I need [specific data point]. Can you provide it?"
```
