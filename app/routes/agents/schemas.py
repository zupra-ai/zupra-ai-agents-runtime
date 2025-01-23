from pydantic import BaseModel, Field
from typing import Optional

from app.domain.schemas.base import BaseResponseList


class NewAgentRequest(BaseModel): 
    mrn: str = Field(description="Model Resource Name",  default="openai:gpt-3.5-turbo")
    name: str = Field(description="Agent name")
    trait_text: str = Field(default="default", description="Behavioral trait of the agent, [default, aggressive, passive]")
    type: str = Field(default="autonomous", description="Type of agent, [autonomous, planned]")
    tools_ids: list[str] = Field(description="Tools ids to be executed by", min_length=1)

class CreatedAgentResponse(BaseModel): 
    id: str = Field(description="Agent Id",  default="AsdD3ds7Jh...")
    mrn: str = Field(description="Model Resource Name",  default="openai:gpt-3.5-turbo")
    name: str = Field(description="Agent name", default="Agent 1")
    trait_text: str = Field(default="default", description="Behavioral trait of the agent, [default, aggressive, passive]")
    type: str = Field(default="autonomous", description="Type of agent, [autonomous, planned]")
    tools_ids: list[str] = Field(description="Tools ids to be executed by", default=[])


    
class AgentResponseList(BaseResponseList[CreatedAgentResponse]):
    pass 