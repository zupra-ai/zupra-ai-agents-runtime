from pymongo import MongoClient
from app.settings import settings 

def get_tools_db(db_name="zupra-functions") -> MongoClient:
    client = MongoClient(settings.tools_database_url)
    return client[db_name]