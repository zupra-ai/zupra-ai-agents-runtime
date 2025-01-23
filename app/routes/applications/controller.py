from fastapi import APIRouter, HTTPException
from app.clients.redis_client import redis_client
from app.domain.schemas.base import BaseResponseList
from app.routes.applications.schemas import ApplicationsResponseList, NewApplicationRequest, CreatedApplicationResponse
from app.routes.applications.services import ApplicationsService

router = APIRouter()

route_prefix = "/applications"

service =  ApplicationsService() 

@router.post(route_prefix , tags=["Applications"])
def create_application(new_application: NewApplicationRequest):
    """
    Endpoint to create and run a container.
    """
    try:
        inserted =  service.create_application(new_application=new_application)
        return {"id": str(inserted)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(route_prefix, tags=["Applications"], response_model=ApplicationsResponseList)
def list_applications():
    try:
        agents = service.get_applications()
        return  ApplicationsResponseList(data=agents, total=len(agents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
