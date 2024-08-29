import socketserver
import json
from kafka import KafkaProducer, KafkaConsumer
from kafka.admin import NewTopic, KafkaAdminClient
from datetime import datetime
from os.path import exists

class WuerfelServer(socketserver.BaseRequestHandler): 
    def handle(self): 
        addr = self.client_address[0] 
        print("[{}] Verbindung hergestellt".format(addr))
        # allparts is used to avoid incomplete json line
        allparts = ""
        while True: 
            # allparts (ideally empty) will be concatenated with next line
            # decode wandelt byte-Strom zu String
            received = allparts+self.request.recv(4096).decode() 
            if received: 
                for allparts in received.splitlines():         # Datenpaket in Zeilen zerlegen

                    # if allparts ends in }, full data is received and is ready to send
                    if len(allparts) > 0 and allparts[-1] == '}':
                        jsondSend = json.loads(allparts)       # JSON-Zeile -> Dictionary
                        allparts = ""
                        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S:%f")[:-1]  # Get current timestamp
                        data = {"n": jsondSend["n"], "timestamp": timestamp, "ax": jsondSend["ax"], "ay": jsondSend["ay"], 
                                "az": jsondSend["az"], "gx": jsondSend["gx"], "gy": jsondSend["gy"], "gz": jsondSend["gz"]}
                        print(data)
                        
                        #savedata(data)
                        producer.send('swtp_team_b', value=data)  # Send data to Kafka
                    # else:
                    #    print(allparts)                        # Debug-Ausgabe
            else: 
                print("[{}] Verbindung geschlossen".format(addr))
                break

def savedata(rawdata):
    output_file = "sent_data.json"
    data = json.loads(open(output_file).read()) if exists(output_file) else []
    data.extend(rawdata if isinstance(rawdata, list) else [rawdata])
    # Write
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)
                           
if __name__ == '__main__':
    # dict to json
    encode = lambda x: json.dumps(x).encode("utf-8")
    #decode = lambda x: json.loads(x.decode('utf-8'))
    # connect to Kafka

    producer = KafkaProducer(bootstrap_servers="slo.swe.th-luebeck.de:9092", value_serializer=encode, acks=0, retries=3, linger_ms = 2, batch_size = 0)
    #producer = KafkaProducer(bootstrap_servers="10.42.0.1:9092", value_serializer=encode, acks=0, retries=3, linger_ms = 2, batch_size = 0)

    server = socketserver.ThreadingTCPServer(("", 5005), WuerfelServer) 
    server.serve_forever()
    
