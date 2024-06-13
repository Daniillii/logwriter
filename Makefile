rebuild:
	docker compose up --force-recreate --build -d 
	docker exec -it logwriter_back alembic upgrade head

build:
	docker compose up -d
	docker exec -it logwriter_back alembic upgrade head

upgrade:
	docker exec -it logwriter_back alembic upgrade head
