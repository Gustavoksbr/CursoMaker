from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente (.env)
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB = os.getenv("MONGO_DB", "meudb")

client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB]
