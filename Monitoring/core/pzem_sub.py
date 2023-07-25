
import paho.mqtt.client as mqtt
import time

from db import models
from db.base import SessionLocal

broker_address = "YOUR IP ADDRESS"

# subscriber callback


def on_voltage(client, userdata, message):
    db = SessionLocal()
    converted = str(message.payload.decode("utf-8"))
    value = float(converted)
    print(message.topic, value)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    db_data = models.Voltage(time=timestamp, voltage=value)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    db.close()


def on_current(client, userdata, message):
    db = SessionLocal()
    converted = str(message.payload.decode("utf-8"))
    value = float(converted)
    print(message.topic, value)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    db_data = models.Current(time=timestamp, current=value)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    db.close()


def on_power(client, userdata, message):
    db = SessionLocal()
    converted = str(message.payload.decode("utf-8"))
    value = float(converted)
    print(message.topic, value)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    db_data = models.Power(time=timestamp, power=value)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    db.close()


def on_energy(client, userdata, message):
    db = SessionLocal()
    converted = str(message.payload.decode("utf-8"))
    value = float(converted)
    print(message.topic, value)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    db_data = models.Energy(time=timestamp, energy=value)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    db.close()


def on_pf(client, userdata, message):
    db = SessionLocal()
    converted = str(message.payload.decode("utf-8"))
    value = float(converted)
    print(message.topic, value)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    db_data = models.PF(time=timestamp, pf=value)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    db.close()


def on_frequency(client, userdata, message):
    db = SessionLocal()
    converted = str(message.payload.decode("utf-8"))
    value = float(converted)
    print(message.topic, value)
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    db_data = models.Frequency(time=timestamp, frequency=value)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    db.close()


if __name__ == "__main__":
    client = mqtt.Client("client123")

    client.message_callback_add("AC/voltage", on_voltage)
    client.message_callback_add("AC/energy", on_energy)
    client.message_callback_add("AC/power", on_power)
    client.message_callback_add("AC/current", on_current)
    client.message_callback_add("AC/pf", on_pf)
    client.message_callback_add("AC/frequency", on_frequency)

    client.connect(broker_address, 1883)
    print("client connected")

    client.subscribe("AC/voltage")
    client.subscribe("AC/energy")
    client.subscribe("AC/power")
    client.subscribe("AC/current")
    client.subscribe("AC/pf")
    client.subscribe("AC/frequency")

    print("client loop started")
    client.loop_forever()
