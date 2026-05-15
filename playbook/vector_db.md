# Playbook: Vector DB Integration

## Overview

The Vector DB is the organizational memory — it stores embeddings of Research Specs, ADRs, architectural decisions, and approved documents. Agents query it for context retrieval (RAG) before producing output.

**Rule:** Agents may only READ from the Vector DB during sessions. Writes require a dedicated indexing pipeline (see Indexing section).

## Supported backends

This playbook is written for **pgvector** (PostgreSQL extension) as the primary backend. Adapters for Pinecone and Chroma follow the same interface contract.

## Connection

```bash
# Required environment variables
VECTOR_DB_HOST=localhost
VECTOR_DB_PORT=5432
VECTOR_DB_NAME=org_knowledge
VECTOR_DB_USER=<service_account>
VECTOR_DB_PASSWORD=<YOUR_PASSWORD>
EMBEDDING_MODEL=text-embedding-3-small   # OpenAI or compatible
```

## Schema

```sql
CREATE TABLE documents (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  doc_type    TEXT NOT NULL,        -- 'spec', 'adr', 'vision', 'roadmap'
  doc_id      TEXT NOT NULL,        -- e.g., 'SPEC-2026-001'
  title       TEXT NOT NULL,
  content     TEXT NOT NULL,
  embedding   VECTOR(1536),         -- dimension matches embedding model
  metadata    JSONB,
  created_at  TIMESTAMPTZ DEFAULT NOW(),
  updated_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX ON documents USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);
```

## Query pattern — semantic search

```python
import psycopg2
import openai
import os

def search_specs(query: str, top_k: int = 5, doc_type: str = None):
    # 1. Embed the query
    response = openai.embeddings.create(
        input=query,
        model=os.environ["EMBEDDING_MODEL"]
    )
    query_embedding = response.data[0].embedding

    # 2. Query the DB
    conn = psycopg2.connect(
        host=os.environ["VECTOR_DB_HOST"],
        port=os.environ["VECTOR_DB_PORT"],
        dbname=os.environ["VECTOR_DB_NAME"],
        user=os.environ["VECTOR_DB_USER"],
        password=os.environ["VECTOR_DB_PASSWORD"]
    )
    cur = conn.cursor()

    type_filter = "AND doc_type = %s" if doc_type else ""
    params = [query_embedding, top_k] if not doc_type else [query_embedding, doc_type, top_k]

    cur.execute(f"""
        SELECT doc_id, title, content, metadata,
               1 - (embedding <=> %s::vector) AS similarity
        FROM documents
        WHERE 1=1 {type_filter}
        ORDER BY embedding <=> %s::vector
        LIMIT %s
    """, [query_embedding] + ([doc_type] if doc_type else []) + [top_k])

    results = cur.fetchall()
    cur.close()
    conn.close()
    return results
```

## Indexing pipeline

Indexing is a separate process — not triggered by agent sessions.

```python
def index_document(doc_id: str, doc_type: str, title: str, content: str, metadata: dict):
    embedding = get_embedding(content)
    upsert_to_db(doc_id, doc_type, title, content, embedding, metadata)
```

Trigger indexing when:
- A new Research Spec is approved at HITL
- A new ADR is produced and accepted
- A Vision or Roadmap document is finalized

## Result format returned to agents

```json
[
  {
    "doc_id": "SPEC-2026-001",
    "title": "User Authentication Redesign",
    "similarity": 0.91,
    "excerpt": "First 500 chars of content...",
    "metadata": { "approved_at": "2026-03-15", "approved_by": "Joel" }
  }
]
```

## Setup checklist

- [ ] PostgreSQL with pgvector extension installed (`CREATE EXTENSION vector;`)
- [ ] Schema created (run the SQL above)
- [ ] Environment variables configured
- [ ] Embedding model API key available
- [ ] At least one document indexed for testing
- [ ] Index created with correct vector dimension
