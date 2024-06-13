import random
from datetime import datetime, timedelta

def generate_random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

def generate_random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds()))
    )

def generate_log_line():
    ip = generate_random_ip()
    date = generate_random_date(datetime(2024, 1, 1), datetime(2024, 12, 31))
    request = random.choice(["GET /index.html HTTP/1.1", "POST /form HTTP/1.1", "GET /style.css HTTP/1.1"])
    status = random.choice([200, 404, 500])
    size = random.randint(200, 2000)
    
    log_line = f'{ip} - - [{date.strftime("%d/%b/%Y:%H:%M:%S %z")}] "{request}" {status} {size}'
    
    return log_line

def generate_logs(filename, num_lines):
    with open(filename, 'w') as file:
        for _ in range(num_lines):
            log_line = generate_log_line()
            file.write(log_line + '\n')

if __name__ == "__main__":
    generate_logs("apache/logs/access.log", 1000)
