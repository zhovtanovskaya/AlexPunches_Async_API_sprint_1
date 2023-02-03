from motor.motor_asyncio import AsyncIOMotorClient

mongo_url = "mongodb+srv://yana:vAhgeeoxP8crYvpE@cluster0.ynuujij.mongodb.net/test_ugc?retryWrites=true&w=majority"
client = AsyncIOMotorClient(mongo_url)
mongo = client.test_ugc