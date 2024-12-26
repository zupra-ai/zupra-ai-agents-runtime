from fastapi import APIRouter, HTTPException
from docker import from_env as docker_from_env
from app.clients.redis_client import redis_client
from app.routes.tools.schemas import NewToolRequest
from app.clients.docker_client import docker_client

router = APIRouter()

route_prefix = "/threads"

@router.post(route_prefix , tags=["Threads"])
def create_thread(new_tool: NewToolRequest):
    """
    Endpoint to create and run a container.
    """
    try:
        return {}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(route_prefix, tags=["Threads"])
def list_thread():
    """
    List all running containers.
    """
    containers = docker_client.containers.list()
    container_info = [{"id": c.id, "name": c.name, "status": c.status} for c in containers]
    return {"containers": container_info}


@router.get(route_prefix + "/{tool_id}", tags=["Threads"])
def get_thread(tool_id: str):
    """
    Get container information by name.
    """
    container_id = redis_client.get(tool_id)
    if not container_id:
        raise HTTPException(status_code=404, detail="Container not found in Redis")
    
    container = docker_client.containers.get(container_id)
    return {
        "id": container.id,
        "name": container.name,
        "status": container.status,
        "image": container.image.tags,
    }
