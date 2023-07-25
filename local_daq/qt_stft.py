import pyqtgraph as pg

from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPalette, QColor, QFont
import numpy as np
import torch
from scipy import signal
import csv

class ShowResult(QWidget):
    def __init__(self):
        super().__init__()
            # read data
        data_file = open("data.csv", "r")
        reader = csv.reader(data_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
        self.entire_data = []
        for row in reader:
            self.entire_data = row
            print(self.entire_data[:10])
            break

        if len(self.entire_data) <= 1:
            print("No data saved. Please try after save data.")
            return 
        
        self.label = QLabel("Analysis Results")
        self.label.setFont(QFont("Arial", 20))
        pg.setConfigOptions(imageAxisOrder='row-major')
        
        box = QVBoxLayout()
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

        self.stft = pg.PlotWidget(title="FFT")
        self.stft.plotItem.setLabels(bottom="Time (s)", left="Frequency (Hz)")
        self.stft.plotItem.getAxis('bottom').setPen(pg.mkPen(color='#000000'))
        self.stft.plotItem.getAxis('left').setPen(pg.mkPen(color='#000000'))
        self.stft.setBackground('w')
        self.stft.setStyleSheet("border: 1px solid black; padding-left:10px; padding-right:10px; background-color: white;")
     
        self.orig_p = self.orig.plot(pen='b')
        self.fft_p = self.fft.plot(pen='b')
        
        self.img = pg.ImageItem()
        self.stft.addItem(self.img)
        self.hist = pg.HistogramLUTItem()
        self.hist.setImageItem(self.img)
        self.hist.gradient.restoreState(
            {"mode": "rgb",
            "ticks": [(0.00, (0, 0, 0)),
                      (0.05, (0, 0, 128)),
                      (0.50, (185, 0 , 0)),
                      (1.00, (255, 220, 0))]})

        self.stft.addItem(self.hist)

        box.addWidget(self.label)
        box.addWidget(self.orig)
        box.addWidget(self.fft)
        box.addWidget(self.stft)
        box.setSpacing(30)
        box.setContentsMargins(50,50,50,50)
        self.setLayout(box)

        self.setGeometry(800, 300, 1500, 1000)
        self.show_result()

    def show_result(self):
        self.orig_p.setData(self.entire_data)

        # plot fft
        Fs = 25600.0
        Ts = 1/Fs
        n = len(self.entire_data)

        # pytorch fft
        graph_data = torch.Tensor(self.entire_data)
        graph_data.to("cuda:0")
        fft_data = torch.fft.rfft(graph_data) / n

        frequency = torch.arange(0.0, Fs/2.0, Fs/n)
        self.fft_p.setData(frequency[1:len(fft_data)//2], np.abs(fft_data[1:len(fft_data)//2]))
        
        # scipy stft
        graph_data = graph_data.unsqueeze(0)
        stft_ = torch.stft(graph_data, n_fft=25600, win_length=2560)
        print(stft_.shape)
        stft_data = torch.sqrt(stft_[:,:,:,0] ** 2 + stft_[:,:,:,1] ** 2)

        self.img.setImage(np.array(stft_data[0], dtype=np.float32))
        # self.img.scale(t[-1] / np.size(Sxx, axis=1),
        #                f[-1] / np.size(Sxx, axis=0))

        self.show()

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    pal = app.palette()
    pal.setColor(QPalette.Window, QColor(245,245,245))
    app.setPalette(pal)

    ex = ShowResult()

    sys.exit(app.exec_())