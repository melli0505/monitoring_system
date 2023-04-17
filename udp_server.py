import socket
import struct
import array
import time
from threading import Lock
from _thread import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def animate(i):
    data_lock.acquire()
    if len(entire_data) > 100000:
        graph_data = entire_data[:50000]
    else: 
        graph_data = entire_data
    data_lock.release()
    ax.clear()
    ax.plot(graph_data)

    
def run():
    global serverSocket
    global data_lock
    global entire_data

    print("Connected", flush=True)
    while True:
        data = serverSocket.recv(8192)
        signals = array.array('f')
        signals.frombytes(data)

        data_lock.acquire()
        entire_data.extend(signals)
        data_lock.release()

if __name__ == "__main__":
    server = ('YOUR_IP_ADDRESS', 2001)
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind(server) 


    entire_data = []
    data_lock = Lock()

    fig = plt.figure(figsize=(10, 2))
    ax = fig.add_subplot(1, 1, 1)

    
    start_new_thread(run, ())

    ani = animation.FuncAnimation(fig, animate, interval=1000)
    plt.show() 
    
    
