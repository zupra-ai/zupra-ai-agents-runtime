import chromadb

from chromadb.config import Settings, APIVersion
# Example setup of the client to connect to your chroma server
client = chromadb.HttpClient(host='127.0.0.1', port=8000)
client.heartbeat()

# # Or for async usage:
# async def main():
#     client = await chromadb.AsyncHttpClient(host='localhost', port=8000)