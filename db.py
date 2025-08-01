import os
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId

# Load environment variables from .env file
# NOTE: Even without a virtual environment, this works
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["llm_processor"]
collection = db["chunks"]

# Store chunk texts and embeddings in MongoDB
def store_chunks(chunks, embeddings):
    ids = []
    for i in range(len(chunks)):
        result = collection.insert_one({
            "text": chunks[i],
            "embedding": embeddings[i].tolist()
        })
        ids.append(str(result.inserted_id))
    return ids

# Retrieve chunks by list of MongoDB IDs
def get_chunks_by_ids(ids):
    obj_ids = [ObjectId(i) for i in ids]
    docs = collection.find({"_id": {"$in": obj_ids}})
    return [doc["text"] for doc in docs]
