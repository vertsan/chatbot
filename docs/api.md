# API Documentation

## Authentication

```
POST /api/v1/auth/register
{
  "email": "user@example.com",
  "password": "securepassword",
  "display_name": "John Doe"
}
→ 201 { "id": "...", "email": "...", ... }

POST /api/v1/auth/login
{
  "email": "user@example.com",
  "password": "securepassword"
}
→ 200 {
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer",
  "expires_in": 1800,
  "user": { ... }
}

POST /api/v1/auth/refresh
{
  "refresh_token": "..."
}
→ 200 { "access_token": "...", "refresh_token": "...", ... }

GET /api/v1/auth/me
Authorization: Bearer <token>
→ 200 { "id": "...", "email": "...", ... }
```

## Chats

```
POST /api/v1/chats
{
  "title": "My Chat",
  "model_id": null,
  "system_prompt": null,
  "temperature": 0.7
}
→ 201 { ... }

GET /api/v1/chats?skip=0&limit=50
→ 200 { "items": [...], "total": 10 }
```

## Conversations

```
POST /api/v1/chats/conversations
{
  "chat_id": "...",
  "title": "New Conversation"
}
→ 201 { ... }

GET /api/v1/chats/conversations?page=1&page_size=50&search=query
→ 200 { "items": [...], "total": 5, "page": 1, "page_size": 50 }

POST /api/v1/chats/conversations/{id}/messages
{
  "content": "Hello!",
  "role": "user"
}
→ 201 { ... }
```

## Streaming

```
POST /api/v1/chats/conversations/{id}/stream
Content-Type: application/json
Authorization: Bearer <token>

{
  "content": "Tell me about AI",
  "role": "user"
}

→ Server-Sent Events:
event: token
data: {"content": "Artificial", "done": false}

event: token
data: {"content": " Intelligence", "done": false}

event: done
data: ""
```

## Knowledge Bases (RAG)

```
POST /api/v1/knowledge/bases
{
  "name": "Company Docs",
  "description": "Internal documentation",
  "embedding_model": "text-embedding-3-small",
  "chunk_size": 1000,
  "chunk_overlap": 200
}
→ 201 { ... }

POST /api/v1/knowledge/bases/{id}/documents/upload
Content-Type: multipart/form-data
file: <binary>
→ 201 { ... }

POST /api/v1/knowledge/search
{
  "query": "What is our return policy?",
  "knowledge_base_id": "...",
  "top_k": 5,
  "similarity_threshold": 0.7
}
→ 200 {
  "chunks": [...],
  "query": "...",
  "total_chunks": 3
}
```

## Providers

```
GET /api/v1/providers
→ 200 [{ "name": "openai", "models": [...] }, ...]

GET /api/v1/providers/available
→ 200 [{ "name": "ollama", "capabilities": {...} }, ...]
```

## Health

```
GET /health
→ 200 { "status": "healthy", "version": "1.0.0" }
```

## Error Format

All errors follow:
```json
{
  "detail": "Error description",
  "status_code": 400,
  "error_code": "VALIDATION_ERROR"
}
```

HTTP Status Codes:
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 409: Conflict
- 429: Rate Limited
- 500: Internal Server Error
