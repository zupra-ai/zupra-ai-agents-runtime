

from bson import ObjectId
from fastapi import HTTPException
from app.routes.agents.schemas import NewAgentRequest

from app.clients.dbs.mongodb_client import get_tools_db


class ApplicationsService:
    collection =  None
    db = None
    
    def __init__(self, fn_collection_name="agents"):
        try:
            self.db = get_tools_db()
            self.collection = self.db[fn_collection_name]
        except:
            raise Exception("Error connection to Functions DB")

        
    def create_agent(self, new_tool: NewAgentRequest):
        try:
           
            tools_collection  = self.db["functions"]
           
            query = {
                "_id": {
                     "$in": [ObjectId(tool_id) for tool_id in new_tool.tools_ids]
                }
              }
            
            tools = tools_collection.find(query)
            
            if len(list(tools)) != len(new_tool.tools_ids):
                raise HTTPException(status_code=404, detail="Some Tool not found")
            
            if ["autonomous", "planned", "hybrid"].index(new_tool.agent_type) == -1:
                raise HTTPException(status_code=400, detail="Invalid agent type")
            
            inserted = self.collection.insert_one(new_tool.model_dump())
              
            return inserted.inserted_id
        
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    
    
    def get_agent(self, agent_id:str):
        try:
            agent = self.collection.find_one({"_id": ObjectId(agent_id)})
            
            if agent is None:
                raise HTTPException(status_code=404, detail="Tool not found")
            
            return {
                "id": str(agent["_id"]),
                "name": agent.get("parsed_params", {}).get("name", ""),
                "mrn": agent.get("mrn"),
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))    
    
    def get_agents(self):
        try:
            functions = self.collection.find({ 
            }).skip(0).limit(20).sort({"_id": -1})
            
            return {
                "data": [{
                    "id": str(func["_id"]),
                    "mrn": func.get("mrn"),
                    "name": func.get("name"),
                    "type": func.get("type"),
                    "application_id": func.get("application_id"),
                    "trait_text": func.get("trait_text"),
                    "tools_ids": func.get("tools_ids", []),
                } for func in functions]
            }
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))