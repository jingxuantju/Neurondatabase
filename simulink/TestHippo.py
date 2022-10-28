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


    ng1 = [0 for i in range(400)]
    ng1_syn_ng2 = [0 for i in range(400)]
    ng1_syn_ng3 = [0 for i in range(400)]
    ng1_syn_ng4 = [0 for i in range(400)]
    ng1_syn_ng5 = [0 for i in range(400)]
    para_stn_gpe = [gsn_ge for i in range(100)]
    para_stn_gpi = [gsn_gi for i in range(100)]
    ng2 = [0 for i in range(400)]
    ng2_syn_ng3 = [gge_sn for i in range(400)]
    ng2_syn_ng4 = [gge_sn for i in range(400)]
    ng2_syn_ng5 = [gge_sn for i in range(400)]
    ng2_syn_ng1 = [gge_sn for i in range(400)]
    gpe_syn_gpe = [gge_ge for i in range(100)]
    para_gpe_stn = [0 for i in range(100)]
    para_gpe_gpi = [0 for i in range(100)]
    para_gpe_gpe = [0 for i in range(100)]
    ng3 = [0 for i in range(400)]
    ng3_syn_ng4 = [gge_sn for i in range(400)]
    ng3_syn_ng5 = [gge_sn for i in range(400)]
    ng3_syn_ng1 = [gge_sn for i in range(400)]
    ng3_syn_ng2 = [gge_sn for i in range(400)]
    gpi_syn_tc = [0 for i in range(100)]
    para_gpi_tc = [ggi_tc for i in range(100)]
    ng4 = [0 for i in range(400)]
    ng4_syn_ng5 = [gge_sn for i in range(400)]
    ng4_syn_ng1 = [gge_sn for i in range(400)]
    ng4_syn_ng2 = [gge_sn for i in range(400)]
    ng4_syn_ng3 = [gge_sn for i in range(400)]
    ng5 = [0 for i in range(400)]
    ng5_syn_ng1 = [gge_sn for i in range(400)]
    ng5_syn_ng2 = [gge_sn for i in range(400)]
    ng5_syn_ng3 = [gge_sn for i in range(400)]
    ng5_syn_ng4 = [gge_sn for i in range(400)]
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
    for i in range(400):
        ng1[i] = IzhikevichNeuron(manager, 'ng1' + str(i), 1, 0.01, 0.26, -55, 3)
        ng1_syn_ng2[i] = EsynapseNeuron(manager, 'ng1_syn_ng2' + str(i), para_stn_gpe, E=0)
        ng1_syn_ng3[i] = EsynapseNeuron(manager, 'ng1_syn_ng3' + str(i), para_stn_gpe, E=0)
        ng1_syn_ng4[i] = EsynapseNeuron(manager, 'ng1_syn_ng4' + str(i), para_stn_gpe, E=0)
        ng1_syn_ng5[i] = EsynapseNeuron(manager, 'ng1_syn_ng5' + str(i), para_stn_gpe, E=0)
        manager.link_output_input(ng1[i], ng1_syn_ng2[i])
        manager.link_output_input(ng1[i], ng1_syn_ng3[i])
        manager.link_output_input(ng1[i], ng1_syn_ng4[i])
        manager.link_output_input(ng1[i], ng1_syn_ng5[i])
        ng2[i] = IzhikevichNeuron(manager, 'ng2' + str(i), 8, 0.01, 0.585, -50, 5)
        ng2_syn_ng3[i] = EsynapseNeuron(manager, 'ng2_syn_ng3' + str(i), para_stn_gpe, E=0)
        ng2_syn_ng4[i] = EsynapseNeuron(manager, 'ng2_syn_ng4' + str(i), para_stn_gpe, E=0)
        ng2_syn_ng5[i] = EsynapseNeuron(manager, 'ng2_syn_ng5' + str(i), para_stn_gpe, E=0)
        ng2_syn_ng1[i] = EsynapseNeuron(manager, 'ng2_syn_ng1' + str(i), para_stn_gpe, E=0)
        manager.link_output_input(ng2[i], ng2_syn_ng3[i])
        manager.link_output_input(ng2[i], ng2_syn_ng4[i])
        manager.link_output_input(ng2[i], ng2_syn_ng5[i])
        manager.link_output_input(ng2[i], ng2_syn_ng1[i])
        ng3[i] = IzhikevichNeuron(manager, 'ng3' + str(i), 2, 0.01, 0.585, -50, 3)
        ng3_syn_ng4[i] = EsynapseNeuron(manager, 'ng3_syn_ng4' + str(i), para_stn_gpe, E=0)
        ng3_syn_ng5[i] = EsynapseNeuron(manager, 'ng3_syn_ng5' + str(i), para_stn_gpe, E=0)
        ng3_syn_ng1[i] = EsynapseNeuron(manager, 'ng3_syn_ng1' + str(i), para_stn_gpe, E=0)
        ng3_syn_ng2[i] = EsynapseNeuron(manager, 'ng3_syn_ng2' + str(i), para_stn_gpe, E=0)
        manager.link_output_input(ng3[i], ng3_syn_ng4[i])
        manager.link_output_input(ng3[i], ng3_syn_ng5[i])
        manager.link_output_input(ng3[i], ng3_syn_ng1[i])
        manager.link_output_input(ng3[i], ng3_syn_ng2[i])
        ng4[i] = IzhikevichNeuron(manager, 'ng4' + str(i), 0, 0.02, 0.25, -65, 0.05)
        ng4_syn_ng5[i] = EsynapseNeuron(manager, 'ng4_syn_ng5' + str(i), para_stn_gpe, E=0)
        ng4_syn_ng1[i] = EsynapseNeuron(manager, 'ng4_syn_ng1' + str(i), para_stn_gpe, E=0)
        ng4_syn_ng2[i] = EsynapseNeuron(manager, 'ng4_syn_ng2' + str(i), para_stn_gpe, E=0)
        ng4_syn_ng3[i] = EsynapseNeuron(manager, 'ng4_syn_ng3' + str(i), para_stn_gpe, E=0)
        ng5[i] = IzhikevichNeuron(manager, 'ng5' + str(i), 0, 0.02, 0.25, -65, 0.05)
        ng5_syn_ng1[i] = EsynapseNeuron(manager, 'ng5_syn_ng1' + str(i), para_stn_gpe, E=0)
        ng5_syn_ng2[i] = EsynapseNeuron(manager, 'ng5_syn_ng2' + str(i), para_stn_gpe, E=0)
        ng5_syn_ng3[i] = EsynapseNeuron(manager, 'ng5_syn_ng3' + str(i), para_stn_gpe, E=0)
        ng5_syn_ng4[i] = EsynapseNeuron(manager, 'ng5_syn_ng4' + str(i), para_stn_gpe, E=0)
    for i in range(400):
        for j in range(400):
            a1 = random.randint(0,10)
            a2 = random.randint(0,10)
            a3 = random.randint(0,10)
            a4 = random.randint(0,10)
            a5 = random.randint(0,10)
            if (a1 < 4):
                manager.link_output_input(ng1_syn_ng2[i], ng2[j], tab='I')
                manager.link_output_input(ng2[j], ng1_syn_ng2[i], tab='houmo')
            if (a2 < 4):
                manager.link_output_input(ng1_syn_ng3[i], ng3[j], tab='I')
                manager.link_output_input(ng3[j], ng1_syn_ng3[i], tab='houmo')
            if (a3 < 4):
                manager.link_output_input(ng1_syn_ng3[i], ng3[j], tab='I')
                manager.link_output_input(ng3[j], ng1_syn_ng3[i], tab='houmo')

    result = manager.start_stimulation(600)
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
            stn_R.append(dictionary['stn'+ str(j)][0])
            gpe_R.append(dictionary['gpe'+ str(j)][0])
            gpi_R.append(dictionary['gpi'+ str(j)][0])
            th_R.append(dictionary['th'+ str(j)][0])
        stn_RESULT.append(stn_R)
        gpe_RESULT.append(gpe_R)
        gpi_RESULT.append(gpi_R)
        th_RESULT.append(th_R)
    STN_array = np.array(stn_RESULT)
    GPE_array = np.array(gpe_RESULT)
    GPI_array = np.array(gpi_RESULT)
    TH_array = np.array(th_RESULT)
    STN_SPK = np.where(STN_array>10,1,0)
    GPE_SPK = np.where(GPE_array>10,1,0)
    GPI_SPK = np.where(GPI_array>10,1,0)
    TH_SPK = np.where(TH_array>10,1,0)
        # if dictionary['comp01'][0] >= 5:
        #     COMP4_RESULT_PULSE.append(1)
        # else:
        #     COMP4_RESULT_PULSE.append(0)
        # COMP5_RESULT.append(dictionary['comp11'][0])
        # if dictionary['comp11'][0] >= 5:
        #     COMP5_RESULT_PULSE.append(1)
        # else:
        #     COMP5_RESULT_PULSE.append(0)
        # COMP6_RESULT.append(dictionary['comp21'][0])
        # if dictionary['comp21'][0] >= 5:
        #     COMP6_RESULT_PULSE.append(1)
        # else:
        #     COMP6_RESULT_PULSE.append(0)
    plt.figure(1)

    stn_s = np.fft.fft(stn_RESULT)
    plt.plot(stn_s)

    # imageio.imwrite('1.png', GPI_SPK)
    # scipy.misc.imsave('a.jpg', a)
    # cv2.waitKey(0)
    # plt.figure(2)
    # plt.plot(COMP5_RESULT)
    # plt.figure(3)
    # plt.plot(COMP6_RESULT)
    # plt.figure(4)
    # plt.plot(COMP7_RESULT)
    # line1, = plt.plot(COMP5_RESULT)
    # line2, = plt.plot(COMP6_RESULT)
    # line3, = plt.plot(COMP7_RESULT)
    # plt.legend(handles=[line1, line2, line3], labels=['Ina', 'Ik', 'Il'], loc='upper right', fontsize=16)
    plt.xlabel('时间(ms)', fontsize=18)  # label = name of label
    # plt.ylabel('电流(mA)', fontsize=18)  # label = name of label
    plt.ylabel('电压(mV)', fontsize=18)  # label = name of label
    plt.title('(a)')
    plt.show()
    print(result)















