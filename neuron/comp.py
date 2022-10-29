from simulink.component import Component, Manager
import math
from neuron.neuron import Neuron

class HHsomaNeuron(Neuron):
    def __init__(self, manager, name, I):
        super().__init__(manager, name=name)
        self.I = I
        self.c = 1

    def function(self):
        Ina = 0.0
        Ik = 0.0
        Il = 0.0
        v = 0.0
        Isyn = 0.0
        for i in range(len(self.inputs_tab)):
            if self.inputs_tab[i] == "Ina":
                Ina += self.inputs[i]
            elif self.inputs_tab[i] == "Ik":
                Ik += self.inputs[i]
            elif self.inputs_tab[i] == "Il":
                Il += self.inputs[i]
            elif self.inputs_tab[i] == "houmo":
                Isyn += self.inputs[i]
            elif self.inputs_tab[i] == "self":
                v += self.inputs[i]
        # clear inputs
        self.inputs.clear()

        output = v + 0.01 * (self.I + Isyn - Ina - Ik - Il) / self.c

        self.output = output
        return self.output


class NaIonHHComponent(Component):
    def __init__(self, manager, name, gna=120, vna=120):
        super().__init__(manager, name=name)
        self.gna = gna
        self.vna = vna
        self.am = 0
        self.bm = 0
        self.ah = 0
        self.bh = 0
        self.m = 0
        self.h = 0

    # inputs是Vs即膜电位
    def function(self):
        v = self.inputs[self.inputs_tab.index('V')]
        self.inputs.clear()

        self.am = 0.1 * (25 - v) / (math.exp((25 - v) / 10) - 1)
        self.bm = 4 * math.exp(-v / 18)
        self.ah = 0.07 * math.exp(-v / 20)
        self.bh = 1 / (1 + math.exp(30 - v) / 10)
        self.m = self.m + 0.01 * (self.am * (1 - self.m) - self.bm * self.m)
        self.h = self.h + 0.01 * (self.ah * (1 - self.h) - self.bh * self.h)
        output = self.gna * self.h * (v - self.vna) * math.pow(self.m, 3)
        self.output = output
        return self.output

    def record(self):
        return self.output, self.m, self.h

class KIonHHComponent(Component):
    def __init__(self, manager, name, gk=36,vk=-12):
        super().__init__(manager, name=name)
        self.gk = gk
        self.vk = vk
        self.an = 0
        self.bn = 0
        self.n = 0

    # inputs是Vs即膜电位
    def function(self):
        v = self.inputs[self.inputs_tab.index('V')]
        self.inputs.clear()

        self.an = 0.01 * (10 - v) / ((math.exp(10 - v) / 10) - 1)
        self.bn = 0.125 * math.exp(-v / 80)
        self.n = self.n + 0.01 * (self.an * (1 - self.n) - self.bn * self.n)
        output = self.gk * (v - self.vk) * math.pow(self.n, 4)
        self.output = output
        return self.output

class lIonHHComponent(Component):
    def __init__(self, manager, name):
        super().__init__(manager, name=name)
        self.gl = 0.3
        self.vl = 10.6


    # inputs是Vs即膜电位
    def function(self):
        v = self.inputs[self.inputs_tab.index('V')]
        self.inputs.clear()

        output = self.gl * (v - self.vl)
        self.output = output
        return self.output


class PRsomaNeuron(Neuron):
    def __init__(self, manager, name, Is=10.0):
        super().__init__(manager, name=name)
        self.Is = Is
        self.p = 0.5

    def function(self):
        # var prepare
        Ina = 0.0
        Isl = 0.0
        Ikdr = 0.0
        Isd = 0.0
        vs = 0.0
        for i in range(len(self.inputs_tab)):
            if self.inputs_tab[i] == "Ina":
                Ina += self.inputs[i]
            elif self.inputs_tab[i] == "Isl":
                Isl += self.inputs[i]
            elif self.inputs_tab[i] == "Ikdr":
                Ikdr += self.inputs[i]
            elif self.inputs_tab[i] == "Isd":
                Isd += self.inputs[i]
            elif self.inputs_tab[i] == "self":
                vs += self.inputs[i]
        # clear inputs
        self.inputs.clear()

        # calculate
        output = vs + 0.01 * (self.Is/self.p - Isd/self.p - Ikdr - Isl - Ina)

        # set output
        self.output = output
        return self.output


