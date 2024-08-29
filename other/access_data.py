import sqlite3
import pandas as pd
import json
from os.path import exists

def export_data_to_json(db_path, output_file, start_time, end_time, result):
    # Connecting to database
    conn = sqlite3.connect(db_path)
    
    # SQL Query with timestamp as range
    query = f"""
    SELECT *, '{result}' AS result, ROW_NUMBER() OVER (ORDER BY timestamp) AS time_tick
    FROM dice_data
    WHERE timestamp BETWEEN '{start_time}' AND '{end_time}'
    """
    
    # Loading data to dataframe
    df = pd.read_sql_query(query, conn)
    
    # Close db connection
    conn.close()
    
    # Prepare new data as JSON
    new_data = df.to_json(orient='records', date_format='iso')

    # Check if the file exists whether to append or create new
    if exists(output_file):
        # Read existing data
        with open(output_file, 'r') as file:
            data = json.load(file)
        # Append new Data
        data.extend(json.loads(new_data))
    else:
        data = json.loads(new_data)

    # Write updated data back to JSON file
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)
    
    print(f"Data appended to {output_file} successfully.")

# Datas
db_path = 'dice_data.db'
output_file = 'filtered_data.json'
start_time = '16-04-2024 14:06:00'
end_time = '16-04-2024 14:07:00'
result = 1  # Dice roll
export_data_to_json(db_path, output_file, start_time, end_time, result)
