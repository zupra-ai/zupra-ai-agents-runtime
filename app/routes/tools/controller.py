from datetime import datetime
import uuid
from fastapi import APIRouter, HTTPException
from docker import from_env as docker_from_env
from app.clients.dbs.chromadb_client import ChromaClient
from app.clients.dbs.schemas import EmbeddableDocument
from app.clients.redis_client import redis_client
from app.docker_handler import create_docker_image_sources, build_image
from app.routes.tools.schemas import NewToolRequest
from app.clients.docker_client import docker_client
from app.routes.tools.services import ToolsService
from app.tools_commons.base import parse_function_docstring, build_base_function

router = APIRouter()

route_prefix = "/tools"

service = ToolsService()


@router.post(route_prefix, tags=["Tools"])
def create_tool(new_tool: NewToolRequest):
    """
    Endpoint to create and run a container.
    """
    try:

        parsed_params = parse_function_docstring(new_tool.code)

        if parsed_params is None:
            raise HTTPException(
                status_code=400, detail="Error parsing function, please see http://docs.zupra.ai/api-ref/tool-main-action#function-parameters")

        base_code = build_base_function(new_tool.code)

        unique_id = str(uuid.uuid4())

        try:
            temp_dir = create_docker_image_sources(unique_id=unique_id,
                                                   base_image_name="python:3.11-slim",
                                                   code=str(
                                                       base_code.encode("utf-8")),
                                                   requirements_txt=new_tool.requirements,
                                                   environments_txt=new_tool.environments,
                                                   )
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error creating docker image sources: {str(e)}")

        try:
            image_data = build_image(unique_id=unique_id,
                                     temp_dir=temp_dir)
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error building docker image: {str(e)}")

        inserted = service.create_tool({
            "deployment_id": unique_id,
            "image_name": image_data["image_name"],
            "hash": "",
            "_function": new_tool.code,
            "requirements": new_tool.requirements,
            "environments": new_tool.environments,
            "parsed_params": {**parsed_params, "name": new_tool.name},
            "organization_id": new_tool.organization_id,
            "tag_name": new_tool.tag_name,
            "updated_at": datetime.now(),
            "created_at": datetime.now(),
            "runtime": "python:3.11-slim",
        })

        
        
        try:
            vector_db = ChromaClient()
            print("Inserting into vector db")
            vector_db.add_document(
                collection_name="tools-mapping",
                documents=[
                    EmbeddableDocument(
                    id=inserted,
                    content=parsed_params.get("description", ""),
                    metadata={"name": new_tool.name}
                )
            ])
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error saving tool to Vector DB: {str(e)}")
        
        try:
            redis_client.set(f"tool-{inserted}", image_data["image_name"])
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Error saving tool to Redis: {str(e)}")

        return {"deployment_id": str(inserted), "hash": "", "status": "created"},

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error creating tool: {str(e)}")


@router.get(route_prefix, tags=["Tools"])
def list_tools():
    try:
        return service.get_tools()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(route_prefix + "/{tool_id}", tags=["Tools"])
def get_tool(tool_id: str):
    try:
        return service.get_tool(tool_id=tool_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put(route_prefix + "/{tool_id}", tags=["Tools"])
def update_tool(tool_id: str):
    try:
        pass
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.delete(route_prefix + "/{tool_id}", tags=["Tools"])
def update_tool(tool_id: str):
    try:
        pass
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
