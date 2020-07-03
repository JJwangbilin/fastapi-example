from pydantic import BaseModel
from datetime import datetime


class TokenPayload(BaseModel):
    id: str
    exp: datetime
