from neuron.neuron import *
import matplotlib.pyplot as plt
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimSun']
matplotlib.rcParams['axes.unicode_minus']=False
import random
from scipy.sparse import csr_matrix
from scipy.signal import find_peaks
import numpy as np


if __name__ == '__main__':
    class SelfAddingUnit(Component):
        def __init__(self, living_dictionary: dict, name):
            super(SelfAddingUnit, self).__init__(living_dictionary, name=name)
            self.hidden = 0

        def function(self):
            self.hidden += 1
            self.output = self.hidden
            return self.output


    manager = Manager()
    comp = [[0 for i in range(100)] for j in range(3)]
    syn = [[0 for i in range(100)] for j in range(3)]
    para1 = []
    para2 = []
    for i in range(100):
        para1.append(0.005)
        para2.append(0.015)
    for i in range(3):
        for j in range(100):
            if (i == 0):
                a = random.randint(0, 4)
                if (a != 0):
                    comp[i][j] = IzhikevichNeuron(manager, 'comp' + str(i) + str(j), 10, 0.02, 0.2, -65, 2)
                else:
                    comp[i][j] = IzhikevichNeuron(manager, 'comp' + str(i) + str(j), 10, 0.1, 0.2, -65, 8)
                syn[i][j] = synapseNeuron(manager, 'syn' + str(i) + str(j), para1)
            else:
                if (a != 0):
                    comp[i][j] = IzhikevichNeuron(manager, 'comp' + str(i) + str(j), 0, 0.02, 0.2, -50, 2)
                else:
                    comp[i][j] = IzhikevichNeuron(manager, 'comp' + str(i) + str(j), 0, 0.1, 0.2, -65, 8)
                syn[i][j] = synapseNeuron(manager, 'syn' + str(i) + str(j), para2)
    for i in range(2):
        for j in range(100):
            manager.link_output_input(comp[i][j], syn[i][j])
            for k in range(100):
                a = random.randint(0, 5)
                if (a == 0):
                    manager.link_output_input(syn[i][j], comp[i+1][k], tab='I')
                    manager.link_output_input(comp[i+1][k], syn[i][j], tab='houmo')
    result = manager.start_stimulation(2000)

    # Full martix
    L1_RESULT_A = []
    L2_RESULT_A = []
    L3_RESULT_A = []
    L1_RESULT_PULSE_A = []
    L2_RESULT_PULSE_A = []
    L3_RESULT_PULSE_A = []
    for j in range(100):
        L1_RESULT = []
        L2_RESULT = []
        L3_RESULT = []
        L1_RESULT_PULSE = []
        L2_RESULT_PULSE = []
        L3_RESULT_PULSE = []
        L1_RESULT_A.append(L1_RESULT)
        L2_RESULT_A.append(L2_RESULT)
        L3_RESULT_A.append(L3_RESULT)
        L1_RESULT_PULSE_A.append(L1_RESULT_PULSE)
        L2_RESULT_PULSE_A.append(L2_RESULT_PULSE)
        L3_RESULT_PULSE_A.append(L3_RESULT_PULSE)
        for dictionary in result:
            L1_RESULT.append(dictionary['comp0'+ str(j)][0])
            if dictionary['comp0'+ str(j)][0] >= 5:
                L1_RESULT_PULSE.append(1)
            else:
                L1_RESULT_PULSE.append(0)
            L2_RESULT.append(dictionary['comp1'+ str(j)][0])
            if dictionary['comp1'+ str(j)][0] >= 5:
                L2_RESULT_PULSE.append(1)
            else:
                L2_RESULT_PULSE.append(0)
            L3_RESULT.append(dictionary['comp2'+ str(j)][0])
            if dictionary['comp2'+ str(j)][0] >= 5:
                L3_RESULT_PULSE.append(1)
            else:
                L3_RESULT_PULSE.append(0)

    # Sprase martix
    # L1 = csr_matrix(L1_RESULT_PULSE_A)
    # L2 = csr_matrix(L2_RESULT_PULSE_A)
    # L3 = csr_matrix(L2_RESULT_PULSE_A)
    L1_x = []
    L1_y = []
    L2_x = []
    L2_y = []
    L3_x = []
    L3_y = []
    for j in range(100):
        for t in range(2000):
            if L1_RESULT_PULSE_A[j][t] == 1:
                L1_x.append(t)
                L1_y.append(j)
        for t in range(2000):
            if L2_RESULT_PULSE_A[j][t] == 1:
                L2_x.append(t)
                L2_y.append(j)
        for t in range(2000):
            if L3_RESULT_PULSE_A[j][t] == 1:
                L3_x.append(t)
                L3_y.append(j)
    # figure = plt.figure()
    # L1_RESULT = []
    # L2_RESULT = []
    # L3_RESULT = []
    # L1_RESULT_PULSEx = []
    # L2_RESULT_PULSEx = []
    # L3_RESULT_PULSEx = []
    # L1_RESULT_PULSEy = []
    # L2_RESULT_PULSEy = []
    # L3_RESULT_PULSEy = []
    # for j in range(100):
    #     for dictionary in result:
    #         t = 0
    #         L1_RESULT.append(dictionary['comp0' + str(j)][0])
    #         L2_RESULT.append(dictionary['comp1' + str(j)][0])
    #         L3_RESULT.append(dictionary['comp2' + str(j)][0])
    #         if dictionary['comp0'+ str(j)][0] >= 5:
    #             L1_RESULT_PULSEx.append(t)
    #             L1_RESULT_PULSEy.append(j)
    #         L2_RESULT.append(dictionary['comp1'+ str(j)][0])
    #         if dictionary['comp1'+ str(j)][0] >= 5:
    #             L2_RESULT_PULSEx.append(t)
    #             L2_RESULT_PULSEy.append(j)
    #         L3_RESULT.append(dictionary['comp2'+ str(j)][0])
    #         if dictionary['comp2'+ str(j)][0] >= 5:
    #             L3_RESULT_PULSEx.append(t)
    #             L3_RESULT_PULSEy.append(j)
    #         t=t+1
        # plt.subplot(131)
        # peaks1, _ = find_peaks(L1_RESULT)
        # X1 = j * np.ones((len(peaks1)))
        # line1, = plt.scatter(X1, peaks1, s=2)
        # plt.subplot(132)
        # peaks2, _ = find_peaks(L2_RESULT)
        # X2 = j * np.ones((len(peaks2)))
        # line2, = plt.scatter(X2, peaks2, s=2)
        # plt.subplot(133)
        # peaks3, _ = find_peaks(L3_RESULT)
        # X3 = j * np.ones((len(peaks3)))
        # line3, = plt.scatter(X3, peaks3, s=2)
    fig1 = plt.figure()
    # plt.subplot(131)
    line1 = plt.scatter(L1_x, L1_y, s=2)
    # plt.legend(handles=[line1, line2, line3], labels=['第一层', '第二层', '第三层'], loc='upper left', fontsize=14)
    plt.xlabel('时间(ms)', fontdict={'family': 'SimHei', 'size': 16})  # label = name of label
    plt.ylabel('神经元索引', fontdict={'family': 'SimHei', 'size': 16})  # label = name of label
    plt.title('第一层', fontdict={'family': 'SimHei', 'size': 16})
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    fig2 = plt.figure()
    # plt.subplot(132)
    line2 = plt.scatter(L2_x, L2_y, s=2)
    plt.xlabel('时间(ms)', fontdict={'family': 'SimHei', 'size': 16})  # label = name of label
    plt.ylabel('神经元索引', fontdict={'family': 'SimHei', 'size': 16})  # label = name of label
    plt.title('第二层', fontdict={'family': 'SimHei', 'size': 16})
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    fig3 = plt.figure()
    # plt.subplot(133)
    line3 = plt.scatter(L3_x, L3_y, s=2)
    # plt.legend(handles=[line1, line2, line3], labels=['第一层', '第二层', '第三层'], loc='upper left', fontsize=14)
    plt.xlabel('时间(ms)', fontdict={'family': 'SimHei', 'size': 16})  # label = name of label
    plt.ylabel('神经元索引', fontdict={'family': 'SimHei', 'size': 16})  # label = name of label
    plt.title('第三层', fontdict={'family': 'SimHei', 'size': 16})
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    #figure.tight_layout()
    plt.show()
    print(result)