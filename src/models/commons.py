from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class ApiResponse(BaseModel):
    code: int
    response: Optional[dict] = None
    error: Optional[str] = None

class UserEntry(BaseModel):
    user_id: str
    time: datetime
    team: str
    project: str