
import paho.mqtt.client as mqtt

broker_address = "YOUR IP ADDRESS"


def publish_control(command: str = "reset"):
    client = mqtt.Client("controller")
    client.connect(broker_address, 1883)
    client.publish("Control", command)
