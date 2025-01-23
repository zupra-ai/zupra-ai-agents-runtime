

from bson import ObjectId
from fastapi import HTTPException
from app.routes.agents.schemas import NewAgentRequest

from app.clients.dbs.mongodb_client import get_tools_db
from app.routes.agents.services import AgentsService
from app.routes.applications.schemas import NewApplicationRequest


class ApplicationsService:
    
    collection =  None
    
    db = None
    
    def __init__(self, fn_collection_name="applications"):
        try:
            self.db = get_tools_db()
            self.collection = self.db[fn_collection_name]
        except:
            raise Exception("Error connection to Functions DB")

        
    def create_application(self, new_application: NewApplicationRequest):
        try:
            agent_service = AgentsService()
            
            agent_service.get_agent(agent_id=new_application.default_agent_id)
            
            inserted = self.collection.insert_one(new_application.model_dump())
              
            return inserted.inserted_id
        
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    
    def get_application(self, agent_id:str):
        try:
            agent = self.collection.find_one({"_id": ObjectId(agent_id)})
            
            if agent is None:
                raise HTTPException(status_code=404, detail="Application not found")
            
            return {
                "id": str(agent["_id"]),
                "name": agent.get("parsed_params", {}).get("name", ""),
                "mrn": agent.get("mrn"),
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))    
    
    def get_applications(self):
        try:
            functions = self.collection.find({ 
            }).skip(0).limit(20).sort({"_id": -1})
            
            return [{
                    "id": str(func["_id"]), 
                    "name": func.get("name"),
                    "description": func.get("description"),
                    "accepted_origins": func.get("accepted_origins",[]),
                    "starter_messages": func.get("starter_messages",[]),
                    "default_agent_id": func.get("default_agent_id"),
                    "agents_ids": func.get("agents_ids", []),
                } for func in functions]
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))