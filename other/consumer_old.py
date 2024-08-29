import sqlite3
from kafka import KafkaConsumer
import json

# CREATE TABLE IF NOT EXISTS
def create_table_if_not_exists(connection):
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS dice_data (
                        n INTEGER PRIMARY KEY, timestamp TEXT, ax REAL, ay REAL, az REAL, gx REAL, gy REAL, gz REAL
                    )''')
    connection.commit()

# INSERT DATA
def insert_data(connection, data):
    required_fields = ['n', 'timestamp', 'ax', 'ay', 'az', 'gx', 'gy', 'gz']
    if all(field in data for field in required_fields):
        cursor = connection.cursor()
        cursor.execute('''INSERT INTO dice_data (n, timestamp, ax, ay, az, gx, gy, gz)
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                          (data['n'], data['timestamp'], data['ax'], data['ay'], data['az'], data['gx'], data['gy'], data['gz']))
        connection.commit()
        #print("Data into dice_data inserted")
    else:
        print("Skipping insertion.")

# Kafka consumer configuration
consumer = KafkaConsumer(bootstrap_servers="slo.swe.th-luebeck.de:9092", auto_offset_reset="latest")
consumer.subscribe(topics=["swtp_team_b"])

# Database
connection = sqlite3.connect('dice_data.db')
create_table_if_not_exists(connection)

# 1
def read_message_and_insert(consumer):
    for message in consumer:
        try:
            data = json.loads(message.value.decode('utf-8'))
            print(data)
            insert_data(connection, data)
        except Exception as e:
            print("Error processing message:", e)

# Entry
read_message_and_insert(consumer)
