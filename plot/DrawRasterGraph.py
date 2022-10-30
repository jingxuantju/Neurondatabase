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

if __name__ == '__main__':


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

    t_span = len(input1n)
    # IstimC1 = [0 for i in range(100)]

    Isyn0 = 1
    Isyn1 = 1
    Isyn2 = 1
    Isyn3 = 1
    a = 0.02
    b = 0.24
    c = -65
    d = 10
    manager = Manager()
    comp0 = IzhikevichNeuron(manager, 'comp0', Isyn0, a, b, c, d)
    comp1 = IzhikevichNeuron(manager, 'comp1', Isyn1, a, b, c, d)
    comp2 = IzhikevichNeuron(manager, 'comp2', Isyn2, a, b, c, d)
    comp3 = IzhikevichNeuron(manager, 'comp3', Isyn3, a, b, c, d)
    IstimC0 = IstimComponent(manager, 'Istim0', copy.deepcopy(input1n))
    manager.link_output_input(IstimC0, comp0, tab='I')
    IstimC1 = IstimComponent(manager, 'Istim1', copy.deepcopy(input2n))
    manager.link_output_input(IstimC1, comp1, tab='I')
    IstimC2 = IstimComponent(manager, 'Istim2', copy.deepcopy(input3n))
    manager.link_output_input(IstimC2, comp2, tab='I')
    IstimC3 = IstimComponent(manager, 'Istim3', copy.deepcopy(input4n))
    manager.link_output_input(IstimC3, comp3, tab='I')
    result = manager.start_stimulation(t_span)
    COMP0_v = []
    COMP1_v = []
    COMP2_v = []
    COMP3_v = []
    # COMP0_u = []
    # COMP1_u = []
    # COMP2_u = []
    for dictionary in result:
        COMP0_v.append(dictionary['comp0'][0])
        COMP1_v.append(dictionary['comp1'][0])
        COMP2_v.append(dictionary['comp2'][0])
        COMP3_v.append(dictionary['comp3'][0])
        # COMP0_u.append(dictionary['comp0'][1])
        # COMP1_u.append(dictionary['comp1'][1])
        # COMP2_u.append(dictionary['comp2'][1])

    fig1 = plt.figure(figsize=(9, 4))
    grid = plt.GridSpec(3, 2, top=0.9, bottom=0.15, wspace=0.5, hspace=0.1)
    plt.subplot(grid[0, 0])
    plt.plot(input1)
    plt.axis('off')
    plt.subplot(grid[1:3, 0])
    plt.plot(COMP0_v, linewidth=1, c='k')
    plt.ylabel("膜电位(mV)", fontdict={'family': 'SimHei', 'size': 14})
    plt.xlabel("时间(ms)", fontdict={'family': 'SimHei', 'size': 14})
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.subplot(grid[0, 1])
    plt.plot(input2)
    plt.axis('off')
    plt.subplot(grid[1:3, 1])
    plt.plot(COMP1_v, linewidth=1, c='k')
    plt.ylabel("膜电位(mV)", fontdict={'family': 'SimHei', 'size': 14})
    plt.xlabel("时间(ms)", fontdict={'family': 'SimHei', 'size': 14})
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)

    fig2 = plt.figure(figsize=(9, 4))
    plt.subplot(grid[0, 0])
    plt.plot(input3)
    plt.axis('off')
    plt.subplot(grid[1:3, 0])
    plt.plot(COMP2_v, linewidth=1, c='k')
    plt.ylabel("膜电位(mV)", fontdict={'family': 'SimHei', 'size': 14})
    plt.xlabel("时间(ms)", fontdict={'family': 'SimHei', 'size': 14})
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.subplot(grid[0, 1])
    plt.plot(input4)
    plt.axis('off')
    plt.subplot(grid[1:3, 1])
    plt.plot(COMP3_v, linewidth=1, c='k')
    plt.ylabel("膜电位(mV)", fontdict={'family': 'SimHei', 'size': 14})
    plt.xlabel("时间(ms)", fontdict={'family': 'SimHei', 'size': 14})
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)