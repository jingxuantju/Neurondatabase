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
    Isyn0 = 0
    Isyn1 = 1
    Isyn2 = 10
    a = 0.01
    b = 0.26
    c = -55
    d = 3
    manager = Manager()
    comp0 = IzhikevichNeuron(manager, 'comp0', Isyn0, a, b, c, d)
    comp1 = IzhikevichNeuron(manager, 'comp1', Isyn1, a, b, c, d)
    comp2 = IzhikevichNeuron(manager, 'comp2', Isyn2, a, b, c, d)
    result = manager.start_stimulation(2000)
    COMP0_v = []
    COMP1_v = []
    COMP2_v = []
    COMP0_u = []
    COMP1_u = []
    COMP2_u = []
    for dictionary in result:
        COMP0_v.append(dictionary['comp0'][0])
        COMP1_v.append(dictionary['comp1'][0])
        COMP2_v.append(dictionary['comp2'][0])
        COMP0_u.append(dictionary['comp0'][1])
        COMP1_u.append(dictionary['comp1'][1])
        COMP2_u.append(dictionary['comp2'][1])

    v1=np.linspace(-90, -30, 10000)
    v2=np.linspace(-90, 30, 10000)
    u0a = 0.04 * v1 * v1 + 5 * v1 + 140 + Isyn0
    u1a = 0.04 * v1 * v1 + 5 * v1 + 140 + Isyn1
    u2a = 0.04 * v1 * v1 + 5 * v1 + 140 + Isyn2
    ub = b * v2

    fig1 = plt.figure(figsize=(15, 5), dpi=100)
    plt.subplot(131)
    plt.title('I=0(mA)', fontdict={'family': 'Times New Roman', 'size': 14})
    plt.plot(v1, u0a, label="电压v零线",c='k', linewidth=2)
    plt.plot(v2, ub, label="恢复变量u零线",c='b', linewidth=2)
    plt.plot(COMP0_v, COMP0_u, label="相轨迹",c='r', linewidth=2)
    plt.legend(prop={'family': 'SimHei', 'size': 14})
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.xlim(-91, 31)
    plt.ylim(-41, 31)
    plt.subplot(132)
    plt.title('I=1(mA)', fontdict={'family': 'Times New Roman', 'size': 14})
    plt.plot(v1, u1a, label="电压v零线",c='k', linewidth=2)
    plt.plot(v2, ub, label="恢复变量u零线",c='b', linewidth=2)
    plt.plot(COMP1_v, COMP1_u, label="相轨迹",c='r', linewidth=2)
    plt.legend(prop={'family': 'SimHei', 'size': 14})
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.xlim(-91, 31)
    plt.ylim(-41, 31)
    plt.subplot(133)
    plt.title('I=10(mA)', fontdict={'family': 'Times New Roman', 'size': 14})
    plt.plot(v1, u2a, label="电压v零线",c='k', linewidth=2)
    plt.plot(v2, ub, label="恢复变量u零线",c='b', linewidth=2)
    plt.plot(COMP2_v, COMP2_u, label="相轨迹",c='r', linewidth=2)
    plt.legend(prop={'family': 'SimHei', 'size': 14})
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.xlim(-91, 31)
    plt.ylim(-41, 31)