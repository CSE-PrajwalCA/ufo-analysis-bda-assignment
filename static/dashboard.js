/**
 * UFO Sightings Analytics Dashboard - Frontend Logic
 * Handles all interactions, API calls, and chart rendering
 */

// ============================================================
// Global State
// ============================================================
let currentData = [];
let allCharts = {};

// ============================================================
// Initialization
// ============================================================
document.addEventListener('DOMContentLoaded', function() {
    console.log("UFO Dashboard initialized");
    
    // Load initial dropdown values
    loadDropdownValues();
    
    // Attach event listeners
    attachEventListeners();
    
    // Apply default filters on load
    applyFilters();
});


// ============================================================
// Event Listeners
// ============================================================
function attachEventListeners() {
    document.getElementById('applyFiltersBtn').addEventListener('click', applyFilters);
    document.getElementById('resetFiltersBtn').addEventListener('click', resetFilters);
    document.getElementById('exportCsvBtn').addEventListener('click', exportToCSV);
    
    // Auto-refresh when filter values change (optional)
    // document.getElementById('countryFilter').addEventListener('change', applyFilters);
}


// ============================================================
// Load Dropdown Values
// ============================================================
function loadDropdownValues() {
    console.log("Loading dropdown values...");
    
    // Load countries
    fetch('/distinct/country')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                populateSelect('countryFilter', data.values);
            }
        })
        .catch(error => console.error('Error loading countries:', error));
    
    // Load states
    fetch('/distinct/state')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                populateSelect('stateFilter', data.values);
            }
        })
        .catch(error => console.error('Error loading states:', error));
    
    // Load shapes
    fetch('/distinct/shape')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                populateSelect('shapeFilter', data.values);
            }
        })
        .catch(error => console.error('Error loading shapes:', error));
}


// ============================================================
// Populate Select Dropdown
// ============================================================
function populateSelect(selectId, values) {
    const select = document.getElementById(selectId);
    
    values.forEach(value => {
        if (value && value.trim()) {
            const option = document.createElement('option');
            option.value = value;
            option.textContent = value.charAt(0).toUpperCase() + value.slice(1);
            select.appendChild(option);
        }
    });
}


// ============================================================
// Get Current Filters
// ============================================================
function getFilters() {
    return {
        country: document.getElementById('countryFilter').value,
        state: document.getElementById('stateFilter').value,
        shape: document.getElementById('shapeFilter').value,
        yearRange: [
            parseInt(document.getElementById('yearFrom').value) || 1900,
            parseInt(document.getElementById('yearTo').value) || 2100
        ],
        durationRange: [
            parseInt(document.getElementById('durationMin').value) || 0,
            parseInt(document.getElementById('durationMax').value) || 999999
        ]
    };
}


// ============================================================
// Apply Filters & Fetch Data
// ============================================================
function applyFilters() {
    console.log("Applying filters...");
    
    showLoadingIndicator(true);
    const filters = getFilters();
    
    // Fetch filtered data
    fetch('/filter', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(filters)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentData = data.data;
            console.log(`Fetched ${data.count} records`);
            
            // Render all charts
            renderAllCharts();
            
            // Update stats
            updateStats(filters);
        } else {
            alert('Error fetching data: ' + data.error);
        }
        showLoadingIndicator(false);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error fetching data');
        showLoadingIndicator(false);
    });
}


// ============================================================
// Update Summary Statistics
// ============================================================
function updateStats(filters) {
    console.log("Updating statistics...");
    
    fetch('/summary', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(filters)
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const stats = data.stats;
            document.getElementById('statTotalSightings').textContent = stats.total_sightings || 0;
            document.getElementById('statAvgDuration').textContent = stats.avg_duration || 0;
            document.getElementById('statCountries').textContent = stats.unique_countries || 0;
            document.getElementById('statShapes').textContent = stats.unique_shapes || 0;
        }
    })
    .catch(error => console.error('Error updating stats:', error));
}


