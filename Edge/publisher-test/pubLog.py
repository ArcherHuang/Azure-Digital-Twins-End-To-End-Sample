import paho.mqtt.client as mqtt  
import json
import random

MQTT_SERVER = "127.0.0.1" 
MQTT_PORT = 1883  
MQTT_ALIVE = 60  
MQTT_TOPIC = "702L_Edge"

mqtt_client = mqtt.Client()  
mqtt_client.connect(MQTT_SERVER, MQTT_PORT, MQTT_ALIVE)    

def publish():
  # Shutdown:
  # payload = { 
  #   'date': '2023/03/13',
  #   'time': '11:17:01',
  #   'message': 'Shutdown:',
  # }
  # Idle
  # payload = { 
  #   'date': '2023/03/13',
  #   'time': '11:20:01',
  #   'message': 'Idle:',
  # }
  # inOperation
  # payload = { 
  #   'date': '2023/03/13',
  #   'time': '11:17:01',
  #   'message': 'inOperation:',
  # }
  # Error
  # payload = { 
  #   'date': '2023/03/13',
  #   'time': '11:17:01',
  #   'message': 'Error: OpenSensor()',
  # }
  # print(f"payload: {payload}")
  # mqtt_client.publish(MQTT_TOPIC, json.dumps(payload), qos=1)
  # mqtt_client.loop(2,10)

  with open('../Datas/L20230218.log') as f:
    lines = f.readlines()
    # print(f"lines: {lines}")
    for idx, content in enumerate(lines):
      # print(f"content: {content}")
      description = list(content.strip().split(None, 3))
      # print(f"\n#1: {description[0]}")
      # print(f"#2: {description[1]}")
      # print(f"#4: {description[3]}")
      payload = { 
        'date': description[0],
        'time': description[1],
        'message': description[3],
      }
      mqtt_client.publish(MQTT_TOPIC, json.dumps(payload), qos=1)
      mqtt_client.loop(2,10)
    f.close()

publish()