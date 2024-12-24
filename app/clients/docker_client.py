from docker import from_env as docker_from_env

docker_client =  None

# Connect to Docker
try:
    docker_client = docker_from_env()
    print(f"🟢  Connected to docker")
except Exception as e:
    print(f"🔴  Error connecting to Docker: {e}")
