import mongomock
from app.config import settings

client = mongomock.MongoClient()
db = client[settings.DATABASE_NAME]

# Collections
users_collection = db["users"]
farms_collection = db["farms"]
fields_collection = db["fields"]
predictions_collection = db["predictions"]
