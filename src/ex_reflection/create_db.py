import sqlite3
import csv

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('../instance/recycling_data.db')
cursor = conn.cursor()

# Create tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS Area (
    id INTEGER PRIMARY KEY,
    code TEXT UNIQUE,
    name TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS RecyclingRate (
    id INTEGER PRIMARY KEY,
    area_id INTEGER,
    year TEXT,
    rate INTEGER,
    FOREIGN KEY (area_id) REFERENCES Area(id)
)
''')

# Read the CSV file and insert data into the tables
with open('Household-rcycling-borough.csv', 'r') as file:
    reader = csv.DictReader(file)
    area_cache = {}

    for row in reader:
        code = row['Code']
        name = row['Area']
        year = row['Year']
        rate = row['Recycling_Rates']

        # Insert into Area table if not already present
        if code not in area_cache:
            cursor.execute('''
            INSERT OR IGNORE INTO Area (code, name) VALUES (?, ?)
            ''', (code, name))
            area_cache[code] = cursor.lastrowid

        # Get the area_id
        cursor.execute('SELECT id FROM Area WHERE code = ?', (code,))
        area_id = cursor.fetchone()[0]

        # Insert into RecyclingRate table
        cursor.execute('''
        INSERT INTO RecyclingRate (area_id, year, rate) VALUES (?, ?, ?)
        ''', (area_id, year, rate))

# Commit the transaction and close the connection
conn.commit()
conn.close()