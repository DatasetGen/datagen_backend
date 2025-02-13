from dataclasses import dataclass
from typing import Any

@dataclass
class DomainException(Exception):
    """Base class for domain-related exceptions with structured JSON output."""
    error_code: str
    message: str

    def to_json(self) -> dict[str, Any]:
        return {
            "error_code": self.error_code,
            "message": self.message
        }
