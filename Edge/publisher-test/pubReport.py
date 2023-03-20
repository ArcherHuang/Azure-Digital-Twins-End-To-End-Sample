import paho.mqtt.client as mqtt  
import os
import json
import random
import pandas as pd
import datetime

EXCEL_NAME = "20230313-140020.xlsx"
MQTT_SERVER = "127.0.0.1" 
MQTT_PORT = 1883  
MQTT_ALIVE = 60  
MQTT_TOPIC = "702L_Report"

mqtt_client = mqtt.Client()  
mqtt_client.connect(MQTT_SERVER, MQTT_PORT, MQTT_ALIVE)    

def publish():
  if os.path.exists(f"../Excel/{EXCEL_NAME}"):
    print(f"檔案 {EXCEL_NAME} 存在。")
    created_timestamp = os.path.getctime(f"../Excel/{EXCEL_NAME}")
    created_datetime = datetime.datetime.fromtimestamp(created_timestamp).strftime("%Y-%m-%d %H:%M:%S")
    print(f"created_timestamp: {created_timestamp}")
    print(f"檔案 ../Excel/{EXCEL_NAME} 建立時間：{created_datetime}")
    data_time = created_datetime.split(' ')
    print(f"data_time: {data_time}")
    replace_date = data_time[0].replace("-", "/")
    print(f"replace_date: {replace_date}")
    df = pd.read_excel(f"../Excel/{EXCEL_NAME}", engine='openpyxl')
    mqtt_client.publish(MQTT_TOPIC, json.dumps({
      'fileName': EXCEL_NAME.split('.')[0],
      'report': df.values.tolist(),
    }), qos=1)
    mqtt_client.loop(2,10)

publish()