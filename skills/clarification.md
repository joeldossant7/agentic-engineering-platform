# Skill: Clarification

**Description:** Detects ambiguity in user inputs and generates targeted clarifying questions.

**When to use:** Inject at the start of any agent's processing when the input may be underspecified. Especially useful for the Clarification Node and any agent that accepts free-text user input.

---

## Injectable prompt block

```
Before proceeding, assess the input for ambiguity across these four dimensions:

1. SCOPE — Is what's being requested clearly bounded? Can you state in one sentence what is in and what is out?
2. ACCEPTANCE CRITERIA — Is there a clear definition of done? Can success be measured?
3. OWNER — Is it clear who is requesting this and for what purpose?
4. CONTRADICTIONS — Does the input contradict itself or conflict with known prior decisions?

If all four are clear: proceed.

If any are unclear: ask targeted questions using this format —
  "I need a few clarifications before proceeding:
  1. [specific question]
  2. [specific question]
  ..."

Rules:
- Maximum 3 questions per message.
- Maximum 3 rounds of clarification.
- Do not answer your own questions.
- After 3 rounds, escalate if still unclear.
```
