import firebase_admin
from firebase_admin import credentials, firestore
from appwrite.client import Client
from appwrite.services.databases import Databases
import uuid
import time
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration

FIREBASE_CREDENTIAL_PATH = os.getenv('FIREBASE_CREDENTIAL_PATH')
APPWRITE_ENDPOINT = os.getenv('APPWRITE_ENDPOINT')
APPWRITE_PROJECT_ID = os.getenv('APPWRITE_PROJECT_ID')
APPWRITE_API_KEY = os.getenv('APPWRITE_API_KEY')
APPWRITE_DATABASE_ID = os.getenv('APPWRITE_DATABASE_ID')

def initialize_firebase():
    cred = credentials.Certificate(FIREBASE_CREDENTIAL_PATH)
    firebase_admin.initialize_app(cred)
    return firestore.client()

def initialize_appwrite():
    client = Client()
    client.set_endpoint(APPWRITE_ENDPOINT)
    client.set_project(APPWRITE_PROJECT_ID)
    client.set_key(APPWRITE_API_KEY)
    return Databases(client)

def infer_appwrite_type(value):
    if isinstance(value, bool):
        return 'boolean'
    elif isinstance(value, int):
        return 'integer'
    elif isinstance(value, float):
        return 'float'
    elif isinstance(value, str):
        return 'string'
    elif isinstance(value, (dict, list)):
        return 'string'  # Store JSON as string
    else:
        return 'string'

def create_appwrite_collection_with_schema(db: Databases, col_name: str, sample_doc: dict):
    try:
        db.create_collection(
            database_id=APPWRITE_DATABASE_ID,
            collection_id=col_name,
            name=col_name,
            permissions=[]
        )
        print(f"✅ Created Appwrite collection: {col_name}")
    except Exception as e:
        print(f"⚠️ Collection '{col_name}' may already exist or failed to create: {e}")

    time.sleep(1)

    # Create attributes based on sample document
    for key, value in sample_doc.items():
        attr_type = infer_appwrite_type(value)
        try:
            if attr_type == 'string':
                db.create_string_attribute(
                    database_id=APPWRITE_DATABASE_ID,
                    collection_id=col_name,
                    key=key,
                    size=1000,
                    required=False
                )
            elif attr_type == 'integer':
                db.create_integer_attribute(
                    database_id=APPWRITE_DATABASE_ID,
                    collection_id=col_name,
                    key=key,
                    required=False
                )
            elif attr_type == 'float':
                db.create_float_attribute(
                    database_id=APPWRITE_DATABASE_ID,
                    collection_id=col_name,
                    key=key,
                    required=False
                )
            elif attr_type == 'boolean':
                db.create_boolean_attribute(
                    database_id=APPWRITE_DATABASE_ID,
                    collection_id=col_name,
                    key=key,
                    required=False
                )
            print(f"   ➕ Created attribute: {key} ({attr_type})")
        except Exception as e:
            print(f"⚠️ Failed to create attribute {key}: {e}")

    time.sleep(2)  # Ensure schema is committed before inserting documents

def migrate_collection(firebase_db, appwrite_db, col_name):
    docs = list(firebase_db.collection(col_name).stream())
    if not docs:
        print(f"📭 Collection '{col_name}' is empty, skipping.")
        return

    # Use the first document to infer schema
    sample_doc = docs[0].to_dict()
    create_appwrite_collection_with_schema(appwrite_db, col_name, sample_doc)

    migrated_count = 0
    for doc in docs:
        data = doc.to_dict()

        # Convert nested dicts/lists to JSON strings
        for k, v in data.items():
            if isinstance(v, (dict, list)):
                data[k] = json.dumps(v)

        try:
            appwrite_db.create_document(
                database_id=APPWRITE_DATABASE_ID,
                collection_id=col_name,
                document_id=str(uuid.uuid4()),
                data=data
            )
            migrated_count += 1
        except Exception as e:
            print(f"❌ Failed to migrate document {doc.id}: {e}")

    print(f"📦 Migrated {migrated_count} documents from '{col_name}'.")

def main():
    firebase_db = initialize_firebase()
    appwrite_db = initialize_appwrite()

    collections = firebase_db.collections()
    for collection in collections:
        col_name = collection.id
        print(f"\n🔄 Migrating collection: {col_name}")
        migrate_collection(firebase_db, appwrite_db, col_name)

if __name__ == '__main__':
    main()