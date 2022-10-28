from simulink.component import Component, Manager
import math
import numpy as np
from neuron.neuron import *
from pylab import *
from neuron.layer import *
import scipy.io as scio
import copy
import cv2
from scipy import misc
import imageio
import matplotlib.gridspec as gridspec


if __name__ == '__main__':
    dt = 0.1
    t_span = 3000
    real_t_span = 300


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
    para_exc_exc = [random.uniform(0,0.65) for i in range(num)]
    para_exc_inh = [random.uniform(0,2) for i in range(num)]
    para_inh_exc = [random.uniform(-1.7,-0.8) for i in range(num)]
    para_inh_inh = [random.uniform(-1.1,-0.3) for i in range(num)]


    manager = Manager()
    for i in range(num):
        ng1[i] = IzhikevichNeuron1(manager, 'ng1' + str(i), 10, 0.02, 0.24, -65, 10)
        ng1_syn_ng1[i] = ExcsynapseNeuron(manager, 'ng1_syn_ng1' + str(i), para_exc_exc)
        ng1_syn_ng2[i] = ExcsynapseNeuron(manager, 'ng1_syn_ng2' + str(i), para_exc_exc)
        ng1_syn_ng3[i] = ExcsynapseNeuron(manager, 'ng1_syn_ng3' + str(i), para_exc_inh)
        manager.link_output_input(ng1[i], ng1_syn_ng1[i])
        manager.link_output_input(ng1[i], ng1_syn_ng2[i])
        manager.link_output_input(ng1[i], ng1_syn_ng3[i])
        ng2[i] = IzhikevichNeuron1(manager, 'ng2' + str(i), 10, 0.02, 0.24, -65, 10)
        ng2_syn_ng2[i] = ExcsynapseNeuron(manager, 'ng2_syn_ng2' + str(i), para_exc_exc)
        ng2_syn_ng3[i] = ExcsynapseNeuron(manager, 'ng2_syn_ng3' + str(i), para_exc_inh)
        ng2_syn_ng1[i] = ExcsynapseNeuron(manager, 'ng2_syn_ng1' + str(i), para_exc_exc)
        manager.link_output_input(ng2[i], ng2_syn_ng2[i])
        manager.link_output_input(ng2[i], ng2_syn_ng3[i])
        manager.link_output_input(ng2[i], ng2_syn_ng1[i])
        ng3[i] = IzhikevichNeuron1(manager, 'ng3' + str(i), 1, 0.01, 0.25, -65, 1)
        ng3_syn_ng3[i] = ExcsynapseNeuron(manager, 'ng3_syn_ng3' + str(i), para_inh_inh, tao=1)
        ng3_syn_ng1[i] = ExcsynapseNeuron(manager, 'ng3_syn_ng1' + str(i), para_inh_exc, tao=1)
        ng3_syn_ng2[i] = ExcsynapseNeuron(manager, 'ng3_syn_ng2' + str(i), para_inh_exc, tao=1)
        manager.link_output_input(ng3[i], ng3_syn_ng3[i])
        manager.link_output_input(ng3[i], ng3_syn_ng1[i])
        manager.link_output_input(ng3[i], ng3_syn_ng2[i])
    for i in range(num):
        for j in range(num):
            a1 = random.randint(0,10)
            a2 = random.randint(0,10)
            a3 = random.randint(0,10)
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

    # np.savez('ng_v', ng1_array=ng1_array[:, 1000:t_span], ng2_array=ng2_array[:, 1000:t_span],
    #          ng3_array=ng3_array[:, 1000:t_span])

    np.savez('ng_v', ng1_array=ng1_array[:, 1000:t_span], ng2_array=ng2_array[:, 1000:t_span],
             ng3_array=ng3_array[:, 1000:t_span])

    SPK_ng1 = np.where(ng1_array > 10, 1, 0)
    SPK_ng2 = np.where(ng2_array > 10, 1, 0)
    SPK_ng3 = np.where(ng3_array > 10, 1, 0)

    # Get the index of a scatter map
    indexX_1 = []
    indexY_1 = []
    indexX_2 = []
    indexY_2 = []
    indexX_3 = []
    indexY_3 = []
    for j in range(100):
        # for t in range(2000, t_span):
        for t in range(t_span):
            if SPK_ng1[j][t] == 1:
                indexX_1.append(t)
                indexY_1.append(j)
        for t in range(t_span):
            if SPK_ng2[j][t] == 1:
                indexX_2.append(t)
                indexY_2.append(j)
        for t in range(t_span):
            if SPK_ng3[j][t] == 1:
                indexX_3.append(t)
                indexY_3.append(j)

    xr = range(2000, t_span, 2000)
    fig5 = plt.figure(figsize=(6, 8), dpi=100)
    gs = gridspec.GridSpec(15, 2)
    plt.subplot(311)
    # plt.title('(a) pd=0')
    line1 = plt.scatter(indexX_1, indexY_1, s=2, c='k')
    plt.xlim(2000, t_span)
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.xticks(xr, range(200, real_t_span, 200))
    plt.ylabel('ng1', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
    plt.subplot(312)
    line3 = plt.scatter(indexX_3, indexY_3, s=2, c='k')
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.xlim(2000, t_span)
    plt.xticks(xr, range(200, real_t_span, 200))
    plt.ylabel('ng2', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
    plt.subplot(313)
    # plt.title('(b) pd=0')
    line2 = plt.scatter(indexX_3, indexY_3, s=2, c='k')
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.xlim(2000, t_span)
    plt.xticks(xr, range(200, real_t_span, 200))
    plt.ylabel('ng3', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label














