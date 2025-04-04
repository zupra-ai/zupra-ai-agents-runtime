up-build:
	docker-compose up --build

up:
	docker-compose up

###########
# DEV CMDS
###########
# UP dev services
ups:
	docker-compose up memory_db_redis tool_runtime_docker vector_db_chroma

dev:
	./venv/Scripts/python.exe launch.py