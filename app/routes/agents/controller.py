from fastapi import APIRouter, HTTPException
from app.clients.redis_client import redis_client
from app.routes.agents.schemas import NewAgentRequest
from app.clients.docker_client import docker_client
from app.routes.agents.services import AgentsService

router = APIRouter()

route_prefix = "/agents"

service =  AgentsService()

@router.post(route_prefix , tags=["Agents"])
def create_thread(new_tool: NewAgentRequest):
    """
    Endpoint to create and run a container.
    """
    try:
        inserted =  service.create_agent(new_tool=new_tool)
        return {"id": str(inserted)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(route_prefix, tags=["Agents"])
def list_agents():
    try:
        return service.get_agents()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(route_prefix + "/{agent_id}/invoke-with/{thread_id}", tags=["Agents"])
def invoke_agent(agent_id: str, thread_id: str):
    """
    Get container information by name.
    """
    container_id = redis_client.get(thread_id)
    if not container_id:
        raise HTTPException(status_code=404, detail="Container not found in Redis")
    
    container = docker_client.containers.get(container_id)
    return {
        "id": container.id,
        "name": container.name,
        "status": container.status,
        "image": container.image.tags,
    }
