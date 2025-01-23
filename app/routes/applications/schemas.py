from pydantic import BaseModel, Field
from typing import Optional

from app.domain.schemas.base import BaseResponseList


class NewApplicationRequest(BaseModel): 
    name: str = Field(description="Application Name",  default="my application name")
    description: Optional[str] = Field(default="", description="Some optional description")
    accepted_origins: Optional[list[str]] = Field(default=["*"], description="Origins accepted, * for all")
    starter_messages: Optional[list[str]] = Field(default=[], description="Default messages")
    default_agent_id: str = Field( description="Default agent id")
    agents_ids: Optional[list[str]] = Field(default=[], description="List of agents ids")


class CreatedApplicationResponse(BaseModel): 
    id: str = Field(description="Model Resource Name",  default="AsdD3ds7Jh...")
    name: str = Field(description="Application Name",  default="my application name")
    description: Optional[str] = Field(default="", description="Some optional description")
    accepted_origins: Optional[list[str]] = Field(default=["*"], description="Origins accepted, * for all")
    starter_messages: Optional[list[str]] = Field(default=[], description="Default messages")
    default_agent_id: str = Field( description="Default agent id")
    agents_ids: Optional[list[str]] = Field(default=[], description="List of agents ids")
    
class ApplicationsResponseList(BaseResponseList[CreatedApplicationResponse]):
    pass 