// ============================================================
// Render All Charts
// ============================================================
function renderAllCharts() {
    console.log("Rendering charts...");
    
    renderSightingsPerYearChart();
    renderSightingsByShapeChart();
    renderSightingsByCountryChart();
    renderMonthlyTrendChart();
    renderDurationDistributionChart();
    renderGeoMapChart();
}


// ============================================================
// Chart 1: Sightings Per Year (Line Chart)
// ============================================================
function renderSightingsPerYearChart() {
    const yearCounts = {};
    
    currentData.forEach(record => {
        const year = extractYear(record.datetime);
        if (year) {
            yearCounts[year] = (yearCounts[year] || 0) + 1;
        }
    });
    
    const sortedYears = Object.keys(yearCounts).sort((a, b) => a - b);
    const counts = sortedYears.map(year => yearCounts[year]);
    
    const trace = {
        x: sortedYears,
        y: counts,
        type: 'scatter',
        mode: 'lines+markers',
        name: 'Sightings',
        line: { color: '#1f77b4', width: 2 },
        marker: { size: 4 }
    };
    
    const layout = {
        title: 'UFO Sightings Per Year',
        xaxis: { title: 'Year' },
        yaxis: { title: 'Number of Sightings' },
        hovermode: 'closest',
        margin: { t: 40, b: 40, l: 60, r: 20 }
    };
    
    Plotly.newPlot('chartSightingsPerYear', [trace], layout, { responsive: true });
}


// ============================================================
// Chart 2: Sightings By Shape (Bar Chart)
// ============================================================
function renderSightingsByShapeChart() {
    const shapeCounts = {};
    
    currentData.forEach(record => {
        const shape = record.shape || 'unknown';
        shapeCounts[shape] = (shapeCounts[shape] || 0) + 1;
    });
    
    // Sort by count and take top 10
    const sorted = Object.entries(shapeCounts)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10);
    
    const shapes = sorted.map(([shape, count]) => shape);
    const counts = sorted.map(([shape, count]) => count);
    
    const trace = {
        x: shapes,
        y: counts,
        type: 'bar',
        marker: { color: '#ff7f0e' }
    };
    
    const layout = {
        title: 'Top 10 UFO Shapes',
        xaxis: { title: 'Shape' },
        yaxis: { title: 'Count' },
        margin: { t: 40, b: 100, l: 60, r: 20 }
    };
    
    Plotly.newPlot('chartSightingsByShape', [trace], layout, { responsive: true });
}


// ============================================================
// Chart 3: Sightings By Country (Pie Chart)
// ============================================================
function renderSightingsByCountryChart() {
    const countryCounts = {};
    
    currentData.forEach(record => {
        const country = record.country || 'unknown';
        countryCounts[country] = (countryCounts[country] || 0) + 1;
    });
    
    const countries = Object.keys(countryCounts);
    const counts = Object.values(countryCounts);
    
    const trace = {
        labels: countries,
        values: counts,
        type: 'pie',
        textposition: 'inside',
        textinfo: 'label+percent'
    };
    
    const layout = {
        title: 'Sightings by Country',
        margin: { t: 40, b: 40, l: 60, r: 60 }
    };
    
    Plotly.newPlot('chartSightingsByCountry', [trace], layout, { responsive: true });
}


// ============================================================
// Chart 4: Monthly Trend (Line Chart)
// ============================================================
function renderMonthlyTrendChart() {
    const monthCounts = {
        1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0,
        7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0
    };
    
    currentData.forEach(record => {
        const month = extractMonth(record.datetime);
        if (month) {
            monthCounts[month]++;
        }
    });
    
    const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                        'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const counts = Object.values(monthCounts);
    
    const trace = {
        x: monthNames,
        y: counts,
        type: 'scatter',
        mode: 'lines+markers',
        fill: 'tozeroy',
        name: 'Sightings',
        line: { color: '#2ca02c', width: 2 },
        marker: { size: 6 }
    };
    
    const layout = {
        title: 'Seasonal Trend (Monthly)',
        xaxis: { title: 'Month' },
        yaxis: { title: 'Number of Sightings' },
        hovermode: 'closest',
        margin: { t: 40, b: 40, l: 60, r: 20 }
    };
    
    Plotly.newPlot('chartMonthlyTrend', [trace], layout, { responsive: true });
}


// ============================================================
// Chart 5: Duration Distribution (Histogram)
// ============================================================
function renderDurationDistributionChart() {
    const durations = currentData
        .map(r => r['duration (seconds)'])
        .filter(d => typeof d === 'number' && d > 0 && d < 100000)
        .slice(0, 1000);  // Limit for performance
    
    const trace = {
        x: durations,
        type: 'histogram',
        nbinsx: 50,
        marker: { color: '#9467bd' }
    };
    
    const layout = {
        title: 'Duration Distribution',
        xaxis: { title: 'Duration (seconds)' },
        yaxis: { title: 'Frequency' },
        margin: { t: 40, b: 40, l: 60, r: 20 }
    };
    
    Plotly.newPlot('chartDurationDistribution', [trace], layout, { responsive: true });
}


// ============================================================
// Chart 6: Geo Map (Scatter Geo)
// ============================================================
function renderGeoMapChart() {
    const lats = [];
    const lons = [];
    const texts = [];
    
    currentData.forEach(record => {
        const lat = parseFloat(record.latitude);
        const lon = parseFloat(record.longitude);
        
        if (lat !== 0 && lon !== 0 && !isNaN(lat) && !isNaN(lon)) {
            lats.push(lat);
            lons.push(lon);
            texts.push(`${record.city}, ${record.state}<br>${record.datetime}`);
        }
    });
    
    const trace = {
        type: 'scattergeo',
        mode: 'markers',
        lon: lons,
        lat: lats,
        marker: {
            size: 5,
            color: '#d62728',
            opacity: 0.7,
            line: { width: 0 }
        },
        text: texts,
        hovertemplate: '%{text}<extra></extra>'
    };
    
    const layout = {
        title: 'UFO Sightings Map',
        geo: {
            scope: 'world',
            projection: { type: 'natural earth' },
            showland: true,
            landcolor: 'rgb(243, 243, 243)'
        },
        margin: { t: 40, b: 40, l: 60, r: 60 }
    };
    
    Plotly.newPlot('chartGeoMap', [trace], layout, { responsive: true });
}


// ============================================================
// Reset Filters
// ============================================================
function resetFilters() {
    document.getElementById('countryFilter').value = '';
    document.getElementById('stateFilter').value = '';
    document.getElementById('shapeFilter').value = '';
    document.getElementById('yearFrom').value = '1900';
    document.getElementById('yearTo').value = '2100';
    document.getElementById('durationMin').value = '0';
    document.getElementById('durationMax').value = '999999';
    
    applyFilters();
}


// ============================================================
// Export to CSV
// ============================================================
function exportToCSV() {
    console.log("Exporting to CSV...");
    
    const filters = getFilters();
    
    fetch('/export/csv', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(filters)
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `ufo_sightings_${new Date().toISOString().slice(0, 10)}.csv`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Error exporting data');
    });
}


// ============================================================
// Utility Functions
// ============================================================

/**
 * Extract year from datetime string
 * Format: "10/10/1949 20:30"
 */
function extractYear(datetimeStr) {
    try {
        if (!datetimeStr) return null;
        const parts = datetimeStr.split(' ')[0].split('/');
        return parseInt(parts[2]);
    } catch (e) {
        return null;
    }
}


/**
 * Extract month from datetime string
 * Format: "10/10/1949 20:30"
 */
function extractMonth(datetimeStr) {
    try {
        if (!datetimeStr) return null;
        const parts = datetimeStr.split(' ')[0].split('/');
        return parseInt(parts[0]);
    } catch (e) {
        return null;
    }
}


/**
 * Show/hide loading indicator
 */
function showLoadingIndicator(show) {
    const indicator = document.getElementById('loadingIndicator');
    if (show) {
        indicator.classList.remove('hidden');
    } else {
        indicator.classList.add('hidden');
    }
}
