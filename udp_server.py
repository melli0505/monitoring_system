import socket, array, time
from threading import Lock, Thread, Event

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Button

from scipy import signal
import numpy as np
from numpy.fft import fft, ifft, rfft

class OriginalAnimation:
    def __init__(self) -> None:
        self.fig = plt.figure(figsize=(20, 4))
        self.original = self.fig.add_subplot(3, 1, 1)
        self.fft_graph = self.fig.add_subplot(3, 1, 2)
        self.stft_graph = self.fig.add_subplot(3, 1, 3)

        self.animation = animation.FuncAnimation(self.fig, self.update, interval=100)

        self.paused = False
        ax = plt.axes([0.8, 0.025, 0.1, 0.04])
        self.button = Button(ax, "Stop")
        self.button.on_clicked(self.toggle_event)

    def update(self, i) -> None:
        # update original graph
        data_lock.acquire()
        if len(entire_data) > 100000:
            graph_data = entire_data[len(entire_data) - len(entire_data) // 3:]
        else: 
            graph_data = entire_data
        data_lock.release()

        self.original.clear()
        self.original.plot(graph_data)

        # update fft graph
        sampling_rate = 20480

        fft_data = fft(graph_data) / len(graph_data)
        fft_data = fft_data[range(int(len(graph_data) / 2))]
        N = len(fft_data)
        n = np.arange(N)
        T = N / sampling_rate
        frequency = n / T
        frequency = frequency[range(int(len(graph_data) / 2))]

        self.fft_graph.clear()
        self.fft_graph.plot(frequency, fft_data)


    def window(self, index, max_index):
        return 0.5 - 0.5 * np.cos(2 * np.pi * index / max_index)
    
    def toggle_event(self, *args, **kwargs):
        if self.paused:
            self.animation.event_source.start()
        else:
            self.animation.event_source.stop()
        self.paused = not self.paused

def run():
    print("Connected", flush=True)
    while not exit_signal.is_set():
        data = serverSocket.recv(16384)
        signals = array.array('f')
        signals.frombytes(data)
        data_lock.acquire()
        entire_data.extend(signals)
        data_lock.release()
    exit()


if __name__ == "__main__":
    server = ('YOUR_IP_ADDRESS', 2001)
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind(server) 

    entire_data = [0]
    data_lock = Lock()

    exit_signal = Event()
    t = Thread(target=run, args=())
    t.start()
    
    animation = OriginalAnimation()
    plt.show() 

        
