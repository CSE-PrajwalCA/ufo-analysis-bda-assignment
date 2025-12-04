"""
UFO Dashboard - MongoDB Query Logic
All database queries for filtering and analyzing data
"""

from utils import get_collection
from datetime import datetime
import re


def extract_year(datetime_str):
    """
    Extracts year from datetime string
    Format expected: "10/10/1949 20:30"
    
    Args:
        datetime_str: String in format "MM/DD/YYYY HH:MM"
    
    Returns:
        Integer year, or None if parsing fails
    """
    try:
        if not datetime_str or not isinstance(datetime_str, str):
            return None
        
        parts = datetime_str.split()
        if len(parts) < 1:
            return None
        
        date_parts = parts[0].split('/')
        if len(date_parts) >= 3:
            return int(date_parts[2])
        
        return None
    except (ValueError, IndexError, AttributeError):
        return None


def get_distinct_values(field):
    """
    Returns all unique values for a given field
    Used to populate dropdown filters
    
    Args:
        field: Field name (country, state, shape)
    
    Returns:
        List of unique values sorted alphabetically
    """
    try:
        collection = get_collection()
        
        # Field mapping
        field_map = {
            'country': 'country',
            'state': 'state',
            'shape': 'shape'
        }
        
        if field not in field_map:
            return []
        
        db_field = field_map[field]
        
        # Get distinct values
        values = collection.distinct(db_field)
        
        # Clean up and sort
        values = [v for v in values if v and v.strip()]
        values = list(set(values))  # Remove duplicates
        values.sort()
        
        return values
    
    except Exception as e:
        print(f"Error getting distinct {field}: {e}")
        return []


def get_filtered_data(country='', state='', shape='', year_range=None, duration_range=None):
    """
    Returns filtered UFO sighting records
    
    Args:
        country: Country code filter (e.g., 'us')
        state: State/province filter (e.g., 'tx')
        shape: UFO shape filter (e.g., 'circle')
        year_range: List [start_year, end_year]
        duration_range: List [min_seconds, max_seconds]
    
    Returns:
        List of dictionaries containing matching records
    """
    try:
        collection = get_collection()
        
        # Build MongoDB query
        query = {}
        
        # Add filters only if provided
        if country and country.strip():
            query['country'] = country.lower().strip()
        
        if state and state.strip():
            query['state'] = state.lower().strip()
        
        if shape and shape.strip():
            query['shape'] = shape.lower().strip()
        
        # Duration filter
        if duration_range:
            min_duration = duration_range[0] if len(duration_range) > 0 else 0
            max_duration = duration_range[1] if len(duration_range) > 1 else 999999
            
            query['duration (seconds)'] = {
                '$gte': min_duration,
                '$lte': max_duration
            }
        
        # Execute query
        cursor = collection.find(query).limit(10000)  # Limit for performance
        
        records = []
        for doc in cursor:
            # Remove MongoDB's internal ID field
            doc.pop('_id', None)
            records.append(doc)
        
        # Post-filter by year (since it's not stored in DB)
        if year_range:
            min_year = year_range[0]
            max_year = year_range[1]
            
            filtered_records = []
            for record in records:
                year = extract_year(record.get('datetime', ''))
                if year and min_year <= year <= max_year:
                    filtered_records.append(record)
            
            records = filtered_records
        
        return records
    
    except Exception as e:
        print(f"Error filtering data: {e}")
        return []


def get_sightings_by_year():
    """
    Groups sightings by year
    
    Returns:
        Dictionary: {year: count}
    """
    try:
        collection = get_collection()
        documents = collection.find({})
        
        year_counts = {}
        
        for doc in documents:
            year = extract_year(doc.get('datetime', ''))
            if year:
                if year not in year_counts:
                    year_counts[year] = 0
                year_counts[year] += 1
        
        # Sort by year
        sorted_years = sorted(year_counts.items())
        return dict(sorted_years)
    
    except Exception as e:
        print(f"Error getting sightings by year: {e}")
        return {}


