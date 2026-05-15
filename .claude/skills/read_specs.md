# Skill: Read Specs

**Description:** Retrieves and interprets existing Research Specs from the Vector DB or filesystem before producing new output.

**When to use:** Inject whenever an agent needs to be aware of prior work, existing specifications, or architectural decisions before generating new content. Prevents duplication and contradiction.

---

## Injectable prompt block

```
Before generating output, retrieve relevant prior specifications:

1. Query the Vector DB with the key terms from the current input (feature name, domain, system name).
2. If results are found, read them and identify:
   - What has already been decided or built
   - Open questions from prior specs that remain unresolved
   - Dependencies that the current work inherits
3. If no results are found, state: "No prior specs found for this domain."

When producing output:
- Reference prior spec IDs where relevant (e.g., "per Spec #YYYY-01...")
- Do not contradict prior decisions without explicitly flagging the conflict
- Flag conflicts as: "⚠️ Conflict with [Spec #ID]: [description of conflict]"

If Vector DB is unavailable: proceed without it and note "Vector DB unavailable — spec context not retrieved."
```
