import hnswlib
import numpy as np
from sentence_transformers import SentenceTransformer
import time
import os


class BaseEmbeddings():
    
    model : SentenceTransformer = None
    
    def __init__(self, model_name:str = 'sentence-transformers/all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(model_name, token=False)
        self.index = None
    
    def embed(self, sentences: list[str]): 
        embeddings = self.model.encode(sentences=sentences)
        return embeddings