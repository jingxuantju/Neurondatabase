from simulink.component import *
from neuron.neuron import *
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

if __name__ == '__main__':
    class SelfAddingUnit(Component):
        def __init__(self, living_dictionary: dict, name):
            super(SelfAddingUnit, self).__init__(living_dictionary, name=name)
            self.hidden = 0

        def function(self):
            self.hidden += 1
            self.output = self.hidden
            return self.output

    # FS
    FiringRate_FS = []
    for I_in in range(100):
        manager = Manager()
        comp2 = IzhikevichNeuron(manager, 'comp2', I_in/4, 0.1, 0.2, -65, 2)
        result = manager.start_stimulation(3000)
        COMP2_RESULT = []
        for dictionary in result:
            COMP2_RESULT.append(dictionary['comp2'][0])
        peaks2, _ = find_peaks(COMP2_RESULT[1000:3000])
        n_spikes = len(peaks2) / 2 * 100
        FiringRate_FS.append(n_spikes)

    # CH
    FiringRate_CH = []
    for I_in in range(100):
        manager = Manager()
        comp3 = IzhikevichNeuron(manager, 'comp3', I_in/4, 0.02, 0.2, -50, 2)
        result = manager.start_stimulation(3000)
        COMP3_RESULT = []
        for dictionary in result:
            COMP3_RESULT.append(dictionary['comp3'][0])
        peaks3, _ = find_peaks(COMP3_RESULT[1000:3000])
        n_spikes = len(peaks3) / 2 * 100
        FiringRate_CH.append(n_spikes)

    # RS
    FiringRate_RS = []
    for I_in in range(100):
        manager = Manager()
        comp4 = IzhikevichNeuron(manager, 'comp4', I_in/4, 0.02, 0.2, -65, 8)
        result = manager.start_stimulation(3000)
        COMP4_RESULT = []
        for dictionary in result:
            COMP4_RESULT.append(dictionary['comp4'][0])
        peaks4, _ = find_peaks(COMP4_RESULT[1000:3000])
        n_spikes = len(peaks4) / 2 * 100
        FiringRate_RS.append(n_spikes)

    # IB
    FiringRate_IB = []
    for I_in in range(100):
        manager = Manager()
        comp5 = IzhikevichNeuron(manager, 'comp5', I_in/4, 0.02, 0.2, -55, 4)
        result = manager.start_stimulation(3000)
        COMP5_RESULT = []
        for dictionary in result:
            COMP5_RESULT.append(dictionary['comp5'][0])
        peaks5, _ = find_peaks(COMP5_RESULT[1000:3000])
        n_spikes = len(peaks5) / 2 * 100
        FiringRate_IB.append(n_spikes)

    I_tick = np.linspace(0,25,100)
    fig2 = plt.figure()
    plt.subplot(221)
    plt.scatter(I_tick, FiringRate_FS, s=2)
    # plt.plot(peaks2, np.array(COMP2_RESULT)[peaks2], "x")
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.xlabel('电流(mA)', fontdict={'family': 'SimHei', 'size': 16})
    plt.ylabel('放电率(Hz)', fontdict={'family': 'SimHei', 'size': 16})
    plt.title('FS', fontdict={'family': 'SimHei', 'size': 16})
    plt.subplot(222)
    plt.scatter(I_tick, FiringRate_CH, s=2)
    #plt.plot(peaks2, np.array(COMP2_RESULT)[peaks2], "x")
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.xlabel('电流(mA)', fontdict={'family': 'SimHei', 'size': 16})
    plt.ylabel('放电率(Hz)', fontdict={'family': 'SimHei', 'size': 16})
    plt.title('CH', fontdict={'family': 'SimHei', 'size': 16})
    plt.subplot(223)
    plt.scatter(I_tick, FiringRate_RS, s=2)
    #plt.plot(peaks3, np.array(COMP3_RESULT)[peaks3], "x")
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.xlabel('电流(mA)', fontdict={'family': 'SimHei', 'size': 16})
    plt.ylabel('放电率(Hz)', fontdict={'family': 'SimHei', 'size': 16})
    plt.title('RS', fontdict={'family': 'SimHei', 'size': 16})
    plt.subplot(224)
    plt.scatter(I_tick, FiringRate_IB, s=2)
    #plt.plot(peaks4, np.array(COMP4_RESULT)[peaks4], "x")
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.xlabel('电流(mA)', fontdict={'family': 'SimHei', 'size': 16})
    plt.ylabel('放电率(Hz)', fontdict={'family': 'SimHei', 'size': 16})
    plt.title('IB', fontdict={'family': 'SimHei', 'size': 16})

    fig2.tight_layout()
    plt.show()
