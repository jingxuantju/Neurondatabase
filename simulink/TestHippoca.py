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



if __name__ == '__main__':
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
        ng3[i] = IzhikevichNeuron1(manager, 'ng3' + str(i), 2, 0.01, 0.25, -65, 1)
        ng3_syn_ng3[i] = ExcsynapseNeuron(manager, 'ng3_syn_ng3' + str(i), para_inh_inh, tao=6)
        ng3_syn_ng1[i] = ExcsynapseNeuron(manager, 'ng3_syn_ng1' + str(i), para_inh_exc, tao=6)
        ng3_syn_ng2[i] = ExcsynapseNeuron(manager, 'ng3_syn_ng2' + str(i), para_inh_exc, tao=6)
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

    result = manager.start_stimulation(3000)
    COMP4_RESULT = []
    COMP5_RESULT = []
    COMP6_RESULT = []
    COMP4_RESULT_PULSE = []
    COMP5_RESULT_PULSE = []
    COMP6_RESULT_PULSE = []
    for dictionary in result:
        COMP4_RESULT.append(dictionary['ng11'][0])
    figure = plt.figure()
    # plt.plot(COMP4_RESULT)
    line1, = plt.plot(COMP4_RESULT)
    # line2, = plt.plot(COMP5_RESULT)
    # line3, = plt.plot(COMP6_RESULT)
    # plt.legend(handles=[line1, line2, line3], labels=['第一层', '第二层', '第三层'], loc='upper left', fontsize=14)
    plt.xlabel('时间(ms)', fontsize=18)  # label = name of label
    # plt.ylabel('电流(mA)', fontsize=18)  # label = name of label
    plt.ylabel('电压(mV)', fontsize=18)  # label = name of label
    figure.show()
    plt.show()
    print(result)














