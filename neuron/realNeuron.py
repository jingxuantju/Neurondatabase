from simulink.component import Component, Manager
import math
from neuron.neuron import Neuron
import numpy as np

class PyramidalNeuron(Neuron):
    def __init__(self, manager, name, Is):
        super().__init__(manager, name=name)
        self.output2 = 0
        self.Ena = 50
        self.Ek = -100
        self.Esl = -70
        self.Edl = -70
        self.E = 0
        self.gna = 20
        self.gk = 20
        self.gsl = 2
        self.gdl = 2
        self.gc = 1
        self.C = 2
        self.p = 0.5
        self.fai = 0.15
        self.n = 0
        self.n_ = 0
        self.tau_n = 0
        self.m_ = 0
        self.Isl = 0
        self.Idl = 0
        self.Ids = 0
        self.Id = 0
        self.Is = Is
        self.Ina = 0
        self.Ik = 0

    def function(self):
        v = 0
        Isyn = 0
        for i in range(len(self.inputs_tab)):
            if self.inputs_tab[i] == "I":
                Isyn += self.inputs[i]
            else:
                v += self.inputs[i]
        self.inputs.clear()
        self.inputs.clear()

        self.Ina = self.gna * self.m_ * (v - self.Ena)
        self.Ik = self.gk * self.n * (v - self.Ek)
        self.Isl = self.gsl * (v - self.Esl)
        self.Idl = self.gdl * (self.output2 - self.Edl)
        self.Ids = self.gc * (self.output2 - v + self.E)
        self.tau_n = 1 / math.cosh(v / 20)
        self.m_ = 0.5 * (1 + math.tanh((v + 1.2) / 18))
        self.n_ = 0.5 * (1 + math.tanh(v / 10))
        self.n = self.n + 0.01 * (self.fai * ((self.n_ - self.n / self.tau_n)))
        self.output = v + 0.01 * (self.Is / self.p + self.Ids / self.p
                                    - self.Ina - self.Ik - self.Isl) / self.C
        self.output2 = self.output2 + 0.01 * \
                       (Isyn + self.Id / (1 - self.p) - self.Ids / (1 - self.p) - self.Idl) / self.C
        return self.output

    def record(self):
        return self.output, self.Ina, self.Ik, self.Isl, self.Idl, self.m_, self.n_, self.n

class hippocampusNeuron(Neuron):
    def __init__(self, manager, name, I):
        super().__init__(manager, name=name)
        self.tao = 1
        self.Rm = 10
        self.I = I

    def function(self):
        v = 0
        Isyn = 0
        for i in range(len(self.inputs_tab)):
            if self.inputs_tab[i] == "I":
                Isyn += self.inputs[i]
            elif self.inputs_tab[i] == "self":
                v += self.inputs[i]
        self.inputs.clear()
        output = v + 0.01 * (-40 - v + self.Rm * (self.I + Isyn))
        if output > 40:
            output = -40
        self.output = output
        return self.output


class BasalNeuron(Neuron):
    def __init__(self, manager: Manager, name, I, a, b, c, d, dt=0.1):
        super().__init__(manager, name=name)
        self.output = -70
        self.u = 0
        self.I = I
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.dt = dt

    def function(self):
        v = 0
        Isyn = 0
        for i in range(len(self.inputs_tab)):
            if self.inputs_tab[i] == "I":
                Isyn += self.inputs[i]
            elif self.inputs_tab[i] == "self":
                v += self.inputs[i]
        self.inputs.clear()

        output = v + 0.1 * (0.04 * v * v + 5 * v + 140 - self.u + self.I + Isyn)
        self.u = self.u + self.dt * (self.a * (self.b * v - self.u))
        if output >= 30:
            output = self.c
            self.u = self.u + self.d
        self.output = output
        return self.output

    def record(self):
        return self.output, self.u