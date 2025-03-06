from pymongo import MongoClient
from secretes.secrets import MONGO_DB_ATLAS_CONNECTION

def get_client():
    try:
        client = MongoClient(
            MONGO_DB_ATLAS_CONNECTION,
            tls=True,
            tlsAllowInvalidCertificates=True
        )
        return client
    except Exception as e:
        # Log the exception without exposing sensitive information
        print("An error occurred while connecting to MongoDB.")
        return None