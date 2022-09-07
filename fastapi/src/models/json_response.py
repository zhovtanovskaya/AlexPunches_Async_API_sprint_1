from typing import Any, Optional

from pydantic import BaseModel


class CacheResponseScheme(BaseModel):
    content: Any
    status_code: int = 200
    headers: Optional[dict] = None
    media_type: Optional[str] = None
