from fastapi import APIRouter, HTTPException
from docker import from_env as docker_from_env
from app.clients.redis_client import redis_client
from app.routes.tools.schemas import NewToolRequest
from app.clients.docker_client import docker_client
from app.routes.tools.services import ToolsService

router = APIRouter()

route_prefix = "/tools"

@router.post(route_prefix , tags=["Tools"])
def create_tool(new_tool: NewToolRequest):
    """
    Endpoint to create and run a container.
    """
    try:
        return {}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(route_prefix, tags=["Tools"])
def list_tools():
    try:
        service =  ToolsService()
        return service.get_tools()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(route_prefix + "/{tool_id}", tags=["Tools"])
def get_tool(tool_id: str):
    try:
        service =  ToolsService()
        return service.get_tools()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

