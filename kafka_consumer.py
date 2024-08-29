import sqlite3
from kafka import KafkaConsumer
import json

class DataProcessor:
    def __init__(self):
        self.connection = sqlite3.connect('dice_data.db')
        self.create_table_if_not_exists()
        self.consumer = KafkaConsumer(bootstrap_servers="slo.swe.th-luebeck.de:9092", auto_offset_reset="latest")
        self.consumer.subscribe(topics=["swtp_team_b"])
        self.hundred_data = []

    # Main Method
    def read_message_and_insert(self):
        for message in self.consumer:
            try:
                data = json.loads(message.value.decode('utf-8'))
                self.hundred_data.append(data)                          # Hold 100 data temporarily
                if len(self.hundred_data) >= 100:
                    self.insert_data_batch()                            # Add to database
                    #self.compare()                                      # Check Loss (Verlust)
                    self.hundred_data = []                              # Empty the temporary list to refill new data
            except Exception as e:
                print("Error processing message:", e)

    def create_table_if_not_exists(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS dice_data (
                            n INTEGER, timestamp TEXT PRIMARY KEY, ax REAL, ay REAL, az REAL, gx REAL, gy REAL, gz REAL
                        )''')
        self.connection.commit()

    def insert_data_batch(self):
        cursor = self.connection.cursor()
        for data in self.hundred_data:
            required_fields = ['n', 'timestamp', 'ax', 'ay', 'az', 'gx', 'gy', 'gz']
            if all(field in data for field in required_fields):
                cursor.execute('''INSERT INTO dice_data (n, timestamp, ax, ay, az, gx, gy, gz)
                                  VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                                  (data['n'], data['timestamp'], data['ax'], data['ay'], data['az'], data['gx'], data['gy'], data['gz']))
                print("+")
            else:
                print("-")
        self.connection.commit()

    def compare(self):
        count = 0
        print("Compare Start !")
        
        for list_data in self.hundred_data:
            
            # Get data from database
            cursor = self.connection.cursor()
            cursor.execute('SELECT * FROM dice_data WHERE timestamp = ?', (list_data['timestamp'],))
            columns = ['n', 'timestamp', 'ax', 'ay', 'az', 'gx', 'gy', 'gz']
            db_data = cursor.fetchone()                     # Tuple
            db_data_dict = dict(zip(columns, db_data))      # Dict

            # Compare
            if db_data:
                if list_data == db_data_dict:
                    count += 1
                else:
                    print("different")
        print("Identical : ", count)

# Instantiate DataProcessor
processor = DataProcessor()

# Start reading and inserting data
processor.read_message_and_insert()
