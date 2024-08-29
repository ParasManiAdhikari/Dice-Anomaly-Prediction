import sqlite3
from kafka import KafkaConsumer
import json

class DataProcessor:
    def __init__(self):
        self.connection = sqlite3.connect('dice_data.db')
        self.create_table_if_not_exists()
        self.consumer = KafkaConsumer(bootstrap_servers="slo.swe.th-luebeck.de:9092", auto_offset_reset="earliest")
        self.consumer.subscribe(topics=["swtp_team_b"])
        self.temp_data_list = []

    # Main Method
    def read_message_and_insert(self):
        for message in self.consumer:
            try:
                data = json.loads(message.value.decode('utf-8'))
                self.insert_data(data)
                self.verlust_check(data)
            except Exception as e:
                print("Error processing message:", e)

    def verlust_check(self, data):
        self.temp_data_list.append(data)
        if len(self.temp_data_list) >= 100:
            self.compare()
            self.temp_data_list = []

    def create_table_if_not_exists(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS dice_data (
                            n INTEGER PRIMARY KEY, timestamp TEXT, ax REAL, ay REAL, az REAL, gx REAL, gy REAL, gz REAL
                        )''')
        self.connection.commit()

    def insert_data(self, data):
        required_fields = ['n', 'timestamp', 'ax', 'ay', 'az', 'gx', 'gy', 'gz']
        if all(field in data for field in required_fields):
            cursor = self.connection.cursor()
            cursor.execute('''INSERT INTO dice_data (n, timestamp, ax, ay, az, gx, gy, gz)
                              VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                              (data['n'], data['timestamp'], data['ax'], data['ay'], data['az'], data['gx'], data['gy'], data['gz']))
            self.connection.commit()
            print("+")
        else:
            print("-")

    def compare(self):
        print("Compare Start !")
        
        # Create a list of timestamps from self.temp_data_list
        timestamps = [data['timestamp'] for data in self.temp_data_list]
        
        # Get data from database for all timestamps in one query
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM dice_data WHERE timestamp IN ({})'.format(','.join(['?']*len(timestamps))), timestamps)
        rows = cursor.fetchall()  # List of tuples
        
        # Create a dictionary to map timestamps to database rows
        db_data_dict = {row['timestamp']: row for row in rows}
        
        # Compare
        for count, list_data in enumerate(self.temp_data_list, start=1):
            db_data = db_data_dict.get(list_data['timestamp'])
            if db_data:
                if list_data == db_data:
                    print("identical", count)
                else:
                    print("different", count)
            else:
                print(f"No data found for timestamp: {list_data['timestamp']}")


# Instantiate DataProcessor
processor = DataProcessor()

# Start reading and inserting messages
processor.read_message_and_insert()