import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from numpy.fft import rfft, rfftfreq
import numpy as np
from scipy import signal
import csv

def show_result(e) -> None:
    """
    Show original signal graph, fft and stft result of saved data.

    Args:
        e: event
    """

    # read data
    data_file = open("data.csv", "r")
    reader = csv.reader(data_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
    entire_data = []
    for row in reader:
        entire_data = row
        print(entire_data[:10])
        break

    if len(entire_data) <= 1:
        print("No data saved. Please try after save data.")
        return 
    
    # calculate rms, not use now
    # rms = []
    # for i in range(65):
    #     a = sum(entire_data[i * 9 : i * 9 + 9])
    #     rms.append((a^2) / len(a))

    gs = gridspec.GridSpec(3, 1)

    # define graph
    fig = plt.figure(figsize=(24, 8))
    original = plt.subplot(gs[0, 0])
    stft = plt.subplot(gs[1, 0])
    fft_graph = plt.subplot(gs[2, 0])

    # plot fft
    Fs = 20480
    Ts = 1/Fs
    n = len(entire_data)

    frequency = rfftfreq(n, Ts)[:-1]
    fft_data = (rfft(entire_data)/n)[:-1] * 2

    fft_graph.plot(frequency, np.abs(fft_data))

    # plot stft
    f, t, Zxx = signal.stft(entire_data, 20480, nperseg=20000)
    stft.pcolormesh(t, f, np.abs(Zxx), shading="gouraud")

    # plot original signal graph
    original.plot(entire_data)

    plt.show()