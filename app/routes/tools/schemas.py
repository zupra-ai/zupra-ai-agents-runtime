from pydantic import BaseModel, Field
from typing import Optional


class NewToolRequest(BaseModel):
    code: str = Field()
    name: str = Field()
    organization_id: Optional[str] = Field(default=None)
    tag_name: Optional[str] = Field(default=None)
    requirements: Optional[str] = Field()
    environments: Optional[str] = Field()
    runtime: str = Field()