def get_sightings_by_shape():
    """
    Groups sightings by shape
    
    Returns:
        Dictionary: {shape: count}
    """
    try:
        collection = get_collection()
        
        result = collection.aggregate([
            {
                '$group': {
                    '_id': '$shape',
                    'count': {'$sum': 1}
                }
            },
            {
                '$sort': {'count': -1}
            }
        ])
        
        shape_counts = {}
        for item in result:
            if item['_id']:
                shape_counts[item['_id']] = item['count']
        
        return shape_counts
    
    except Exception as e:
        print(f"Error getting sightings by shape: {e}")
        return {}


def get_sightings_by_country():
    """
    Groups sightings by country
    
    Returns:
        Dictionary: {country: count}
    """
    try:
        collection = get_collection()
        
        result = collection.aggregate([
            {
                '$group': {
                    '_id': '$country',
                    'count': {'$sum': 1}
                }
            },
            {
                '$sort': {'count': -1}
            }
        ])
        
        country_counts = {}
        for item in result:
            if item['_id']:
                country_counts[item['_id']] = item['count']
        
        return country_counts
    
    except Exception as e:
        print(f"Error getting sightings by country: {e}")
        return {}


def get_sightings_by_month():
    """
    Groups sightings by month across all years
    
    Returns:
        Dictionary: {month: count} where month is 1-12
    """
    try:
        collection = get_collection()
        documents = collection.find({})
        
        month_counts = {i: 0 for i in range(1, 13)}
        
        for doc in documents:
            datetime_str = doc.get('datetime', '')
            if datetime_str:
                try:
                    parts = datetime_str.split()
                    if len(parts) > 0:
                        date_parts = parts[0].split('/')
                        if len(date_parts) >= 2:
                            month = int(date_parts[0])
                            if 1 <= month <= 12:
                                month_counts[month] += 1
                except (ValueError, IndexError):
                    pass
        
        return month_counts
    
    except Exception as e:
        print(f"Error getting sightings by month: {e}")
        return {}


def get_duration_distribution():
    """
    Returns duration distribution statistics
    
    Returns:
        List of durations for histogram
    """
    try:
        collection = get_collection()
        documents = collection.find({}, {'duration (seconds)': 1})
        
        durations = []
        for doc in documents:
            duration = doc.get('duration (seconds)', 0)
            if isinstance(duration, (int, float)) and duration > 0:
                durations.append(duration)
        
        return durations
    
    except Exception as e:
        print(f"Error getting duration distribution: {e}")
        return []


def get_geolocations():
    """
    Returns all sightings with latitude and longitude
    
    Returns:
        List of dictionaries with lat/lon data
    """
    try:
        collection = get_collection()
        documents = collection.find(
            {'latitude': {'$ne': 0}, 'longitude': {'$ne': 0}},
            {'latitude': 1, 'longitude': 1, 'city': 1, 'country': 1}
        )
        
        locations = []
        for doc in documents:
            if doc.get('latitude') and doc.get('longitude'):
                locations.append({
                    'lat': doc['latitude'],
                    'lon': doc['longitude'],
                    'city': doc.get('city', ''),
                    'country': doc.get('country', '')
                })
        
        return locations
    
    except Exception as e:
        print(f"Error getting geolocations: {e}")
        return []


def get_summary_stats(country='', state='', shape='', year_range=None, duration_range=None):
    """
    Returns summary statistics for filtered data
    
    Returns:
        Dictionary with stats
    """
    try:
        data = get_filtered_data(country, state, shape, year_range, duration_range)
        
        if not data:
            return {
                'total_sightings': 0,
                'avg_duration': 0,
                'countries': 0,
                'shapes': 0
            }
        
        # Calculate statistics
        total = len(data)
        
        # Average duration
        durations = [
            d.get('duration (seconds)', 0) 
            for d in data 
            if isinstance(d.get('duration (seconds)'), (int, float))
        ]
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        # Unique countries
        countries = len(set(d.get('country', '') for d in data if d.get('country')))
        
        # Unique shapes
        shapes = len(set(d.get('shape', '') for d in data if d.get('shape')))
        
        return {
            'total_sightings': total,
            'avg_duration': round(avg_duration, 2),
            'unique_countries': countries,
            'unique_shapes': shapes
        }
    
    except Exception as e:
        print(f"Error getting summary stats: {e}")
        return {}
