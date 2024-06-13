import os
from datetime import datetime
from sqlalchemy.orm import Session
from apps.logwriter.models import LogEntry

def parse_log_line(line, log_format):
    parts = line.split()
    ip = parts[0]
    date = datetime.strptime(parts[3][1:], "%d/%b/%Y:%H:%M:%S")
    request = " ".join(parts[5:8])
    status = int(parts[8])
    size = int(parts[9])
    return LogEntry(ip=ip, date=date, request=request, status=status, size=size)

def parse_logs(db: Session, settings):
    for filename in os.listdir(settings.files_dir):
        if filename.endswith(settings.file_extension):
            with open(os.path.join(settings.files_dir, filename), 'r') as file:
                for line in file:
                    log_entry = parse_log_line(line, settings.log_format)
                    db.add(log_entry)
    db.commit()
