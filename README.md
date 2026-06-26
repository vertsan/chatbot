# Chatbot Platform

An open-source AI chatbot platform supporting multiple LLM providers, RAG, and multi-modal conversations.

## Features

- **Multi-Provider AI**: OpenAI, Anthropic, Google Gemini, Ollama, DeepSeek, Groq, and more
- **RAG Pipeline**: Upload documents (PDF, Word, Markdown, CSV, HTML) and query them
- **Streaming Responses**: Real-time token streaming via SSE
- **Vector Database**: pgvector, Chroma, Qdrant, Milvus
- **File Storage**: Local, S3, MinIO
- **Authentication**: JWT, OAuth ready, RBAC
- **Background Tasks**: Celery workers for embeddings, cleanup, notifications
- **Real-time**: Server-Sent Events for streaming
- **Dark Mode**: Full dark/light theme support
- **Responsive**: Works on desktop and mobile
- **Docker**: Full Docker Compose setup
- **Kubernetes**: Production-ready K8s manifests
- **CI/CD**: GitHub Actions pipeline

## Tech Stack

### Backend
- Python 3.13+, FastAPI, SQLAlchemy 2.0, Alembic
- PostgreSQL (pgvector), Redis, Celery
- Pydantic v2, OpenAPI, Swagger

### Frontend
- React 19, TypeScript, Vite
- TanStack Router, TanStack Query, TanStack Table
- TailwindCSS, shadcn/ui, Framer Motion
- Zustand, React Hook Form, Zod

### AI Providers
- OpenAI / Azure OpenAI
- Anthropic Claude
- Google Gemini
- Ollama (local)
- DeepSeek
- Groq
- HuggingFace
- LM Studio
- vLLM

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Python 3.13+ (for local development)
- Node.js 22+ (for frontend development)

### Clone and Run

```bash
git clone https://github.com/your-org/chatbot-platform
cd chatbot-platform

# Copy environment variables
cp .env.example .env
# Edit .env with your API keys

# Start all services
docker compose up -d

# Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Local Development

#### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\Activate.ps1  # Windows

pip install -e ".[dev]"

# Run database migrations
alembic upgrade head

# Start the server
uvicorn app.main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Project Structure

```
├── backend/
│   ├── app/
│   │   ├── api/          # HTTP layer (controllers, middleware)
│   │   ├── core/         # Configuration, security
│   │   ├── database/     # Database setup, base models
│   │   ├── domain/       # Domain models
│   │   ├── models/       # SQLAlchemy models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── services/     # Business logic
│   │   ├── repositories/ # Data access
│   │   ├── providers/    # AI provider abstractions
│   │   ├── workers/      # Celery tasks
│   │   └── main.py       # App entry point
│   ├── alembic/          # Database migrations
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── api/          # API client
│   │   ├── components/   # UI components
│   │   ├── features/     # Feature modules
│   │   ├── hooks/        # React hooks
│   │   ├── pages/        # Route pages
│   │   ├── store/        # Zustand stores
│   │   └── types/        # TypeScript types
│   └── public/
├── deployment/
│   ├── k8s/              # Kubernetes manifests
│   └── monitoring/       # Prometheus/Grafana configs
├── docs/                 # Documentation
└── docker-compose.yml
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Authentication

All API endpoints (except login/register) require JWT authentication.

```
POST /api/v1/auth/register   - Register new user
POST /api/v1/auth/login      - Login
POST /api/v1/auth/refresh    - Refresh token
GET  /api/v1/auth/me         - Get current user
```

### Chat

```
GET    /api/v1/chats                  - List chats
POST   /api/v1/chats                  - Create chat
POST   /api/v1/chats/conversations    - Create conversation
GET    /api/v1/chats/conversations    - List conversations
POST   /api/v1/chats/conversations/{id}/messages    - Send message
POST   /api/v1/chats/conversations/{id}/stream      - Stream message
```

### RAG

```
POST /api/v1/knowledge/bases              - Create knowledge base
POST /api/v1/knowledge/bases/{id}/documents/upload  - Upload document
POST /api/v1/knowledge/search             - Search knowledge base
```

## Configuration

See `.env.example` for all configuration options. Key settings:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `REDIS_URL` | Redis connection string | Required |
| `SECRET_KEY` | Application secret key | Required |
| `JWT_SECRET_KEY` | JWT signing key | Required |
| `OPENAI_API_KEY` | OpenAI API key | Optional |
| `ANTHROPIC_API_KEY` | Anthropic API key | Optional |
| `OLLAMA_BASE_URL` | Ollama server URL | http://localhost:11434 |

## Testing

```bash
# Backend tests
cd backend
pytest app/tests/ -v --cov=app

# Frontend tests
cd frontend
npm run test:run

# E2E tests
npm run test:e2e
```

## Deployment

### Docker Compose (recommended for production)

```bash
docker compose -f docker-compose.yml up -d
```

### Kubernetes

```bash
kubectl apply -f deployment/k8s/
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

MIT License - see [LICENSE](LICENSE) for details.
