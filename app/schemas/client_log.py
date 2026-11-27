from typing import Any, Literal, Optional
from pydantic import BaseModel


class ClientLogIn(BaseModel):
    level: Literal["info", "warn", "error"] = "info"
    message: str
    url: Optional[str] = None
    user_agent: Optional[str] = None
    stack: Optional[str] = None
    context: Optional[dict[str, Any]] = None
    timestamp: Optional[str] = None
