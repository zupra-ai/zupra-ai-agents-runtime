from pymongo import MongoClient
from app.settings import settings 

def get_database(db_name="zupra-functions"):
    client = MongoClient(settings.tools_database_url)
    return client[db_name]