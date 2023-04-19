import socket, array, csv
from threading import Lock, Thread

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.gridspec as gridspec
from matplotlib.widgets import Button

import numpy as np
from numpy.fft import rfft, rfftfreq

from stft import show_result

class RealTimeAnimation:
    """
    Animate original voltage signal graph and fft result.
    """
    def __init__(self):
        # define plot
        self.fig = plt.figure(figsize=(15, 10))
        gs = gridspec.GridSpec(3, 1)
        self.original = self.fig.add_subplot(2, 1, 1)
        self.fft_graph = self.fig.add_subplot(2, 1, 2)

        # connect animation method
        self.animation = animation.FuncAnimation(self.fig, self.update, interval=100)

        # define buttons
        self.paused = False
        ax = plt.axes([0.8, 0.025, 0.1, 0.04])
        ax2 = plt.axes([0.68, 0.025, 0.1, 0.04])
        ax3 = plt.axes([0.56, 0.025, 0.1, 0.04])
        
        # plot control button
        self.pause_button = Button(ax, "Pause/Restart")
        self.pause_button.on_clicked(self.toggle_event)

        # data save button
        self.save_button = Button(ax2, "Save Data")
        self.save_button.on_clicked(self.save_data)

        # show entire data analysis button
        self.show_button = Button(ax3, "Show Analysis")
        self.show_button.on_clicked(show_result)

    def update(self, i) -> None:
        """
        Run every interval and update graphs.
        Using lock.

        Args:
            i : interval
        """

        # update original graph
        data_lock.acquire()
        if len(entire_data) > 110000:
            graph_data = entire_data[len(entire_data) - 100000:]
        else: 
            graph_data = entire_data
        data_lock.release()

        self.original.clear()
        self.original.plot(graph_data)

        # update fft graph
        Fs = 20480
        Ts = 1/Fs
        n = len(graph_data)

        frequency = rfftfreq(n, Ts)[:-1]
        fft_data = (rfft(graph_data)/n)[:-1] * 2

        self.fft_graph.clear()
        self.fft_graph.plot(frequency, np.abs(fft_data))

    
    def toggle_event(self, *args, **kwargs) -> None:
        """
        On click event function of pause button.
        Stop / Restart plotting graphs.
        """

        if self.paused:
            self.animation.event_source.start()
        else:
            self.animation.event_source.stop()

        self.paused = not self.paused

    def save_data(self, *args, **kwargs) -> None:
        """
        Save entire voltage data in csv.
        During save data, graph plotting will be paused.
        Using lock.
        """

        self.animation.event_source.stop()
        print("Saving...")

        data_lock.acquire()
        f = open("data.csv", "w")
        target = csv.writer(f)
        target.writerow(entire_data)
        data_lock.release()

        print("Saved {0} Data. Restart plotting.".format(len(entire_data)))
        self.animation.event_source.start()

def run() -> None:
    """
    UDP data receive function.
    Using lock.
    """

    print("Connected", flush=True)

    while True:
        data = serverSocket.recv(16384)
        signals = array.array('f')
        signals.frombytes(data)
        data_lock.acquire()
        entire_data.extend(signals)
        data_lock.release()


if __name__ == "__main__":
    
    # define socket setting and bind
    server = ('YOUR_IP_ADDRESS', 2001)
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind(server) 

    # set data / data lock
    entire_data = [0]
    data_lock = Lock()

    # start UDP in another thread
    t = Thread(target=run, args=())
    t.start()
    
    # start animation 
    animation = RealTimeAnimation()
    plt.show() 

        
