build:
	docker-compose up --build

dev:
	docker-compose up

run-api:
	./venv/Scripts/python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug