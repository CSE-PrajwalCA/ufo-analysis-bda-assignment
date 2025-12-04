"""
UFO Dashboard - Export Utilities
Handles CSV and PDF export of filtered data
"""

import csv
import io
from datetime import datetime
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def export_csv(data):
    """
    Converts list of documents to CSV bytes
    
    Args:
        data: List of dictionaries containing UFO sighting records
    
    Returns:
        Bytes object of CSV data
    """
    try:
        if not data:
            return b"No data to export"
        
        # CSV field order
        fieldnames = [
            'datetime',
            'city',
            'state',
            'country',
            'shape',
            'duration (seconds)',
            'duration (hours/min)',
            'comments',
            'date posted',
            'latitude',
            'longitude'
        ]
        
        # Create string buffer
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames)
        
        # Write header
        writer.writeheader()
        
        # Write rows
        for record in data:
            # Ensure all fields exist in record
            row = {}
            for field in fieldnames:
                row[field] = record.get(field, '')
            writer.writerow(row)
        
        # Convert to bytes
        csv_string = output.getvalue()
        return csv_string.encode('utf-8')
    
    except Exception as e:
        print(f"Error exporting CSV: {e}")
        return b"Error exporting data"


def export_pdf(data):
    """
    Converts list of documents to PDF
    Creates a simple table-based PDF
    
    Args:
        data: List of dictionaries containing UFO sighting records
    
    Returns:
        Bytes object of PDF data
    """
    try:
        if not data:
            return b"No data to export"
        
        # Limit to first 100 records for PDF (too many = huge file)
        data = data[:100]
        
        # Create PDF buffer
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=landscape(letter),
            topMargin=0.5*72,
            bottomMargin=0.5*72,
            leftMargin=0.5*72,
            rightMargin=0.5*72
        )
        
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph(
            f"UFO Sightings Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            styles['Heading1']
        )
        elements.append(title)
        elements.append(Spacer(1, 0.3*72))
        
        # Prepare table data
        table_data = [
            ['DateTime', 'City', 'State', 'Country', 'Shape', 'Duration', 'Comments']
        ]
        
        for record in data:
            row = [
                str(record.get('datetime', ''))[:15],
                str(record.get('city', ''))[:15],
                str(record.get('state', ''))[:5],
                str(record.get('country', ''))[:3],
                str(record.get('shape', ''))[:10],
                str(record.get('duration (hours/min)', ''))[:12],
                str(record.get('comments', ''))[:30]
            ]
            table_data.append(row)
        
        # Create table
        table = Table(table_data, colWidths=[1.2*72, 1*72, 0.7*72, 0.7*72, 0.9*72, 1*72, 2*72])
        
        # Style table
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey])
        ]))
        
        elements.append(table)
        
        # Build PDF
        doc.build(elements)
        
        return pdf_buffer.getvalue()
    
    except Exception as e:
        print(f"Error exporting PDF: {e}")
        return b"Error exporting PDF"


def get_export_filename(file_type='csv'):
    """
    Generates a unique filename for exports
    
    Args:
        file_type: 'csv' or 'pdf'
    
    Returns:
        String filename
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"ufo_sightings_{timestamp}.{file_type}"
