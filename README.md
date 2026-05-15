# Agentic Engineering Platform

Este repo NO pertenece a un proyecto. Pertenece a la organización.

**ESTE REPO NO TIENE FEATURES.**
Tiene: conocimiento reusable, operational doctrine, engineering governance.

Es el "cerebro corporativo".

---

## Estructura

```
agentic-engineering-platform/
├── .claude/                    ← Contenedor de configuración y knowledge base
│   ├── CLAUDE.md               ← Comportamiento de Claude en sesión (leer primero)
│   ├── settings.json           ← Permisos y hooks de Claude Code
│   ├── requirements.txt        ← anthropic, psycopg2, pgvector, python-dotenv
│   │
│   ├── agents/                 ← Identidad de cada agente
│   │   ├── clarification_node/
│   │   │   └── config.json     ← Modelo: claude-sonnet-4-6
│   │   ├── po_agent/
│   │   │   └── config.json     ← Modelo: claude-opus-4-7
│   │   ├── planner_agent/
│   │   │   └── config.json     ← Modelo: claude-opus-4-7
│   │   └── jira_agent/
│   │       └── config.json     ← Modelo: claude-sonnet-4-6
│   │
│   ├── contracts/              ← Schemas de mensajes entre agentes
│   │   ├── clarification_to_po.json
│   │   ├── po_to_specialists.json
│   │   └── planner_to_hitl.json
│   │
│   ├── llm/                    ← Implementaciones de nodos LLM
│   │   └── clarification_node.py
│   │
│   ├── playbook/               ← Guías de integración con herramientas externas
│   │   ├── jira.md             ← Autenticación, field mapping, rate limits
│   │   ├── github.md           ← PR workflow, issue creation, branch conventions
│   │   └── vector_db.md        ← pgvector schema, query patterns, indexing
│   │
│   ├── policies/               ← Governance y constraints para Claude
│   │   ├── constraints.md      ← Límites duros de comportamiento
│   │   ├── rules.md            ← Reglas de flujo de trabajo (R-01 a R-10)
│   │   ├── work-dynamic.md     ← Dinámica HITL y patrones de interacción
│   │   ├── constraints.json    ← Índice machine-readable de constraints
│   │   ├── rules.json          ← Índice machine-readable de rules
│   │   └── README.es.md        ← Guía de políticas en español
│   │
│   ├── prompts/                ← System prompts por agente
│   │   ├── po_agent.md
│   │   ├── planner_agent.md
│   │   ├── jira_agent.md
│   │   └── clarification_node.md
│   │
│   └── skills/                 ← Fragmentos de prompt inyectables
│       ├── clarification.md    ← Detección de ambigüedad
│       ├── read_specs.md       ← Recuperación de specs del Vector DB
│       ├── read_data.md        ← Recuperación de datos estructurados
│       ├── systems_design.md   ← Diseño de sistemas, ADRs, Mermaid
│       ├── project_management.md ← MoSCoW, fases, roadmaps, risks
│       └── ticket_assembly.md  ← Epic → Story → Task hierarchy
│
└── README.md                   ← Este archivo
```

## Cómo usar este repo

### En una sesión de Claude Code
Claude Code lee `CLAUDE.md` automáticamente al iniciar. Las políticas aplican sin configuración adicional.

### Para un nuevo proyecto
1. Copia los `config.json` del agente relevante a tu proyecto
2. Referencia los prompts y skills de este repo en tu `CLAUDE.md` de proyecto
3. Configura tus variables de entorno (ver `playbook/`)

### Para extender
- Nuevo agente: crear `agents/<nombre>/config.json` + `prompts/<nombre>.md`
- Nueva integración: agregar `playbook/<herramienta>.md`
- Nueva skill: agregar `skills/<nombre>.md` con el bloque inyectable
- Nueva policy: agregar `.md` en `policies/` y referenciarla en `CLAUDE.md`

## Flujo SDD

```
Input → Clarification Node → PO Agent → [HITL: approve specs]
      → Specialist Agents  → Planner Agent → [HITL: approve docs]
      → Jira Agent         → Tickets creados en Jira
```

Los checkpoints HITL son obligatorios. Ver `policies/work-dynamic.md`.
