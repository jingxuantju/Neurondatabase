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


    manager = Manager()
    comp2 = IzhikevichNeuron(manager, 'comp2', 10, 0.1, 0.2, -65, 2)
    result = manager.start_stimulation(2000)
    COMP2_RESULT = []
    for dictionary in result:
        COMP2_RESULT.append(dictionary['comp2'][0])
    peaks2, _ = find_peaks(COMP2_RESULT)

    manager = Manager()
    comp3 = IzhikevichNeuron(manager, 'comp3', 10, 0.02, 0.2, -65, 2)
    result = manager.start_stimulation(2000)
    COMP3_RESULT = []
    for dictionary in result:
        COMP3_RESULT.append(dictionary['comp3'][0])
    peaks3, _ = find_peaks(COMP3_RESULT)

    manager = Manager()
    comp4 = IzhikevichNeuron(manager, 'comp4', 10, 0.02, 0.25, -65, 2)
    result = manager.start_stimulation(2000)
    COMP4_RESULT = []
    for dictionary in result:
        COMP4_RESULT.append(dictionary['comp4'][0])
    peaks4, _ = find_peaks(COMP4_RESULT)

    manager = Manager()
    comp5 = IzhikevichNeuron(manager, 'comp5', 10, 0.1, 0.25, -65, 2)
    result = manager.start_stimulation(2000)
    COMP5_RESULT = []
    for dictionary in result:
        COMP5_RESULT.append(dictionary['comp5'][0])
    peaks5, _ = find_peaks(COMP5_RESULT)

    FiringRate_ab = []
    for a_param in range(1,16):
        FiringRate_x = []
        for b_param in range(1,16):
            manager = Manager()
            comp1 = IzhikevichNeuron(manager, 'comp1', 10, a_param * 0.01, b_param * 0.02, -65, 2)
            result = manager.start_stimulation(3000)  # 2s

            COMP1_RESULT = []
            for dictionary in result:
                COMP1_RESULT.append(dictionary['comp1'][0])
            peaks, _ = find_peaks(COMP1_RESULT[1000:3000])
            n_spikes = len(peaks) / 2
            FiringRate_x.append(n_spikes)
        FiringRate_ab.append(FiringRate_x)

    # a_ticks = np.linspace(0, 0.15, 15)
    # b_ticks = np.linspace(0, 0.3, 15)
    # grid = plt.GridSpec(2, 4, wspace=0.4, hspace=0.3)
    fig1 = plt.figure()
    # plt.subplot(grid[0:1, 0:1])
    plt.imshow(FiringRate_ab,origin = 'lower')
    plt.xticks([-0.5,14.5],[0,0.15])
    plt.yticks([-0.5,14.5],[0,0.3])
    plt.colorbar()
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.xlabel('a', fontdict={'family' : 'Times New Roman', 'size'   : 16})
    plt.ylabel('b', fontdict={'family' : 'Times New Roman', 'size'   : 16})
    # plt.legend(prop={'family': 'Times New Roman', 'size': 16})
    plt.title('Izhikevich放电率', fontdict={'family': 'SimHei', 'size': 16})
    plt.show()

    fig2 = plt.figure()
    plt.subplot(221)
    plt.plot(COMP5_RESULT)
    # plt.plot(peaks2, np.array(COMP2_RESULT)[peaks2], "x")
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.xlabel('时间(ms)', fontdict={'family': 'SimHei', 'size': 16})
    plt.ylabel('膜电位(mV)', fontdict={'family': 'SimHei', 'size': 16})
    plt.title('a=0.1, b=0.25, c=-65, d=2', fontdict={'family': 'SimHei', 'size': 16})
    plt.subplot(222)
    plt.plot(COMP2_RESULT)
    #plt.plot(peaks2, np.array(COMP2_RESULT)[peaks2], "x")
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.xlabel('时间(ms)', fontdict={'family': 'SimHei', 'size': 16})
    plt.ylabel('膜电位(mV)', fontdict={'family': 'SimHei', 'size': 16})
    plt.title('a=0.1, b=0.2, c=-65, d=2', fontdict={'family': 'SimHei', 'size': 16})
    plt.subplot(223)
    plt.plot(COMP3_RESULT)
    #plt.plot(peaks3, np.array(COMP3_RESULT)[peaks3], "x")
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.xlabel('时间(ms)', fontdict={'family': 'SimHei', 'size': 16})
    plt.ylabel('膜电位(mV)', fontdict={'family': 'SimHei', 'size': 16})
    plt.title('a=0.02, b=0.2, c=-65, d=2', fontdict={'family': 'SimHei', 'size': 16})
    plt.subplot(224)
    plt.plot(COMP4_RESULT)
    #plt.plot(peaks4, np.array(COMP4_RESULT)[peaks4], "x")
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.xlabel('时间(ms)', fontdict={'family': 'SimHei', 'size': 16})
    plt.ylabel('膜电位(mV)', fontdict={'family': 'SimHei', 'size': 16})
    plt.title('a=0.02, b=0.25, c=-65, d=2', fontdict={'family': 'SimHei', 'size': 16})

    fig2.tight_layout()
    plt.show()
