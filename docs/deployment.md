# Deployment Guide

## Prerequisites

- Docker 24+
- Docker Compose v2+
- 4GB+ RAM (8GB+ recommended)
- API keys for desired AI providers

## Production Deployment

### 1. Configure Environment

```bash
cp .env.example .env
# Edit .env with production values:
# - Generate secure SECRET_KEY and JWT_SECRET_KEY
# - Set strong database passwords
# - Configure S3/MinIO settings
# - Add API keys for providers
```

### 2. Deploy with Docker Compose

```bash
docker compose -f docker-compose.yml up -d

# Check logs
docker compose logs -f

# Verify health
curl http://localhost:8000/health
```

### 3. Run Database Migrations

```bash
docker compose exec backend alembic upgrade head
```

### 4. Create Initial Admin User

```bash
# The API will auto-create initial setup
# Access http://localhost:3000 to verify
```

## Kubernetes Deployment

### Prerequisites

- Kubernetes 1.28+
- kubectl configured
- Ingress controller (nginx-ingress recommended)
- cert-manager for TLS

### Deploy

```bash
# Create namespace
kubectl create namespace chatbot

# Apply configurations
kubectl apply -f deployment/k8s/configmap.yaml
kubectl apply -f deployment/k8s/secrets.yaml

# Deploy services
kubectl apply -f deployment/k8s/

# Verify
kubectl get pods -n chatbot
kubectl get ingress -n chatbot
```

## Scaling

### Horizontal Pod Autoscaling

```bash
kubectl autoscale deployment chatbot-backend \
  --cpu-percent=80 \
  --min=3 \
  --max=10 \
  -n chatbot
```

### Database Scaling

- Use read replicas for PostgreSQL
- Cluster Redis for high availability
- Use MinIO in distributed mode for storage

## Monitoring

### Prometheus

Metrics available at `/metrics` endpoint.

### Grafana

Import the dashboard from `deployment/monitoring/grafana-dashboard.json`

### Logging

Structured JSON logs are output to stdout. Use Loki or ELK for log aggregation.

## Backup

### Database

```bash
docker compose exec postgres pg_dump -U chatbot chatbot > backup.sql
```

### Storage

```bash
# Backup MinIO data
docker compose exec minio mc mirror /data /backup
```
