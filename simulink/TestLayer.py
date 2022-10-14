
from simulink.component import Component, Manager
import math
import numpy as np
from neuron.neuron import *
from pylab import *
from neuron.layer import *


if __name__ == '__main__':


    manager = Manager()
    layer1 = Layer(manager, 'layer1', number=10, type=IzhikevichNeuron)
    layer2 = Layer(manager, 'layer2', number=10, type=HHNeuron, key=(10, 0.01))
    result = manager.start_stimulation(2000)
    COMP4_RESULT = []
    for dictionary in result:
        COMP4_RESULT.append(dictionary['layer11'][0])
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