# 1. Receive log information through MQTT.
#   1-1 Send a message to Azure if the string is parsed
#       to contain 'Error', 'Shutdown', 'inOperation', 'Idle' keywords.
#   1-2 Store the received log information locally.
# 2. Receive report information through MQTT.
#   2-1 Retrieve the last six sets of statistical data and upload them to Azure IoT Hub.
#   2-2 Store the received report information locally.
#   2-3 Upload report file to Azure Blob

import os
import json
from datetime import datetime
from dotenv import load_dotenv
import paho.mqtt.client as mqtt
from azure.storage.blob import BlobClient
from azure.iot.device import IoTHubDeviceClient

load_dotenv()
BLOB_CONNECTION_STRING = os.getenv("BLOB_CONNECTION_STRING")
BLOB_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME")
CONNECTION_STRING = os.getenv("IOT_HUB_DEVICE_CONNECTION_STRING")
device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)

print(f"CONNECTION_STRING: {CONNECTION_STRING}")

MQTT_SERVER = "127.0.0.1" 
MQTT_PORT = 1883  
MQTT_ALIVE = 60  
MQTT_TOPIC1 = "702L_Edge"
MQTT_TOPIC2 = "702L_Report"

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(MQTT_TOPIC1)
    client.subscribe(MQTT_TOPIC2)

def on_message(client, userdata, msg):
  print(f"Message Received from other topic: {msg.payload.decode()}") 

def on_message_TOPIC1(client, userdata, msg):
    # 1-1
    typeInfo = ""
    if json.loads(msg.payload)['message'].startswith('Error'):
        print("error")
        typeInfo = 'Error'
    elif json.loads(msg.payload)['message'].startswith('Shutdown'):
        typeInfo = 'Shutdown'
    elif json.loads(msg.payload)['message'].startswith('inOperation'):
        typeInfo = 'inOperation'
    elif json.loads(msg.payload)['message'].startswith('Idle'):
        typeInfo = 'Idle'
    if typeInfo: # typeInfo is not empty
        jsonToAzure = {
            'status': {
                'date': json.loads(msg.payload)['date'],
                'time': json.loads(msg.payload)['time'],
                'type': typeInfo,
                'message': json.loads(msg.payload)['message']
            }
        }
        print(f"jsonToAzure: {jsonToAzure}")
        device_client.send_message(json.dumps(jsonToAzure))
        typeInfo = ""

    # 1-2
    log_file_path = f"./Log/L{datetime.strftime(datetime.now(), '%Y%m%d')}.log"
    print(f"log file path: {log_file_path}")
    with open(log_file_path, "a") as log:
        log_string = f"{json.loads(msg.payload)['date']}\t{json.loads(msg.payload)['time']}\tact:\t{json.loads(msg.payload)['message']}"
        log.write(log_string + "\n")

def on_message_TOPIC2(client, userdata, msg):
    print(f"{msg.topic} - data: {json.loads(msg.payload)['report']}")
    # 2-1
    last_six_elements = json.loads(msg.payload)['report'][-6:]
    jsonToAzure = {
      'statistics': {
        'date': json.loads(msg.payload)['fileName'].split('-')[0],
        'time': json.loads(msg.payload)['fileName'].split('-')[1],
        'standardDeviation': last_six_elements[0][1],
        'average': last_six_elements[1][1],
        'uniformity': last_six_elements[2][1],
        'max': last_six_elements[3][1],
        'min': last_six_elements[4][1],
        'maxMin': last_six_elements[5][1],
        'fileName': json.loads(msg.payload)['fileName'],
      }
    }
    print(f"jsonToAzure: {jsonToAzure}")
    device_client.send_message(json.dumps(jsonToAzure))

    # 2-2
    with open(f"./Report/{json.loads(msg.payload)['fileName']}.csv", "a") as csv:
        for idx, info in enumerate(json.loads(msg.payload)['report']):
            csvString = f"{info[0]},{info[1]},{info[2]},{info[3]},{info[4]},{info[5]},{info[6]},{info[7]}"
            csv.write(csvString + "\n")
    
    # 2-3
    blob = BlobClient.from_connection_string(conn_str = BLOB_CONNECTION_STRING, container_name = BLOB_CONTAINER_NAME, blob_name = f"Report/{json.loads(msg.payload)['fileName']}.csv")
    with open(f"./Report/{json.loads(msg.payload)['fileName']}.csv", "rb") as data:
        try:
            blob_client = blob.upload_blob(data, overwrite=True)
            print(f"blob_client: {blob_client}")
        except Exception as ex:
            print(f"Exception: {ex}")

mqtt_client = mqtt.Client()
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
mqtt_client.message_callback_add(MQTT_TOPIC1, on_message_TOPIC1)
mqtt_client.message_callback_add(MQTT_TOPIC2, on_message_TOPIC2)
mqtt_client.connect(MQTT_SERVER, MQTT_PORT, MQTT_ALIVE)  
mqtt_client.loop_forever()
