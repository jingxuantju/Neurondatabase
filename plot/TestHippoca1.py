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



if __name__ == '__main__':
    dt = 0.1
    t_span = 10000
    real_t_span = 900
    taot_sn_ge = 2 / dt
    taot_ge_ge = 6 / dt
    taot_ge_gi = 6 / dt
    taot_sn_gi = 2 / dt
    taot_ge_sn = 6 / dt
    taot_gi_tc = 6 / dt
    gsn_ge = 0.075
    gsn_gi = 0.075
    gge_ge = 0.025
    gge_gi = 0.015
    gge_sn = 0.025
    ggi_tc = 0.202

    # 1 2 4 5 Exc, 3 inh
    num = 20
    para_exc_exc = [random.uniform(0,0.65) for i in range(num)]
    para_exc_inh = [random.uniform(0,2) for i in range(num)]
    para_inh_exc = [random.uniform(-1.7,-0.8) for i in range(num)]
    para_inh_inh = [random.uniform(-1.1,-0.3) for i in range(num)]

    ng1 = [0 for i in range(num)]
    ng1_syn_ng1 = [0 for i in range(num)]
    ng1_syn_ng2 = [0 for i in range(num)]
    ng1_syn_ng3 = [0 for i in range(num)]
    ng2 = [0 for i in range(num)]
    ng2_syn_ng2 = [gge_sn for i in range(num)]
    ng2_syn_ng3 = [gge_sn for i in range(num)]
    ng2_syn_ng1 = [gge_sn for i in range(num)]

    ng4 = [0 for i in range(num)]
    ng4_syn_ng4 = [0 for i in range(num)]
    ng4_syn_ng5 = [0 for i in range(num)]
    ng4_syn_ng3 = [0 for i in range(num)]
    ng5 = [0 for i in range(num)]
    ng5_syn_ng5 = [gge_sn for i in range(num)]
    ng5_syn_ng3 = [gge_sn for i in range(num)]
    ng5_syn_ng4 = [gge_sn for i in range(num)]

    ng3 = [0 for i in range(num)]
    ng3_syn_ng3 = [gge_sn for i in range(num)]
    ng3_syn_ng1 = [gge_sn for i in range(num)]
    ng3_syn_ng2 = [gge_sn for i in range(num)]
    para_gpi_tc = [ggi_tc for i in range(num)]



    manager = Manager()
    for i in range(num):
        ng1[i] = IzhikevichNeuron(manager, 'ng1' + str(i), 3, 0.02, 0.24, -65, 10)
        ng1_syn_ng1[i] = ExcsynapseNeuron(manager, 'ng1_syn_ng1' + str(i), para_exc_exc)
        ng1_syn_ng2[i] = ExcsynapseNeuron(manager, 'ng1_syn_ng2' + str(i), para_exc_exc)
        ng1_syn_ng3[i] = ExcsynapseNeuron(manager, 'ng1_syn_ng3' + str(i), para_exc_inh)
        manager.link_output_input(ng1[i], ng1_syn_ng1[i])
        manager.link_output_input(ng1[i], ng1_syn_ng2[i])
        manager.link_output_input(ng1[i], ng1_syn_ng3[i])
        ng2[i] = IzhikevichNeuron(manager, 'ng2' + str(i), 3, 0.02, 0.24, -65, 10)
        ng2_syn_ng2[i] = ExcsynapseNeuron(manager, 'ng2_syn_ng2' + str(i), para_exc_exc)
        ng2_syn_ng3[i] = ExcsynapseNeuron(manager, 'ng2_syn_ng3' + str(i), para_exc_inh)
        ng2_syn_ng1[i] = ExcsynapseNeuron(manager, 'ng2_syn_ng1' + str(i), para_exc_exc)
        manager.link_output_input(ng2[i], ng2_syn_ng2[i])
        manager.link_output_input(ng2[i], ng2_syn_ng3[i])
        manager.link_output_input(ng2[i], ng2_syn_ng1[i])
        ng4[i] = IzhikevichNeuron(manager, 'ng4' + str(i), 3, 0.02, 0.24, -65, 10)
        ng4_syn_ng4[i] = ExcsynapseNeuron(manager, 'ng4_syn_ng4' + str(i), para_exc_exc)
        ng4_syn_ng5[i] = ExcsynapseNeuron(manager, 'ng4_syn_ng5' + str(i), para_exc_exc)
        ng4_syn_ng3[i] = ExcsynapseNeuron(manager, 'ng4_syn_ng3' + str(i), para_exc_inh)
        manager.link_output_input(ng1[i], ng1_syn_ng1[i])
        manager.link_output_input(ng1[i], ng1_syn_ng2[i])
        manager.link_output_input(ng1[i], ng1_syn_ng3[i])
        ng5[i] = IzhikevichNeuron(manager, 'ng5' + str(i), 3, 0.02, 0.24, -65, 10)
        ng5_syn_ng5[i] = ExcsynapseNeuron(manager, 'ng5_syn_ng5' + str(i), para_exc_exc)
        ng5_syn_ng3[i] = ExcsynapseNeuron(manager, 'ng5_syn_ng3' + str(i), para_exc_inh)
        ng5_syn_ng4[i] = ExcsynapseNeuron(manager, 'ng5_syn_ng4' + str(i), para_exc_exc)
        manager.link_output_input(ng2[i], ng2_syn_ng2[i])
        manager.link_output_input(ng2[i], ng2_syn_ng3[i])
        manager.link_output_input(ng2[i], ng2_syn_ng1[i])

        ng3[i] = IzhikevichNeuron(manager, 'ng3' + str(i), 3, 0.01, 0.25, -65, 0.8)
        ng3_syn_ng3[i] = ExcsynapseNeuron(manager, 'ng3_syn_ng3' + str(i), para_inh_inh, tao=3)
        ng3_syn_ng1[i] = ExcsynapseNeuron(manager, 'ng3_syn_ng1' + str(i), para_inh_exc, tao=3)
        ng3_syn_ng2[i] = ExcsynapseNeuron(manager, 'ng3_syn_ng2' + str(i), para_inh_exc, tao=3)
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
            d1 = random.randint(0, 10)
            d2 = random.randint(0, 10)
            d3 = random.randint(0, 10)
            if (d1 < 4):
                manager.link_output_input(ng4_syn_ng4[i], ng4[j], tab='I')
                manager.link_output_input(ng4[j], ng4_syn_ng4[i], tab='houmo')
            if (d2 < 4):
                manager.link_output_input(ng4_syn_ng5[i], ng4[j], tab='I')
                manager.link_output_input(ng4[j], ng4_syn_ng5[i], tab='houmo')
            if (d3 < 4):
                manager.link_output_input(ng4_syn_ng3[i], ng3[j], tab='I')
                manager.link_output_input(ng3[j], ng4_syn_ng3[i], tab='houmo')
            e1 = random.randint(0, 10)
            e2 = random.randint(0, 10)
            e3 = random.randint(0, 10)
            if (e1 < 4):
                manager.link_output_input(ng5_syn_ng5[i], ng5[j], tab='I')
                manager.link_output_input(ng5[j], ng5_syn_ng5[i], tab='houmo')
            if (e2 < 4):
                manager.link_output_input(ng5_syn_ng4[i], ng4[j], tab='I')
                manager.link_output_input(ng4[j], ng5_syn_ng4[i], tab='houmo')
            if (e3 < 4):
                manager.link_output_input(ng5_syn_ng3[i], ng3[j], tab='I')
                manager.link_output_input(ng3[j], ng5_syn_ng3[i], tab='houmo')

    result = manager.start_stimulation(t_span)
    ng1_RESULT = []
    ng2_RESULT = []
    ng4_RESULT = []
    ng5_RESULT = []
    ng3_RESULT = []
    for j in range(num):
        ng1_R = []
        ng2_R = []
        ng3_R = []
        ng4_R = []
        ng5_R = []
        for dictionary in result:
            ng1_R.append(dictionary['ng1' + str(j)][0])
            ng2_R.append(dictionary['ng2' + str(j)][0])
            ng3_R.append(dictionary['ng3' + str(j)][0])
            ng4_R.append(dictionary['ng4' + str(j)][0])
            ng5_R.append(dictionary['ng5' + str(j)][0])
        ng1_RESULT.append(ng1_R)
        ng2_RESULT.append(ng2_R)
        ng3_RESULT.append(ng3_R)
        ng4_RESULT.append(ng4_R)
        ng5_RESULT.append(ng5_R)

    ng1_array = np.array(ng1_RESULT)
    ng2_array = np.array(ng2_RESULT)
    ng3_array = np.array(ng3_RESULT)
    ng4_array = np.array(ng4_RESULT)
    ng5_array = np.array(ng5_RESULT)

    np.savez('ng_v5', ng1_array=ng1_array, ng2_array=ng2_array, ng4_array=ng4_array, ng5_array=ng5_array,
             ng3_array=ng3_array)

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
    for j in range(num):
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

    # xr = range(2000, t_span, 2000)
    # fig5 = plt.figure(figsize=(6, 8), dpi=100)
    # gs = gridspec.GridSpec(15, 2)
    # plt.subplot(311)
    # # plt.title('(a) pd=0')
    # line1 = plt.scatter(indexX_1, indexY_1, s=2, c='k')
    # plt.xlim(2000, t_span)
    # plt.yticks(fontproperties='Times New Roman', size=14)
    # plt.xticks(fontproperties='Times New Roman', size=14)
    # plt.xticks(xr, range(200, real_t_span, 200))
    # plt.ylabel('ng1', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
    # plt.subplot(312)
    # line3 = plt.scatter(indexX_3, indexY_3, s=2, c='k')
    # plt.yticks(fontproperties='Times New Roman', size=14)
    # plt.xticks(fontproperties='Times New Roman', size=14)
    # plt.xlim(2000, t_span)
    # plt.xticks(xr, range(200, real_t_span, 200))
    # plt.ylabel('ng2', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
    # plt.subplot(313)
    # # plt.title('(b) pd=0')
    # line2 = plt.scatter(indexX_3, indexY_3, s=2, c='k')
    # plt.yticks(fontproperties='Times New Roman', size=14)
    # plt.xticks(fontproperties='Times New Roman', size=14)
    # plt.xlim(2000, t_span)
    # plt.xticks(xr, range(200, real_t_span, 200))
    # plt.ylabel('ng3', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label














