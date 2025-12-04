"""
UFO Dashboard - MongoDB Connection Utilities
Handles all database connection logic
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# MongoDB Configuration
MONGO_URI = "mongodb://localhost:27017"  # Change this if using MongoDB Atlas
DB_NAME = "ufo_database"
COLLECTION_NAME = "sightings"

# Global connection object
_client = None
_db = None


def connect_to_db():
    """
    Establishes connection to MongoDB
    Creates the database and collection if they don't exist
    
    Returns:
        Database object
        
    Raises:
        ConnectionFailure: If MongoDB is not running
    """
    global _client, _db
    
    try:
        _client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        
        # Test the connection
        _client.admin.command('ping')
        print(f"✓ Connected to MongoDB: {MONGO_URI}")
        
        # Get database reference
        _db = _client[DB_NAME]
        print(f"✓ Using database: {DB_NAME}")
        
        return _db
    
    except (ConnectionFailure, ServerSelectionTimeoutError) as e:
        print(f"✗ Failed to connect to MongoDB: {e}")
        print(f"Make sure MongoDB is running at {MONGO_URI}")
        raise


def get_db():
    """
    Returns the database object
    Creates connection if not already connected
    """
    global _db
    
    if _db is None:
        _db = connect_to_db()
    
    return _db


def get_collection():
    """
    Returns the 'sightings' collection from MongoDB
    Use this function to access the collection
    
    Returns:
        MongoDB collection object
    """
    db = get_db()
    collection = db[COLLECTION_NAME]
    return collection


def close_connection():
    """
    Closes the MongoDB connection
    Call this when shutting down the app
    """
    global _client, _db
    
    if _client:
        _client.close()
        print("✓ MongoDB connection closed")
        _client = None
        _db = None


def clear_collection():
    """
    Deletes all documents from the sightings collection
    USE WITH CAUTION - This cannot be undone!
    """
    collection = get_collection()
    result = collection.delete_many({})
    print(f"Deleted {result.deleted_count} documents from collection")


def create_indexes():
    """
    Creates database indexes for faster queries
    Improves performance for filtering operations
    """
    collection = get_collection()
    
    # Create indexes on commonly searched fields
    collection.create_index('country')
    collection.create_index('state')
    collection.create_index('shape')
    collection.create_index('datetime')
    collection.create_index('year')  # If we add this field
    
    print("✓ Database indexes created")
