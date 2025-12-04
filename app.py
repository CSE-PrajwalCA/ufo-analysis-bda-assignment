"""
UFO Sightings Analytics Dashboard - Main Flask Application (FIXED)
Entry point for the entire project
"""

import os
from flask import Flask, render_template, request, jsonify, send_file
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import json
from datetime import datetime
import io
import csv

# ============================================================
# CONFIGURATION
# ============================================================
MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "ufo_database"
COLLECTION_NAME = "sightings"

# ============================================================
# FLASK APP CONFIGURATION
# ============================================================
app = Flask(__name__, 
            static_folder=os.path.join(os.path.dirname(__file__), 'static'),
            template_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Global MongoDB connection
mongo_client = None
mongo_db = None


# ============================================================
# MONGODB CONNECTION HELPER
# ============================================================
def get_db():
    """Get database connection"""
    global mongo_client, mongo_db
    
    try:
        if mongo_client is None:
            mongo_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
            mongo_client.admin.command('ping')
            mongo_db = mongo_client[DB_NAME]
            print("✓ Connected to MongoDB")
        
        return mongo_db
    except ServerSelectionTimeoutError:
        print("✗ ERROR: MongoDB not running!")
        return None
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return None


def get_collection():
    """Get MongoDB collection"""
    db = get_db()
    if db is None:
        return None
    return db[COLLECTION_NAME]


# ============================================================
# ROUTE: Serve the Dashboard UI
# ============================================================
@app.route('/')
def dashboard():
    """Serves the main dashboard HTML page"""
    try:
        return render_template('index.html')
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ============================================================
# ROUTE: Get Distinct Values for Dropdowns
# ============================================================
@app.route('/distinct/<field>', methods=['GET'])
def distinct_values(field):
    """Returns unique values for dropdown filters"""
    try:
        collection = get_collection()
        if collection is None:
            return jsonify({"success": False, "error": "MongoDB not connected"}), 500
        
        valid_fields = ['country', 'state', 'shape']
        if field not in valid_fields:
            return jsonify({"success": False, "error": "Invalid field"}), 400
        
        # Get distinct values
        values = collection.distinct(field)
        
        # Clean up
        values = [v for v in values if v and str(v).strip()]
        values = sorted(list(set(values)))
        
        print(f"✓ GET /distinct/{field} - Found {len(values)} unique values")
        return jsonify({"success": True, "values": values})
    
    except Exception as e:
        print(f"✗ Error in /distinct/{field}: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================================
# ROUTE: Get Filtered Data
# ============================================================
@app.route('/filter', methods=['POST'])
def filter_data():
    """Returns filtered UFO sighting data"""
    try:
        collection = get_collection()
        if collection is None:
            return jsonify({"success": False, "error": "MongoDB not connected"}), 500
        
        filters = request.get_json() or {}
        
        # Extract filters
        country = filters.get('country', '').strip().lower()
        state = filters.get('state', '').strip().lower()
        shape = filters.get('shape', '').strip().lower()
        year_range = filters.get('yearRange', [1900, 2100])
        duration_range = filters.get('durationRange', [0, 999999])
        
        # Build query
        query = {}
        
        if country:
            query['country'] = country
        if state:
            query['state'] = state
        if shape:
            query['shape'] = shape
        
        # Duration filter
        if duration_range:
            query['duration (seconds)'] = {
                '$gte': int(duration_range[0]),
                '$lte': int(duration_range[1])
            }
        
        # Execute query
        cursor = collection.find(query).limit(10000)
        
        records = []
        for doc in cursor:
            doc.pop('_id', None)
            
            # Year filtering (client-side for now)
            if 'datetime' in doc:
                try:
                    year = int(doc['datetime'].split('/')[-1].split()[0])
                    if year_range[0] <= year <= year_range[1]:
                        records.append(doc)
                except:
                    records.append(doc)
            else:
                records.append(doc)
        
        print(f"✓ POST /filter - Returned {len(records)} records")
        return jsonify({"success": True, "count": len(records), "data": records})
    
    except Exception as e:
        print(f"✗ Error in /filter: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================================
# ROUTE: Get Summary Statistics
# ============================================================
@app.route('/summary', methods=['POST'])
def summary_stats():
    """Returns summary statistics"""
    try:
        collection = get_collection()
        if collection is None:
            return jsonify({"success": False, "error": "MongoDB not connected"}), 500
        
        filters = request.get_json() or {}
        
        # Build query (same as /filter)
        country = filters.get('country', '').strip().lower()
        state = filters.get('state', '').strip().lower()
        shape = filters.get('shape', '').strip().lower()
        duration_range = filters.get('durationRange', [0, 999999])
        
        query = {}
        if country:
            query['country'] = country
        if state:
            query['state'] = state
        if shape:
            query['shape'] = shape
        if duration_range:
            query['duration (seconds)'] = {
                '$gte': int(duration_range[0]),
                '$lte': int(duration_range[1])
            }
        
        # Get filtered data
        cursor = collection.find(query).limit(10000)
        data = list(cursor)
        
        # Calculate stats
        total = len(data)
        
        durations = [d.get('duration (seconds)', 0) for d in data 
                    if isinstance(d.get('duration (seconds)'), (int, float))]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        countries = len(set(d.get('country', '') for d in data if d.get('country')))
        shapes = len(set(d.get('shape', '') for d in data if d.get('shape')))
        
        stats = {
            'total_sightings': total,
            'avg_duration': round(avg_duration, 2),
            'unique_countries': countries,
            'unique_shapes': shapes
        }
        
        print(f"✓ POST /summary - Stats: {total} sightings")
        return jsonify({"success": True, "stats": stats})
    
    except Exception as e:
        print(f"✗ Error in /summary: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================================
# ROUTE: Export to CSV
# ============================================================
@app.route('/export/csv', methods=['POST'])
def export_csv():
    """Exports filtered data as CSV"""
    try:
        collection = get_collection()
        if collection is None:
            return jsonify({"success": False, "error": "MongoDB not connected"}), 500
        
        filters = request.get_json() or {}
        
        # Get filtered data
        country = filters.get('country', '').strip().lower()
        state = filters.get('state', '').strip().lower()
        shape = filters.get('shape', '').strip().lower()
        duration_range = filters.get('durationRange', [0, 999999])
        
        query = {}
        if country:
            query['country'] = country
        if state:
            query['state'] = state
        if shape:
            query['shape'] = shape
        if duration_range:
            query['duration (seconds)'] = {
                '$gte': int(duration_range[0]),
                '$lte': int(duration_range[1])
            }
        
        cursor = collection.find(query).limit(10000)
        data = list(cursor)
        
        # Create CSV
        output = io.StringIO()
        fieldnames = [
            'datetime', 'city', 'state', 'country', 'shape',
            'duration (seconds)', 'duration (hours/min)', 'comments',
            'date posted', 'latitude', 'longitude'
        ]
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        writer.writeheader()
        
        for record in data:
            row = {field: record.get(field, '') for field in fieldnames}
            writer.writerow(row)
        
        csv_bytes = output.getvalue().encode('utf-8')
        
        print(f"✓ POST /export/csv - Exported {len(data)} records")
        return send_file(
            io.BytesIO(csv_bytes),
            mimetype='text/csv',
            as_attachment=True,
            download_name=f'ufo_sightings_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        )
    
    except Exception as e:
        print(f"✗ Error in /export/csv: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================================
# ERROR HANDLERS
# ============================================================
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Route not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


# ============================================================
# MAIN ENTRY POINT
# ============================================================
if __name__ == '__main__':
    print("\n" + "="*60)
    print("UFO Sightings Analytics Dashboard")
    print("="*60)
    print("Checking MongoDB connection...")
    
    db = get_db()
    if db is None:
        print("\n✗ ERROR: Cannot start app without MongoDB!")
        print("Please start MongoDB first:")
        print("  $ mongod")
        print("\nThen run this script again.")
    else:
        collection = get_collection()
        if collection is not None:
            count = collection.count_documents({})
            print(f"✓ MongoDB connection successful!")
            print(f"✓ Found {count:,} records in database")
            print("\n" + "="*60)
            print("Starting Flask server...")
            print("Navigate to: http://localhost:5000")
            print("="*60 + "\n")
            
            app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
        else:
            print("\n✗ ERROR: Could not access collection!")
