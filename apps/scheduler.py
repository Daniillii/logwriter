from sqlalchemy import URL

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

from config.settings import DATABASES

db_config = DATABASES.copy()
jobstores = {"default": SQLAlchemyJobStore(url=URL.create(**db_config))}
scheduler = AsyncIOScheduler(jobstores=jobstores, timezone="Europe/Moscow")
