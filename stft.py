import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from numpy.fft import rfft, rfftfreq
import numpy as np
import tensorflow as tf
from scipy import signal
import csv, os

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

    # frequency = rfftfreq(n, Ts)[:-1]
    # fft_data = (rfft(entire_data)/n)[:-1] * 2

    # entire_data = torch.Tensor(entire_data)
    # entire_data.to('cuda:0')
    with tf.device("/device:GPU:0"):
        fft_data = tf.signal.rfft(input_tensor=tf.cast(entire_data, tf.float32))
        frequency = tf.range(0.0, tf.divide(Fs,2.0), tf.divide(Fs,tf.cast(n, tf.float32)))

    # fft_data = torch.fft.rfft(entire_data)[:-1]
    # frequency = torch.fft.rfftfreq(Fs)[:-1]
    fft_graph.clear()
    fft_graph.plot(frequency[:len(fft_data)//2], np.abs(fft_data[:len(fft_data)//2]))
    # fft_graph.plot(frequency, np.abs(fft_data))

    
    # plot stft
    f, t, Zxx = signal.stft(entire_data, fs=Fs, nperseg=len(entire_data)//100)
    stft.pcolormesh(t, f, np.abs(Zxx), shading="gouraud")

    # plot original signal graph
    original.plot(entire_data)

    plt.show()


os.environ["CUDA_VISIBLE_DEVICES"]="0"
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        tf.config.experimental.set_memory_growth(gpus[0], True)
    except RuntimeError as e:
        print(e)
print(tf.config.experimental.list_logical_devices())
show_result('a')