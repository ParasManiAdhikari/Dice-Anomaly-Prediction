import sqlite3
from kafka import KafkaConsumer
import json
from datetime import datetime, timedelta
from queue import Queue
from threading import Thread

# Set time start
start = '17-05-2024 15:53:00:000000'

normal_start = datetime.strptime(start, "%d-%m-%Y %H:%M:%S:%f")
anomalie_start = normal_start + timedelta(minutes=1)
end = normal_start + timedelta(minutes=2)

def create_mock_db_ifnotexists(connection):
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS mockdata (
                        n INTEGER PRIMARY KEY, timestamp TEXT, ax REAL, ay REAL, az REAL, gx REAL, gy REAL, gz REAL, label TEXT
                    )''')
    connection.commit()

# Kafka consumer configuration
consumer = KafkaConsumer(bootstrap_servers="slo.swe.th-luebeck.de:9092", auto_offset_reset="latest")
consumer.subscribe(topics=["swtp_team_b"])

# Database
connection = sqlite3.connect('beta.db')
create_mock_db_ifnotexists(connection)

# Queue for buffering messages
message_queue = Queue()

# Batch size for database inserts
BATCH_SIZE = 100

def read_message_and_insert(consumer, queue):
    for message in consumer:
        try:
            data = json.loads(message.value.decode('utf-8'))
            queue.put(data)
        except Exception as e:
            print("Error processing message:", e)

def insert_mockdata_batch(queue, connection):
    while True:
        batch = []
        while len(batch) < BATCH_SIZE:
            data = queue.get()
            if data is None:  # Stop signal
                break
            timestamp = datetime.strptime(data['timestamp'], "%d-%m-%Y %H:%M:%S:%f")
            print(timestamp)
            print("adding") if normal_start < timestamp < end else print(".")
            if normal_start < timestamp < anomalie_start:
                data['label'] = 'normal'
            else:
                data['label'] = 'anomalie'
            if normal_start < timestamp < end:
                batch.append((data['n'], data['timestamp'], data['ax'], data['ay'], data['az'], data['gx'], data['gy'], data['gz'], data['label']))
        
        if batch:
            cursor = connection.cursor()
            cursor.executemany('''INSERT INTO mockdata (n, timestamp, ax, ay, az, gx, gy, gz, label)
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', batch)
            connection.commit()

# Start the Kafka consumer thread
consumer_thread = Thread(target=read_message_and_insert, args=(consumer, message_queue))
consumer_thread.start()

# Start the database insertion thread
insertion_thread = Thread(target=insert_mockdata_batch, args=(message_queue, connection))
insertion_thread.start()

# To gracefully shutdown, you would signal the threads to stop by adding a None to the queue
# message_queue.put(None)
# consumer_thread.join()
# insertion_thread.join()
