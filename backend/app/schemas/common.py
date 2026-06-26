from pydantic import BaseModel


class PaginationParams(BaseModel):
    page: int = 1
    page_size: int = 50


class PaginatedResponse(BaseModel):
    items: list
    total: int
    page: int
    page_size: int


class MessageResponse(BaseModel):
    message: str
    status_code: int = 200


class ErrorResponse(BaseModel):
    detail: str
    error_code: str | None = None
    status_code: int = 400
