import socket, array, time
from threading import Lock, Thread, Event

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
from matplotlib.widgets import Button


from scipy import signal
import numpy as np
from numpy.fft import fft, ifft, rfft

class OriginalAnimation:
    def __init__(self) -> None:
        self.fig = plt.figure(figsize=(20, 20))
        gs = gridspec.GridSpec(3, 1)
        self.original = plt.subplot(gs[0, 0])
        self.fft_graph = plt.subplot(gs[1, 0])
        self.stft_graph = plt.subplot(gs[2, 0])

        self.is_first = True

        self.animation = animation.FuncAnimation(self.fig, self.update, interval=100)

        self.paused = False
        ax = plt.axes([0.8, 0.025, 0.1, 0.04])
        self.button = Button(ax, "Stop")
        self.button.on_clicked(self.toggle_event)

    def update(self, i) -> None:
        # update original graph
        data_lock.acquire()
        if len(entire_data) > 100000:
            graph_data = entire_data[len(entire_data) - 100000:]
        else: 
            graph_data = entire_data
        data_lock.release()

        self.original.clear()
        self.original.plot(graph_data)

        # update fft graph
        n = len(graph_data)
        k = np.arange(n)
        Fs = 20480
        T = n/Fs
        frequency = k / T
        frequency = frequency[range(int(n/2))]

        fft_data = fft(graph_data) / n
        fft_data = fft_data[range(int(n / 2))]

        self.fft_graph.clear()
        self.fft_graph.plot(frequency, abs(fft_data))
        
        f, t, Zxx = signal.stft(graph_data, Fs, nperseg=2000)
        
        if self.is_first:
            self.stft = self.stft_graph.pcolormesh(t, f, abs(Zxx), shading="gouraud")
            self.is_first = False
        else:
            self.stft.set_array([t, abs(Zxx)])
        # self.draw_stft(f, t, Zxx)

    def draw_stft(self, f, t, Zxx):
        plt.pcolormesh(t, f, np.abs(Zxx), vmin=0, vmax=1, shading="gouraud")    


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

        
