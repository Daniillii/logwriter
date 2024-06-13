from apps.scheduler import scheduler
from config.database import DatabaseManager
from apscheduler.triggers.cron import CronTrigger
from apps.logwriter.parser import parse_logs
from config.settings import ApacheConfig

every_day_trigger = CronTrigger(hour=0, minute=0)


@scheduler.scheduled_job(trigger=every_day_trigger)
def parse_logs_every_day():
    parse_logs(DatabaseManager.session, ApacheConfig.get_config())