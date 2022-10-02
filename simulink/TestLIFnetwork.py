from neuron.neuron import *
import matplotlib.pyplot as plt
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimSun']
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
    comp = [[0 for i in range(20)] for j in range(3)]
    syn = [[0 for i in range(20)] for j in range(3)]
    para = []
    for i in range(20):
        para.append(0.015)
    for i in range(3):
        for j in range(20):
            if (i == 0):
                comp[i][j] = LIFNeuron(manager, 'comp' + str(i) + str(j), 10)
            else:
                comp[i][j] = LIFNeuron(manager, 'comp' + str(i) + str(j), 0)
            syn[i][j] = synapseNeuron(manager, 'syn' + str(i) + str(j), para)
    for i in range(2):
        for j in range(20):
            manager.link_output_input(comp[i][j], syn[i][j])
            for k in range(20):
                manager.link_output_input(syn[i][j], comp[i+1][k], tab='I')
                manager.link_output_input(comp[i+1][k], syn[i][j], tab='houmo')
    result = manager.start_stimulation(2000)
    COMP4_RESULT = []
    COMP5_RESULT = []
    COMP6_RESULT = []
    COMP7_RESULT = []
    for dictionary in result:
        COMP4_RESULT.append(dictionary['comp21'])
        # COMP5_RESULT.append(dictionary['comp11'])
        # COMP6_RESULT.append(dictionary['comp21'])
        # COMP5_RESULT.append(dictionary['comp21'])
        # COMP5_RESULT.append(dictionary['Ina1'])
        # COMP6_RESULT.append(dictionary['Ik1'])
        # COMP7_RESULT.append(dictionary['Il1'])
    figure = plt.figure()
    plt.plot(COMP4_RESULT, color='orange')
    # plt.plot(COMP5_RESULT)
    # line1, = plt.plot(COMP5_RESULT)
    # line2, = plt.plot(COMP6_RESULT)
    # line3, = plt.plot(COMP7_RESULT)
    # plt.legend(handles=[line1, line2, line3], labels=['Ina', 'Ik', 'Il'], loc='upper right', fontsize=16)
    plt.xlabel('时间(ms)', fontsize=18)  # label = name of label
    # plt.ylabel('电流(mA)', fontsize=18)  # label = name of label
    plt.ylabel('电压(mV)', fontsize=18)  # label = name of label
    plt.title('(a)')
    figure.show()
    plt.show()
    print(result)