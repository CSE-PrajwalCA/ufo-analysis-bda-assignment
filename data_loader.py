"""
UFO Dashboard - Data Loader
Imports UFO sightings from CSV into MongoDB
Run this ONCE to load the data
"""

import csv
import os
from utils import get_collection, clear_collection


def load_data_from_csv(csv_file='cleaned_ufo.csv'):
    """
    Loads UFO sightings from CSV file into MongoDB
    
    Steps:
    1. Read cleaned_ufo.csv
    2. Parse each row
    3. Insert into MongoDB
    4. Print summary
    
    Args:
        csv_file: Path to CSV file
    """
    
    # Check if file exists
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found!")
        return False
    
    try:
        collection = get_collection()
        
        print(f"\n{'='*60}")
        print(f"UFO Data Loader - Importing from {csv_file}")
        print(f"{'='*60}\n")
        
        # Ask user if they want to clear existing data
        response = input("Clear existing data before importing? (y/n): ").strip().lower()
        if response == 'y':
            clear_collection()
        
        documents = []
        row_count = 0
        
        # Read CSV file
        with open(csv_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                row_count += 1
                
                # Create document from row
                # Keep all fields exactly as they appear in CSV
                document = {
                    'datetime': row.get('datetime', '').strip(),
                    'city': row.get('city', '').strip().lower(),
                    'state': row.get('state', '').strip().lower(),
                    'country': row.get('country', '').strip().lower(),
                    'shape': row.get('shape', '').strip().lower(),
                    'duration (seconds)': convert_duration_to_seconds(
                        row.get('duration (seconds)', '0')
                    ),
                    'duration (hours/min)': row.get('duration (hours/min)', '').strip(),
                    'comments': row.get('comments', '').strip(),
                    'date posted': row.get('date posted', '').strip(),
                    'latitude': convert_to_float(row.get('latitude', '0')),
                    'longitude': convert_to_float(row.get('longitude', '0'))
                }
                
                documents.append(document)
                
                # Insert in batches of 1000 for better performance
                if len(documents) >= 1000:
                    result = collection.insert_many(documents)
                    print(f"✓ Inserted {len(result.inserted_ids)} documents")
                    documents = []
                
                # Progress indicator
                if row_count % 5000 == 0:
                    print(f"  Processed {row_count} rows...")
        
        # Insert remaining documents
        if documents:
            result = collection.insert_many(documents)
            print(f"✓ Inserted {len(result.inserted_ids)} documents")
        
        # Print summary
        total_in_db = collection.count_documents({})
        
        print(f"\n{'='*60}")
        print(f"Import Complete!")
        print(f"{'='*60}")
        print(f"Total rows in CSV:       {row_count}")
        print(f"Total documents in DB:  {total_in_db}")
        print(f"{'='*60}\n")
        
        return True
    
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        return False


def convert_duration_to_seconds(duration_str):
    """
    Converts duration string to seconds
    Already in seconds in the CSV, just ensure it's a number
    
    Args:
        duration_str: String representation of duration
    
    Returns:
        Integer seconds or 0 if invalid
    """
    try:
        if not duration_str or not str(duration_str).strip():
            return 0
        
        # Try to convert directly to float first
        return int(float(str(duration_str).strip()))
    except (ValueError, AttributeError, TypeError):
        return 0


def convert_to_float(value):
    """
    Safely converts string to float
    
    Args:
        value: String representation of number
    
    Returns:
        Float or 0.0 if invalid
    """
    try:
        if not value or str(value).strip() == '0':
            return 0.0
        return float(str(value).strip())
    except (ValueError, AttributeError, TypeError):
        return 0.0


def verify_data():
    """
    Verifies the loaded data
    Prints sample documents and statistics
    """
    try:
        collection = get_collection()
        
        total = collection.count_documents({})
        print(f"\n{'='*60}")
        print(f"Data Verification")
        print(f"{'='*60}")
        print(f"Total documents: {total}\n")
        
        if total > 0:
            # Show a sample document
            sample = collection.find_one()
            print("Sample document:")
            for key, value in sample.items():
                if key != '_id':
                    print(f"  {key}: {value}")
            
            # Show field statistics
            print(f"\n{'='*60}")
            print("Field Statistics:")
            print(f"{'='*60}")
            
            countries = collection.distinct('country')
            shapes = collection.distinct('shape')
            states = collection.distinct('state')
            
            print(f"Unique countries: {len(countries)}")
            print(f"Unique states:    {len(states)}")
            print(f"Unique shapes:    {len(shapes)}")
            
            print(f"\nTop 5 countries:")
            country_counts = {}
            for doc in collection.find({}, {'country': 1}):
                country = doc.get('country', 'unknown')
                country_counts[country] = country_counts.get(country, 0) + 1
            
            for country, count in sorted(country_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {country}: {count}")
            
            print(f"\nTop 5 shapes:")
            shape_counts = {}
            for doc in collection.find({}, {'shape': 1}):
                shape = doc.get('shape', 'unknown')
                shape_counts[shape] = shape_counts.get(shape, 0) + 1
            
            for shape, count in sorted(shape_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                print(f"  {shape}: {count}")
    
    except Exception as e:
        print(f"✗ Error verifying data: {e}")


if __name__ == '__main__':
    """
    Entry point - Run this script once to load data
    """
    print("\n" + "="*60)
    print("UFO Sightings Data Loader")
    print("="*60)
    print("\nThis script will:")
    print("1. Read cleaned_ufo.csv")
    print("2. Import into MongoDB")
    print("3. Verify the data")
    print("\nMake sure MongoDB is running!")
    print("="*60 + "\n")
    
    # Load data
    success = load_data_from_csv('cleaned_ufo.csv')
    
    if success:
        # Verify
        verify_data()
        print("\n✓ Data loaded successfully!")
        print("You can now run: python app.py\n")
    else:
        print("\n✗ Data loading failed!\n")
