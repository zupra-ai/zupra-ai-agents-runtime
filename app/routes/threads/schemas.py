from pydantic import BaseModel, Field
from typing import Optional


class NewThreadRequest(BaseModel): 
    application_id: Optional[str] = Field() 
    agent_id: str = Field() 


class AgentInvokeRequest(BaseModel):
    instructions: str = Field(description="Instructions text")