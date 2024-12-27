up-build:
	docker-compose up --build

up:
	docker-compose up


dev-basics:
	docker-compose up memory_db_redis tool_runtime_docker


dev-api:
	./venv/Scripts/python.exe -m uvicorn app.main:app --reload --port 8080 --host 0.0.0.0