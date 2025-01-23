

from bson import ObjectId
from fastapi import HTTPException
from app.clients.dbs.chromadb_client import ChromaClient
from app.clients.dbs.schemas import EmbeddableDocument
import json
from app.routes.agents.schemas import CreatedAgentResponse, NewAgentRequest
from app.clients.redis_client import redis_client

from app.clients.dbs.mongodb_client import get_tools_db


class AgentsService:
    collection =  None
    db = None
    
    def __init__(self, fn_collection_name="agents"):
        try:
            self.db = get_tools_db()
            self.collection = self.db[fn_collection_name]
        except:
            raise Exception("Error connection to Functions DB")

        
    def create_agent(self, new_agent: NewAgentRequest):
        try:
           
            tools_collection  = self.db["functions"]
           
            query = {
                "_id": {
                     "$in": [ObjectId(tool_id) for tool_id in new_agent.tools_ids]
                }
            }
            
            tools_bound = tools_collection.find(query)
            
            tools_bound_list = list(tools_bound)
            
            if len(tools_bound_list) != len(new_agent.tools_ids):
                raise HTTPException(status_code=400, detail=f"Some Tool were not found, initial length ({len(new_agent.tools_ids)}) does't match with found ({len(tools_bound_list)}) length")
            
            if ["autonomous", "planned", "hybrid"].index(new_agent.type) == -1:
                raise HTTPException(status_code=400, detail="Invalid agent type")
            
            inserted = self.collection.insert_one(new_agent.model_dump())
              
            inserted_id = inserted.inserted_id
            
            doc_store = ChromaClient()
            
            print("Inserting into vector db")
            
            doc_store.add_document(
                collection_name=f"agent-{str(inserted_id)}-snapshot",
                documents=[
                    EmbeddableDocument(
                    id=str(tool.get("_id")),
                    content=tool.get("parsed_params",{}).get("description", ""),
                    metadata={
                        "name": tool.get("parsed_params", {}).get("name", ""),
                        "parameters": json.dumps(tool.get("parsed_params", {}).get("args", [])),
                        }
                ) for tool in tools_bound_list
            ])
            
            return inserted_id
        
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
    
    def get_agents(self) -> list[dict]:
        try:
            agents_list = self.collection.find().skip(0).limit(20).sort({"_id": -1})
            
            
            
            return  [{
                    "id": str(agent["_id"]),
                    "mrn": agent.get("mrn", ""),
                    "name": agent.get("name", ""),
                    "type": agent.get("type", ""),
                    "organization_id": agent.get("organization_id", ""),
                    "trait_text": agent.get("trait_text", ""),
                    "tools_ids": agent.get("tools_ids", []),
                } for agent in agents_list]
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))