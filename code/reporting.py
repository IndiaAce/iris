import sqlite3
import csv
from reportlab.pdfgen import canvas
from reportlab.lib import pagesizes

# Function to export PIR data to CSV
def export_pir_to_csv(csv_filename):
    connection = sqlite3.connect('intelligence.db')
    cursor = connection.cursor()
    
    cursor.execute('''
        SELECT p.id, p.description, p.priority_level, p.status, 
               GROUP_CONCAT(s.name, ', ') as mapped_sources
        FROM PIRs p
        LEFT JOIN Mappings m ON p.id = m.pir_id
        LEFT JOIN Sources s ON m.source_id = s.source_id
        GROUP BY p.id
    ''')
    rows = cursor.fetchall()
    
    with open(csv_filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['PIR ID', 'Description', 'Priority', 'Mapped Sources', 'Status'])
        csv_writer.writerows(rows)
    
    connection.close()
    print(f"PIR data successfully exported to {csv_filename}")

# Function to generate PDF report summarizing PIRs
def generate_pir_pdf_report(pdf_filename):
    connection = sqlite3.connect('intelligence.db')
    cursor = connection.cursor()
    
    # Fetch all PIRs and their mapping information
    cursor.execute('''
        SELECT p.id, p.description, p.priority_level, p.status, 
               GROUP_CONCAT(s.name, ', ') as mapped_sources
        FROM PIRs p
        LEFT JOIN Mappings m ON p.id = m.pir_id
        LEFT JOIN Sources s ON m.source_id = s.source_id
        GROUP BY p.id
    ''')
    all_pirs = cursor.fetchall()
    
    # Create PDF
    c = canvas.Canvas(pdf_filename, pagesize=pagesizes.letter)
    width, height = pagesizes.letter
    c.setFont('Helvetica', 12)
    c.drawString(30, height - 30, 'PIR Summary Report')
    c.setFont('Helvetica', 10)
    y = height - 50
    
    # Add PIR summary
    for pir in all_pirs:
        pir_id, description, priority, status, mapped_sources = pir
        c.drawString(30, y, f"PIR ID: {pir_id}")
        y -= 15
        c.drawString(30, y, f"Description: {description}")
        y -= 15
        c.drawString(30, y, f"Priority: {priority}")
        y -= 15
        c.drawString(30, y, f"Status: {status}")
        y -= 15
        c.drawString(30, y, f"Mapped Sources: {mapped_sources or 'None'}")
        y -= 30
        if y < 50:
            c.showPage()
            y = height - 50
    
    # Fetch unmet PIRs
    cursor.execute('''
        SELECT id, description, priority_level, status
        FROM PIRs
        WHERE status = 'Unmet'
    ''')
    unmet_pirs = cursor.fetchall()
    
    # Add unmet PIRs section
    c.setFont('Helvetica', 12)
    c.drawString(30, y, 'Unmet PIRs')
    c.setFont('Helvetica', 10)
    y -= 20
    for pir in unmet_pirs:
        pir_id, description, priority, status = pir
        c.drawString(30, y, f"PIR ID: {pir_id}")
        y -= 15
        c.drawString(30, y, f"Description: {description}")
        y -= 15
        c.drawString(30, y, f"Priority: {priority}")
        y -= 15
        c.drawString(30, y, f"Status: {status}")
        y -= 30
        if y < 50:
            c.showPage()
            y = height - 50
    
    connection.close()
    c.save()
    print(f"PIR PDF report successfully generated as {pdf_filename}")

if __name__ == "__main__":
    # Example usage
    export_pir_to_csv('pir_data.csv')
    generate_pir_pdf_report('pir_summary_report.pdf')
