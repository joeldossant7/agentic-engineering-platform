# Agentic Engineering Platform

Este repo NO pertenece a un proyecto. Pertenece a la organización.

**ESTE REPO NO TIENE FEATURES.**
Tiene: conocimiento reusable, operational doctrine, engineering governance.

Es el "cerebro corporativo".

---

## Estructura

```
agentic-engineering-platform/
├── .sdd/                       ← SDD Framework documentation
│   ├── spec-driven-development.md  ← Core SDD methodology and architecture
│   └── sdd-workflow.pdf        ← Visual workflow diagrams
│
├── .claude/                    ← Contenedor de configuración y knowledge base
│   ├── settings.json           ← Permisos y hooks de Claude Code
│   ├── settings.local.json     ← Configuración local (no versionada)
│   ├── requirements.txt        ← anthropic, psycopg2, pgvector, python-dotenv
│   ├── audit.log               ← Registro de operaciones
│   │
│   ├── agents/                 ← Identidad e implementación de cada agente
│   │   ├── clarification_node/
│   │   │   ├── config.json     ← Modelo: claude-sonnet-4-6
│   │   │   └── clarification_node.py ← Node implementation
│   │   ├── po_agent/
│   │   │   ├── config.json     ← Modelo: claude-opus-4-7
│   │   │   └── po_agent.py     ← Agent implementation
│   │   ├── planner_agent/
│   │   │   ├── config.json     ← Modelo: claude-opus-4-7
│   │   │   └── planner_agent.py
│   │   └── jira_agent/
│   │       ├── config.json     ← Modelo: claude-sonnet-4-6
│   │       └── jira_agent.py   ← Jira integration
│   │
│   ├── contracts/              ← Schemas de mensajes entre agentes
│   │   ├── clarification_to_po.json      ← Output → PO Agent
│   │   ├── po_to_specialists.json        ← PO Agent → Sub-agents
│   │   └── planner_to_hitl.json          ← Planner → HITL handoff
│   │
│   ├── llm/                    ← Node implementations (agent logic)
│   │   └── clarification_node.py
│   │
│   ├── playbook/               ← Guías de integración con herramientas
│   │   ├── jira.md             ← Autenticación, field mapping, rate limits
│   │   ├── github.md           ← PR workflow, branches, commits
│   │   └── vector_db.md        ← pgvector schema, queries, indexing
│   │
│   ├── policies/               ← Governance y constraints
│   │   ├── sdd.md              ← SDD policy enforcement
│   │   ├── constraints.md      ← Límites duros de comportamiento
│   │   ├── constraints.json    ← Machine-readable index
│   │   ├── rules.md            ← Workflow rules
│   │   ├── rules.json          ← Machine-readable index
│   │   └── work-dynamic.md     ← HITL dynamics and interactions
│   │
│   ├── prompts/                ← System prompts por agente
│   │   ├── clarification_node.md
│   │   ├── po_agent.md
│   │   ├── planner_agent.md
│   │   └── jira_agent.md
│   │
│   └── skills/                 ← Fragmentos de prompt inyectables
│       ├── clarification.md    ← Detección de ambigüedad
│       ├── validator.md        ← Critical evaluation
│       ├── executioner.md      ← Strict implementation execution
│       ├── read_specs.md       ← Recuperación de specs
│       ├── read_data.md        ← Recuperación de datos
│       ├── systems_design.md   ← Diseño de sistemas
│       ├── project_management.md ← Planning and roadmaps
│       └── ticket_assembly.md  ← Epic → Story → Task
│
└── README.md                   ← Este archivo
```

## Cómo usar este repo

### Overview of Components

**Agents:**
- **Clarification Node** — Disambiguates ambiguous input before work begins (max 3 rounds)
- **Product Owner Agent** — Researches specs against Vector DB, writes draft specifications
- **Planner Agent** — Assembles documentation, roadmap, and TODO from specs
- **Jira Agent** — Generates Jira tickets from approved specs

