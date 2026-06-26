from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.auth import get_current_user
from app.database.session import get_session
from app.models.user import User
from app.schemas.rag import (
    DocumentUploadResponse,
    KnowledgeBaseCreate,
    KnowledgeBaseResponse,
    RAGQuery,
    RAGResult,
)
from app.services.rag import RAGService

router = APIRouter(prefix="/knowledge", tags=["Knowledge Bases"])


@router.post("/bases", response_model=KnowledgeBaseResponse, status_code=201)
async def create_knowledge_base(
    request: KnowledgeBaseCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    service = RAGService(session)
    result = await service.create_knowledge_base(
        user_id=current_user.id,
        name=request.name,
        description=request.description,
        embedding_model=request.embedding_model,
        chunk_size=request.chunk_size,
        chunk_overlap=request.chunk_overlap,
    )
    return result.data


@router.post("/bases/{kb_id}/documents/upload", response_model=DocumentUploadResponse, status_code=201)
async def upload_document(
    kb_id: str,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    import aiofiles
    import os
    from pathlib import Path

    upload_dir = Path("uploads/documents")
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / f"{os.urandom(16).hex()}_{file.filename}"
    async with aiofiles.open(str(file_path), "wb") as f:
        content = await file.read()
        await f.write(content)

    service = RAGService(session)
    result = await service.upload_document(
        user_id=current_user.id,
        kb_id=kb_id,
        file_name=file.filename or "unknown",
        file_path=str(file_path),
        file_size=len(content),
        mime_type=file.content_type or "application/octet-stream",
    )
    if not result.success:
        raise HTTPException(status_code=result.status_code, detail=result.error)
    return result.data


@router.post("/bases/{kb_id}/documents/{doc_id}/process")
async def process_document(
    kb_id: str,
    doc_id: str,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    service = RAGService(session)
    result = await service.process_document(doc_id)
    if not result.success:
        raise HTTPException(status_code=result.status_code, detail=result.error)
    return result.data


@router.post("/search", response_model=RAGResult)
async def search_knowledge_base(
    request: RAGQuery,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    service = RAGService(session)
    result = await service.search(
        kb_id=request.knowledge_base_id,
        query=request.query,
        top_k=request.top_k,
        similarity_threshold=request.similarity_threshold,
    )
    if not result.success:
        raise HTTPException(status_code=result.status_code, detail=result.error)
    return result.data
