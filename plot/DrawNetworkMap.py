from simulink.component import Component, Manager
import math
import numpy as np
from neuron.neuron import *
from pylab import *
from neuron.layer import *
import scipy.io as scio
import copy
import random
import matplotlib.gridspec as gridspec
import cv2
from scipy import misc

# import imageio
mpl.rcParams['font.sans-serif'] = ['SimSun']
matplotlib.rcParams['axes.unicode_minus'] = False


def Gaussian_Distribution(mx=0, my=0, mz=0, sigma=4, M=100, N=3):
    '''
    Parameters
    ----------
    N 维度
    M 样本数
    m 样本均值
    sigma: 样本方差

    Returns
    -------
    data  shape(M, N), M 个 N 维服从高斯分布的样本
    Gaussian  高斯分布概率密度函数
    :param mx:
    '''
    mean = np.array([mx, my, mz])  # 均值矩阵，每个维度的均值
    cov = np.eye(N) * sigma  # 协方差矩阵，每个维度的方差都为 sigma

    # 产生 N 维高斯分布数据
    data = np.random.multivariate_normal(mean, cov, M)
    # N 维数据高斯分布概率密度函数
    Gaussian = multivariate_normal(mean=mean, cov=cov)

    return data, Gaussian


if __name__ == '__main__':
    dt = 0.1
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
    t_span = 3000
    real_t_span = 13000

    stn = [0 for i in range(100)]
    stn_syn_gpe = [0 for i in range(100)]
    stn_syn_gpi = [0 for i in range(100)]
    para_stn_gpe = [gsn_ge for i in range(100)]
    para_stn_gpi = [gsn_gi for i in range(100)]
    gpe = [0 for i in range(100)]
    gpe_syn_stn = [gge_sn for i in range(100)]
    gpe_syn_gpi = [gge_gi for i in range(100)]
    gpe_syn_gpe = [gge_ge for i in range(100)]
    para_gpe_stn = [0 for i in range(100)]
    para_gpe_gpi = [0 for i in range(100)]
    para_gpe_gpe = [0 for i in range(100)]
    gpi = [0 for i in range(100)]
    gpi_syn_tc = [0 for i in range(100)]
    para_gpi_tc = [ggi_tc for i in range(100)]
    th = [0 for i in range(100)]
    th_syn = [0 for i in range(100)]
    plusFile = 'lianjiejuzhen.mat'
    data = scio.loadmat(plusFile)
    Csn_ge = data['Csn_ge'].tolist()
    Csn_gi = data['Csn_gi'].tolist()
    Cge_sn = data['Cge_sn'].tolist()
    Cge_gi = data['Cge_gi'].tolist()
    Cge_ge = data['Cge_ge'].tolist()
    Cgi_tc = data['Cgi_tc'].tolist()
    plusFile1 = 'chushihua.mat'
    data1 = scio.loadmat(plusFile1)
    Istim = data1['Istim'].tolist()[0]
    Istim = [i * 5 for i in Istim]
    IstimC = [0 for i in range(100)]
    manager = Manager()
    for i in range(100):
        stn[i] = IzhikevichNeuron(manager, 'stn' + str(i), 1, 0.01, 0.26, -55, 3)
        stn_syn_gpe[i] = EsynapseNeuron(manager, 'stn_syn_gpe' + str(i), para_stn_gpe, E=0)
        # print(stn_syn_gpe[i].E)
        stn_syn_gpi[i] = EsynapseNeuron(manager, 'stn_syn_gpi' + str(i), para_stn_gpi, E=0)
        manager.link_output_input(stn[i], stn_syn_gpe[i])
        manager.link_output_input(stn[i], stn_syn_gpi[i])
        gpe[i] = IzhikevichNeuron(manager, 'gpe' + str(i), 8, 0.01, 0.585, -50, 5)
        gpe_syn_stn[i] = EsynapseNeuron(manager, 'gpe_syn_stn' + str(i), para_gpe_stn, ts=5)
        gpe_syn_gpi[i] = EsynapseNeuron(manager, 'gpe_syn_gpi' + str(i), para_gpe_gpi, ts=5)
        gpe_syn_gpe[i] = EsynapseNeuron(manager, 'gpe_syn_gpe' + str(i), para_gpe_gpe, ts=5)
        manager.link_output_input(gpe[i], gpe_syn_stn[i])
        manager.link_output_input(gpe[i], gpe_syn_gpi[i])
        manager.link_output_input(gpe[i], gpe_syn_gpe[i])
        gpi[i] = IzhikevichNeuron(manager, 'gpi' + str(i), 2, 0.01, 0.585, -50, 3)
        gpi_syn_tc[i] = EsynapseNeuron(manager, 'gpi_syn_tc' + str(i), para_gpi_tc, ts=100)
        manager.link_output_input(gpi[i], gpi_syn_tc[i])
        th[i] = IzhikevichNeuron(manager, 'th' + str(i), 0, 0.02, 0.25, -65, 0.05)
        th_syn[i] = EsynapseNeuron(manager, 'th_syn' + str(i), para_gpi_tc)
        IstimC[i] = IstimComponent(manager, 'Istim_th' + str(i), copy.deepcopy(Istim))
        manager.link_output_input(th[i], th_syn[i])
        manager.link_output_input(IstimC[i], th[i], tab='I')

    #    Start Plot
    lw = 0.2
    pointarea = 2
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    STN_dis, _ = Gaussian_Distribution(mx=5, my=5, mz=5, sigma=4, M=100)
    GPE_dis, _ = Gaussian_Distribution(mx=15, my=5, mz=5, sigma=4, M=100)
    GPI_dis, _ = Gaussian_Distribution(mx=5, my=15, mz=15, sigma=4, M=100)
    TH_dis, _ = Gaussian_Distribution(mx=15, my=15, mz=15, sigma=4, M=100)
    STN_x, STN_y, STN_z = STN_dis.T
    GPE_x, GPE_y, GPE_z = GPE_dis.T
    GPI_x, GPI_y, GPI_z = GPI_dis.T
    TH_x, TH_y, TH_z = TH_dis.T
    # Draw the dots
    for i in range(100):
        ax.scatter(STN_x[i], STN_y[i], STN_z[i], c='coral', s=pointarea)
        ax.scatter(GPE_x[i], GPE_y[i], GPE_z[i], c='royalblue', s=pointarea)
        ax.scatter(GPI_x[i], GPI_y[i], GPI_z[i], c='gold', s=pointarea)
        ax.scatter(TH_x[i], TH_y[i], TH_z[i], c='limegreen', s=pointarea)
    # Draw the edges
    for i in range(100):
        for j in range(100):
            if (Csn_ge[i][j] == 1):
                manager.link_output_input(stn_syn_gpe[i], gpe[j], tab='I')
                if (stn_syn_gpe[i].E == 0):
                    c_edge = 'lightsalmon'
                else:
                    c_edge = 'lightskyblue'
                ax.plot([STN_x[i], GPE_x[j]], [STN_y[i], GPE_y[j]], [STN_z[i], GPE_z[j]], c=c_edge, linewidth=lw)
                manager.link_output_input(gpe[j], stn_syn_gpe[i], tab='houmo')
            if (Csn_gi[i][j] == 1):
                manager.link_output_input(stn_syn_gpi[i], gpi[j], tab='I')
                if (stn_syn_gpe[i].E == 0):
                    c_edge = 'lightsalmon'
                else:
                    c_edge = 'lightskyblue'
                ax.plot([STN_x[i], GPI_x[j]], [STN_y[i], GPI_y[j]], [STN_z[i], GPI_z[j]], c=c_edge, linewidth=lw)
                manager.link_output_input(gpi[j], stn_syn_gpi[i], tab='houmo')
            if (Cge_sn[i][j] == 1):
                manager.link_output_input(gpe_syn_stn[i], stn[j], tab='I')
                # if (stn_syn_gpe[i].E == 0):
                #     c_edge = 'lightsalmon'
                # else:
                c_edge = 'lightskyblue'
                ax.plot([GPE_x[i], STN_x[j]], [GPE_y[i], STN_y[j]], [GPE_z[i], STN_z[j]], c=c_edge, linewidth=lw)
                manager.link_output_input(stn[j], gpe_syn_stn[i], tab='houmo')
            if (Cge_gi[i][j] == 1):
                manager.link_output_input(gpe_syn_gpi[i], gpi[j], tab='I')
                # if (stn_syn_gpe[i].E == 0):
                #     c_edge = 'lightsalmon'
                # else:
                c_edge = 'lightskyblue'
                ax.plot([GPE_x[i], GPI_x[j]], [GPE_y[i], GPI_y[j]], [GPE_z[i], GPI_z[j]], c=c_edge, linewidth=lw)
                manager.link_output_input(gpi[j], gpe_syn_gpi[i], tab='houmo')
            if (Cge_ge[i][j] == 1):
                manager.link_output_input(gpe_syn_gpe[i], gpe[j], tab='I')
                # if (stn_syn_gpe[i].E == 0):
                #     c_edge = 'lightsalmon'
                # else:
                c_edge = 'lightskyblue'
                ax.plot([GPE_x[i], GPE_x[j]], [GPE_y[i], GPE_y[j]], [GPE_z[i], GPE_z[j]], c=c_edge, linewidth=lw)
                manager.link_output_input(gpe[j], gpe_syn_gpe[i], tab='houmo')
            if (Cgi_tc[i][j] == 1):
                manager.link_output_input(gpi_syn_tc[i], th[j], tab='I')
                # if (stn_syn_gpe[i].E == 0):
                #     c_edge = 'lightsalmon'
                # else:
                c_edge = 'lightskyblue'
                ax.plot([GPE_x[i], TH_x[j]], [GPE_y[i], TH_y[j]], [GPE_z[i], TH_z[j]], c=c_edge, linewidth=lw)
                manager.link_output_input(th[j], gpi_syn_tc[i], tab='houmo')

    # plt.xticks([])
    # plt.yticks([])
    # plt.axis('off')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    plt.show()
    plt.savefig("NetworkMap.svg", dpi=300, format="png")