**Skills (reusable prompt fragments):**
- `clarification.md` — Ambiguity detection patterns
- `validator.md` — Critical evaluation and verification
- `executioner.md` — Strict implementation execution
- `read_specs.md` — Vector DB retrieval patterns
- `systems_design.md` — Architecture and design patterns
- `ticket_assembly.md` — Epic → Story → Task hierarchy
- `project_management.md` — MoSCoW, phases, roadmaps

**Integrations (playbooks):**
- `jira.md` — Jira authentication, field mapping, rate limits
- `github.md` — PR workflow, branch conventions, commit strategy
- `vector_db.md` — pgvector schema, query patterns, indexing

### Para implementar SDD en un proyecto

1. **Copy agent configs** to your project:
   ```
   .claude/agents/{clarification_node,po_agent,planner_agent,jira_agent}/config.json
   ```

2. **Reference SDD policies** in your project's CLAUDE.md:
   - Include `policies/sdd.md`
   - Include `policies/work-dynamic.md`
   - Include `policies/constraints.md`

3. **Set up integrations** (see `playbook/`):
   - Configure Jira credentials and field mappings
   - Configure Vector DB connection
   - Configure GitHub branch conventions

4. **Use skills in prompts**:
   - Inject skills via CLAUDE.md or prompt templates
   - Skills are stateless, composable prompt fragments

### Para extender el framework

- **Nuevo agente:** crear `agents/<nombre>/config.json` + `prompts/<nombre>.md` + implementación
- **Nueva skill:** agregar `skills/<nombre>.md` con la lógica inyectable
- **Nueva integración:** agregar `playbook/<herramienta>.md` con autenticación y patrones
- **Nueva policy:** agregar en `policies/` y referenciarla en `CLAUDE.md`

## Spec-Driven Development (SDD) Framework

Agentic Engineering Platform implements a **3-phase pipeline** that transforms raw requests into shipped code, with human veto power at every critical gate.

### Quick Flow

```
Input/Basket
    ↓
[Phase 1] Documentation + Specs Generation
    ├─ Clarification Node: disambiguates input
    ├─ Product Owner Agent + Vector DB: researches specs
    ├─ Sub-agents (coding, systems, infra, PM): contribute specs
    ├─ [HITL] Approve/Edit Specs ← human gate
    ├─ Assemble docs (vision, roadmap, TODO, ticket draft)
    └─ [HITL] Approve/Edit Docs ← human gate
    ↓
[Phase 2] Planning
    ├─ Developers Team receives approved docs
    ├─ Jira Agent: generates tickets from specs
    └─ [HITL] Approve/Edit Tickets ← human gate
    ↓
[Phase 3] Execution
    ├─ Coding Agents: implement tickets
    │  (read repo + ticket before coding)
    └─ [HITL] Approve/Edit Code ← human gate
    ↓
GitHub (commit branch)
```

### Key Principles

- **Human veto at every gate.** Agents propose; humans decide.
- **Grounded generation.** Agents read existing context (Vector DB, repo, tickets) before producing output.
- **Sequential fidelity.** Specs → Docs → Tickets → Code. Nothing written in a vacuum.
- **Separation of concerns.** Documentation, planning, and execution are distinct phases with distinct roles.
- **Tool vs. Agent distinction.** Write operations (Jira Tool) are bounded, non-autonomous.

### HITL Checkpoints

| Checkpoint | Phase | What's reviewed | Condition |
|---|---|---|---|
| Approve/Edit Specs | 1 | Draft specification from research | Dev review required |
| Approve/Edit Docs | 1 | Vision, roadmap, TODO, ticket draft | Dev review required |
| Approve/Edit Tickets | 2 | Jira tickets generated from specs | Dev review required |
| Approve/Edit Code | 3 | Code from Coding Agents | Dev review required |

All checkpoints are **hard stops** — no timeout-based auto-approval.

For details, see [`.sdd/spec-driven-development.md`](./.sdd/spec-driven-development.md).
