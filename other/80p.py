import sqlite3

# Connect to both databases
conn_db1 = sqlite3.connect('Cleaned_DB.db')
conn_db2 = sqlite3.connect('Cleaned_Test_Data_20.db')

# Assuming the table name is the same in both databases
table_name = 'mockdata'
matching_column = 'timestamp'  # Replace with your actual unique identifier column

# Create a cursor object for each database
cursor_db1 = conn_db1.cursor()
cursor_db2 = conn_db2.cursor()

# Fetch all rows from db2.db to delete from db1.db
cursor_db2.execute(f'SELECT {matching_column} FROM {table_name}')
rows_to_delete = cursor_db2.fetchall()

# Delete rows from db1.db where the matching column value exists in db2.db
for row in rows_to_delete:
    cursor_db1.execute(f'DELETE FROM {table_name} WHERE {matching_column} = ?', (row[0],))

# Commit the changes and close connections
conn_db1.commit()
conn_db1.close()
conn_db2.close()

print("Deletion completed successfully.")
