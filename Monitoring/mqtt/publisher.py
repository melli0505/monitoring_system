import paho.mqtt.client as mqtt
import random
import time

mqttc = mqtt.Client("local_pub")
mqttc.connect("BROKER_IP_ADDRESS", 1883)

for i in range(5):
    mqttc.publish("Temperature", "0 " + str(random.uniform(10, 18)))
    print("published 0 ", i)
    time.sleep(1)
    mqttc.publish("Temperature2", "1 " + str(random.uniform(10, 18)))
    print("published 1", i)
    time.sleep(9)
    
