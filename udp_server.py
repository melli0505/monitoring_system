import socket
import struct
import time

host = '127.0.0.1'

port = 8888

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


serverSocket.connect((host,port)) 

print("Connected")

count = 0
current = time.time()

while True:
    data =  serverSocket.recv(1024)
    struct.unpack('f', data)
    count += 1
    
    now = time.time()
    if now - current >= 1:
        print(count)
        count = 0
        current = time.time()