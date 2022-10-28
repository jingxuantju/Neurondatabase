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


if __name__ == '__main__':
    t_span = 30000
    session_t_span = 10000
    real_t_span = 3000
    num = 100

    n0 = np.load('ng_input.npz')
    input1 = n0['input1'].tolist()
    input2 = n0['input2'].tolist()
    input3 = n0['input3'].tolist()
    input4 = n0['input4'].tolist()

    input1n = n0['input1n'].tolist()
    input2n = n0['input2n'].tolist()
    input3n = n0['input3n'].tolist()
    input4n = n0['input4n'].tolist()

    dt = 0.1
    num = 100
    ng1 = [0 for i in range(num)]
    ng1_syn_ng1 = [0 for i in range(num)]
    ng1_syn_ng2 = [0 for i in range(num)]
    ng1_syn_ng3 = [0 for i in range(num)]
    ng2 = [0 for i in range(num)]
    ng2_syn_ng2 = [0 for i in range(num)]
    ng2_syn_ng3 = [0 for i in range(num)]
    ng2_syn_ng1 = [0 for i in range(num)]
    ng3 = [0 for i in range(num)]
    ng3_syn_ng3 = [0 for i in range(num)]
    ng3_syn_ng1 = [0 for i in range(num)]
    ng3_syn_ng2 = [0 for i in range(num)]
    para_exc_exc = [random.uniform(0, 0.65) for i in range(num)]
    para_exc_inh = [random.uniform(0, 2) for i in range(num)]
    para_inh_exc = [random.uniform(-1.7, -0.8) for i in range(num)]
    para_inh_inh = [random.uniform(-1.1, -0.3) for i in range(num)]

    IstimC1 = [0 for i in range(100)]
    IstimC2 = [0 for i in range(100)]

    manager = Manager()
    for i in range(num):
        ng1[i] = IzhikevichNeuron1(manager, 'ng1' + str(i), 0, 0.02, 0.24, -65, 10)
        ng1_syn_ng1[i] = ExcsynapseNeuron(manager, 'ng1_syn_ng1' + str(i), para_exc_exc)
        ng1_syn_ng2[i] = ExcsynapseNeuron(manager, 'ng1_syn_ng2' + str(i), para_exc_exc)
        ng1_syn_ng3[i] = ExcsynapseNeuron(manager, 'ng1_syn_ng3' + str(i), para_exc_inh)
        manager.link_output_input(ng1[i], ng1_syn_ng1[i])
        manager.link_output_input(ng1[i], ng1_syn_ng2[i])
        manager.link_output_input(ng1[i], ng1_syn_ng3[i])
        ng2[i] = IzhikevichNeuron1(manager, 'ng2' + str(i), 0, 0.02, 0.24, -65, 10)
        ng2_syn_ng2[i] = ExcsynapseNeuron(manager, 'ng2_syn_ng2' + str(i), para_exc_exc)
        ng2_syn_ng3[i] = ExcsynapseNeuron(manager, 'ng2_syn_ng3' + str(i), para_exc_inh)
        ng2_syn_ng1[i] = ExcsynapseNeuron(manager, 'ng2_syn_ng1' + str(i), para_exc_exc)
        manager.link_output_input(ng2[i], ng2_syn_ng2[i])
        manager.link_output_input(ng2[i], ng2_syn_ng3[i])
        manager.link_output_input(ng2[i], ng2_syn_ng1[i])
        ng3[i] = IzhikevichNeuron1(manager, 'ng3' + str(i), 0, 0.01, 0.25, -65, 1)
        ng3_syn_ng3[i] = ExcsynapseNeuron(manager, 'ng3_syn_ng3' + str(i), para_inh_inh, tao=1)
        ng3_syn_ng1[i] = ExcsynapseNeuron(manager, 'ng3_syn_ng1' + str(i), para_inh_exc, tao=1)
        ng3_syn_ng2[i] = ExcsynapseNeuron(manager, 'ng3_syn_ng2' + str(i), para_inh_exc, tao=1)
        manager.link_output_input(ng3[i], ng3_syn_ng3[i])
        manager.link_output_input(ng3[i], ng3_syn_ng1[i])
        manager.link_output_input(ng3[i], ng3_syn_ng2[i])
        IstimC1[i] = IstimComponent(manager, 'Istim' + str(i), copy.deepcopy(input3n))
        manager.link_output_input(IstimC1[i], ng1[i], tab='I')
        IstimC2[i] = IstimComponent(manager, 'Istim' + str(i), copy.deepcopy(input3n))
        manager.link_output_input(IstimC2[i], ng2[i], tab='I')
    for i in range(num):
        for j in range(num):
            a1 = random.randint(0, 10)
            a2 = random.randint(0, 10)
            a3 = random.randint(0, 10)
            if (a1 < 4):
                manager.link_output_input(ng1_syn_ng1[i], ng1[j], tab='I')
                manager.link_output_input(ng1[j], ng1_syn_ng1[i], tab='houmo')
            if (a2 < 4):
                manager.link_output_input(ng1_syn_ng2[i], ng2[j], tab='I')
                manager.link_output_input(ng2[j], ng1_syn_ng2[i], tab='houmo')
            if (a3 < 4):
                manager.link_output_input(ng1_syn_ng3[i], ng3[j], tab='I')
                manager.link_output_input(ng3[j], ng1_syn_ng3[i], tab='houmo')
            b1 = random.randint(0, 10)
            b2 = random.randint(0, 10)
            b3 = random.randint(0, 10)
            if (b1 < 4):
                manager.link_output_input(ng2_syn_ng2[i], ng2[j], tab='I')
                manager.link_output_input(ng2[j], ng2_syn_ng2[i], tab='houmo')
            if (b2 < 4):
                manager.link_output_input(ng2_syn_ng3[i], ng3[j], tab='I')
                manager.link_output_input(ng3[j], ng2_syn_ng3[i], tab='houmo')
            if (b3 < 4):
                manager.link_output_input(ng2_syn_ng1[i], ng1[j], tab='I')
                manager.link_output_input(ng1[j], ng2_syn_ng1[i], tab='houmo')
            c1 = random.randint(0, 10)
            c2 = random.randint(0, 10)
            c3 = random.randint(0, 10)
            if (c1 < 4):
                manager.link_output_input(ng3_syn_ng3[i], ng3[j], tab='I')
                manager.link_output_input(ng3[j], ng3_syn_ng3[i], tab='houmo')
            if (c2 < 4):
                manager.link_output_input(ng3_syn_ng1[i], ng1[j], tab='I')
                manager.link_output_input(ng1[j], ng3_syn_ng1[i], tab='houmo')
            if (c3 < 4):
                manager.link_output_input(ng3_syn_ng2[i], ng2[j], tab='I')
                manager.link_output_input(ng2[j], ng3_syn_ng2[i], tab='houmo')

    result = manager.start_stimulation(t_span)

    ng1_RESULT = []
    ng2_RESULT = []
    ng3_RESULT = []
    for j in range(100):
        ng1_R = []
        ng2_R = []
        ng3_R = []
        for dictionary in result:
            ng1_R.append(dictionary['ng1' + str(j)][0])
            ng2_R.append(dictionary['ng2' + str(j)][0])
            ng3_R.append(dictionary['ng3' + str(j)][0])
        ng1_RESULT.append(ng1_R)
        ng2_RESULT.append(ng2_R)
        ng3_RESULT.append(ng3_R)

    ng1_array = np.array(ng1_RESULT)
    ng2_array = np.array(ng2_RESULT)
    ng3_array = np.array(ng3_RESULT)

    # np.savez('ng_vs', ng1_array=ng1_array[:, 1000:9000], ng2_array=ng2_array[:, 1000:9000],
    #          ng3_array=ng3_array[:, 1000:9000])

    # Caculate LFP
    V_mean_1 = np.mean(ng1_array, axis=0)
    V_mean_2 = np.mean(ng2_array, axis=0)
    V_mean_3 = np.mean(ng3_array, axis=0)

    fig1 = plt.figure(figsize=(6, 8), dpi=100)
    plt.title('正常', fontdict={'family': 'SimHei', 'size': 14})
    plt.subplot(311)
    plt.plot(V_mean_1, c='k', linewidth=2)
    # plt.xlim(2000, t_span)
    # plt.ylim(-70, -45)
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.ylabel('ng1', fontdict={'family': 'SimHei', 'size': 14})
    plt.subplot(312)
    plt.plot(V_mean_2, c='k', linewidth=2)
    # plt.xlim(2000, t_span)
    # plt.ylim(-70, -54)
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.ylabel('ng1', fontdict={'family': 'SimHei', 'size': 14})
    plt.subplot(313)
    plt.plot(V_mean_3, c='k', linewidth=2)
    # plt.xlim(2000, t_span)
    # plt.ylim(-70, -40)
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.ylabel('ng1', fontdict={'family': 'SimHei', 'size': 14})
    # plt.show()

    sampling_rate = 256
    wavename = 'cgau8'
    totalscal = 50
    fc = pywt.central_frequency(wavename)
    cparam = 2 * fc * totalscal
    scales = cparam / np.arange(totalscal, 1, -1)
    [cwtmatr1, frequencies1] = pywt.cwt(0.5*(V_mean_1+V_mean_2), scales, wavename, 1.0 / sampling_rate)
    # [cwtmatr2, frequencies2] = pywt.cwt(V_mean_2, scales, wavename, 1.0 / sampling_rate)
    [cwtmatr3, frequencies3] = pywt.cwt(V_mean_3, scales, wavename, 1.0 / sampling_rate)
    fig2 = plt.figure(figsize=(6, 8), dpi=100)
    plt.subplot(311)
    plt.plot(input3, c='k', linewidth=2)
    plt.subplot(312)
    plt.contourf(range(t_span), frequencies1, abs(cwtmatr1))
    # plt.subplot(413)
    # plt.contourf(range(t_span), frequencies1, abs(cwtmatr2))
    plt.subplot(313)
    plt.contourf(range(t_span), frequencies1, abs(cwtmatr3))
