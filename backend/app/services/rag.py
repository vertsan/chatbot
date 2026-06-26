from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.knowledge import DocumentChunk, DocumentStatus
from app.repositories.knowledge import DocumentRepository, KnowledgeBaseRepository
from app.services.base import ServiceResult


class RAGService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.kb_repo = KnowledgeBaseRepository(session)
        self.doc_repo = DocumentRepository(session)

    async def create_knowledge_base(
        self, user_id: str, name: str, **kwargs: object
    ) -> ServiceResult:
        kb = await self.kb_repo.create(
            user_id=user_id,
            name=name,
            **kwargs,
        )
        return ServiceResult.ok(kb, status_code=201)

    async def upload_document(
        self,
        user_id: str,
        kb_id: str,
        file_name: str,
        file_path: str,
        file_size: int,
        mime_type: str,  # noqa: ARG002
    ) -> ServiceResult:
        kb = await self.kb_repo.get(kb_id)
        if not kb:
            return ServiceResult.error_response("Knowledge base not found", 404)

        import magic
        mime = magic.from_file(file_path, mime=True)

        document_type = self._detect_document_type(file_name, mime)
        doc = await self.doc_repo.create(
            knowledge_base_id=kb_id,
            user_id=user_id,
            file_name=file_name,
            file_path=file_path,
            file_size=file_size,
            mime_type=mime,
            document_type=document_type,
            status=DocumentStatus.PENDING,
        )
        return ServiceResult.ok(doc, status_code=201)

    async def process_document(self, document_id: str) -> ServiceResult:
        doc = await self.doc_repo.get(document_id)
        if not doc:
            return ServiceResult.error_response("Document not found", 404)

        await self.doc_repo.update(document_id, status=DocumentStatus.PROCESSING)

        try:
            kb = await self.kb_repo.get(doc.knowledge_base_id)
            content = await self._extract_text(doc.file_path, doc.document_type)
            chunks = self._chunk_text(
                content,
                chunk_size=kb.chunk_size if kb else 1000,
                chunk_overlap=kb.chunk_overlap if kb else 200,
            )

            for i, chunk_content in enumerate(chunks):
                await self.session.execute(
                    # Insert chunk
                    await self._create_chunk(doc.id, i, chunk_content)
                )

            await self.doc_repo.update(
                document_id,
                status=DocumentStatus.READY,
                chunk_count=len(chunks),
            )
        except Exception as e:
            await self.doc_repo.update(
                document_id,
                status=DocumentStatus.ERROR,
                error_message=str(e),
            )
            return ServiceResult.error_response(f"Failed to process document: {e}")

        return ServiceResult.ok({"chunks": len(chunks)})

    async def search(
        self,
        kb_id: str,
        query: str,
        top_k: int = 5,
        similarity_threshold: float = 0.7,
    ) -> ServiceResult:
        kb = await self.kb_repo.get(kb_id)
        if not kb:
            return ServiceResult.error_response("Knowledge base not found", 404)

        documents, total = await self.doc_repo.get_by_knowledge_base(kb_id)
        relevant_chunks = []
        query_lower = query.lower()
        query_terms = set(query_lower.split())

        for doc in documents:
            if not doc.chunks:
                continue
            for chunk in doc.chunks:
                score = self._compute_similarity(query_lower, query_terms, chunk.content)
                if score >= similarity_threshold:
                    relevant_chunks.append({
                        "chunk_id": chunk.id,
                        "content": chunk.content,
                        "document_id": doc.id,
                        "document_name": doc.file_name,
                        "score": score,
                        "chunk_index": chunk.chunk_index,
                    })

        relevant_chunks.sort(key=lambda x: x["score"], reverse=True)
        relevant_chunks = relevant_chunks[:top_k]

        return ServiceResult.ok({
            "chunks": relevant_chunks,
            "query": query,
            "total_chunks": len(relevant_chunks),
        })

    def _detect_document_type(self, file_name: str, mime_type: str) -> str:  # noqa: ARG002
        ext = Path(file_name).suffix.lower()
        type_map = {
            ".pdf": "pdf",
            ".doc": "word",
            ".docx": "word",
            ".md": "markdown",
            ".txt": "text",
            ".csv": "csv",
            ".html": "html",
            ".htm": "html",
        }
        return type_map.get(ext, "text")

    async def _extract_text(self, file_path: str, doc_type: str) -> str:
        path = Path(file_path)
        if doc_type == "pdf":
            try:
                import pypdf
                reader = pypdf.PdfReader(str(path))
                return "\n".join(page.extract_text() for page in reader.pages)
            except ImportError:
                pass
        elif doc_type == "word":
            try:
                import docx
                doc = docx.Document(str(path))
                return "\n".join(p.text for p in doc.paragraphs)
            except ImportError:
                pass
        return path.read_text(encoding="utf-8", errors="replace")

    def _chunk_text(
        self, text: str, chunk_size: int = 1000, chunk_overlap: int = 200
    ) -> list[str]:
        if not text:
            return []
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            if end >= len(text):
                chunks.append(text[start:])
                break
            # Try to find a natural break
            break_chars = ["\n\n", "\n", ". ", "! ", "? "]
            adjusted_end = end
            for bc in break_chars:
                idx = text.rfind(bc, start, end)
                if idx > start + chunk_size // 2:
                    adjusted_end = idx + len(bc)
                    break
            chunks.append(text[start:adjusted_end])
            start = adjusted_end - chunk_overlap
        return chunks

    async def _create_chunk(
        self, doc_id: str, index: int, content: str
    ) -> DocumentChunk:
        import sqlalchemy as sa
        stmt = sa.insert(DocumentChunk).values(
            document_id=doc_id,
            content=content,
            chunk_index=index,
            token_count=len(content) // 4,
        ).returning(DocumentChunk)
        result = await self.session.execute(stmt)
        await self.session.flush()
        return result.scalar_one()

    def _compute_similarity(
        self, query_lower: str, query_terms: set, content: str
    ) -> float:
        content_lower = content.lower()
        # Simple keyword overlap scoring
        content_terms = set(content_lower.split())
        if not query_terms:
            return 0.0
        overlap = query_terms & content_terms
        score = len(overlap) / len(query_terms)
        # Boost for exact phrase match
        if query_lower in content_lower:
            score = max(score, 0.8)
        return score
