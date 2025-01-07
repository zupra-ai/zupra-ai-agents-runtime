

from bson import ObjectId
from fastapi import HTTPException

from app.clients.dbs.mongodb_client import get_tools_db


class ToolsService:
    collection = None
    db = None

    def __init__(self, fn_collection_name="functions"):
        try:
            self.db = get_tools_db()
            self.collection = self.db[fn_collection_name]
        except:
            raise Exception("Error connection to Functions DB")

    def create_tool(self, tool):
        try:
            inserted = self.collection.insert_one(tool)
            return inserted.inserted_id
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def update_one(self, tool_id: ObjectId, payload: dict):
        try:
            inserted = self.collection.update_one({"_id": tool_id}, payload)
            return inserted
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def find_all(self, params: dict):
        try:
            tools = self.collection.find(params)

            return [{
                "id": str(tool["_id"]),
                "name": tool.get("parsed_params", {}).get("name", ""),
                "body": tool.get("_function", ""),
                "image_name": tool["image_name"],
                "runtime": tool.get("runtime", ""),
                "environments": tool.get("environments", ""),
                "requirements": tool.get("requirements", ""),
                "hash": tool.get("hash"),
                "parsed_params": tool.get("parsed_params", {})
            } for tool in tools]

        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    def find_one(self, params: dict):
        try:
            tool = self.collection.find_one(params)
            return {
                "id": str(tool["_id"]),
                "name": tool.get("parsed_params", {}).get("name", ""),
                "image_name": tool["image_name"],
                "body": tool.get("_function", ""),
                "runtime": tool.get("runtime", ""),
                "environments": tool.get("environments", ""),
                "requirements": tool.get("requirements", ""),
                "hash": tool.get("hash"),
                "parsed_params": tool.get("parsed_params", {})
            } 

        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_tool(self, tool_id):
        try:
            tool = self.collection.find_one({"_id": ObjectId(tool_id)})
            if tool is None:
                raise HTTPException(status_code=404, detail="Tool not found")
            return {
                "id": str(tool["_id"]),
                "name": tool.get("parsed_params", {}).get("name", ""),
                "body": tool.get("_function", ""),
                "runtime": tool.get("runtime", ""),
                "environments": tool.get("environments", ""),
                "requirements": tool.get("requirements", ""),
                "hash": tool.get("hash"),
                "parsed_params": tool.get("parsed_params", {})
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    def get_tools(self):
        try:
            functions = self.collection.find({
            }).skip(0).limit(20).sort({"_id": -1})

            return {
                "data": [{
                    "id": str(func["_id"]),
                    "name": func.get("parsed_params", {}).get("name", ""),
                    "description": func.get("parsed_params", {}).get("description", ""),
                    "runtime": func["runtime"],
                    "hash": func.get("hash"),
                    "organization_id": func.get("organization_id"),
                    "tag_name": func.get("tag_name"),
                    "updated_at": func.get("updated_at"),
                } for func in functions]
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
