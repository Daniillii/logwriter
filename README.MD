Инструкция пользования проектом:

1. Клонируйте репозиторий:
    ```bash
    git clone https://github.com/Daniillii/logwriter.git
    cd logwriter
    ```

2. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

3. Настройте переменные окружения в файле `.env`, пользуясь .env.template:
    ```plaintext
    
    APP_NAME=App_name
    ALLOWED_HOSTS=localhost:3000 localhost:3001
    SECRET_KEY="key"
    ACCESS_TOKEN_EXPIRE_MINUTES=30

    OTP_SECRET_KEY = "1234"
    OTP_EXPIRE_SECONDS = 30

    DB_USERNAME=postgres
    DB_PASSWORD=kali
    DB_HOST=localhost
    DB_NAME=name
    DB_PORT=5432

    FILES_DIR=/apache/logs
    FILE_EXTENSION=.log
    LOG_FORMAT=%h %l %t "%r" %>s %b

    USE_LOCAL_FALLBACK=false
    ```

4. Примените миграции в базе данных!
```bash
  alembic upgrade head
```

4. Вы также можете локально протестировать, сгенериров фейковые логи:
```bash
python generate_logs.py
```

5. Запустите парсинг логов:
```bash
python logwriter.py parse
```

6. Запустите приложение:
    ```bash
    uvicorn apps.main:app --host 127.0.0.1 --port 8000
    ```

7. API будет доступен по адресу `http://127.0.0.1:8000`.

## Использование API

- Получение всех логов:
    ```bash
    GET /logs/
    ```

- Получение логов по IP:
    ```bash
    GET /logs/ip/{ip}
    ```

- Получение логов по дате:
    ```bash
    GET /logs/date/{date}
    ```

- Получение логов по диапазону дат:
    ```bash
    GET /logs/date-range/?start_date={start_date}&end_date={end_date}
    ```

## Использование CLI

- Парсинг логов:
    ```bash
    python logwriter.py parse
    ```

- Просмотр логов:
    ```bash
    python logwriter.py 10.06.2024
    python logwriter.py 10.06.2024 ip
    python logwriter.py 10.06.2024 ip status
    python logwriter.py 10.06.2024 12.06.2004
    python logwriter.py 10.06.2024 12.06.2004 ip
    ```