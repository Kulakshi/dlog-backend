from typing import Optional

from pydantic import BaseModel


class ApiResponse(BaseModel):
    code: int
    response: Optional[dict] = None
    error: Optional[str] = None
