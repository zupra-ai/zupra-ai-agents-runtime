from pydantic import BaseModel, Field
from typing import Optional


class NewAgentRequest(BaseModel): 
    name: str = Field(description="Name of the agent")
    trait_text: str = Field(default="default", description="Behavioral trait of the agent, [default, aggressive, passive]")
    type: str = Field(default="autonomous", description="Type of agent, [autonomous, planned]")
    tools_ids: list[str] = Field(description="Tools ids to be executed by")
    organization_id: Optional[str] = Field(description="Organization id", default=None)