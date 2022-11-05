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
    num = 10
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
        IstimC1[i] = IstimComponent(manager, 'IstimC1' + str(i), copy.deepcopy(input3n))
        manager.link_output_input(IstimC1[i], ng1[i], tab='I')
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
        IstimC2[i] = IstimComponent(manager, 'IstimC2' + str(i), copy.deepcopy(input3n))
        manager.link_output_input(IstimC2[i], ng2[i], tab='I')
    for i in range(num):
        for j in range(num):
            a1 = random.randint(0, 9)
            a2 = random.randint(0, 9)
            a3 = random.randint(0, 9)
            if (a1 < 4):
                manager.link_output_input(ng1_syn_ng1[i], ng1[j], tab='I')
                manager.link_output_input(ng1[j], ng1_syn_ng1[i], tab='houmo')
            if (a2 < 4):
                manager.link_output_input(ng1_syn_ng2[i], ng2[j], tab='I')
                manager.link_output_input(ng2[j], ng1_syn_ng2[i], tab='houmo')
            if (a3 < 4):
                manager.link_output_input(ng1_syn_ng3[i], ng3[j], tab='I')
                manager.link_output_input(ng3[j], ng1_syn_ng3[i], tab='houmo')
            b1 = random.randint(0, 9)
            b2 = random.randint(0, 9)
            b3 = random.randint(0, 9)
            if (a2 < 4):
                manager.link_output_input(ng2_syn_ng2[i], ng2[j], tab='I')
                manager.link_output_input(ng2[j], ng2_syn_ng2[i], tab='houmo')
            if (a3 < 4):
                manager.link_output_input(ng2_syn_ng3[i], ng3[j], tab='I')
                manager.link_output_input(ng3[j], ng2_syn_ng3[i], tab='houmo')
            if (a1 < 4):
                manager.link_output_input(ng2_syn_ng1[i], ng1[j], tab='I')
                manager.link_output_input(ng1[j], ng2_syn_ng1[i], tab='houmo')
            c1 = random.randint(0, 9)
            c2 = random.randint(0, 9)
            c3 = random.randint(0, 9)
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
    COMP4_RESULT = []
    COMP5_RESULT = []
    COMP6_RESULT = []
    COMP7_RESULT = []
    for dictionary in result:
        # COMP4_RESULT.append(dictionary['soma1'])
        # COMP4_RESULT.append(dictionary['comp1'][0])
        # COMP5_RESULT.append(dictionary['comp1'][1])
        # COMP6_RESULT.append(dictionary['comp1'][2])
        # COMP7_RESULT.append(dictionary['comp1'][3])
        COMP4_RESULT.append(dictionary['ng11'][0])
        COMP5_RESULT.append(dictionary['ng21'][0])
        COMP6_RESULT.append(dictionary['ng31'][0])
    figure = plt.figure()
    plt.plot(COMP4_RESULT)
    plt.plot(COMP5_RESULT)
    plt.plot(COMP6_RESULT)
    # line1, = plt.plot(COMP4_RESULT, COMP5_RESULT, color='black')
    # line2, = plt.plot(COMP5_RESULT)
    # line3, = plt.plot(COMP6_RESULT)
    # plt.legend(handles = [line1, line2,line3 ],labels = ['m','h','n'],loc = 'upper right', fontsize=16)
    plt.xlabel('时间(ms)', fontsize=20)  # label = name of label
    plt.title('(a)')
    figure.show()
    plt.show()
    print(result)