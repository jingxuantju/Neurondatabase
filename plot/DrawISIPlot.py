# libraries & dataset
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.io as scio
from neuron.neuron import *

def fun_calDiff(data):
    data_diff = []
    for i in range(len(data) - 1):
        data_diff.append(data[i + 1] - data[i])

    return data_diff

if __name__ == '__main__':
    SpikeFile = 'spknew.mat'
    data = scio.loadmat(SpikeFile)
    Spike2 = data['spk2']

    # Gen a Iz sequence
    # manager=Manager()
    # comp1 = IzhikevichNeuron(manager, 'comp', 10, 0.02, 0.2, -50, 2)
    #
    # result = manager.start_stimulation(2000)
    # COMP4_RESULT = []
    # COMP4_RESULT_PULSE = []
    # for dictionary in result:
    #     COMP4_RESULT.append(dictionary['comp'][0])
    #     if dictionary['comp'][0] >= 5:
    #         COMP4_RESULT_PULSE.append(1)
    #     else:
    #         COMP4_RESULT_PULSE.append(0)

    # Load Basal
    n0 = np.load('pd0.npz')
    V_STN_array = n0['V_STN_array']
    V_GPE_array = n0['V_GPE_array']
    V_GPI_array = n0['V_GPI_array']
    V_TH_array = n0['V_TH_array']
    t_span = 12000
    real_t_span = 1200
    data_t_span = len(V_STN_array)

    SPK_STN = np.where(V_STN_array > 10, 1, 0)
    SPK_GPE = np.where(V_GPE_array > 10, 1, 0)
    SPK_GPI = np.where(V_GPI_array > 10, 1, 0)
    SPK_TH = np.where(V_TH_array > 10, 1, 0)

    Splot = 0
    Lplot = 1
    Nneuron = 10
    lw = 0.3
    if (Splot):
        plt.scatter(0, 0, s=2, c='b', label="GPE")
        plt.scatter(0, 0, s=2, c='r', label="STN")
        plt.scatter(0, 0, s=2, c='g', label="GPI")
        plt.scatter(0, 0, s=2, c='y', label="TC")
    if (Lplot):
        plt.plot([0, 0], [0.01, 0.01], c='lightsalmon', linewidth=lw, label="STN")
        plt.plot([0, 0], [0.01, 0.01], c='lightskyblue', linewidth=lw, label="GPE")
        plt.plot([0, 0], [0.01, 0.01], c='plum', linewidth=lw, label="GPI")
        plt.plot([0, 0], [0.01, 0.01], c='lightgreen', linewidth=lw, label="TC")
    for i in range(Nneuron):
        s2_idx = np.nonzero(SPK_STN[i, :])
        idzero = [0]
        ids = s2_idx[0].tolist()
        idall = np.hstack((idzero, ids))
        idy = np.diff(idall)
        if(Lplot):
            plt.plot(s2_idx[0], idy, c='lightsalmon', linewidth=lw)
        if (Splot):
            for indexs in s2_idx:
                plt.scatter(indexs, idy, s=2, c='r')
    for i in range(Nneuron):
        s2_idx = np.nonzero(SPK_GPE[i, :])
        idzero = [0]
        ids = s2_idx[0].tolist()
        idall = np.hstack((idzero, ids))
        idy = np.diff(idall)
        if (Lplot):
            plt.plot(s2_idx[0], idy, c='lightskyblue', linewidth=lw)
        if (Splot):
            for indexs in s2_idx:
                plt.scatter(indexs, idy, s=2, c='b')
    for i in range(Nneuron):
        s2_idx = np.nonzero(SPK_GPI[i, :])
        idzero = [0]
        ids = s2_idx[0].tolist()
        idall = np.hstack((idzero, ids))
        idy = np.diff(idall)
        if (Lplot):
            plt.plot(s2_idx[0], idy, c='plum', linewidth=lw)
        if (Splot):
            for indexs in s2_idx:
                plt.scatter(indexs, idy, s=2, c='g')
    for i in range(Nneuron):
        s2_idx = np.nonzero(SPK_TH[i, :])
        idzero = [0]
        ids = s2_idx[0].tolist()
        idall = np.hstack((idzero, ids))
        idy = np.diff(idall)
        if (Lplot):
            plt.plot(s2_idx[0], idy, c='lightgreen', linewidth=lw)
        if (Splot):
            for indexs in s2_idx:
                plt.scatter(indexs, idy, s=2, c='y')
    # s2_idxs = []
    # for i in range(1):
    #     s2_idx = np.nonzero(Spike2[i, :])
    #     s2_idxs.append(s2_idx)
    #     idzero = [0]
    #     ids = s2_idx[0].tolist()
    #     idall = np.hstack((idzero, ids))
    #     idy = np.diff(idall)
    #     for indexs in s2_idx:
    #         plt.scatter(indexs, idy, s=2, c='k')

    plt.ylabel('ISI时间（ms）', fontdict={'family': 'SimHei', 'size': 14})
    plt.xlabel('时间（ms）', fontdict={'family': 'SimHei', 'size': 14})
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.title('ISI', fontdict={'family': 'SimHei', 'size': 16})
    font1 = {'family': 'Times New Roman', 'size': 16}
    legend = plt.legend(prop=font1)


