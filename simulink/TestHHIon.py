from neuron.neuron import *
import matplotlib.pyplot as plt
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimSun']

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
    Ina1 = NaIonHHComponent(manager, 'Ina1')
    Ik1 = KIonHHComponent(manager, 'Ik1')
    Il1 = lIonHHComponent(manager, 'Il1')
    soma1 = HHsomaNeuron(manager, 'soma1', 10.0)
    manager.link_output_input(soma1, Ina1, 'V')
    manager.link_output_input(Ina1, soma1, 'Ina')
    manager.link_output_input(soma1, Ik1, 'V')
    manager.link_output_input(Ik1, soma1, 'Ik')
    manager.link_output_input(soma1, Il1, 'V')
    manager.link_output_input(Il1, soma1, 'Il')


    result = manager.start_stimulation(10000)
    COMP4_RESULT = []
    COMP5_RESULT = []
    COMP6_RESULT = []
    COMP7_RESULT = []
    for dictionary in result:
        COMP4_RESULT.append(dictionary['soma1'])
        # COMP5_RESULT.append(dictionary['Ina1'])
        # COMP6_RESULT.append(dictionary['Ik1'])
        # COMP7_RESULT.append(dictionary['Il1'])
    figure = plt.figure()
    plt.plot(COMP4_RESULT)
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