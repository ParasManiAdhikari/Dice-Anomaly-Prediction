import sqlite3
from kafka import KafkaConsumer
import json
from datetime import datetime, timedelta

# Set time start
start = '10-06-2024 20:43:00:000000'

normal_start = datetime.strptime(start, "%d-%m-%Y %H:%M:%S:%f")
anomalie_start = normal_start + timedelta(minutes=5)
end = normal_start + timedelta(minutes=5)

def create_mock_db_ifnotexists(connection):
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS mockdata (
                        n INTEGER, timestamp TEXT PRIMARY KEY, ax REAL, ay REAL, az REAL, gx REAL, gy REAL, gz REAL, label TEXT
                    )''')
    connection.commit()

# Kafka consumer configuration
consumer = KafkaConsumer(bootstrap_servers="slo.swe.th-luebeck.de:9092", auto_offset_reset="latest")
consumer.subscribe(topics=["swtp_team_b"])
# Database
connection = sqlite3.connect('Training.db')
create_mock_db_ifnotexists(connection)


# 1
def read_message_and_insert(consumer):
    for message in consumer:
        try:
            data = json.loads(message.value.decode('utf-8'))
            insert_mockdata(data)
        except Exception as e:
            print("Error processing message:", e)

# Sashi Issue 8
def insert_mockdata(data):
    timestamp = datetime.strptime(data['timestamp'], "%d-%m-%Y %H:%M:%S:%f")
    print("adding") if normal_start < timestamp < end else print(".")
    if normal_start < timestamp < anomalie_start:
        data['label'] = 'anomalie'
    else:
        data['label'] = 'anomalie'
    if normal_start < timestamp < end:
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO mockdata (n, timestamp, ax, ay, az, gx, gy, gz, label)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                          (data['n'], data['timestamp'], data['ax'], data['ay'], data['az'], data['gx'], data['gy'], data['gz'], data['label']))
        connection.commit()

# Entry
read_message_and_insert(consumer)
