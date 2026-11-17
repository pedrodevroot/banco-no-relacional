import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

if not MONGO_URI or not MONGO_DB:
    raise RuntimeError("Defina MONGO_URI e MONGO_DB no arquivo .env")

_client = None


def conectar_mongo():
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=10000)
        try:
            _client.admin.command("ping")
            print("Conectado ao MongoDB")
        except PyMongoError as e:
            _client = None
            raise ConnectionError(f"Não foi possível conectar ao MongoDB: {e}") from e
    return _client[MONGO_DB]


def fechar_conexao():
    global _client
    if _client is not None:
        _client.close()
        _client = None
