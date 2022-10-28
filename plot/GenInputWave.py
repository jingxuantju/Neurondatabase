from simulink.component import Component, Manager
import math
import numpy as np
from neuron.neuron import *
from pylab import *
from neuron.layer import *
import scipy.io as scio
import copy
import cv2
import matplotlib.gridspec as gridspec
from scipy import misc
# import imageio
import seaborn as sns
import pywt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.io as scio
from neuron.neuron import *


def sin_wave(A, f, fs, phi, t):
    '''
    :params A:    振幅
    :params f:    信号频率
    :params fs:   采样频率
    :params phi:  相位
    :params t:    时间长度
    '''
    # 若时间序列长度为 t=1s,
    # 采样频率 fs=1000 Hz, 则采样时间间隔 Ts=1/fs=0.001s
    # 对于时间序列采样点个数为 n=t/Ts=1/0.001=1000, 即有1000个点,每个点间隔为 Ts
    Ts = 1 / fs
    n = t / Ts
    n = np.arange(t)
    y = A * np.sin(2 * np.pi * f * n * Ts + phi * (np.pi / 180))
    return y


def Gaussian_Noise(seql=100, mx=0, sigma=4):
    """
    :param sigma: 方差
    :param seql: 序列长度
    :param mx: 噪声均值
    """
    mean = np.array([mx])
    cov = np.eye(1) * sigma

    G_seq = []
    for i in range(seql):
        data = np.random.multivariate_normal(mean, cov, 1)
        G_seq.append(data[0][0])

    return G_seq


def square_wave(start, end, zhouqi, midu):
    '''
    :param start: the fist value of the wave
    :param end:  the end value of the wave
    :param zhouqi:  the zhouqi range of the wave
    :param midu:  every zhouqi, there are how many points in this zhouqi
    :return: the x array and the y array
    '''
    xout = []
    yout = []
    for i in range(start, end, zhouqi):
        x = np.arange(i, i + zhouqi, midu)
        # y = np.where(x<start+0.5, x-start, 0)
        y = np.where(x >= i + zhouqi / 2, 1, 0)

        xout = np.append(xout, x)
        yout = np.append(yout, y)
    return xout, yout


if __name__ == '__main__':
    t_span = 30000
    session_t_span = 10000
    real_t_span = 3000
    num = 100
    Add_noise = 1
    # z0_t = np.zeros((1, session_t_span))
    # z0 = z0_t.reshape(session_t_span,1)

    # Gen Gaussian Noise
    noise = Gaussian_Noise(seql=t_span, mx=0, sigma=2)

    # Gen Square Wave
    square1 = square_wave(start=session_t_span, end=2*session_t_span, zhouqi=10, midu=5)

    # Gen Sine Wave
    fs = 5000
    sin_1_T = sin_wave(A=4, f=2, fs=fs, phi=0, t=session_t_span)
    sin_2_T = sin_wave(A=5, f=28, fs=fs, phi=0, t=session_t_span)
    sin_1 = np.transpose(sin_1_T)
    sin_2 = np.transpose(sin_2_T)

    # Gen Direct-Current
    Amp1 = 6
    Amp2 = -6
    dc_0_t = np.ones((1, session_t_span)) * 0
    dc_0 = dc_0_t.reshape(session_t_span)
    dc_1 = np.ones((1, session_t_span)) * Amp1
    dc_2 = np.ones((1, session_t_span)) * Amp2

    is1 = np.hstack([dc_1.reshape(session_t_span), dc_0])
    is2 = np.hstack([dc_2.reshape(session_t_span), dc_0])
    isine1 = np.hstack([dc_0, sin_1])
    isine2 = np.hstack([dc_0, sin_2])
    input1 = np.hstack([dc_0, is2])
    input2 = np.hstack([dc_0, is1])
    input3 = np.hstack([isine1, dc_0])
    input4 = np.hstack([isine2, dc_0])

    np.savez('ng_input', input1=input1, input2=input2, input3=input3, input4=input4, input1n=input1 + noise, input2n=input2 + noise, input3n=input3 + noise, input4n=input4 + noise)

    if(Add_noise==0):
        np.savez('ng_input', input1=input1, input2=input2, input3=input3, input4=input4)

        fig1 = plt.figure(figsize=(10, 5), dpi=100)
        plt.title('正常', fontdict={'family': 'SimHei', 'size': 14})
        plt.subplot(411)
        plt.plot(input1, c='k', linewidth=2)
        plt.yticks(fontproperties='Times New Roman', size=14)
        plt.xticks(fontproperties='Times New Roman', size=14)
        plt.ylabel('ng1', fontdict={'family': 'SimHei', 'size': 14})
        plt.subplot(412)
        plt.plot(input2, c='k', linewidth=2)
        plt.yticks(fontproperties='Times New Roman', size=14)
        plt.xticks(fontproperties='Times New Roman', size=14)
        plt.ylabel('ng1', fontdict={'family': 'SimHei', 'size': 14})
        plt.subplot(413)
        plt.plot(input3, c='k', linewidth=2)
        plt.yticks(fontproperties='Times New Roman', size=14)
        plt.xticks(fontproperties='Times New Roman', size=14)
        plt.ylabel('ng1', fontdict={'family': 'SimHei', 'size': 14})
        plt.subplot(414)
        plt.plot(input4, c='k', linewidth=2)
        plt.yticks(fontproperties='Times New Roman', size=14)
        plt.xticks(fontproperties='Times New Roman', size=14)
        plt.ylabel('ng1', fontdict={'family': 'SimHei', 'size': 14})
    else:
        fig1 = plt.figure(figsize=(10, 5), dpi=100)
        plt.title('正常', fontdict={'family': 'SimHei', 'size': 14})
        plt.subplot(411)
        plt.plot(input1 + noise, c='k', linewidth=2)
        plt.yticks(fontproperties='Times New Roman', size=14)
        plt.xticks(fontproperties='Times New Roman', size=14)
        plt.ylabel('ng1', fontdict={'family': 'SimHei', 'size': 14})
        plt.subplot(412)
        plt.plot(input2 + noise, c='k', linewidth=2)
        plt.yticks(fontproperties='Times New Roman', size=14)
        plt.xticks(fontproperties='Times New Roman', size=14)
        plt.ylabel('ng1', fontdict={'family': 'SimHei', 'size': 14})
        plt.subplot(413)
        plt.plot(input3 + noise, c='k', linewidth=2)
        plt.yticks(fontproperties='Times New Roman', size=14)
        plt.xticks(fontproperties='Times New Roman', size=14)
        plt.ylabel('ng1', fontdict={'family': 'SimHei', 'size': 14})
        plt.subplot(414)
        plt.plot(input4 + noise, c='k', linewidth=2)
        plt.yticks(fontproperties='Times New Roman', size=14)
        plt.xticks(fontproperties='Times New Roman', size=14)
        plt.ylabel('ng1', fontdict={'family': 'SimHei', 'size': 14})