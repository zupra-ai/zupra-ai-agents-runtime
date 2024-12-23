from pydantic import BaseModel, Field
from typing import Optional


class NewToolRequest(BaseModel):
    code: str = Field()
    name: str = Field()
    organization_id: Optional[str] = Field()
    tag_name: Optional[str] = Field()
    requirements: Optional[str] = Field()
    environments: Optional[str] = Field()
    runtime: str = Field()