class dendriteNeuron(Component):
    def __init__(self, manager: dict, name, I):
        super().__init__(manager, name=name)
        self.tao = 1
        self.Rm = 10
        self.I = I

    def function(self):
        din = sum(self.inputs)
        self.inputs.clear()
        self.output = self.output + 0.01 * (self.Id / (1 - self.p) -
                                self.Ids / (1 - self.p) - self.Idl) / self.C
        return self.output


class synapseNeuron(Component):
    tab = 'houmo'
    def __init__(self, manager, name, gs):
        super().__init__(manager, name=name)
        self.gs = gs


    def function(self):
        Vpost = []
        for i in range(len(self.inputs_tab)):
            if self.inputs_tab[i] == synapseNeuron.tab:
                Vpost.append(self.inputs[i])
            else:
                Vpre = self.inputs[i]

        self.inputs.clear()
        self.output = 0
        for i in range(len(Vpost)):
            self.output += self.gs[i] * (Vpre - Vpost[i])
        return self.output

class EsynapseNeuron(Component):
    tab = 'houmo'
    def __init__(self, manager, name, gs, E=-80, ts=10):
        super().__init__(manager, name=name)
        self.gs = gs
        self.E = E
        self.dt = 0.1
        self.ts = ts
        self.r = 0

    def function(self):
        Isyn = 0
        r = 0
        Vpost = []
        for i in range(len(self.inputs_tab)):
            if self.inputs_tab[i] == synapseNeuron.tab:
                Vpost.append(self.inputs[i])
            else:
                Vpre = self.inputs[i]
        self.inputs.clear()
        self.r = ((1 - self.r) / (1 + math.exp(-Vpre)) - self.r / self.ts) * self.dt + self.r
        for i in range(len(Vpost)):
            Isyn += self.gs[i] * self.r * (self.E - Vpost[i])
        self.output = Isyn
        return self.output

class ExcsynapseNeuron(Component):
    tab = 'houmo'
    def __init__(self, manager, name, gs, tao=0.5):
        super().__init__(manager, name=name)
        self.gs = gs
        self.dt = 0.1
        self.tao = tao
        self.Is = 0

    def function(self):
        Isyn = 0
        Vpost = []
        for i in range(len(self.inputs_tab)):
            if self.inputs_tab[i] == synapseNeuron.tab:
                Vpost.append(self.inputs[i])
            else:
                Vpre = self.inputs[i]
        self.inputs.clear()
        for i in range(len(Vpost)):
            if (Vpre == 30):
                Isyn += self.gs[i]
            self.Is = self.Is + self.dt *(-self.Is + Isyn) / self.tao
        self.output = self.Is
        return self.output

class InhsynapseNeuron(Component):
    tab = 'houmo'
    def __init__(self, manager, name, gs, tao=6):
        super().__init__(manager, name=name)
        self.gs = gs
        self.dt = 0.1
        self.tao = tao
        self.Is = 0

    def function(self):
        Isyn = 0
        Vpost = []
        for i in range(len(self.inputs_tab)):
            if self.inputs_tab[i] == synapseNeuron.tab:
                Vpost.append(self.inputs[i])
            else:
                Vpre = self.inputs[i]
        self.inputs.clear()
        for i in range(len(Vpost)):
            if (Vpre == 30):
                Isyn += self.gs[i]
            self.Is = self.Is + self.dt *(-self.Is + Isyn) / self.tao
        self.output = -self.Is
        return self.output

class CsynapseNeuron(Component):
    tab = 'houmo'
    def __init__(self, manager, name, gs):
        super().__init__(manager, name=name)
        self.gs = gs
        self.s = 0
        self.alpha = 2
        self.beta = 1


    def function(self):
        Vpost = []
        for i in range(len(self.inputs_tab)):
            if self.inputs_tab[i] == synapseNeuron.tab:
                Vpost.append(self.inputs[i])
            else:
                Vpre = self.inputs[i]

        self.inputs.clear()
        self.output = 0
        self.s = self.s + 0.01 * (self.alpha * (1 - self.s) - self.beta * self.s)
        for i in range(len(Vpost)):
            self.output += self.gs[i] * self.s * (Vpre - Vpost[i])
        return self.output

