from neuron.neuron import *
import matplotlib.pyplot as plt
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimSun']
matplotlib.rcParams['axes.unicode_minus']=False
import random



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
    comp = [[0 for i in range(20)] for j in range(3)]
    syn = [[0 for i in range(20)] for j in range(3)]
    para1 = []
    para2 = []
    for i in range(20):
        para1.append(0.05)
        para2.append(0.25)
    for i in range(3):
        for j in range(20):
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
        for j in range(20):
            manager.link_output_input(comp[i][j], syn[i][j])
            for k in range(20):
                a = random.randint(0, 5)
                if (a == 0):
                    manager.link_output_input(syn[i][j], comp[i+1][k], tab='I')
                    manager.link_output_input(comp[i+1][k], syn[i][j], tab='houmo')
    result = manager.start_stimulation(2000)
    COMP4_RESULT = []
    COMP5_RESULT = []
    COMP6_RESULT = []
    COMP4_RESULT_PULSE = []
    COMP5_RESULT_PULSE = []
    COMP6_RESULT_PULSE = []
    for dictionary in result:
        COMP4_RESULT.append(dictionary['comp01'][0])
        if dictionary['comp01'][0] >= 5:
            COMP4_RESULT_PULSE.append(1)
        else:
            COMP4_RESULT_PULSE.append(0)
        COMP5_RESULT.append(dictionary['comp11'][0])
        if dictionary['comp11'][0] >= 5:
            COMP5_RESULT_PULSE.append(1)
        else:
            COMP5_RESULT_PULSE.append(0)
        COMP6_RESULT.append(dictionary['comp21'][0])
        if dictionary['comp21'][0] >= 5:
            COMP6_RESULT_PULSE.append(1)
        else:
            COMP6_RESULT_PULSE.append(0)
    figure = plt.figure()
    # plt.plot(COMP4_RESULT)
    plt.subplot(211)
    line1, = plt.plot(COMP4_RESULT)
    line2, = plt.plot(COMP5_RESULT)
    line3, = plt.plot(COMP6_RESULT)
    plt.legend(handles=[line1, line2, line3], labels=['Ina', 'Ik', 'Il'], loc='upper left', fontsize=16)
    plt.xlabel('时间(ms)', fontsize=18)  # label = name of label
    # plt.ylabel('电流(mA)', fontsize=18)  # label = name of label
    plt.ylabel('电压(mV)', fontsize=18)  # label = name of label
    plt.title('(a)')
    plt.subplot(212)
    line1, = plt.plot(COMP4_RESULT_PULSE)
    line2, = plt.plot(COMP5_RESULT_PULSE)
    line3, = plt.plot(COMP6_RESULT_PULSE)
    plt.legend(handles=[line1, line2, line3], labels=['Ina', 'Ik', 'Il'], loc='upper left', fontsize=16)
    plt.xlabel('时间(ms)', fontsize=18)  # label = name of label
    # plt.ylabel('电流(mA)', fontsize=18)  # label = name of label
    plt.ylabel('放电脉冲', fontsize=18)  # label = name of label
    # plt.title('(a)')
    figure.tight_layout()
    figure.show()
    plt.show()
    print(result)