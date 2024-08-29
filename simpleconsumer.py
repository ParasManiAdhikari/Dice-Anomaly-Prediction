from kafka import KafkaConsumer
import json
decode = lambda x: json.loads(x.decode('utf-8'))
consumer = KafkaConsumer(bootstrap_servers="slo.swe.th-luebeck.de:9092", auto_offset_reset = "latest") #value_deserializer=decode)
consumer.subscribe(topics = ["swtp_team_b"])

def read_message(consumer):
    for message in consumer:
        print(message.value)

read_message(consumer)