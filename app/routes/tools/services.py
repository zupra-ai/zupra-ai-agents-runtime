

from fastapi import HTTPException

from app.clients.dbs.mongodb_client import get_tools_db


class ToolsService:
    collection =  None
    
    def __init__(self, db):
        self.collection = db
        try:
            db = get_tools_db()
            self.collection = db["functions"]
        except:
            raise Exception("Error connection to Functions DB")

        
        
    def get_tools(self):
        try:
            functions = self.collection.find({
                "$or": [
                    # _filter
                ]
            }).skip(0).limit(20).sort({"_id": -1})
            
            return {
                "data": [{
                    "id": str(func["_id"]),
                    "name": func.get("parsed_params").get("name"),
                    "description": func.get("parsed_params").get("description"),
                    "runtime": func["runtime"],
                    "hash": func.get("hash"),
                    "organization_id": func.get("organization_id"),
                    "tag_name": func.get("tag_name"),
                    "updated_at": func.get("updated_at"),
                } for func in functions]
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))