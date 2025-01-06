

from bson import ObjectId
from fastapi import HTTPException

from app.clients.dbs.mongodb_client import get_tools_db


class ThreadsService:
    collection =  None
    db =  None
    
    def __init__(self, fn_collection_name="threads"):
        try:
            self.db = get_tools_db()
            self.collection = self.db[fn_collection_name]
        except:
            raise Exception("Error connection to Functions DB")

        
    def create_thread(self, tool):
        try:
           inserted = self.collection.insert_one(tool)
           return inserted.inserted_id
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    
    def get_thread(self, tool_id):
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
    
    def get_threads(self):
        try:
            functions = self.collection.find({ 
            }).skip(0).limit(20).sort({"_id": -1})
            
            return {
                "data": [{
                    "id": str(func["_id"]),
                    "agent_id": func.get("agent_id"),
                    "application_id": func.get("application_id"),
                } for func in functions]
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))