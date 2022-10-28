from simulink.component import Component, Manager
import math
import numpy as np
from neuron.neuron import *
from neuron.comp import *


class Layer(Neuron):

    def __init__(self, manager, name, number=10, type=IzhikevichNeuron, key=(10, 0.02, 0.2, -65, 2)):
        """

        :param manager:
        :param name:
        :param number:
        :param type:
        :param key:
        """
        super().__init__(manager, name=name)
        self.layerComp = []
        self.layerSyn = []
        for i in range(number):
            self.layerComp.append(type(manager, name + str(i), *key))
            self.layerSyn.append(synapseNeuron(manager, name+'synpase'+str(i), *key))
            manager.link_output_input(name + str(i), name+'synpase'+str(i))