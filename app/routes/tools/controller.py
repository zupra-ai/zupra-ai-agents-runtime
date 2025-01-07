from datetime import datetime
import uuid
from bson import ObjectId
from fastapi import APIRouter, HTTPException
from docker import from_env as docker_from_env
from fastapi.responses import JSONResponse
from app.clients.dbs.chromadb_client import ChromaClient
from app.clients.dbs.schemas import EmbeddableDocument
from app.clients.redis_client import redis_client
from app.docker_handler import create_docker_image_sources, build_image, remove_image
from app.routes.tools.schemas import NewToolRequest
from app.clients.docker_client import docker_client
from app.routes.tools.services import ToolsService
from app.tools_commons.base import parse_function_docstring, build_base_function
import hashlib
hasher = hashlib.sha256()

python_executor_image = "python:3.11-slim"

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
                                                   code=str(base_code.encode("utf-8")),
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
def update_tool(tool_id: str, request: NewToolRequest):
    try:

        parsed = parse_function_docstring(request.code)

        # try:
        #     db = get_database()
        # except:
        #     raise Exception("Error connection to Functions DB")

        # tools_collection = db["functions"]
        
        new_function = service.find_one({"parsed_params.name": request.name,})
        
        
        # tool_exists = tools_collection.find_one({
        #     "parsed_params.name": request.name,
        #     # "organization_id": request.organization_id
        # })

        # @TODO: avoid duplicate names
        # if len(tools_search) > 0 and tool_exists["id"] != tool_id:
        #     return JSONResponse(content={"error": f"A tool name with '{request.name}' already exist , try other name"}, status_code=500)

        if parsed is None:
            raise Exception("Invalid docstring")

        base_code = build_base_function(request.code)

        # new_function = tools_collection.find_one({
        #     "_id": ObjectId(deployment_id),
        #     # "organization_id": request.organization_id
        # })

        # if new_function is None:
        #     raise Exception(f"Function not found {deployment_id}")

        try:
            print("removing  image", new_function["image_name"])

            remove_image(
                image_name=new_function["image_name"],
            )

            redis_client.delete(
                f"tool-{str(tool_id)}")

            print("removed  image", new_function["image_name"])
        except Exception as e:
            print(f"🧧  Error deleting image: {e}")

        # Generate a unique identifier for the Dockerfile and image
        unique_id = str(uuid.uuid4())

        try:
            temp_dir = create_docker_image_sources(unique_id=unique_id,
                                                   base_image_name=python_executor_image,
                                                   code=str(base_code.encode("utf-8")),
                                                   requirements_txt=request.requirements,
                                                   environments_txt=request.environments
                                                   )
        except Exception as e:
            print("Error creating docker image", f"{e}")
            raise Exception("Failed to create docker resources")

        try:
            image_data = build_image(unique_id=unique_id, temp_dir=temp_dir)
        except Exception as e:
            # print("Error building image", f"{e}")
            return JSONResponse(content={"error": f"{e}"}, status_code=500)

        hasher.update(str(request.code + request.environments +
                          request.requirements).encode())

        new_hash = f"sha256:{hasher.hexdigest()}"

        new_function = service.update_one(ObjectId(str(tool_id)), {
            "$set": {
                "deployment_id": unique_id,
                # "description": parsed["description"],
                "image_name": image_data["image_name"],
                "hash": new_hash,
                # "_function_name": request.name,
                "_function": request.code,
                "requirements": request.requirements,
                "environments": request.environments,
                "parsed_params": {**parsed, "name": request.name},
            }
        })
        
        print("image data", image_data)

        redis_client.set(f"tool-{str(tool_id)}", image_data["image_name"])
        
        try:
            vector_db = ChromaClient()
            
            print("Updating into vector db")
            
            vector_db.update_documents(
                collection_name="tools-mapping",
                documents=[
                    EmbeddableDocument(
                    id=tool_id,
                    content=parsed.get("description", ""),
                    metadata={"name": request.name}
                )
            ])
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error saving tool to Vector DB: {str(e)}")

        return {
            "deployment_id": str(tool_id),
            "status": "re-deployed",
            "hash": new_hash
        }
    except Exception as e:
        print("🔴   ", e)
        return JSONResponse(content={"error": f"{e}"}, status_code=500)

@router.delete(route_prefix + "/{tool_id}", tags=["Tools"])
def update_tool(tool_id: str):
    try:
        pass
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
