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
    comp = []
    syn = []
    para = []
    for i in range(3):
        for j in range(10):
            comp[i][j] = LIFNeuron(manager, 'comp' + 'i' + 'j', 10)
            syn[i][j] = synapseNeuron(manager, 'syn', [0.2])
    comp1 = LIFNeuron(manager, 'comp1', 20)
    comp2 = LIFNeuron(manager, 'comp2', 0)
    syn1 = synapseNeuron(manager,'syn1', [0.2])
    manager.link_output_input(comp1, syn1)
    manager.link_output_input(syn1, comp2, tab='I')
    manager.link_output_input(comp2, syn1, tab='houmo')
    result = manager.start_stimulation(10000)