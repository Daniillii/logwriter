from pydantic import BaseModel

from datetime import datetime


class LogEntryResponse(BaseModel):
    ip: str
    date: datetime
    request: str
    status: int
    size: int

    class Config:
        orm_mode = True