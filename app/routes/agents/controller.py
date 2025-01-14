from fastapi import APIRouter, HTTPException
from app.routes.agents.schemas import AgentResponseList, NewAgentRequest
from app.routes.agents.services import AgentsService

router = APIRouter()

route_prefix = "/agents"

service =  AgentsService()

@router.post(route_prefix , tags=["Agents"])
def create_agent(new_agent: NewAgentRequest):
    """
    Endpoint to create and run a container.
    """
    try:
        inserted =  service.create_agent(new_agent=new_agent)
        return {"id": str(inserted)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(route_prefix, tags=["Agents"], response_model=AgentResponseList)
def list_agents():
    try:
        agents = service.get_agents()
        return  AgentResponseList(data=agents, total=len(agents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
