from dataclasses import dataclass, field
from typing import Any


@dataclass
class ServiceResult:
    success: bool = True
    data: Any = None
    error: str | None = None
    status_code: int = 200

    @classmethod
    def ok(cls, data: Any = None, status_code: int = 200) -> "ServiceResult":
        return cls(success=True, data=data, status_code=status_code)

    @classmethod
    def error_response(
        cls, message: str, status_code: int = 400, data: dict[str, Any] | None = None
    ) -> "ServiceResult":
        return cls(
            success=False, error=message, status_code=status_code, data=data
        )
