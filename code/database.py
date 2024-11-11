import sqlite3

# Function to create database and tables
def setup_database():
    connection = sqlite3.connect(r'C:\\Users\\lukew\\OneDrive\\Documents\\dev_link\\Threat\\iris\\intelligence.db')
    cursor = connection.cursor()

    # Create PIRs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PIRs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            priority_level TEXT NOT NULL,
            date_added TEXT NOT NULL,
            status TEXT NOT NULL,
            intelligence_gaps TEXT
        )
    ''')

    # Create Sources table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Sources (
            source_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            relevance TEXT NOT NULL
        )
    ''')

    # Create Mappings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Mappings (
            mapping_id INTEGER PRIMARY KEY AUTOINCREMENT,
            pir_id INTEGER NOT NULL,
            source_id INTEGER NOT NULL,
            FOREIGN KEY (pir_id) REFERENCES PIRs (id),
            FOREIGN KEY (source_id) REFERENCES Sources (source_id)
        )
    ''')

    connection.commit()
    connection.close()

# CRUD functions for PIRs table
def add_pir(description, priority_level, date_added, status, intelligence_gaps):
    connection = sqlite3.connect(r'C:\\Users\\lukew\\OneDrive\\Documents\\dev_link\\Threat\\iris\\intelligence.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO PIRs (description, priority_level, date_added, status, intelligence_gaps)
        VALUES (?, ?, ?, ?, ?)
    ''', (description, priority_level, date_added, status, intelligence_gaps))
    connection.commit()
    connection.close()

def update_pir(pir_id, description=None, priority_level=None, status=None, intelligence_gaps=None):
    connection = sqlite3.connect(r'C:\\Users\\lukew\\OneDrive\\Documents\\dev_link\\Threat\\iris\\intelligence.db')

    cursor = connection.cursor()
    query = 'UPDATE PIRs SET '
    params = []
    if description:
        query += 'description = ?, '
        params.append(description)
    if priority_level:
        query += 'priority_level = ?, '
        params.append(priority_level)
    if status:
        query += 'status = ?, '
        params.append(status)
    if intelligence_gaps:
        query += 'intelligence_gaps = ?, '
        params.append(intelligence_gaps)
    query = query.rstrip(', ')
    query += ' WHERE id = ?'
    params.append(pir_id)
    cursor.execute(query, tuple(params))
    connection.commit()
    connection.close()

def delete_pir(pir_id):
    connection = sqlite3.connect(r'C:\\Users\\lukew\\OneDrive\\Documents\\dev_link\\Threat\\iris\\intelligence.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM PIRs WHERE id = ?', (pir_id,))
    connection.commit()
    connection.close()

# CRUD functions for Sources table
def add_source(name, type, relevance):
    connection = sqlite3.connect(r'C:\\Users\\lukew\\OneDrive\\Documents\\dev_link\\Threat\\iris\\intelligence.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO Sources (name, type, relevance)
        VALUES (?, ?, ?)
    ''', (name, type, relevance))
    connection.commit()
    connection.close()

def update_source(source_id, name=None, type=None, relevance=None):
    connection = sqlite3.connect(r'C:\\Users\\lukew\\OneDrive\\Documents\\dev_link\\Threat\\iris\\intelligence.db')
    cursor = connection.cursor()
    query = 'UPDATE Sources SET '
    params = []
    if name:
        query += 'name = ?, '
        params.append(name)
    if type:
        query += 'type = ?, '
        params.append(type)
    if relevance:
        query += 'relevance = ?, '
        params.append(relevance)
    query = query.rstrip(', ')
    query += ' WHERE source_id = ?'
    params.append(source_id)
    cursor.execute(query, tuple(params))
    connection.commit()
    connection.close()

def delete_source(source_id):
    connection = sqlite3.connect(r'C:\\Users\\lukew\\OneDrive\\Documents\\dev_link\\Threat\\iris\\intelligence.db')
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Sources WHERE source_id = ?', (source_id,))
    connection.commit()
    connection.close()

# CRUD functions for Mappings table
def add_mapping(pir_id, source_id):
    connection = sqlite3.connect(r'C:\\Users\\lukew\\OneDrive\\Documents\\dev_link\\Threat\\iris\\intelligence.db')
    cursor = connection.cursor()
    cursor.execute('''
        INSERT INTO Mappings (pir_id, source_id)
        VALUES (?, ?)
    ''', (pir_id, source_id))
    connection.commit()
    connection.close()

def delete_mapping(mapping_id):
    connection = sqlite3.connect(r'C:\\Users\\lukew\\OneDrive\\Documents\\dev_link\\Threat\\iris\\intelligence.db') 
    cursor = connection.cursor()
    cursor.execute('DELETE FROM Mappings WHERE mapping_id = ?', (mapping_id,))
    connection.commit()
    connection.close()

if __name__ == '__main__':
    setup_database()
    print("Database setup completed successfully.")
