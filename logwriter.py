import click
from sqlalchemy.orm import Session
from apps.logwriter.parser import parse_logs
from config.settings import ApacheConfig
from sqlalchemy import cast, Date
from config.database import DatabaseManager
from apps.logwriter.models import LogEntry
from datetime import datetime

DatabaseManager().load()

class LogWriterCLI:
    def __init__(self):
        self.settings = ApacheConfig.get_config()

    def parse(self):
        db: Session = DatabaseManager.session
        parse_logs(db, self.settings)
        db.close()

    def view_logs(self, start_date=None, end_date=None, ip=None, status=None):
        db: Session = DatabaseManager.session
        query = db.query(LogEntry)
        if start_date and end_date:
            query = query.filter(cast(LogEntry.date, Date).between(start_date, end_date))
        elif start_date:
             query = query.filter(cast(LogEntry.date, Date) == start_date)
        if ip:
            query = query.filter(LogEntry.ip == ip)
        if status:
            query = query.filter(LogEntry.status == status)
        logs = query.all()
        db.close()
        return logs
    
def is_date(value, date_format="%d.%m.%Y"):
    try:
        datetime.strptime(value, date_format)
        return True
    except ValueError:
        return False

@click.group()
def cli():
    pass

@cli.command()
def parse():
    """Parse logs and store them in the database."""
    cli = LogWriterCLI()
    cli.parse()

@click.command()
@click.argument('args', nargs=-1)
def cli(args):
    cli = LogWriterCLI()
    
    if len(args) == 0:
        click.echo("No arguments provided. Use 'parse', or provide dates and filters.")
        return
    
    if args[0] == 'parse':
        cli.parse()
    else:
        start_date = None
        end_date = None
        ip = None
        status = None


        if len(args) >= 1 and is_date(args[0]):
            start_date = datetime.strptime(args[0], "%d.%m.%Y")
        else:
            click.echo("Первый аргумент всегда дата в формате DD.MM.YYYY")
            return
        
        if len(args) >= 2:
            if is_date(args[1]):
                end_date = datetime.strptime(args[1], "%d.%m.%Y")
            else:
                ip = args[1]
        
        if len(args) == 3:
            if end_date:
                ip = args[2]
            else:
                status = args[2]
        
        if len(args) == 4:
            if is_date(args[1]):
                end_date = datetime.strptime(args[1], "%d.%m.%Y")
                ip = args[2]
                status = args[3]
            else:
                click.echo("Второй аргумент должен быть датой в формате DD.MM.YYYY")
                return


        logs = cli.view_logs(start_date, end_date, ip, status)
        for log in logs:
            print(f"IP: {log.ip}, Date: {log.date}, Request: {log.request}, Status: {log.status}, Size: {log.size}")


if __name__ == "__main__":
    cli()