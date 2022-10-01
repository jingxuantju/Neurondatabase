from simulink.component import *
from neuron.neuron import *
import matplotlib.pyplot as plt

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
    comp1 = LIFNeuron(manager, 'comp1', 10)
    # comp2 = LIFNeuron(manager.living_dictionary, 'comp2', 8)
    # manager.link_output_input(comp1, comp2.inputs)
    # manager.link_output_input(comp1, comp1.inputs)
    # manager.link_output_input(comp2, comp2.inputs)
    # comp1 = IzhikevichNeuron(manager, 'comp1', 10, 0.02, 0.2, -50, 2)
    # comp1 = IzhikevichNeuron(manager, 'comp1', 10, 0.02, 0.2, -65, 8)
    # comp3 = synapseNeuron(manager,'comp3', [0.2])
    # manager.link_output_input(comp1, comp3)
    # manager.link_output_input(comp3, comp2, tab='I')
    # manager.link_output_input(comp2, comp3, tab='houmo')
    # comp4 = PRNeuron(manager, 'comp1', -0.5, 0)
    # comp2 = Component(manager.living_dictionary, 'comp2')
    # comp3 = SelfAddingUnit(manager.living_dictionary, 'comp3')
    # manager.link_output_input(comp1, comp1.inputs)
    # manager.link_output_input(comp3, comp2.inputs)
    # manager.link_output_input(comp2, comp1.inputs)
    # comp1 = HHNeuron(manager, 'comp1', 20)
    # manager.link_output_input(comp1, comp1)
    result = manager.start_stimulation(2000)

    # COMP1_RESULT = []
    # com1_pulse = []
    # COMP2_RESULT = []
    # for dictionary in result:
    #     COMP1_RESULT.append(dictionary['comp1'])
    #     if dictionary['comp1'] >= 39:
    #         com1_pulse.append(1)
    #     else:
    #         com1_pulse.append(0)
    #     COMP2_RESULT.append(dictionary['comp2'])
    # figure = plt.figure()
    # plt.plot(COMP1_RESULT)
    # plt.plot(COMP2_RESULT)
    # figure.show()
    # figure2 = plt.figure()
    # plt.plot(com1_pulse)
    # plt.show()
    #
    # print(result)

    # COMP1_RESULT = []
    # COMP2_RESULT = []
    # com1_pulse = []
    # com2_pulse = []
    # for dictionary in result:
    #     COMP1_RESULT.append(dictionary['comp1'])
    #     COMP2_RESULT.append(dictionary['comp2'])
    #     if dictionary['comp1'] >= -7:
    #         com1_pulse.append(1)
    #     else:
    #         com1_pulse.append(0)
    #     if dictionary['comp2'] >= -66.33:
    #         com2_pulse.append(1)
    #     else:
    #         com2_pulse.append(0)

    COMP4_RESULT = []
    COMP5_RESULT = []
    for dictionary in result:
        COMP4_RESULT.append(dictionary['comp1'])
        # COMP4_RESULT.append(dictionary['comp1'][0])
        # COMP5_RESULT.append(dictionary['comp1'][1])
    # figure = plt.figure()
    # plt.plot(COMP1_RESULT)
    # figure.show()
    # figure1 = plt.figure()
    # plt.plot(COMP2_RESULT)
    # figure1.show()
    # figure2 = plt.figure()
    # plt.plot(com1_pulse)
    # figure2.show()
    # figure3 = plt.figure()
    # plt.plot(com2_pulse)
    # plt.show()

    # figure = plt.figure()
    # plt.plot(COMP1_RESULT)
    # plt.plot(COMP2_RESULT)
    # figure.show()
    # figure2 = plt.figure()
    # plt.xlim((200, 1000))
    # plt.plot(com1_pulse)
    # plt.plot(com2_pulse)
    # plt.title("RUNOOB TEST TITLE")
    # plt.xlabel("x - label")
    # plt.ylabel("y - label")
    # plt.show()
    figure = plt.figure()
    plt.plot(COMP4_RESULT)
    plt.plot(COMP5_RESULT)
    figure.show()
    plt.show()
    print(result)