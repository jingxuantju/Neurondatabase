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



class Basal():
    def __init__(self, manager, name, I=0, dt=0.01):
        # super().__init__(manager, name=name)

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
        plusFile = 'D:\FPGA\ku\simulink\plot\lianjiejuzhen.mat'
        data = scio.loadmat(plusFile)
        Csn_ge = data['Csn_ge'].tolist()
        Csn_gi = data['Csn_gi'].tolist()
        Cge_sn = data['Cge_sn'].tolist()
        Cge_gi = data['Cge_gi'].tolist()
        Cge_ge = data['Cge_ge'].tolist()
        Cgi_tc = data['Cgi_tc'].tolist()
        plusFile1 = 'D:\FPGA\ku\simulink\plot\chushihua.mat'
        data1 = scio.loadmat(plusFile1)
        Istim = data1['Istim'].tolist()[0]
        Istim = [i * 5 for i in Istim]
        IstimC = [0 for i in range(100)]
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

