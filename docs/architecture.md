# Architecture

## Clean Architecture Layers

```
┌─────────────────────────────────────────┐
│          Presentation (API)             │
│  Controllers, Middleware, Dependencies  │
├─────────────────────────────────────────┤
│          Application (Services)         │
│      Business Logic, Orchestration      │
├─────────────────────────────────────────┤
│             Domain (Models)             │
│     Entities, Value Objects, Rules      │
├─────────────────────────────────────────┤
│         Infrastructure (Data)           │
│  Repositories, Database, External APIs  │
└─────────────────────────────────────────┘
```

## Component Diagram

```
┌──────────┐     ┌──────────┐     ┌──────────┐
│  Frontend │────▶│  Backend │────▶│    AI    │
│  (React)  │     │ (FastAPI)│     │Providers │
└──────────┘     └────┬─────┘     └──────────┘
                      │
              ┌───────┴────────┐
              │                │
         ┌────▼────┐    ┌─────▼─────┐
         │PostgreSQL│    │   Redis   │
         │(pgvector)│    │           │
         └─────────┘    └───────────┘
              │
         ┌────▼────┐
         │  MinIO  │
         │  (S3)   │
         └─────────┘
```

## Data Flow

1. User sends message via frontend
2. Frontend sends POST to `/api/v1/chats/conversations/{id}/stream`
3. Backend creates user message in database
4. Backend loads conversation history
5. Backend calls appropriate AI provider
6. Response streamed back via SSE
7. Frontend renders tokens in real-time
8. Assistant message saved to database
