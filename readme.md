📘 UFO Sightings Analytics Dashboard — README (Extremely Detailed)
End-to-End Explanation of Every File, Flow, Feature, and Implementation Choice
🌍 Overview

UFO Sightings Analytics Dashboard is a full-stack data analytics project built using:

Flask (Python backend)

MongoDB (NoSQL storage)

Plotly.js (frontend charts)

HTML/CSS/JS (frontend)

REST APIs for filter-driven data retrieval

CSV Export for filtered results

This project imports real UFO sighting data, stores it in MongoDB, and visualizes it through an interactive dashboard where users can:

✔ Select filters (country, state, year, shape, etc.)
✔ View multiple data visualizations
✔ Export filtered results
✔ Explore the dataset interactively

📁 Directory Structure (Explained in Depth)
ufo_dashboard/
│
├── app.py
├── utils.py
├── queries.py
├── data_loader.py
├── export_utils.py
│
├── static/
│   ├── index.html
│   ├── dashboard.js
│   ├── styles.css
│
├── cleaned_ufo.csv
│
└── README.md


Below is an extremely detailed explanation of each component.

🧠 Backend Architecture (Flask + MongoDB)

Your backend has five key files:

1️⃣ app.py — Main Flask Application

This is the entry point of your project.

Responsibilities:

Starts the web server

Defines all REST API endpoints

Handles filter requests from the frontend

Calls functions inside queries.py and export_utils.py

Serves the frontend (index.html)

Key Endpoints:
Endpoint	Description
/	Serves dashboard UI
/filter	Returns filtered data to frontend
/export/csv	Returns filtered data as CSV file
/export/pdf	(Optional) Converts filtered data to PDF
/distinct/<field>	Returns unique values for dropdowns (countries/states/shapes)
2️⃣ utils.py — MongoDB Connection Helper

A small file with one intention:

Make connecting to MongoDB simple and reusable.

What it does:

Reads Mongo connection URI

Connects using pymongo

Exposes get_collection() so other files don’t need to write connection code

Why this exists:

Keeps code clean

Prevents repeating connection logic

Lets you change DB/collection name in one place

3️⃣ queries.py — All MongoDB Query Logic

This file contains all business logic for retrieving data from MongoDB.

Responsibilities:

Apply filters:

country

state

shape

year range

duration range

Convert MongoDB documents to Python dicts

Return data to the Flask app

Why it's separate:

Keeps app.py clean

Makes query logic reusable

Easier to test and modify

4️⃣ data_loader.py — One-Time Data Import Script

This file loads the UFO dataset from your cleaned CSV file (cleaned_ufo.csv) and inserts rows into MongoDB.

Important:

✔ NO datetime conversion
✔ datetime is stored exactly as it appears in your CSV
✔ No new columns are added
✔ Minimal changes from raw data

Steps performed:

Reads cleaned_ufo.csv

Converts each row into a dictionary

Inserts into MongoDB collection

Prints summary: count inserted, total rows, etc.

You run this script once:

python data_loader.py

5️⃣ export_utils.py — CSV/PDF Export Logic

This file handles export features.

Functions:

export_csv(data)
Converts list of documents → CSV bytes

export_pdf(data)
Converts list of documents → minimal PDF table

Used by /export/csv endpoint.

🌐 Frontend Architecture (HTML + JS + Plotly)

The frontend is inside the static/ folder.

6️⃣ index.html — The Main Dashboard Page

This is the ONLY HTML file.

Includes:

Dropdowns:

Country

State

Shape

Year range

Buttons:

Apply Filters

Export CSV

Div containers for 6 graphs

Links to:

Plotly.js CDN

dashboard.js

styles.css

This page is sent to the user when they hit /.

7️⃣ dashboard.js — All Frontend Logic

This file handles all interactions.

Responsibilities:

Fetch dropdown values (countries, states, shapes)

Fetch filtered data from /filter

Render charts using Plotly:

Sightings per year

Distribution by shape

Country-wise counts

Seasonal trends

Duration histogram

Map visualization (lat/lon)

Handle CSV export by calling /export/csv

Why separate from HTML?

Cleaner code

All JavaScript logic stays organized

UI stays simple

8️⃣ styles.css — Custom Styling

Contains minimal styling:

Layout

Chart spacing

Dropdown/group styling

Buttons

Simple grid system

Nothing complex — lightweight styling for readability.

🧬 Dataset Details

You are using:

cleaned_ufo.csv


Based on your requirement:

✔ Original datetime column left as-is
✔ No conversion to Python datetime
✔ No extra preprocessing
✔ Only minimal cleanup performed earlier

Inserted into MongoDB exactly as stored in CSV.

🛰 MongoDB Data Model

Each document looks like:

{
  "datetime": "10/10/1949 20:30",
  "city": "san marcos",
  "state": "tx",
  "country": "us",
  "shape": "circle",
  "duration_seconds": 2700,
  "comments": "This is a UFO sighting...",
  "latitude": 29.883056,
  "longitude": -97.941111
}


No transformations — minimal changes.

🖥 How the App Works (Step-by-Step Flow)
1. User opens the dashboard

index.html loads.

2. JS requests dropdown values

It calls:

/distinct/country
/distinct/state
/distinct/shape

3. User selects filters and clicks Apply

JS sends a POST request:

/filter
{
  "country": "...",
  "state": "...",
  "shape": "...",
  "yearRange": [start, end]
}

4. Flask receives request

app.py → calls queries.py → queries MongoDB.

5. MongoDB returns filtered rows

They go back to the frontend.

6. JS renders 6 charts with Plotly

Each chart uses the same filtered dataset.

7. User exports CSV

Dashboard sends:

/export/csv


Flask → export_utils.py → returns a downloadable file.

🧪 Graphs Included

The dashboard renders:

Sightings per Year (Line Chart)

Sightings by Shape (Bar Chart)

Sightings by Country (Pie Chart)

Sightings per Month (Trend Line)

Duration Distribution (Histogram)

UFO Map (Scatter Geo)

📦 How to Install and Run
Step 1 — Install dependencies
pip install flask pymongo pandas plotly reportlab

Step 2 — Edit MongoDB URI

In utils.py:

MONGO_URI = "mongodb://localhost:27017"

Step 3 — Load dataset into MongoDB
python data_loader.py

Step 4 — Run the dashboard
python app.py

Step 5 — Open browser

Navigate to:

http://localhost:5000

🧩 Why This Project Is Designed This Way
✔ Minimal logic
✔ Minimal files
✔ Easy to understand
✔ Simple to scale
✔ All “data ops” isolated
✔ All “query ops” isolated
✔ All “export ops” isolated
✔ All “frontend logic” isolated

This structure is optimal for learning, interviews, portfolio projects, or production extensions.

🏁 Conclusion

This README gives you:

A fully detailed explanation of every file

Complete backend + frontend architecture

Data flow from CSV → MongoDB → UI

Graphs, dropdown filters, and exports

Installation and usage guide

Data model explanation

Full control with minimal changes