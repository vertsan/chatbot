from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.provider import AIModelRepository, AIProviderRepository
from app.schemas.provider import AIProviderCreate, AIProviderUpdate
from app.services.base import ServiceResult


class ProviderService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.provider_repo = AIProviderRepository(session)
        self.model_repo = AIModelRepository(session)

    async def get_all_providers(self) -> list[dict]:
        providers = await self.provider_repo.get_active()
        result = []
        for p in providers:
            models = await self.model_repo.get_by_provider(p.id)
            result.append({
                "id": p.id,
                "name": p.name,
                "provider_type": p.provider_type,
                "is_active": p.is_active,
                "is_default": p.is_default,
                "models": [
                    {"id": m.id, "name": m.name, "model_id": m.model_id}
                    for m in models
                ],
                "created_at": p.created_at,
            })
        return result

    async def create_provider(self, data: AIProviderCreate) -> ServiceResult:
        existing = await self.provider_repo.exists(name=data.name)
        if existing:
            return ServiceResult.error_response("Provider already exists", 409)

        provider = await self.provider_repo.create(**data.model_dump())
        return ServiceResult.ok(provider, status_code=201)

    async def get_provider_models(self, provider_id: str) -> ServiceResult:
        provider = await self.provider_repo.get(provider_id)
        if not provider:
            return ServiceResult.error_response("Provider not found", 404)

        models = await self.model_repo.get_by_provider(provider_id)
        return ServiceResult.ok(models)
