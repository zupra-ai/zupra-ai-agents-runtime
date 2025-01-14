from fastapi import APIRouter, HTTPException, Query
from app.clients.redis_client import redis_client
from app.routes.threads.schemas import AgentInvokeRequest
from app.routes.agents.services import AgentsService
from app.routes.threads.schemas import NewThreadRequest
from app.clients.docker_client import docker_client
from app.routes.threads.services import ThreadsService

router = APIRouter()

route_prefix = "/threads"

service =  ThreadsService()
agent_service =  AgentsService()
@router.post(route_prefix , tags=["Threads"])
def create_thread(new_tool: NewThreadRequest):
    """
    Endpoint to create and run a container.
    """
    try:
        inserted =  service.create_thread({
            **new_tool.model_dump()
        })
        
        return {"id": str(inserted)}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(route_prefix, tags=["Threads"])
def list_thread():
    try:
        return service.get_threads()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(route_prefix + "/{thread_id}/history", tags=["Threads"])
def get_thread_history(thread_id: str, offset: int = Query(default=0), limit: int = Query(default=10)):
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

@router.post(route_prefix + "/{thread_id}/invoke-as/{agent_id}", tags=["Threads"])
def invoke_agent(agent_id: str, thread_id: str, request: AgentInvokeRequest):
    """
    Get container information by name.
    """
    
    agent = agent_service.get_agent(agent_id=agent_id)
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not Found")
    
    thread = service.get_thread(agent_id=agent_id)
    
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not Found")
    
    return {
        "id": "call",
    }