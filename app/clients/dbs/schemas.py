from typing import Optional


class EmbeddableDocument():
    id: str | int
    content: str
    metadata: Optional[dict]
    
    def __init__(self, id: str | int, content: str, metadata: Optional[dict] = None):
        self.id = id
        self.content = content  
        self.metadata = metadata
        