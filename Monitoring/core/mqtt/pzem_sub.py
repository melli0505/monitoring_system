
import paho.mqtt.client as mqtt
import time
import json

from db import models
from db.base import SessionLocal

broker_address = "YOUR IP ADDRESS"

# subscriber callback

def on_message(client, userdata, message):
    db = SessionLocal()
    converted = str(message.payload.decode("utf-8"))
    value = json.loads(converted)
    print(message.topic, value['voltage'], type(value['voltage']))
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    data = [models.Voltage(time=timestamp, frequency=value["voltage"]),
            models.Energy(time=timestamp, frequency=value["energy"]),
            models.Power(time=timestamp, frequency=value["power"]),
            models.Current(time=timestamp, frequency=value["current"]),
            models.Frequency(time=timestamp, frequency=value["frequency"]),
            models.PF(time=timestamp, frequency=value["pf"])]
    for db_data in data:
        db.add(db_data)
        db.commit()
        db.refresh(db_data)
    db.close()


if __name__ == "__main__":
    client = mqtt.Client("client123")
    
    client.connect(broker_address, 1883)
    print("client connected")

    client.on_message = on_message
    client.subscribe("data")

    print("client loop started")
    client.loop_forever()
