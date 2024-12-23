from fastapi import APIRouter, HTTPException
from docker import from_env as docker_from_env
from app.clients.redis_client import redis_client
from app.routes.tools.schemas import NewToolRequest
router = APIRouter()

# Connect to Docker
try:
    docker_client = docker_from_env()
    print(f"🟢  Connected to docker")
except Exception as e:
    print(f"🔴  Error connecting to Docker: {e}")

_prefix = "/tools"

@router.post(_prefix )
def create_tool(new_tool: NewToolRequest):
    """
    Endpoint to create and run a container.
    """
    try:
        return {}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(_prefix)
def list_containers():
    """
    List all running containers.
    """
    containers = docker_client.containers.list()
    container_info = [{"id": c.id, "name": c.name, "status": c.status} for c in containers]
    return {"containers": container_info}


@router.get(_prefix + "{name}")
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
