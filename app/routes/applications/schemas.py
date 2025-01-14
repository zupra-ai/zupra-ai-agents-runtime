from pydantic import BaseModel, Field
from typing import Optional


class NewApplicationRequest(BaseModel): 
    name: str = Field(description="Model Resource Name",  default="openai:gpt-3.5-turbo")
    description: str = Field(description="Agent name")
    accepted_origins: list[str] = Field(default=[], description="Origins accepted, * for all")
    starter_messages: list[str] = Field(default=[], description="Default messages")
    default_agent_id: str = Field( description="Default agent id")
    agents_ids: list[str] = Field(default=[], description="List of agents ids")


class CreatedApplicationResponse(BaseModel): 
    id: str = Field(description="Model Resource Name",  default="openai:gpt-3.5-turbo")
    name: str = Field(description="Model Resource Name",  default="openai:gpt-3.5-turbo")
    description: str = Field(description="Agent name")
    accepted_origins: list[str] = Field(default=[], description="Origins accepted, * for all")
    starter_messages: list[str] = Field(default=[], description="Default messages")
    default_agent_id: str = Field( description="Default agent id")
    agents_ids: list[str] = Field(default=[], description="List of agents ids")