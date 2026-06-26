from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_current_user
from app.core.security.password import hash_password, verify_password
from app.database.session import get_session
from app.models.user import User
from app.repositories.user import UserRepository
from app.schemas.auth import (
    ChangePasswordRequest,
    LoginRequest,
    OAuthLoginRequest,
    PasswordResetConfirm,
    PasswordResetRequest,
    RefreshTokenRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)
from app.schemas.common import MessageResponse
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=201)
async def register(
    request: RegisterRequest,
    session: AsyncSession = Depends(get_session),
) -> User:
    service = AuthService(session)
    result = await service.register(
        email=request.email,
        password=request.password,
        display_name=request.display_name,
    )
    if not result.success:
        raise HTTPException(status_code=result.status_code, detail=result.error)
    return result.data["user"]


@router.post("/login", response_model=TokenResponse)
async def login(
    request: LoginRequest,
    session: AsyncSession = Depends(get_session),
) -> dict:
    service = AuthService(session)
    result = await service.login(
        email=request.email,
        password=request.password,
    )
    if not result.success:
        raise HTTPException(status_code=result.status_code, detail=result.error)
    return result.data


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    session: AsyncSession = Depends(get_session),
) -> dict:
    service = AuthService(session)
    result = await service.refresh_token(request.refresh_token)
    if not result.success:
        raise HTTPException(status_code=result.status_code, detail=result.error)
    return result.data


@router.post("/oauth/{provider}", response_model=TokenResponse)
async def oauth_login(
    provider: str,
    request: OAuthLoginRequest,
    session: AsyncSession = Depends(get_session),
) -> dict:
    service = AuthService(session)
    result = await service.oauth_login(
        provider=provider,
        provider_id=request.code,
        email="",
        display_name="",
    )
    if not result.success:
        raise HTTPException(status_code=result.status_code, detail=result.error)
    return result.data


@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: User = Depends(get_current_user),
) -> User:
    return current_user


@router.post("/change-password", response_model=MessageResponse)
async def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    if not verify_password(request.current_password, current_user.password_hash or ""):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    user_repo = UserRepository(session)
    await user_repo.update(
        current_user.id, password_hash=hash_password(request.new_password)
    )
    return {"message": "Password changed successfully", "status_code": 200}


@router.post("/logout", response_model=MessageResponse)
async def logout(
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> dict:
    return {"message": "Logged out successfully", "status_code": 200}
