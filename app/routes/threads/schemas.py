from pydantic import BaseModel, Field
from typing import Optional


class NewThreadRequest(BaseModel): 
    organization_id: Optional[str] = Field() 
    application_id: Optional[str] = Field() 
    agent_id: str = Field() 
