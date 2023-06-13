import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import torch
import csv, os
import pandas as pd

from scipy import signal

def show_result(e) -> None:
    """
    Show original signal graph, fft and stft result of saved data.

    Args:
        e: event
    """

    # read data
    limit = 3
    entire_data = []
    for filename in os.listdir('C:/Users/dk866/Desktop/monitoring_system/Data/test_17.0khz/'):
        file = open('./Data/test_17.0khz/' + filename)
        reader = csv.reader(file, delimiter=',')
        for row in reader:
            print(len(row))
            entire_data.extend(list(map(float, row)))

        limit -= 1
        if limit < 0: break


        # break



    # data_file = open("data.csv", "r")
    # reader = csv.reader(data_file, delimiter=',', quoting=csv.QUOTE_NONNUMERIC)
    # entire_data = []
    # for row in reader:
    #     entire_data = row
    #     print(entire_data[:10])
    #     break

    if len(entire_data) <= 1:
        print("No data saved. Please try after save data.")
        return 

    print("Complete loading.", entire_data[:10])
    gs = gridspec.GridSpec(3, 1)

    # define graph
    fig = plt.figure(figsize=(20, 12))
    fig.suptitle("Data Analysis Result", fontsize=20)

    original = plt.subplot(gs[0, 0])
    original.set_title("Original Signal")
    original.set(xlabel="Samples", ylabel="mV")

    stft = plt.subplot(gs[1, 0])
    stft.set_title("Short-Term FFT")
    stft.set(xlabel="Time(sec)", ylabel="Frequency")

    fft_graph = plt.subplot(gs[2, 0])
    fft_graph.set_title("FFT")
    fft_graph.set(xlabel="Frequency", ylabel="Amplitude")

    plt.subplots_adjust(hspace=0.5)

    # plot fft
    Fs = 17066.0
    Ts = 1/Fs
    n = len(entire_data)

    f, t, Sxx = signal.stft(entire_data, Fs)
    print(f.shape, t.shape, Sxx.shape)
    # pytorch fft
    graph_data = torch.Tensor(entire_data)
    graph_data.to("cuda:0")
    fft_data = torch.fft.rfft(graph_data) / n

    frequency = torch.arange(0.0, Fs/2.0, Fs/n)
    fft_graph.clear()
    fft_graph.plot(frequency[1:len(fft_data)], np.abs(fft_data[1:len(fft_data)]))
    
    # pytorch stft

    # graph_data = graph_data.unsqueeze(0)
    # stft_ = torch.stft(graph_data, n_fft=17066, win_length=17066)
    # print(stft_.shape)
    # stft_data = torch.sqrt(stft_[:,:,:,0] ** 2 + stft_[:,:,:,1] ** 2)
    # stft.pcolormesh(stft_data[0])
    # print(stft_data.shape)

    # mean = []
    # for i in range(len(entire_data) // 1425):
    #     slice = entire_data[i * 1425:(i + 1) * 1425]
    #     m = sum(slice) / 1425
    #     mean.append(m)

    # fft_graph.plot(mean)

    # plot original signal graph
    original.plot(entire_data[:100000])

    plt.show()

# show_result('a')