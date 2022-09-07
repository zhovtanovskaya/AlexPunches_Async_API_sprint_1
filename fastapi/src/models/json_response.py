from typing import Any, Optional

from pydantic import BaseModel


class CacheResponseScheme(BaseModel):
    content: Any
    status_code: int = 200
    headers: dict[str, str] = {}
    media_type: Optional[str] = None
