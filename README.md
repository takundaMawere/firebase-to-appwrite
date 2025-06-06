# Firebase to Appwrite Migration Script

This Python script migrates collections and documents from a Firebase Firestore database to an Appwrite database. It automatically creates collections and attributes in Appwrite based on your Firestore schema and migrates all documents, converting nested data to JSON strings as needed.

## Features

- Connects to Firebase Firestore using a service account.
- Connects to Appwrite using API credentials.
- Automatically creates Appwrite collections and attributes based on Firestore documents.
- Migrates all documents from each Firestore collection to Appwrite.
- Handles nested dictionaries and lists by storing them as JSON strings.

## Requirements

- Python 3.9+
- [Appwrite Python SDK](https://github.com/appwrite/sdk-for-python)
- [firebase-admin](https://github.com/firebase/firebase-admin-python)
- [python-dotenv](https://github.com/theskumar/python-dotenv)

## Setup

1. **Clone the repository and install dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

2. **Prepare your environment variables:**

    Create a `.env` file in the project root with the following content:

    ```
    FIREBASE_CREDENTIAL_PATH=student-residents-d7f36742d326.json
    APPWRITE_ENDPOINT=https://appwrite.example.com/v1
    APPWRITE_PROJECT_ID=your-appwrite-project-id
    APPWRITE_API_KEY=your-appwrite-api-key
    APPWRITE_DATABASE_ID=your-appwrite-database-id
    ```

    - Place your Firebase service account JSON file in the project root and update the path accordingly.

3. **Run the migration script:**

    ```sh
    python migr.py
    ```

## Notes

- The script will attempt to create collections and attributes in Appwrite. If they already exist, it will skip creation and continue.
- Nested objects and arrays in Firestore documents are stored as JSON strings in Appwrite.
- Make sure your Appwrite API key has permissions to create collections, attributes, and documents.

## License

See [LICENSE](LICENSE) for details.

---

**Disclaimer:** Use at your own risk. Always back up your data before running migration scripts.