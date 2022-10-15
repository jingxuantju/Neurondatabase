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
# import imageio
mpl.rcParams['font.sans-serif'] = ['SimSun']
matplotlib.rcParams['axes.unicode_minus']=False

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
    t_span = 12000
    real_t_span = 1200

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
    for i in range(100):
        for j in range(100):
            if (Csn_ge[i][j] == 1):
                manager.link_output_input(stn_syn_gpe[i], gpe[j], tab='I')
                manager.link_output_input(gpe[j], stn_syn_gpe[i], tab='houmo')
            elif (Csn_gi[i][j] == 1):
                manager.link_output_input(stn_syn_gpi[i], gpi[j], tab='I')
                manager.link_output_input(gpi[j], stn_syn_gpi[i], tab='houmo')
            elif (Cge_sn[i][j] == 1):
                manager.link_output_input(gpe_syn_stn[i], stn[j], tab='I')
                manager.link_output_input(stn[j], gpe_syn_stn[i], tab='houmo')
            elif (Cge_gi[i][j] == 1):
                manager.link_output_input(gpe_syn_gpi[i], gpi[j], tab='I')
                manager.link_output_input(gpi[j], gpe_syn_gpi[i], tab='houmo')
            elif (Cge_ge[i][j] == 1):
                manager.link_output_input(gpe_syn_gpe[i], gpe[j], tab='I')
                manager.link_output_input(gpe[j], gpe_syn_gpe[i], tab='houmo')
            elif (Cgi_tc[i][j] == 1):
                manager.link_output_input(gpi_syn_tc[i], th[j], tab='I')
                manager.link_output_input(th[j], gpi_syn_tc[i], tab='houmo')

    result = manager.start_stimulation(t_span)
    stn_RESULT = []
    gpe_RESULT = []
    gpi_RESULT = []
    th_RESULT = []
    for j in range(100):
        stn_R = []
        gpe_R = []
        gpi_R = []
        th_R = []
        for dictionary in result:
            stn_R.append(dictionary['stn' + str(j)][0])
            gpe_R.append(dictionary['gpe' + str(j)][0])
            gpi_R.append(dictionary['gpi' + str(j)][0])
            th_R.append(dictionary['th' + str(j)][0])
        stn_RESULT.append(stn_R)
        gpe_RESULT.append(gpe_R)
        gpi_RESULT.append(gpi_R)
        th_RESULT.append(th_R)
    V_STN_array = np.array(stn_RESULT)
    V_GPE_array = np.array(gpe_RESULT)
    V_GPI_array = np.array(gpi_RESULT)
    V_TH_array = np.array(th_RESULT)
    np.savez('pd0', V_STN_array=V_STN_array, V_GPE_array=V_GPE_array, V_GPI_array=V_GPI_array, V_TH_array=V_TH_array)

    SPK_STN = np.where(V_STN_array > 10, 1, 0)
    SPK_GPE = np.where(V_GPE_array > 10, 1, 0)
    SPK_GPI = np.where(V_GPI_array > 10, 1, 0)
    SPK_TH = np.where(V_TH_array > 10, 1, 0)

    # Get the index of a scatter map
    indexX_STN = []
    indexY_STN = []
    indexX_GPE = []
    indexY_GPE = []
    indexX_TH = []
    indexY_TH = []
    indexX_GPI = []
    indexY_GPI = []
    for j in range(100):
        # for t in range(2000, t_span):
        for t in range(t_span):
            if SPK_STN[j][t] == 1:
                indexX_STN.append(t)
                indexY_STN.append(j)
        for t in range(t_span):
            if SPK_GPE[j][t] == 1:
                indexX_GPE.append(t)
                indexY_GPE.append(j)
        for t in range(t_span):
            if SPK_GPI[j][t] == 1:
                indexX_GPI.append(t)
                indexY_GPI.append(j)
        for t in range(t_span):
            if SPK_TH[j][t] == 1:
                indexX_TH.append(t)
                indexY_TH.append(j)

    xr = range(2000, t_span, 2000)
    fig5 = plt.figure(figsize=(6, 8), dpi=100)
    gs = gridspec.GridSpec(15, 2)
    plt.subplot(411)
    # plt.title('(a) pd=0')
    line1 = plt.scatter(indexX_STN, indexY_STN, s=2, c='k')
    plt.xlim(2000, t_span)
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.xticks(xr, range(200, real_t_span, 200))
    plt.ylabel('STN', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
    plt.subplot(412)
    # line2 = plot(V_STN_array[1][2000: t_span])
    line2 = plot(V_STN_array[1], c='k')
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.xlim(2000, t_span)
    plt.xticks(xr, range(200, real_t_span, 200))
    # plt.xlabel('时间(ms)', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
    plt.ylabel('STN电位(mV)', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
    plt.subplot(413)
    # plt.title('(b) pd=0')
    line3 = plt.scatter(indexX_GPE, indexY_GPE, s=2, c='k')
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.xlim(2000, t_span)
    plt.xticks(xr, range(200, real_t_span, 200))
    plt.ylabel('GPE', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
    plt.subplot(414)
    # line2 = plot(V_STN_array[1][2000: t_span])
    line4 = plot(V_GPE_array[1], c='k')
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.xlim(2000, t_span)
    plt.xticks(xr, range(200, real_t_span, 200))
    # plt.xlabel('时间(ms)', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
    plt.ylabel('GPE电位(mV)', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
    fig5.tight_layout()
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.15, hspace=0.275)

    fig6 = plt.figure(figsize=(6, 8), dpi=100)
    plt.subplot(411)
    # plt.title('(c) pd=0')
    line5 = plt.scatter(indexX_GPI, indexY_GPI, s=2, c='k')
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.xlim(2000, t_span)
    plt.xticks(xr, range(200, real_t_span, 200))
    plt.ylabel('GPI', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
    plt.subplot(412)
    # line2 = plot(V_STN_array[1][2000: t_span])
    line6 = plot(V_GPI_array[1], c='k')
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.xlim(2000, t_span)
    plt.xticks(xr, range(200, real_t_span, 200))
    # plt.xlabel('时间(ms)', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
    plt.ylabel('GPI电位(mV)', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
    plt.subplot(413)
    # plt.title('(d) pd=0')
    line7 = plt.scatter(indexX_TH, indexY_TH, s=2, c='k')
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.xlim(2000, t_span)
    plt.xticks(xr, range(200, real_t_span, 200))
    plt.ylabel('TH', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
    plt.subplot(414)
    # line2 = plot(V_STN_array[1][2000: t_span])
    line8 = plot(V_TH_array[1], c='k')
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.xlim(2000, t_span)
    plt.xticks(xr, range(200, real_t_span, 200))
    # plt.xlabel('时间(ms)', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
    plt.ylabel('TH电位(mV)', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
    fig6.tight_layout()
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.15, hspace=0.275)
    plt.show()
"""
    fig1 = plt.figure()
    plt.title('(a) pd=0')
    plt.subplot(211)
    line1 = plt.scatter(indexX_STN, indexY_STN, s=2, c='k')
    plt.xlim(2000, t_span)
    plt.xticks(range(200, real_t_span))
    plt.ylabel('STN', fontdict={'family': 'SimHei', 'size': 16})  # label = name of label
    plt.subplot(212)
    # line2 = plot(V_STN_array[1][2000: t_span])
    line2 = plot(V_STN_array[1], c='k')
    plt.xlim(2000, t_span)
    plt.xticks(range(200, real_t_span))
    plt.xlabel('时间(ms)', fontdict={'family': 'SimHei', 'size': 16})  # label = name of label
    plt.ylabel('STN电位(mV)', fontdict={'family': 'SimHei', 'size': 16})  # label = name of label
    fig1.tight_layout()

    fig2 = plt.figure()
    plt.title('(b) pd=0')
    plt.subplot(211)
    line3 = plt.scatter(indexX_GPE, indexY_GPE, s=2, c='k')
    plt.xlim(2000, t_span)
    plt.xticks(range(200, real_t_span))
    plt.ylabel('GPE', fontdict={'family': 'SimHei', 'size': 16})  # label = name of label
    plt.subplot(212)
    # line2 = plot(V_STN_array[1][2000: t_span])
    line4 = plot(V_GPE_array[1], c='k')
    plt.xlim(2000, t_span)
    plt.xticks(range(200, real_t_span))
    plt.xlabel('时间(ms)', fontdict={'family': 'SimHei', 'size': 16})  # label = name of label
    plt.ylabel('GPE电位(mV)', fontdict={'family': 'SimHei', 'size': 16})  # label = name of label
    fig2.tight_layout()

    fig3 = plt.figure()
    plt.title('(c) pd=0')
    plt.subplot(211)
    line5 = plt.scatter(indexX_GPI, indexY_GPI, s=2, c='k')
    plt.xlim(2000, t_span)
    plt.xticks(range(200, real_t_span))
    plt.ylabel('GPI', fontdict={'family': 'SimHei', 'size': 16})  # label = name of label
    plt.subplot(212)
    # line2 = plot(V_STN_array[1][2000: t_span])
    line6 = plot(V_GPI_array[1], c='k')
    plt.xlim(2000, t_span)
    plt.xticks(range(200, real_t_span))
    plt.xlabel('时间(ms)', fontdict={'family': 'SimHei', 'size': 16})  # label = name of label
    plt.ylabel('GPI电位(mV)', fontdict={'family': 'SimHei', 'size': 16})  # label = name of label
    fig3.tight_layout()

    fig4 = plt.figure()
    plt.title('(d) pd=0')
    plt.subplot(211)
    line7 = plt.scatter(indexX_TH, indexY_TH, s=2, c='k')
    plt.xlim(2000, t_span)
    plt.xticks(range(200, real_t_span))
    plt.ylabel('TH', fontdict={'family': 'SimHei', 'size': 16})  # label = name of label
    plt.subplot(212)
    # line2 = plot(V_STN_array[1][2000: t_span])
    line8 = plot(V_TH_array[1], c='k')
    plt.xlim(2000, t_span)
    plt.xticks(range(200, real_t_span))
    plt.xlabel('时间(ms)', fontdict={'family': 'SimHei', 'size': 16})  # label = name of label
    plt.ylabel('TH电位(mV)', fontdict={'family': 'SimHei', 'size': 16})  # label = name of label
    fig4.tight_layout()
    plt.show()
"""