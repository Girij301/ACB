from pydantic import BaseModel
from typing import Any, Optional


class APIResponse(BaseModel):
    success: bool = True
    message: str = "Success"
    data: Any = None
    error: Optional[str] = None