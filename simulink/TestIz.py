from neuron.neuron import *
from neuron.comp import *
import matplotlib.pyplot as plt
from pylab import *
import random
mpl.rcParams['font.sans-serif'] = ['SimSun']
matplotlib.rcParams['axes.unicode_minus']=False

if __name__ == '__main__':
    class SelfAddingUnit(Component):
        def __init__(self, living_dictionary: dict, name):
            super(SelfAddingUnit, self).__init__(living_dictionary, name=name)
            self.hidden = 0

        def function(self):
            self.hidden += 1
            self.output = self.hidden
            return self.output

    time = 4000
    manager = Manager()
    list1 = []
    list2 = []
    # comp1 = MLNeuron(manager, 'comp1', 50)
    # comp1 = IzhikevichNeuron1(manager, 'comp1', 10, 0.02, 0.2, -50, 2)
    comp1 = hLNComponent(manager, 'comp1', 0.4, 1.08)
    for i in range(10000):
        a = random.randint(0,3)
        if a == 1:
            list1.append(0)
        else:
            list1.append(1)
    IS1 = IstimComponent(manager, 'IS1', list1)
    for i in range(10000):
        a = random.randint(0,1)
        if a == 1:
            list2.append(0)
        else:
            list2.append(1)
    IS1 = IstimComponent(manager, 'IS1', list1)
    IS2 = IstimComponent(manager, 'IS2', list2)
    manager.link_output_input(IS1, comp1, tab='spikeE')
    manager.link_output_input(IS2, comp1, tab='spikeI')
    # comp1 = LIFNeuron(manager, 'comp1', 10)
    # comp1 = HHNeuron(manager, 'comp1', 10)
    # comp1 = simplePRNeuron(manager, 'comp1', 60)
    # comp1 = FNNeuron(manager, 'comp1',10)
    # comp1 = PurkinjeNeuron(manager, 'comp1')
    result = manager.start_stimulation(time)
    COMP4_RESULT = []
    COMP5_RESULT = []
    COMP6_RESULT = []
    COMP7_RESULT = []
    for dictionary in result:
        # COMP4_RESULT.append(dictionary['soma1'])
        # COMP4_RESULT.append(dictionary['comp1'][0])
        # COMP5_RESULT.append(dictionary['comp1'][1])
        # COMP6_RESULT.append(dictionary['comp1'][2])
        # COMP7_RESULT.append(dictionary['comp1'][3])
        COMP4_RESULT.append(dictionary['comp1'][2])
        # COMP5_RESULT.append(dictionary['comp1'][1])
    figure = plt.figure()
    plt.plot(COMP4_RESULT)
    # line1, = plt.plot(COMP4_RESULT, COMP5_RESULT, color='black')
    # line2, = plt.plot(COMP5_RESULT)
    # line3, = plt.plot(COMP6_RESULT)
    # plt.legend(handles = [line1, line2,line3 ],labels = ['m','h','n'],loc = 'upper right', fontsize=16)
    plt.xlabel('时间(ms)',fontsize=20)  # label = name of label
    plt.ylabel('电压(mV)',fontsize=20)  # label = name of label
    plt.xlim(1000, time)
    figure.show()
    plt.show()
    print(result)