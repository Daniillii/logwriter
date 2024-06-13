from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    func
)
from config.database import FastModel


class LogEntry(FastModel):
    __tablename__ = 'log_entries'
    id = Column(Integer, primary_key=True)
    ip = Column(String, index=True)
    date = Column(DateTime, index=True, server_default=func.now())
    request = Column(String)
    status = Column(Integer)
    size = Column(Integer)