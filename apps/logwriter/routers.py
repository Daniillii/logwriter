from fastapi import APIRouter, Query
from sqlalchemy import cast, Date
from apps.logwriter.models import LogEntry
from config.database import DatabaseManager
from typing import List
from apps.logwriter import schemas
from datetime import datetime

router = APIRouter(tags=['Логи'])


@router.get("/logs/", response_model=List[schemas.LogEntryResponse], summary="Прочитать логи")
def read_logs(skip: int = 0, limit: int = 10):
    return DatabaseManager.session.query(LogEntry).offset(skip).limit(limit).all()


@router.get("/logs/ip/{ip}", response_model=List[schemas.LogEntryResponse], summary="Получить логи по IP")
def read_logs_by_ip(ip: str):
    return DatabaseManager.session.query(LogEntry).filter(LogEntry.ip == ip).all()


@router.get("/logs/date/", response_model=List[schemas.LogEntryResponse], summary="Получить логи по дате")
def read_logs_by_date(date: str = Query(..., description="Формат даты dd.mm.yyyy")):
    try:
        date_obj = datetime.strptime(date, "%d.%m.%Y")
    except ValueError:
        return {"error": "Incorrect date format, should be dd.mm.yyyy"}
    return (
        DatabaseManager.session.query(LogEntry)
        .filter(cast(LogEntry.date, Date) == date_obj)
        .all()
    )


@router.get("/logs/date-range/", response_model=List[schemas.LogEntryResponse], summary="Получить логи по временному промежутку")
def read_logs_by_date_range(start_date: str = Query(..., description="Формат даты dd.mm.yyyy"),
    end_date: str = Query(..., description="Формат даты dd.mm.yyyy")):
    try:
        start_date_obj = datetime.strptime(start_date, "%d.%m.%Y")
    except ValueError:
        return {"error": "Incorrect date format, should be dd.mm.yyyy"}
    try:
        end_date_obj = datetime.strptime(end_date, "%d.%m.%Y")
    except ValueError:
        return {"error": "Incorrect date format, should be dd.mm.yyyy"}
    return (
        DatabaseManager.session.query(LogEntry)
        .filter(cast(LogEntry.date, Date).between(start_date_obj, end_date_obj))
        .all()
    )
