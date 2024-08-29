from flask import Flask, render_template, jsonify, request
from threading import Thread
import sqlite3
from kafka import KafkaConsumer
import json
import joblib
import numpy as np

Kafka_Consumer = Flask(__name__)

class DataProcessor:
    def __init__(self):
        self.connection = sqlite3.connect('dice_data.db', check_same_thread=False)
        self.create_table_if_not_exists()
        self.consumer = KafkaConsumer(bootstrap_servers="slo.swe.th-luebeck.de:9092", auto_offset_reset="latest")
        self.consumer.subscribe(topics=["swtp_team_b"])
        self.hundred_data = []
        self.model = joblib.load('rf_model.joblib')
        self.batchsize = 200
        self.consumer_thread = None

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
            else:
                print("Missing fields in data:", data)
        self.connection.commit()

    def read_message_and_insert(self):
        for message in self.consumer:
            try:
                data = json.loads(message.value.decode('utf-8'))
                if data['gx'] <= -6.290076 or data['gx'] >= -1.85420:
                    self.hundred_data.append(data)
                if len(self.hundred_data) >= self.batchsize:
                    self.insert_data_batch()
                    self.hundred_data = []
            except Exception as e:
                print("Error processing message:", e)

    def start_kafka_consumer(self):
        if self.consumer_thread is None or not self.consumer_thread.is_alive():
            self.consumer_thread = Thread(target=self.read_message_and_insert)
            self.consumer_thread.start()

    def preprocess_data(self, data):
        features = [data['ax'], data['ay'], data['az'], data['gx'], data['gy'], data['gz']]
        processed_data = np.array(features).reshape(1, -1)  
        return processed_data

    def perform_prediction(self):
        self.hundred_data = []                                                                        # Clear List

        while len(self.hundred_data) < self.batchsize:                                                # Wait untill List is full of 200 Data
            print(len(self.hundred_data))
            pass

        responses = []
        for data in self.hundred_data:                                                                 # Run Prediction on the List
            processed_data = self.preprocess_data(data)
            prediction = self.model.predict(processed_data)
            
            if prediction[0] == 1:
                label = 'NORMAL'
            else:
                label = 'ANOMALIE'
            responses.append(label)
        majority_label, count_normal, count_anomalie = self.determine_majority_label(responses)         # Count majority zustand
        return {"prediction": majority_label, "n_count": count_normal, "a_count": count_anomalie}
    
    def determine_majority_label(self, responses):
        count_normal = responses.count('NORMAL')
        count_anomalie = responses.count('ANOMALIE')
        majority_label = 'NORMAL' if count_normal > count_anomalie else 'ANOMALIE'
        return majority_label, count_normal, count_anomalie

processor = DataProcessor()

@Kafka_Consumer.route('/')
def index():
    return render_template('index.html')

@Kafka_Consumer.route('/start', methods=['POST'])
def start_prediction():
    processor.start_kafka_consumer()
    return jsonify(message="Prediction ongoing ...")

@Kafka_Consumer.route('/predict', methods=['GET'])
def predict_result():
    prediction_result = processor.perform_prediction()
    return jsonify(prediction_result)

def main():
    Kafka_Consumer.run(debug=True)

if __name__ == '__main__':
    main()