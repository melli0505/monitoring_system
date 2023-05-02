import sys
from threading import Lock, Thread
import csv, socket, array, time

import pyqtgraph as pg

from PyQt5.QtWidgets import *
from PyQt5.QtCore import pyqtSlot, QTimer
from PyQt5.QtGui import QPalette, QColor, QFont

import torch
import numpy as np

from stft import show_result

c = 0

class Main(QWidget):
    def __init__(self):
        super().__init__()

        self.paused = False
        self.label = QLabel("Real-Time Graph")
        self.label.setFont(QFont("Arial", 20))

        # define plot
        self.orig = pg.PlotWidget(title="Original")
        self.orig.plotItem.setLabels(bottom='Samples', left="IEPE (mV)")
        self.orig.plotItem.getAxis('bottom').setPen(pg.mkPen(color='#000000'))
        self.orig.plotItem.getAxis('left').setPen(pg.mkPen(color='#000000'))
        self.orig.setBackground('w')
        self.orig.setStyleSheet("border: 1px solid black; padding-left:10px; padding-right:10px; background-color: white;")
        
        self.fft = pg.PlotWidget(title="FFT")
        self.fft.plotItem.setLabels(bottom="Frequency (Hz)", left="Amplitude")
        self.fft.plotItem.getAxis('bottom').setPen(pg.mkPen(color='#000000'))
        self.fft.plotItem.getAxis('left').setPen(pg.mkPen(color='#000000'))
        self.fft.setBackground('w')
        self.fft.setStyleSheet("border: 1px solid black; padding-left:10px; padding-right:10px; background-color: white;")

        # plot control button
        self.pause_button = QPushButton()
        self.pause_button.setText("Pause/Restart")
        self.pause_button.clicked.connect(self.toggle_event)
        self.pause_button.setMinimumSize(300, 50)
        self.pause_button.setStyleSheet("background-color: white; padding-left:10px; padding-right:10px; font-size: 15px; font-family: Arial;")

        # start record button
        self.record_button = QPushButton()
        self.record_button.setText("Start Recording")
        self.record_button.clicked.connect(self.start_recording)
        self.record_button.setMinimumSize(300, 50)
        self.record_button.setStyleSheet("background-color: white; font-size: 15px;font-family: Arial;")
        
        # data save button
        self.save_button = QPushButton()
        self.save_button.setText("Stop Recording")
        self.save_button.clicked.connect(self.stop_recording)
        self.save_button.setMinimumSize(300, 50)
        self.save_button.setStyleSheet("background-color: white; font-size: 15px;font-family: Arial;")

        # show entire data analysis button
        self.show_button = QPushButton()
        self.show_button.setText("Show Analysis")
        self.show_button.clicked.connect(show_result)
        self.show_button.setMinimumSize(300, 50)
        self.show_button.setStyleSheet("background-color: white; font-size: 15px;font-family: Arial;")

        buttons = QHBoxLayout()
        buttons.addWidget(self.pause_button)
        buttons.addWidget(self.record_button)
        buttons.addWidget(self.save_button)
        buttons.addWidget(self.show_button)

        box = QVBoxLayout()
        box.addWidget(self.label)
        box.addWidget(self.orig)
        box.addWidget(self.fft)
        box.addLayout(buttons)
        box.setSpacing(30)
        box.setContentsMargins(50,50,50,50)
        self.setLayout(box)

        # set Window
        self.setGeometry(800, 300, 1500, 1000)
        self.setWindowTitle("Real Time Data Graphs")

        self.graph_data = [0]
        self.pos = 0
        self.record = False
        self.time = time.time()

        # set line graph
        self.orig_p = self.orig.plot(pen='b')
        self.fft_p = self.fft.plot(pen='r')

        # set timer - animation controller
        self.mytimer = QTimer()
        self.mytimer.start(25)  
        self.mytimer.timeout.connect(self.get_data)

        self.draw_chart()
        self.show()

    def draw_chart(self):
        """
        Update plot data and calculate FFT.
        """
        # update original signal graph
        self.orig_p.setData(self.graph_data)  
        
        # update fft graph
        Fs = 25600.0
        n = len(self.graph_data)
        
        # pytorch fft
        graph_data = torch.Tensor(self.graph_data)
        graph_data.to("cuda:0")
        fft_data = torch.fft.rfft(graph_data) / n
        frequency = torch.arange(0.0, Fs/2.0, Fs/n)

        self.fft_p.setData(frequency[:len(fft_data)//2], np.abs(fft_data[:len(fft_data)//2]))

        
    @pyqtSlot()
    def get_data(self):
        """
        Separate plotting data from entire data.
        """
        data_lock.acquire()
        if len(entire_data) > 110000:
            self.graph_data = entire_data[len(entire_data) - 100000:]
        else:
            self.graph_data = entire_data

        if self.record and time.time() - self.time >= 60:
            self.time = time.time()
            self.save_data()

        data_lock.release()
        self.draw_chart()

    def toggle_event(self):
        """
        Control animation. Pause/Restart.
        """
        if self.paused:
            self.mytimer.start()
        else:
            self.mytimer.stop()
        self.paused = not self.paused

    def start_recording(self) -> None:
        """
        Set start point of saving data.
        """
        self.record = True
        self.pos = len(entire_data) - 1
        print("Recording Start.")

    def stop_recording(self) -> None:
        """
        Stop recording data.
        """
        self.record = False
        self.pos = len(entire_data) - 1
        print("Recording Stopped. Press Start Recording button to restart recording.")

    def save_data(self) -> None:
        """
        Save entire voltage data in csv(46).
        """
        print("Saving...")

        t = '.'.join(list(map(str, time.localtime()))[:6])
        f = open(f"./Data/{t}.46", "w")
        f.write(','.join(list(map(str, entire_data[self.pos:]))))
        self.pos = len(entire_data) - 1

        


def run() -> None:
    """
    UDP data receive function.
    Using lock.
    """
    global c
    print("Connected", flush=True)
    while True:
        data = serverSocket.recv(40000)
        signals = array.array('d')
        signals.frombytes(data)
        # print(c, len(signals))
        sys.stdout.flush()
        data_lock.acquire()
        entire_data.extend(signals)
        data_lock.release()
        c += 1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    pal = app.palette()
    pal.setColor(QPalette.Window, QColor(245,245,245))
    app.setPalette(pal)

    ex = Main()

    # define socket setting and bind
    server = ('YOUR_IP_ADDRESS', 2001)
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind(server)

    # set data / data lock
    entire_data = [0, 0]
    data_lock = Lock()

    # start UDP in another thread
    t = Thread(target=run, args=())
    t.start()

    sys.exit(app.exec_())