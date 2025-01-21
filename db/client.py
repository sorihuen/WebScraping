
### MongoDB client ###

from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Obtener la URL de MongoDB desde las variables de entorno
mongodb_url = os.getenv("MONGODB_URL")
db_name = os.getenv("DB_NAME") 


# Conectar a la base de datos remota MongoDB Atlas
db_client = MongoClient(mongodb_url)[db_name] 


# nOdGZlqrziPS5ZPc clave / username: sanyelibermudez