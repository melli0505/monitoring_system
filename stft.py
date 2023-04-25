import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import torch
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
    Fs = 25600.0
    Ts = 1/Fs
    n = len(entire_data)

    # pytorch fft
    graph_data = torch.Tensor(entire_data)
    graph_data.to("cuda:0")
    fft_data = torch.fft.rfft(graph_data) / n

    frequency = torch.arange(0.0, Fs/2.0, Fs/n)
    fft_graph.clear()
    fft_graph.plot(frequency[1:len(fft_data)//2], np.abs(fft_data[1:len(fft_data)//2]))
    
    # pytorch stft
    graph_data = graph_data.unsqueeze(0)
    stft_ = torch.stft(graph_data, 12800)
    stft_data = torch.sqrt(stft_[:,:,:,0] ** 2 + stft_[:,:,:,1]**2)
    stft.pcolormesh(stft_data[0])

    # plot original signal graph
    original.plot(entire_data)

    plt.show()
