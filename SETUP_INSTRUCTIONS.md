# UFO Sightings Analytics Dashboard - Complete Setup Guide

## 📋 Overview

This is a complete end-to-end data analytics project that analyzes UFO sightings data using:
- **Backend**: Flask (Python web framework)
- **Database**: MongoDB (NoSQL database)
- **Frontend**: HTML, CSS, JavaScript, Plotly (interactive charts)
- **Dataset**: 88,877 UFO sighting records

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: Make sure you have Python 3.7+ installed.

### Step 2: Start MongoDB

```bash
# On Linux/Mac:
mongod

# On Windows:
# Open Command Prompt and run:
mongod
```

**Note**: MongoDB must be running on `localhost:27017` (default)

### Step 3: Load Data & Run App

```bash
# Terminal 1: Load the dataset (run this ONCE)
python data_loader.py

# Terminal 2: Run the Flask app
python app.py
```

Open your browser and navigate to: **http://localhost:5000**

---

## 📁 Project Structure

```
UFO/
├── app.py                    # Main Flask application (ENTRY POINT)
├── utils.py                  # MongoDB connection helper
├── queries.py                # Database query functions
├── data_loader.py            # CSV data import script
├── export_utils.py           # CSV/PDF export utilities
├── requirements.txt          # Python dependencies
│
├── static/
│   ├── index.html           # Frontend dashboard HTML
│   ├── dashboard.js         # Frontend logic & chart rendering
│   ├── styles.css           # Dashboard styling
│
├── cleaned_ufo.csv          # Dataset (88,877 records)
├── readme.md                # Project documentation
└── SETUP_INSTRUCTIONS.md    # This file
```

---

## 🔧 Detailed Setup Instructions

### 1. Prerequisites

Before starting, ensure you have installed:
- **Python 3.7+** 
- **MongoDB Community Edition**
- **pip** (Python package manager)

### 2. Create & Activate Virtual Environment (Optional but Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Packages installed:**
- `Flask` - Web framework
- `pymongo` - MongoDB driver
- `pandas` - Data manipulation
- `plotly` - Interactive charts
- `reportlab` - PDF generation

### 4. Configure MongoDB Connection

The default connection is `mongodb://localhost:27017`

**To use a different MongoDB instance:**
1. Open `utils.py`
2. Find line: `MONGO_URI = "mongodb://localhost:27017"`
3. Replace with your MongoDB URI

**For MongoDB Atlas Cloud:**
```python
MONGO_URI = "mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority"
```

### 5. Load the Dataset

Run the data loader script (ONLY ONCE):

```bash
python data_loader.py
```

**What it does:**
1. Reads `cleaned_ufo.csv` (88,877 records)
2. Parses each row
3. Inserts into MongoDB collection `ufo_database.sightings`
4. Prints summary statistics

**Output should look like:**
```
============================================================
UFO Data Loader - Importing from cleaned_ufo.csv
============================================================

Clear existing data before importing? (y/n): y
✓ Inserted 1000 documents
✓ Inserted 1000 documents
...
============================================================
Import Complete!
============================================================
Total rows in CSV:       88877
Total documents in DB:   88877
============================================================
```

### 6. Start the Flask Application

```bash
python app.py
```

