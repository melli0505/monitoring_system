
import paho.mqtt.client as mqtt
import time 

from db import models
from base import SessionLocal

def add_data(db: any, sensor_id: int, datetime: str, value: float):
    db_data = models.Sensor(timestamp=datetime, sensor_number=sensor_id, value=value, administer_id=1)
    # database session에 db_user 정보 추가
    db.add(db_data)
    # db에 반영
    db.commit()
    # 최신 db 정보 받아오기
    db.refresh(db_data)
    return db_data

# subscriber callback
def on_message(client, userdata, message):
        print(message)
        converted = str(message.payload.decode("utf-8")).split()
        sensor_id = int(converted[0])
        value = float(converted[1])
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        add_data(db=SessionLocal(), sensor_id=sensor_id, datetime=timestamp, value=value)
        print("message received ", str(message.payload.decode("utf-8")))
        print("message topic= ", message.topic)
        print("message qos=", message.qos)
        print("message retain flag= ", message.retain)

broker_address = "YOUR_IP_ADDRESS"
client1 = mqtt.Client("client1")
client1.connect(broker_address, 1883)
client1.subscribe("Temperature")
client1.on_message = on_message
client1.loop_forever()

