import sqlite3

# Connect to the original SQLite database
source_conn = sqlite3.connect('TrainingDB.db')
source_cursor = source_conn.cursor()

# Define the intervals
intervals = {
    'gx': (-6.290076, -1.85420),
}

select_query = f"""
SELECT *,
    CASE
        WHEN gx BETWEEN {intervals['gx'][0]} AND {intervals['gx'][1]}
        THEN 0
        ELSE 1
    END AS zustand
FROM mockdata
"""

# Execute the select query
source_cursor.execute(select_query)
rows = source_cursor.fetchall()

# Get the column names from the original table
source_cursor.execute("PRAGMA table_info(mockdata)")
columns = [column[1] for column in source_cursor.fetchall()]
columns.append('zustand')

# Close the connection to the source database
source_cursor.close()
source_conn.close()

# Create a new database and connect to it
new_conn = sqlite3.connect('Training_Zustand.db')
new_cursor = new_conn.cursor()

# Create the new table with the "zustand" column
create_table_query = f"""
CREATE TABLE mockdata (
    {', '.join([f'{col} REAL' for col in columns])}
)
"""
new_cursor.execute(create_table_query)

# Insert the data into the new table
insert_query = f"INSERT INTO mockdata ({', '.join(columns)}) VALUES ({', '.join(['?' for _ in columns])})"
new_cursor.executemany(insert_query, rows)

# Commit the changes and close the connection
new_conn.commit()
new_cursor.close()
new_conn.close()
