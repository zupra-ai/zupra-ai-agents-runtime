from fastapi import FastAPI, HTTPException
from docker import from_env as docker_from_env
from app.clients.redis_client import redis_client
from app.routes.tools.controller import router as tools_router



app = FastAPI()

# Connect to Docker
try:
    docker_client = docker_from_env()
    print(f"🟢  Connected to docker")
except Exception as e:
    print(f"🔴  Error connecting to Docker: {e}")

@app.post("/run-container/")
def run_container(image: str, name: str):
    """
    Endpoint to create and run a container.
    """
    try:
        # Pull the image
        docker_client.images.pull(image)

        # Create and start the container
        container = docker_client.containers.run(
            image,
            name=name,
            detach=True
        )

        # Save container info in Redis
        redis_client.set(name, container.id)

        return {"message": f"Container {name} is running", "container_id": container.id}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/containers/")
def list_containers():
    """
    List all running containers.
    """
    containers = docker_client.containers.list()
    container_info = [{"id": c.id, "name": c.name, "status": c.status} for c in containers]
    return {"containers": container_info}


@app.get("/container-info/{name}")
def get_container_info(name: str):
    """
    Get container information by name.
    """
    container_id = redis_client.get(name)
    if not container_id:
        raise HTTPException(status_code=404, detail="Container not found in Redis")
    
    container = docker_client.containers.get(container_id)
    return {
        "id": container.id,
        "name": container.name,
        "status": container.status,
        "image": container.image.tags,
    }
    


app.include_router(router=tools_router, prefix="/v1")