class STDPsynapseNeuron(Component):
    tab = 'houmo'
    def __init__(self, manager, name, gs, Vth=10):
        super().__init__(manager, name=name)
        self.gs = gs
        self.Vth=Vth
        self.preSpikeInterval = 0
        # self.postSpikeInterval = []
        # for num in range(len(gs)):
        #     self.postSpikeInterval.append(0)
        self.postSpikeInterval = [0 for i in range(len(gs))]

    def function(self):
        Vpost = []
        Vpre = 0
        for i in range(len(self.inputs_tab)):
            if self.inputs_tab[i] == synapseNeuron.tab:
                Vpost.append(self.inputs[i])
            else:
                Vpre = self.inputs[i]

        self.inputs.clear()
        self.output = 0

        for i in range(len(Vpost)):
            self.output += self.gs[i] * (Vpre - Vpost[i])

        # condition init
        preSpike = False
        postSpike = []
        for num in range(len(self.postSpikeInterval)):
            postSpike.append(False)
        if Vpre > self.Vth:
            preSpike = True
        for num in range(len(Vpost)):
            print(num, len(self.postSpikeInterval),len(Vpost))
            if Vpost[num] > self.Vth:
                postSpike[num] = True

        # interval
        self.preSpikeInterval += 1
        if preSpike:
            self.preSpikeInterval = 0
        for num in range(len(self.postSpikeInterval)):
            self.postSpikeInterval[num] += 1
            if postSpike[num]:
                self.postSpikeInterval[num] = 0

        # if enhanced
        for num in range(len(self.postSpikeInterval)):
            isSpike = postSpike[num]
            if isSpike:
                interval = self.preSpikeInterval
                if interval<100 and interval>10:
                    self.gs[i] = self.gs[i] + math.exp(-interval / 100)
                    if (self.gs[i] > 0.04):
                        self.gs[i] = 0.04
                    elif (self.gs[i] < 0.01):
                        self.gs[i] = 0.01


        # if weaken
        for num in range(len(self.postSpikeInterval)):
            isSpike = preSpike
            if isSpike:
                interval = self.postSpikeInterval[num]
                if interval<100 and interval>10:
                    self.gs[i] = min(self.gs[i] - 0.4 * math.exp(-interval / 100), 0.01)
                    if (self.gs[i] > 0.04):
                        self.gs[i] = 0.04
                    elif (self.gs[i] < 0.01):
                        self.gs[i] = 0.01

        return self.output


class NaIonComponent(Component):
    def __init__(self, manager, name):
        super().__init__(manager, name=name)
        self.gNa = 120
        self.hs = 0.999
        self.Vna = 120
        self.Minfs = 0

    # inputs是Vs即膜电位
    def function(self):
        Vs = self.inputs[self.inputs_tab.index('Vs')]
        self.inputs.clear()
        alphams = 0.32 * (13.1 - Vs) / (math.exp((13.1 - Vs) / 4.0) - 1.0)
        betams = 0.28 * (Vs - 40.1) / (math.exp((Vs - 40.1) / 5.0) - 1.0)
        self.Minfs= alphams/(alphams+betams)
        alphahs = 0.128 * math.exp((17 - Vs) / 18.0)
        betahs = 4.0 / (1.0 + math.exp((40 - Vs) / 5.0))
        self.hs = self.hs + 0.01 * (alphahs - (alphahs + betahs) * self.hs)
        output = self.gNa * math.pow(self.Minfs, 2) * self.hs * (Vs - self.Vna)
        self.output = output
        return self.output


class CaIonComponent(Component):
    def __init__(self, manager, name, Vs):
        super().__init__(manager, name=name)
        self.Vs = Vs
        self.gCa = 10
        self.s = 0.009
        self.Vca = 140

    # inputs是Vs即膜电位
    def function(self):
        din = sum(self.inputs)
        self.inputs.clear()
        self.output = self.gCa * math.pow(self.s, 2) * (din - self.Vca)
        return self.output

