from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_superuser
from app.database.session import get_session
from app.models.user import User
from app.providers.ai.registry import ProviderRegistry
from app.schemas.provider import (
    AIModelResponse,
    AIProviderCreate,
    AIProviderResponse,
)
from app.services.provider import ProviderService

router = APIRouter(prefix="/providers", tags=["Providers"])


@router.get("")
async def list_providers(
    session: AsyncSession = Depends(get_session),
    _: User = Depends(get_superuser),
) -> list[dict]:
    service = ProviderService(session)
    return await service.get_all_providers()


@router.post("", response_model=AIProviderResponse, status_code=201)
async def create_provider(
    request: AIProviderCreate,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(get_superuser),
) -> dict:
    service = ProviderService(session)
    result = await service.create_provider(request)
    if not result.success:
        raise HTTPException(status_code=result.status_code, detail=result.error)
    return result.data


@router.get("/{provider_id}/models", response_model=list[AIModelResponse])
async def list_provider_models(
    provider_id: str,
    session: AsyncSession = Depends(get_session),
    _: User = Depends(get_superuser),
) -> dict:
    service = ProviderService(session)
    result = await service.get_provider_models(provider_id)
    if not result.success:
        raise HTTPException(status_code=result.status_code, detail=result.error)
    return result.data


@router.get("/available")
async def list_available_providers() -> list[dict]:
    providers = ProviderRegistry.get_all()
    return [
        {"name": name, "capabilities": provider.capabilities}
        for name, provider in providers.items()
    ]
