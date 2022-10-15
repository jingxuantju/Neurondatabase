from simulink.component import Component, Manager
import math
import numpy as np
from neuron.neuron import *
from pylab import *
from neuron.layer import *
import scipy.io as scio
import copy
import matplotlib.gridspec as gridspec
import cv2
from scipy import misc
# import imageio
mpl.rcParams['font.sans-serif'] = ['SimSun']
matplotlib.rcParams['axes.unicode_minus']=False

if __name__ == '__main__':
    dt = 0.1
    t_span = 12000
    real_t_span = 1200

    n0=np.load('pd0.npz')
    n1=np.load('pd1.npz')

    Vmean_stn = np.mean(n0['V_STN_array'], axis=0)
    Vmean_gpe = np.mean(n0['V_GPE_array'], axis=0)
    Vmean_gpi = np.mean(n0['V_GPI_array'], axis=0)
    AVE_STN = np.mean(Vmean_stn)
    AVE_GPE = np.mean(Vmean_gpe)
    AVE_GPI = np.mean(Vmean_gpi)

    V1mean_stn = np.mean(n1['V1_STN_array'], axis=0)
    V1mean_gpe = np.mean(n1['V1_GPE_array'], axis=0)
    V1mean_gpi = np.mean(n1['V1_GPI_array'], axis=0)
    AVE1_STN = np.mean(V1mean_stn)
    AVE1_GPE = np.mean(V1mean_gpe)
    AVE1_GPI = np.mean(V1mean_gpi)

    fft_values_STN = np.fft.fft(Vmean_stn - AVE_STN)
    fft_values_GPE = np.fft.fft(Vmean_gpe - AVE_GPE)
    fft_values_GPI = np.fft.fft(Vmean_gpi - AVE_GPI)
    fft_values1_STN = np.fft.fft(V1mean_stn - AVE_STN)
    fft_values1_GPE = np.fft.fft(V1mean_gpe - AVE_GPE)
    fft_values1_GPI = np.fft.fft(V1mean_gpi - AVE_GPI)

    frequencies = np.linspace(0, 10000/2, 32768 // 2)
    ff_STN = np.abs(fft_values_STN) * np.abs(fft_values_STN) / 10000
    ff_GPE = np.abs(fft_values_GPE) * np.abs(fft_values_GPE) / 10000
    ff_GPI = np.abs(fft_values_GPI) * np.abs(fft_values_GPI) / 10000
    ff1_STN = np.abs(fft_values1_STN) * np.abs(fft_values1_STN) / 10000
    ff1_GPE = np.abs(fft_values1_GPE) * np.abs(fft_values1_GPE) / 10000
    ff1_GPI = np.abs(fft_values1_GPI) * np.abs(fft_values1_GPI) / 10000
    f1 = frequencies[1:340]
    ff_STN_l = ff_STN[1:340]
    ff_GPE_l = ff_GPE[1:340]
    ff_GPI_l = ff_GPI[1:340]
    ff1_STN_l = ff1_STN[1:340]
    ff1_GPE_l = ff1_GPE[1:340]
    ff1_GPI_l = ff1_GPI[1:340]

    fig5 = plt.figure(figsize=(16, 5), dpi=100)
    plt.subplot(131)
    plt.title('STN', fontdict={'family': 'SimHei', 'size': 14})
    plt.plot(f1, ff_STN_l)
    plt.plot(f1, ff1_STN_l)
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.xlabel('频率(Hz)', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
    plt.ylabel('功率', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
    plt.subplot(132)
    plt.title('GPE', fontdict={'family': 'SimHei', 'size': 14})
    plt.plot(f1, ff_GPE_l)
    plt.plot(f1, ff1_GPE_l)
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.xlabel('频率(Hz)', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
    plt.ylabel('功率', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
    plt.subplot(133)
    plt.title('GPI', fontdict={'family': 'SimHei', 'size': 14})
    plt.plot(f1, ff_GPI_l)
    plt.plot(f1, ff1_GPI_l)
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.xlabel('频率(Hz)', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
    plt.ylabel('功率', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
    fig5.tight_layout()