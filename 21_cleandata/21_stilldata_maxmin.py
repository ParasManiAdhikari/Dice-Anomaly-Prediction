import sqlite3

database_path = 'still_3.db'
table_name = 'mockdata'

# SQL query to find the maximum and minimum values for each column
query = f"""
SELECT 
    MAX(ax) AS max_ax, MIN(ax) AS min_ax,
    MAX(ay) AS max_ay, MIN(ay) AS min_ay,
    MAX(az) AS max_az, MIN(az) AS min_az,
    MAX(gx) AS max_gx, MIN(gx) AS min_gx,
    MAX(gy) AS max_gy, MIN(gy) AS min_gy,
    MAX(gz) AS max_gz, MIN(gz) AS min_gz
FROM {table_name};
"""

# Connect to the SQLite database and execute the query
with sqlite3.connect(database_path) as conn:
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()

    # Print the results
    if result:
        print("STILL_3 Maximum and Minimum values:")
        print(f"ax: max = {result[0]}, min = {result[1]}")
        print(f"ay: max = {result[2]}, min = {result[3]}")
        print(f"az: max = {result[4]}, min = {result[5]}")
        print(f"gx: max = {result[6]}, min = {result[7]}")
        print(f"gy: max = {result[8]}, min = {result[9]}")
        print(f"gz: max = {result[10]}, min = {result[11]}")
    else:
        print("No data found in the table.")
