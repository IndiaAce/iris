import sqlite3
from database import add_mapping

# Function to map a PIR to a source
def map_pir_to_source(pir_id, source_id):
    try:
        add_mapping(pir_id, source_id)
        print(f"Successfully mapped PIR ID {pir_id} to Source ID {source_id}.")
    except sqlite3.Error as e:
        print(f"An error occurred while mapping PIR to Source: {e}")

# Function to identify PIRs without sufficient mapped sources (intelligence gaps)
def identify_unmet_pirs():
    connection = sqlite3.connect(r'C:\\Users\\lukew\\OneDrive\\Documents\\dev_link\\Threat\\iris\\intelligence.db')
    cursor = connection.cursor()
    
    # Fetch all PIRs
    cursor.execute("SELECT id FROM PIRs")
    all_pirs = set(row[0] for row in cursor.fetchall())
    
    # Fetch all PIRs that have at least one mapping
    cursor.execute("SELECT DISTINCT pir_id FROM Mappings")
    mapped_pirs = set(row[0] for row in cursor.fetchall())
    
    # Find unmet PIRs (those without any mapped sources)
    unmet_pirs = all_pirs - mapped_pirs
    
    # Update status of unmet PIRs to 'Unmet'
    for pir_id in unmet_pirs:
        cursor.execute("UPDATE PIRs SET status = ? WHERE id = ?", ("Unmet", pir_id))
    
    connection.commit()
    connection.close()
    
    print(f"Identified {len(unmet_pirs)} unmet PIR(s). Updated their status to 'Unmet'.")

if __name__ == "__main__":
    # Example usage of mapping a PIR to a source
    map_pir_to_source(1, 2)
    
    # Example usage of identifying unmet PIRs
    identify_unmet_pirs()
