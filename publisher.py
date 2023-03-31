import paho.mqtt.client as mqtt
import random
import time

mqttc = mqtt.Client("python_pub")
mqttc.connect("YOUR_IP_ADDRESS", 1883)

for i in range(10):
    mqttc.publish("Temperature", "1 " + str(random.randint(0, 20)))
    time.sleep(10)
    
    print("published ", i)
