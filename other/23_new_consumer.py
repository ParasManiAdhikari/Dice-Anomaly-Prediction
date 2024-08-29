from flask import Flask, render_template, jsonify, request
from threading import Thread
import sqlite3
from kafka import KafkaConsumer
import json
import numpy as np
from tensorflow.keras.models import load_model

Kafka_Consumer = Flask(__name__)

class DataProcessor:
    def __init__(self):
        self.connection = sqlite3.connect('dice_data.db', check_same_thread=False)
        self.create_table_if_not_exists()
        self.consumer = KafkaConsumer(bootstrap_servers="slo.swe.th-luebeck.de:9092", auto_offset_reset="latest")
        self.consumer.subscribe(topics=["swtp_team_b"])
        self.hundred_data = []
        self.model = load_model('Sequential.h5')
        self.last_message = None
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
                self.hundred_data.append(data)
                self.last_message = data  # Store the last received message for prediction
                if len(self.hundred_data) >= 100:
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
        if self.last_message:
            processed_data = self.preprocess_data(self.last_message)
            prediction = self.model.predict(processed_data)
            label = self.interpret_prediction(prediction)
            print({"data": processed_data, "prediction": label})
            return label
        return {"error": "No data available for prediction"}

    def interpret_prediction(self, prediction):
        # probabilities for two classes: [probability_normal, probability_anomalie]
        class_labels = ['normal', 'anomalie']
        predicted_class = class_labels[np.argmax(prediction)]
        return {"prediction": predicted_class, "probabilities": prediction.tolist()}

processor = DataProcessor()

@Kafka_Consumer.route('/')
def index():
    return render_template('index.html')

@Kafka_Consumer.route('/start', methods=['POST'])
def start_prediction():
    processor.start_kafka_consumer()
    return jsonify(message="Prediction started")

@Kafka_Consumer.route('/predict', methods=['GET'])
def predict_result():
    prediction_result = processor.perform_prediction()
    return jsonify(prediction_result)

def main():
    Kafka_Consumer.run(debug=True)

if __name__ == '__main__':
    main()
