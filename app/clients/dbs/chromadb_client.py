import chromadb
from chromadb import Collection
from app.clients.dbs.schemas import EmbeddableDocument
from app.embeddings.base import BaseEmbeddings

class ChromaClient:

    client: chromadb.HttpClient = None

    def __init__(self, host: str = "127.0.0.1", port: int = 8529):
        self.client = chromadb.HttpClient(host=host, port=port, ssl=False)
        # self.client.heartbeat()

    def add_document(self, collection_name: str, documents: list[EmbeddableDocument]):

        collection :Collection = self.client.get_or_create_collection(
            name=collection_name, metadata={"hnsw:space": "cosine"})

        embeddings = BaseEmbeddings()
        
        embeddings = embeddings.embed([doc.content for doc in documents])
        ids = []
        metadatas = []

        for doc in documents:
            ids.append(str(doc.id))
            metadatas.append(doc.metadata)

        return collection.add(embeddings=embeddings, ids=ids, metadatas=metadatas)