class KCIonComponent(Component):
    def __init__(self, manager, name, Vd):
        super().__init__(manager, name=name)
        self.Vd = Vd
        self.gkahp = 0.7
        self.q = 0.01
        self.Vk = 120

    # inputs是Vs即膜电位
    def function(self):
        din = sum(self.inputs)
        self.inputs.clear()
        self.output = self.gkahp * self.q * (din - self.Vk)
        return self.output

class KAHPIonComponent(Component):
    def __init__(self, manager, name, Vd):
        super().__init__(manager, name=name)
        self.Vd = Vd
        self.gkahp = 0.7
        self.q = 0.01
        self.Vk = 120

    # inputs是Vs即膜电位
    def function(self):
        din = sum(self.inputs)
        self.inputs.clear()
        self.output = self.gkahp * self.q * (din - self.Vk)
        return self.output


class KDRIonComponent(Component):
    def __init__(self, manager, name, Vs):
        super().__init__(manager, name=name)
        self.Vs = Vs
        self.gkdr = 15
        self.n = 0.001
        self.Vk = 120

    # inputs是Vs即膜电位
    def function(self):
        din = sum(self.inputs)
        self.inputs.clear()
        self.output = self.gkdr * self.n * (din - self.Vk)
        return self.output

class IsIonComponent(Component):
    def __init__(self, manager, name, Vs):
        super().__init__(manager, name=name)
        self.Vs = Vs
        self.gl = 0.1
        self.Vl = 0

    # inputs是Vs即膜电位
    def function(self):
        din = sum(self.inputs)
        self.inputs.clear()
        self.output = self.gl * self.n * (din - self.Vl)
        return self.output

class IleakIonComponent(Component):
    def __init__(self, manager, name, Vd):
        super().__init__(manager, name=name)
        self.Vd = Vd
        self.gl = 0.1
        self.Vl = 0

    # inputs是Vs即膜电位
    def function(self):
        din = sum(self.inputs)
        self.inputs.clear()
        self.output = self.gl * self.n * (din - self.Vl)
        return self.output


class hLNComponent(Component):
    def __init__(self, manager, name, I):
        super().__init__(manager, name=name)
        self.I = I

    def function(self):
        din = sum(self.inputs)
        self.inputs.clear()

        self.output = din
        return self.output



class addComponent(Component):
    def __init__(self, manager, name, I):
        super().__init__(manager, name=name)
        self.I = I

    def function(self):
        din = sum(self.inputs)
        self.inputs.clear()

        self.output = din
        return self.output


class mulComponent(Component):
    def __init__(self, manager, name, I):
        super().__init__(manager, name=name)
        self.I = I

    def function(self):
        din = 1
        for i in self.inputs:
            din = din * i
        self.inputs.clear()

        self.output = din
        return self.output


class selectComponent(Component):
    def __init__(self, living_dictionary: dict, name, I, threshold):
        super().__init__(living_dictionary, name=name)
        self.I = I
        self.threshold = threshold

    def function(self):
        din = self.inputs
        self.inputs.clear()

        if (din >= self.threshold):
            return 1
        else:
            return 0


class LUTComponent(Component):
    def __init__(self, manager, name, I):
        super().__init__(manager, name=name)
        self.I = I

    def function(self):
        din = sum(self.inputs)
        self.inputs.clear()

        self.output = din + 0.01 * (-40 + din + self.Rm * self.I)
        if self.output > 40:
            self.output = -40
        return self.output


class IstimComponent(Component):
    def __init__(self, manager, name, list, I=0):
        super().__init__(manager, name=name)
        self.I = I
        self.list = list

    def function(self):
        self.inputs.clear()

        a = self.list.pop()
        self.output = a
        return self.output

class IstimComponentNdarray(Component):
    def __init__(self, manager, name, list, I=0):
        super().__init__(manager, name=name)
        self.I = I
        self.list = list

    def function(self):
        self.inputs.clear()

        a = self.list.tolist.pop()
        self.output = a
        return self.output