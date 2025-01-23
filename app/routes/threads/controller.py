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
        inserted =  service.create_thread(tool=new_tool)
        
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
    raise HTTPException(status_code=500, detail="Not Implemented")

@router.post(route_prefix + "/{thread_id}/invoke-as/{agent_id}", tags=["Threads"], summary="Invoke Agent within a context")
def invoke_agent(agent_id: str, thread_id: str, request: AgentInvokeRequest):
    """
    Get container information by name.
    """
    
    agent = agent_service.get_agent(agent_id=agent_id)
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not Found")
    
    thread = service.get_thread(thread_id=thread_id)
    
    if not thread:
        raise HTTPException(status_code=404, detail="Thread not Found")
    
    raise HTTPException(status_code=500, detail="Not Implemented")