**Expected output:**
```
============================================================
UFO Sightings Analytics Dashboard
============================================================
Starting Flask server...
Navigate to: http://localhost:5000
============================================================
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

### 7. Open Dashboard in Browser

Navigate to: **http://localhost:5000**

---

## 📊 Features & Usage

### Dashboard Filters

- **Country**: Filter by country (us, gb, ca, etc.)
- **State**: Filter by state/province (tx, ca, ny, etc.)
- **UFO Shape**: Filter by reported shape (circle, disk, triangle, etc.)
- **Year Range**: Filter by date range (e.g., 1950-2000)
- **Duration Range**: Filter by sighting duration in seconds

### Interactive Charts

The dashboard displays 6 charts:

1. **Sightings Per Year** - Trend over time
2. **Sightings by Shape** - Distribution of UFO shapes
3. **Sightings by Country** - Geographic distribution
4. **Seasonal Trend** - Monthly patterns
5. **Duration Distribution** - How long sightings lasted
6. **UFO Map** - Geographic locations of sightings

### Summary Statistics

Display real-time statistics:
- Total sightings matching filters
- Average duration
- Unique countries represented
- Unique UFO shapes reported

### Export Function

Click **"Export CSV"** to download filtered results as a CSV file.

---

## 📊 Dataset Details

**File**: `cleaned_ufo.csv`  
**Records**: 88,877 sightings  
**Date Range**: 1949 - 2010+

**Columns**:
- `datetime` - Date and time of sighting (MM/DD/YYYY HH:MM)
- `city` - City name
- `state` - State/province code
- `country` - Country code (us, gb, ca, etc.)
- `shape` - Reported UFO shape
- `duration (seconds)` - Duration in seconds
- `duration (hours/min)` - Human-readable duration
- `comments` - Detailed description
- `date posted` - When reported to NUFORC
- `latitude` - Geographic latitude
- `longitude` - Geographic longitude

---

## 🔌 API Endpoints

### GET `/`
Serves the dashboard HTML page

### GET `/distinct/<field>`
Returns unique values for dropdown filters

**Example**:
```
GET /distinct/country
Response: {"success": true, "values": ["us", "gb", "ca", ...]}
```

### POST `/filter`
Returns filtered UFO sightings data

**Request**:
```json
{
    "country": "us",
    "state": "tx",
    "shape": "circle",
    "yearRange": [1949, 2010],
    "durationRange": [0, 10000]
}
```

**Response**:
```json
{
    "success": true,
    "count": 150,
    "data": [
        {
            "datetime": "10/10/1949 20:30",
            "city": "san marcos",
            "state": "tx",
            ...
        }
    ]
}
```

### POST `/summary`
Returns summary statistics for filtered data

### POST `/export/csv`
Returns filtered data as downloadable CSV file

---

## 🐛 Troubleshooting

### Error: "Failed to connect to MongoDB"
**Solution**: Make sure MongoDB is running
```bash
mongod
```

### Error: "ModuleNotFoundError: No module named 'flask'"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Error: "Port 5000 already in use"
**Solution**: Change the port in `app.py`
```python
# Change line at bottom:
app.run(debug=True, host='0.0.0.0', port=8000)  # Use 8000 instead
```

### No data showing in dashboard
**Solution**: Make sure you ran `python data_loader.py` first

### Charts not rendering
**Solution**: Check browser console for errors (F12 → Console tab)

---

## 📝 File Descriptions

### Backend Files

#### `app.py` (Main Application)
- Entry point for the entire project
- Defines Flask routes (/, /filter, /export/csv, /distinct/<field>)
- Handles HTTP requests from frontend
- Calls functions from queries.py and export_utils.py

#### `utils.py` (MongoDB Helper)
- Manages MongoDB connection
- Provides `get_collection()` function
- Can clear/reset data
- Creates database indexes

#### `queries.py` (Data Queries)
- Contains all MongoDB query logic
- Functions:
  - `get_filtered_data()` - Main filter function
  - `get_sightings_by_year()` - Year grouping
  - `get_sightings_by_shape()` - Shape distribution
  - `get_sightings_by_country()` - Country grouping
  - `get_sightings_by_month()` - Monthly grouping
  - `get_summary_stats()` - Statistics calculation

#### `data_loader.py` (Data Import)
- Reads cleaned_ufo.csv
- Inserts records into MongoDB
- Provides data verification
- Run ONCE before starting app

#### `export_utils.py` (Export Functions)
- `export_csv()` - Convert data to CSV bytes
- `export_pdf()` - Convert data to PDF
- Generate download filenames

### Frontend Files

#### `index.html` (Dashboard UI)
- HTML structure of dashboard
- Dropdown filter selectors
- Chart containers (divs)
- Summary statistics displays
- Export button
- Links external libraries (Plotly, Bootstrap)

#### `dashboard.js` (Frontend Logic)
- Fetches dropdown values from backend
- Sends filter requests to backend
- Renders 6 interactive Plotly charts
- Handles CSV export
- Updates statistics in real-time

#### `styles.css` (Styling)
- Modern dashboard styling
- Responsive design (mobile-friendly)
- Color scheme and layout
- Button and input styling
- Gradient backgrounds
- Hover effects

---

## 🚀 How It All Works Together

### Data Flow:

1. **User opens http://localhost:5000**
   - Browser downloads index.html

2. **JavaScript loads**
   - dashboard.js starts
   - Fetches dropdown values from /distinct/* endpoints
   - Populates filter dropdowns

3. **User applies filters**
   - JavaScript sends POST to /filter
   - Flask calls queries.py → MongoDB
   - MongoDB returns filtered documents
   - Flask returns JSON to frontend

4. **Frontend renders charts**
   - dashboard.js processes data
   - Plotly renders 6 interactive charts
   - Summary statistics update

5. **User exports data**
   - Click "Export CSV"
   - Frontend sends filter criteria
   - Flask calls export_utils.py
   - CSV bytes returned as download

---

## 📊 MongoDB Data Structure

**Database**: `ufo_database`  
**Collection**: `sightings`

**Sample Document**:
```json
{
    "_id": ObjectId("..."),
    "datetime": "10/10/1949 20:30",
    "city": "san marcos",
    "state": "tx",
    "country": "us",
    "shape": "cylinder",
    "duration (seconds)": 2700,
    "duration (hours/min)": "45 minutes",
    "comments": "This event took place in early fall...",
    "date posted": "4/27/2004",
    "latitude": 29.8830556,
    "longitude": -97.9411111
}
```

---

## 🔐 Security Notes

This is a portfolio/learning project. For production:
- Use environment variables for sensitive data
- Implement user authentication
- Add rate limiting
- Use HTTPS
- Validate/sanitize all inputs
- Use MongoDB authentication

---

## 🎯 Next Steps / Enhancements

Possible improvements:
- [ ] Add user authentication
- [ ] Implement data caching
- [ ] Add more chart types
- [ ] Search by comments
- [ ] PDF export
- [ ] Data analysis/statistics
- [ ] Time series analysis
- [ ] Machine learning predictions
- [ ] API documentation (Swagger)
- [ ] Unit tests
- [ ] Docker containerization
- [ ] Deploy to cloud (Heroku, AWS, Azure)

---

## 📚 Learning Resources

- **Flask**: https://flask.palletsprojects.com/
- **MongoDB**: https://docs.mongodb.com/
- **Plotly**: https://plotly.com/javascript/
- **PyMongo**: https://pymongo.readthedocs.io/

---

## 📞 Support

If you encounter issues:
1. Check the Troubleshooting section
2. Verify all dependencies are installed
3. Make sure MongoDB is running
4. Check browser console (F12) for JavaScript errors
5. Check terminal output for Python errors

---

## ✅ Checklist Before Running

- [ ] Python 3.7+ installed
- [ ] All dependencies installed (`pip install -r requirements.txt`)
- [ ] MongoDB installed and running
- [ ] `cleaned_ufo.csv` in project folder
- [ ] No other app running on port 5000
- [ ] Data loader run (`python data_loader.py`)
- [ ] Ready to run app (`python app.py`)

---

## 🎉 You're All Set!

Your UFO Sightings Analytics Dashboard is ready to use!

**Quick Start**:
```bash
# Terminal 1: Start MongoDB
mongod

# Terminal 2: Load data (first time only)
python data_loader.py

# Terminal 3: Run app
python app.py

# Browser: Open http://localhost:5000
```

Enjoy exploring UFO sighting data! 🛸

---

**Project Created**: 2024  
**Version**: 1.0  
**License**: MIT
