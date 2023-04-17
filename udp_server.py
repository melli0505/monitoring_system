import socket
import array
from threading import Lock
from _thread import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button

class OnOffAnimation:
    def __init__(self) -> None:
        self.fig = plt.figure(figsize=(16, 4))
        self.ax = self.fig.add_subplot(1, 1, 1)
        self.ax.set_title("진동 센서")
        
        self.animation = animation.FuncAnimation(self.fig, self.update, interval=100)
        self.paused = False
        self.fig.canvas.mpl_connect("button_press_event", self.toggle_event)

    def update(self, i) -> None:
        data_lock.acquire()
        if len(entire_data) > 100000:
            graph_data = entire_data[30000:]
        else: 
            graph_data = entire_data
        data_lock.release()
        self.ax.clear()
        self.ax.plot(graph_data)
    
    def toggle_event(self, *args, **kwargs):
        if self.paused:
            self.animation.event_source.start()
        else:
            self.animation.event_source.stop()
        self.paused = not self.paused

    
def run():
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
    server = ('YOUR_IP_ADDRESS', 2001)
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind(server) 

    entire_data = [0]
    data_lock = Lock()
    
    start_new_thread(run, ())

    animation = OnOffAnimation()
    plt.show() 
    

