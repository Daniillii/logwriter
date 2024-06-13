from fastapi import APIRouter
from sqlalchemy import cast, Date
from apps.logwriter.models import LogEntry
from config.database import DatabaseManager
from typing import List
from apps.logwriter import schemas

router = APIRouter()


@router.get("/logs/", response_model=List[schemas.LogEntryResponse])
def read_logs(skip: int = 0, limit: int = 10):
    return DatabaseManager.session.query(LogEntry).offset(skip).limit(limit).all()


@router.get("/logs/ip/{ip}", response_model=List[schemas.LogEntryResponse])
def read_logs_by_ip(ip: str):
    return DatabaseManager.session.query(LogEntry).filter(LogEntry.ip == ip).all()


@router.get("/logs/date/{date}", response_model=List[schemas.LogEntryResponse])
def read_logs_by_date(date: str):
    return (
        DatabaseManager.session.query(LogEntry)
        .filter(cast(LogEntry.date, Date) == date)
        .all()
    )


@router.get("/logs/date-range/", response_model=List[schemas.LogEntryResponse])
def read_logs_by_date_range(start_date: str, end_date: str):
    return (
        DatabaseManager.session.query(LogEntry)
        .filter(cast(LogEntry.date, Date).between(start_date, end_date))
        .all()
    )
