from simulink.component import Component, Manager
import math
import numpy as np
from neuron.neuron import *
from pylab import *
from neuron.layer import *
import seaborn as sns
import scipy.io as scio
import copy
import random
import matplotlib.gridspec as gridspec
import cv2
from scipy import misc

# import imageio
mpl.rcParams['font.sans-serif'] = ['Times New Roman']
matplotlib.rcParams['axes.unicode_minus'] = False


if __name__ == '__main__':
    mean_ee = [0.5]
    mean_ei = [1.2]
    mean_ie = [-1.2]
    mean_ii = [-0.5]
    cov = np.eye(1) * 0.25

    weight_ee = []
    for i in range(1600):
        wee = []
        for j in range(1600):
            data = np.random.multivariate_normal(mean_ee, cov, 1)
            wee.append(data[0][0])
        weight_ee.append(wee)

    weight_ei = []
    for i in range(1600):
        wei = []
        for j in range(400):
            data = np.random.multivariate_normal(mean_ei, cov, 1)
            wei.append(data[0][0])
        weight_ei.append(wei)

    weight_ie = []
    for i in range(400):
        wie = []
        for j in range(1600):
            data = np.random.multivariate_normal(mean_ie, cov, 1)
            wie.append(data[0][0])
        weight_ie.append(wie)

    weight_ii = []
    for i in range(400):
        wii = []
        for j in range(400):
            data = np.random.multivariate_normal(mean_ii, cov, 1)
            wii.append(data[0][0])
        weight_ii.append(wii)

    wa_ee = np.array(weight_ee)
    wa_ie = np.array(weight_ie)
    wa_ei = np.array(weight_ei)
    wa_ii = np.array(weight_ii)
    w_l1 = np.hstack((wa_ee, wa_ei))
    w_l2 = np.hstack((wa_ie, wa_ii))
    w_a = np.vstack((w_l1, w_l2))

    # valx = [500, 1000, 1500, 2000]
    # valy = [500, 1000, 1500, 2000]
    # h = sns.heatmap(w_a, cbar=False, cmap="icefire").invert_yaxis()
    h = sns.heatmap(w_a, cmap="icefire").invert_yaxis()
    plt.yticks(np.arange(0, 2001, 500), np.arange(0, 2001, 500), fontproperties='Times New Roman', size=14)
    plt.xticks(np.arange(0, 2001, 500), np.arange(0, 2001, 500), fontproperties='Times New Roman', size=14)
    plt.title('权值矩阵', fontdict={'family': 'SimHei', 'size': 16})
    font1 = {'family': 'Times New Roman', 'size': 16}
    # cb = h.plt.colorbar(prop=font1)  # 显示colorbar
    # cb = plt.colorbar(prop=font1)
    # cb.ax.tick_params(labelsize=14)  # 设置colorbar刻度字体大小。
    plt.show()
    # plt.savefig("NetworkMap.svg", dpi=300, format="png")
