import paho.mqtt.client as mqtt

broker_address = "BROKER_IP_ADDRESS"


def controller(motor: int = 1):
    client = mqtt.Client("controller")
    client.connect(broker_address, 1883)
    control = str(motor)
    if motor == 1:
        client.publish("motor12", control)
        client.publish("motor34", control)
    elif motor == 2:
        client.publish("motor12", control)
        client.publish("motor34", control)
    elif motor == 3:
        client.publish("motor12", control)
        client.publish("motor34", control)
    else:
        client.publish("motor12", control)
        client.publish("motor34", control)
