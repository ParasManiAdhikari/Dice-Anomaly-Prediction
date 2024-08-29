import sqlite3

# Connect to the original SQLite database
source_conn = sqlite3.connect('TrainingDB.db')
source_cursor = source_conn.cursor()

# Define the intervals
intervals = {
    'gx': (-6.290076, -1.85420),
}

# Formulate the SELECT query to get the filtered data
select_query = f"""
SELECT * FROM mockdata
WHERE NOT (
    (gx BETWEEN {intervals['gx'][0]} AND {intervals['gx'][1]})
)
"""

# Execute the SELECT query
source_cursor.execute(select_query)
filtered_data = source_cursor.fetchall()

# Connect to the new SQLite database
destination_conn = sqlite3.connect('Cleaned_DB.db')
destination_cursor = destination_conn.cursor()

# Create the new table
create_table_query = """
CREATE TABLE mockdata (
    n INTEGER,
    timestamp TEXT PRIMARY KEY,
    ax REAL,
    ay REAL,
    az REAL,
    gx REAL,
    gy REAL,
    gz REAL,
    label TEXT
)
"""
destination_cursor.execute(create_table_query)

# Insert the filtered data into the new table
insert_query = """
INSERT INTO mockdata (n, timestamp, ax, ay, az, gx, gy, gz, label)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
"""
destination_cursor.executemany(insert_query, filtered_data)

# Commit the changes and close the connections
destination_conn.commit()
source_conn.close()
destination_conn.close()

