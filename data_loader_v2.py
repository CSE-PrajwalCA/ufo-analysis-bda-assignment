"""
UFO Dashboard - Data Loader V2 (FIXED)
Imports UFO sightings from CSV into MongoDB
THIS VERSION VERIFIES MONGODB CONNECTION FIRST!
"""

import csv
import os
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

# ============================================================
# CONFIGURATION
# ============================================================
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "ufo_database"
COLLECTION_NAME = "sightings"
CSV_FILE = "cleaned_ufo.csv"


def check_mongodb():
    """Check if MongoDB is running"""
    print("\n" + "="*60)
    print("Checking MongoDB Connection...")
    print("="*60)
    
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command('ping')
        print("✓ MongoDB is running and accessible!")
        return client
    except ServerSelectionTimeoutError:
        print("✗ ERROR: MongoDB is NOT running!")
        print("Please start MongoDB first:")
        print("  $ mongod")
        print("\nThen run this script again.")
        return None
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return None


def load_data():
    """Load CSV data into MongoDB"""
    
    # Check MongoDB first
    client = check_mongodb()
    if not client:
        return False
    
    try:
        # Get database and collection
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        print("\n" + "="*60)
        print(f"Loading data from {CSV_FILE}")
        print("="*60)
        
        # Check if CSV exists
        if not os.path.exists(CSV_FILE):
            print(f"✗ ERROR: {CSV_FILE} not found!")
            return False
        
        # Clear existing data (optional)
        response = input("\nClear existing data before importing? (y/n): ").strip().lower()
        if response == 'y':
            result = collection.delete_many({})
            print(f"✓ Deleted {result.deleted_count} existing documents\n")
        
        # Load CSV
        documents = []
        row_count = 0
        
        with open(CSV_FILE, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                row_count += 1
                
                try:
                    # Convert types
                    duration_seconds = 0
                    try:
                        duration_seconds = int(float(str(row.get('duration (seconds)', '0')).strip() or '0'))
                    except:
                        duration_seconds = 0
                    
                    latitude = 0.0
                    try:
                        lat_val = str(row.get('latitude', '0')).strip()
                        latitude = float(lat_val) if lat_val and lat_val != '0' else 0.0
                    except:
                        latitude = 0.0
                    
                    longitude = 0.0
                    try:
                        lon_val = str(row.get('longitude', '0')).strip()
                        longitude = float(lon_val) if lon_val and lon_val != '0' else 0.0
                    except:
                        longitude = 0.0
                    
                    # Create document
                    document = {
                        'datetime': row.get('datetime', '').strip(),
                        'city': row.get('city', '').strip().lower(),
                        'state': row.get('state', '').strip().lower(),
                        'country': row.get('country', '').strip().lower(),
                        'shape': row.get('shape', '').strip().lower(),
                        'duration (seconds)': duration_seconds,
                        'duration (hours/min)': row.get('duration (hours/min)', '').strip(),
                        'comments': row.get('comments', '').strip(),
                        'date posted': row.get('date posted', '').strip(),
                        'latitude': latitude,
                        'longitude': longitude
                    }
                    
                    documents.append(document)
                    
                    # Insert in batches
                    if len(documents) >= 1000:
                        collection.insert_many(documents)
                        print(f"✓ Inserted {len(documents)} documents (Total so far: {row_count})")
                        documents = []
                
                except Exception as e:
                    print(f"Warning: Error processing row {row_count}: {e}")
                    continue
        
        # Insert remaining documents
        if documents:
            result = collection.insert_many(documents)
            print(f"✓ Inserted {len(result.inserted_ids)} documents (Total so far: {row_count})")
        
        # Verify
        total = collection.count_documents({})
        
        print("\n" + "="*60)
        print("✓ DATA LOADING COMPLETE!")
        print("="*60)
        print(f"CSV rows processed:    {row_count}")
        print(f"Documents in MongoDB:  {total}")
        print("="*60 + "\n")
        
        if total > 0:
            print("✓ MongoDB is now ready with data!")
            return True
        else:
            print("✗ No documents were inserted!")
            return False
    
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False
    finally:
        client.close()


def verify_data():
    """Verify the loaded data"""
    print("\n" + "="*60)
    print("Verifying Data...")
    print("="*60)
    
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        
        total = collection.count_documents({})
        print(f"\nTotal documents: {total}")
        
        if total > 0:
            # Sample document
            sample = collection.find_one()
            print("\nSample document:")
            for key, value in sample.items():
                if key != '_id':
                    print(f"  {key}: {value}")
            
            # Statistics
            print("\n" + "="*60)
            print("Field Statistics:")
            print("="*60)
            
            countries = len(collection.distinct('country'))
            shapes = len(collection.distinct('shape'))
            states = len(collection.distinct('state'))
            
            print(f"Unique countries: {countries}")
            print(f"Unique states:    {states}")
            print(f"Unique shapes:    {shapes}")
            
            print("\n" + "="*60 + "\n")
        
        client.close()
    except Exception as e:
        print(f"Error verifying data: {e}")


if __name__ == '__main__':
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  UFO Sightings Data Loader V2 (FIXED)  ".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    print("\n")
    
    # Load data
    success = load_data()
    
    if success:
        # Verify
        verify_data()
        print("✓ Ready to use! Run: python app.py")
    else:
        print("✗ Data loading failed!")
