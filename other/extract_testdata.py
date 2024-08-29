import sqlite3
import random

# Connect to the SQLite database
conn = sqlite3.connect('Cleaned_DB.db')
cursor = conn.cursor()

# Select 20% of normal data
cursor.execute("SELECT * FROM mockdata WHERE label = 'normal' ORDER BY RANDOM() LIMIT (SELECT ROUND(COUNT(*) * 0.2) FROM mockdata WHERE label = 'normal')")
normal_data = cursor.fetchall()

# Select 20% of anomaly data
cursor.execute("SELECT * FROM mockdata WHERE label = 'anomalie' ORDER BY RANDOM() LIMIT (SELECT ROUND(COUNT(*) * 0.2) FROM mockdata WHERE label = 'anomalie')")
anomaly_data = cursor.fetchall()

# Combine normal and anomaly data
combined_data = normal_data + anomaly_data

# Shuffle the combined data
random.shuffle(combined_data)

conn.close()

# Create a new database connection for the test data
conn_test = sqlite3.connect('Cleaned_Test_Data_20.db')
cursor_test = conn_test.cursor()

# Create a new table for test data
cursor_test.execute('''CREATE TABLE IF NOT EXISTS mockdata (
                        n INTEGER,
                        timestamp TEXT,
                        ax REAL,
                        ay REAL,
                        az REAL,
                        gx REAL,
                        gy REAL,
                        gz REAL,
                        label TEXT
                    )''')

# Insert test data into the new table
cursor_test.executemany("INSERT INTO mockdata VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", combined_data)

# Commit changes and close the connection
conn_test.commit()
conn_test.close()
