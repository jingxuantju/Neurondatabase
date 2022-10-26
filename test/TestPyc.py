from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimSun']
from neuron.network import *

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
    # comp1 = PurkinjeNeuron(manager, 'comp1',25)
    comp1 = Basal(manager,'basal1')

    result = manager.start_stimulation(4000)

    COMP4_RESULT = []
    COMP5_RESULT = []
    COMP6_RESULT = []
    COMP7_RESULT = []
    for dictionary in result:
        # COMP4_RESULT.append(dictionary['soma1'])
        COMP4_RESULT.append(dictionary['stn0'][0])
        # COMP5_RESULT.append(dictionary['comp1'][2])
        # COMP6_RESULT.append(dictionary['comp1'][3])
        # COMP7_RESULT.append(dictionary['comp1'][4])
        # COMP4_RESULT.append(dictionary['comp1'][0])
        # COMP5_RESULT.append(dictionary['comp1'][3])
    figure = plt.figure()
    # plt.plot(COMP4_RESULT)
    line1, = plt.plot(COMP4_RESULT)
    # line2, = plt.plot(COMP5_RESULT)
    # line3, = plt.plot(COMP6_RESULT)
    # line4, = plt.plot(COMP7_RESULT)
    # plt.legend(handles = [line1, line2,line3 ],labels = ['m','h','n'],loc = 'upper right', fontsize=16)
    plt.xlabel('时间(ms)',fontsize=20)  # label = name of label
    plt.title('(a)')
    figure.show()
    plt.show()
    print(result)