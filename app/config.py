import os
from dotenv import load_dotenv
from storage.json_storage import JSONStorage
from storage.postgres_storage import PostgreSQLStorage
from storage.mongo_storage import MongoDBStorage

load_dotenv()

def get_storage_choice():
    print("Choose your storage:")
    print("1. JSON Files (Local)")
    print("2. PostgreSQL DB")
    #print("3. MongoDB")
    ch = input("Enter choice (1-2): ")
    if ch == "1":
        return JSONStorage()
    elif ch == "2":
        config = {
            "host": os.getenv("POSTGRES_HOST"),
            "port": int(os.getenv("POSTGRES_PORT", 5432)),
            "database": os.getenv("POSTGRES_DB"),
            "user": os.getenv("POSTGRES_USER"),
            "password": os.getenv("POSTGRES_PASSWORD"),
        }
        return PostgreSQLStorage(config)
    # elif ch == "3":
    #     config = {
    #         "uri": os.getenv("MONGO_URI"),
    #         "database": os.getenv("MONGO_DB"),
    #     }
    #     return MongoDBStorage(config)
    else:
        print("Invalid, defaulting to JSON")
        return JSONStorage()
