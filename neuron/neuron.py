from simulink.component import Component, Manager
import math
import numpy as np
import random

class Neuron(Component):

    def __init__(self, manager, name):
        super().__init__(manager, name=name)
        manager.link_output_input(self, self, 'self')

class LIFNeuron(Neuron):
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


class IzhikevichNeuron(Neuron):
    def __init__(self, manager: Manager, name, I, a, b, c, d, dt=0.1):
        super().__init__(manager, name=name)
        self.output = random.randint(-75,-30)
        self.u = random.randint(-10,0)
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


class simplePRNeuron(Neuron):
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

# class PRNeuron(Neuron):
#     def __init__(self, manager, name, Is, Id):
#         super().__init__(manager, name=name)
#         self.output2 = -60
#         self.Ena = 120
#         self.Eca = 140
#         self.Ek = -38.56
#         self.Esyn = 60
#         self.El = 0
#         self.gl = 0.1
#         self.gna = 30
#         self.gca = 10
#         self.gkdr = 15
#         self.gkahp = 0.8
#         self.gkc = 15
#         self.gc = 2.1
#         self.hs = 0
#         self.ns = 0
#         self.sd = 0
#         self.cd = 0
#         self.e = 0
#         self.qd = 0
#         self.ca = 0.2
#         self.Minfs = 0
#         self.cm = 3
#         self.Cad = 0
#         self.chid = 0
#         self.p = 0.5
#         self.Is = Is
#         self.Id = Id
#         self.dt = 0.01
#
#
#
#
#     def function(self):
#         din = sum(self.inputs)
#         self.inputs.clear()
#
#         self.Ina = self.gna * self.Minfs * self.Minfs * self.hs * (self.output - self.Ena)
#         self.Ikdr = self.gkdr * self.ns * (self.output - self.Ek)
#         self.Ikahp = self.gkahp * self.qd * (self.output2 - self.Ek)
#         self.Ikc = self.gkc * self.cd * self.chid * (self.output2 - self.Ek)
#         self.Ica = self.gca * self.sd * self.sd * (self.output2 - self.Eca)
#         self.Isl = self.gl * (self.output - self.El)
#         self.Idl = self.gl * (self.output2 - self.El)
#         self.Ids = (self.output - self.output2)
#         self.alphams = 0.32 * (13.1 - self.output) / (math.exp((13.1 - self.output) / 4.0) - 1.0)
#         self.betams = 0.28 * (self.output - 40.1) / (math.exp((self.output - 40.1) / 5.0) - 1.0)
#         self.Minfs= self.alphams/(self.alphams+self.betams)
#         self.alphans = 0.016 * (35.1 - self.output) / (math.exp((35.1 - self.output) / 5.0) - 1.0)
#         self.betans = 0.25 * math.exp(0.5 - 0.025 * self.output)
#         self.ns = self.ns + self.dt * (self.alphans - (self.alphans + self.betans) * self.ns)
#         self.alphahs = 0.128 * math.exp((17 - self.output) / 18.0)
#         self.betahs = 4.0 / (1.0 + math.exp((40 - self.output) / 5.0))
#         self.hs = self.hs + self.dt * (self.alphahs - (self.alphahs + self.betahs) * self.hs)
#         self.alphasd = 1.6 / (1.0 + math.exp(-0.072 * (self.output2 - 65)))
#         self.betasd = 0.02 * (self.output2 - 51.1) / (math.exp((self.output2 - 51.1) / 5.0) - 1.0)
#         self.sd = self.sd + self.dt * (self.alphasd - (self.alphasd + self.betasd) * self.sd)
#         if self.output2 <= 50:
#             self.alphacd = (math.exp((self.output2 - 10) /11)- math.exp((self.output2 - 6.5)/27.0)) / 18.975
#             self.betacd = 2 * math.exp((6.5 - self.output2) / 27) - self.alphacd
#         if self.output2 > 50:
#             self.alphacd = 2 * math.exp((6.5 - self.output2) / 27)
#             self.betacd = 0
#         self.cd = self.cd + self.dt * (self.alphacd - (self.alphacd + self.betacd) * self.cd)
#         self.alphaqd = min(0.00002 * self.Cad, 0.01)
#         self.betaqd = 0.001
#         self.qd = self.qd + self.dt * (self.alphaqd-(self.alphaqd+self.betaqd)*self.qd)
#         self.Cad = self.Cad - self.dt * (0.13 * self.Ica+0.075*self.Cad)
#         self.chid = min(self.Cad / 250.0, 1.0)
#         self.output = self.output + self.dt * (self.Is / self.p + self.gc * self.Ids / self.p
#                                     - self.Ina - self.Ikdr - self.Isl) / self.cm
#         self.output2 = self.output2 + self.dt * (self.Id / (1 - self.p) - self.gc * self.Ids /
#                                               (1 - self.p) - self.Idl - self.Ica - self.Ikahp - self.Ikc) / self.cm
#         return self.output
#
#     def record(self):
#         return self.output, self.output2


class PRNeuron(Neuron):
    def __init__(self, manager, name, Is, Id):
        super().__init__(manager, name=name)
        self.output2 = -60
        self.Ena = 60
        self.Eca = 80
        self.Ek = -75
        self.Esyn = 60
        self.El = -60
        self.gl = 0.1
        self.gna = 30
        self.gca = 10
        self.gkdr = 15
        self.gkahp = 0.8
        self.gkc = 15
        self.gc = 2.1
        self.hs = 0
        self.ns = 0
        self.sd = 0
        self.cd = 0
        self.e = 0
        self.qd = 0
        self.ca = 0.2
        self.Minfs = 0
        self.cm = 3
        self.Cad = 0
        self.chid = 0
        self.p = 0.5
        self.Is = Is
        self.Id = Id
        self.dt = 0.01
        self.output = -60
        self.output2 = -60




    def function(self):
        din = sum(self.inputs)
        self.inputs.clear()

        self.Ina = self.gna * self.Minfs * self.Minfs * self.hs * (self.output - self.Ena)
        self.Ikdr = self.gkdr * self.ns * (self.output - self.Ek)
        self.Ikahp = self.gkahp * self.qd * (self.output2 - self.Ek)
        self.Ikc = self.gkc * self.cd * self.chid * (self.output2 - self.Ek)
        self.Ica = self.gca * self.sd * self.sd * (self.output2 - self.Eca)
        self.Isl = self.gl * (self.output - self.El)
        self.Idl = self.gl * (self.output2 - self.El)
        self.Ids = (self.output - self.output2)
        self.alphams = 0.32 * (46.9 - self.output) / (math.exp((46.9 - self.output) / 4.0) - 1.0)
        self.betams = 0.28 * (self.output + 19.9) / (math.exp((self.output + 19.9) / 5.0) - 1.0)
        self.Minfs= self.alphams/(self.alphams+self.betams)
        self.alphans = 0.016 * (-24.9 - self.output) / (math.exp((-24.9 - self.output) / 5.0) - 1.0)
        self.betans = 0.25 * math.exp(-1.0 - 0.025 * self.output)
        self.ns = self.ns + self.dt * (self.alphans - (self.alphans + self.betans) * self.ns)
        self.alphahs = 0.128 * math.exp((-43.0 - self.output) / 18.0)
        self.betahs = 4.0 / (1.0 + math.exp((-20 - self.output) / 5.0))
        self.hs = self.hs + self.dt * (self.alphahs - (self.alphahs + self.betahs) * self.hs)
        self.alphasd = 1.6 / (1.0 + math.exp(-0.072 * (self.output2 - 5)))
        self.betasd = 0.02 * (self.output2 + 8.9) / (math.exp((self.output2 + 8.9) / 5.0) - 1.0)
        self.sd = self.sd + self.dt * (self.alphasd - (self.alphasd + self.betasd) * self.sd)
        self.alphacd = (1.0-self.heav(self.output2+10.0))*math.exp((self.output2+50.0)/11-(self.output2+53.5)/27)/18.975+self.heav(self.output2+10.0)*2.0*math.exp((-53.5-self.output2)/27.0)
        self.betacd = (1.0-self.heav(self.output2+10.0))*(2.0*math.exp((-53.5-self.output2)/27.0)-self.alphacd)
        self.cd = self.cd + self.dt * (self.alphacd - (self.alphacd + self.betacd) * self.cd)
        self.alphaqd = min(0.00002 * self.Cad, 0.01)
        self.betaqd = 0.001
        self.qd = self.qd + self.dt * (self.alphaqd-(self.alphaqd+self.betaqd)*self.qd)
        self.Cad = self.Cad - self.dt * (0.13 * self.Ica+0.075*self.Cad)
        self.chid = min(self.Cad / 250.0, 1.0)
        self.output = self.output + self.dt * (self.Is / self.p + self.gc * self.Ids / self.p
                                    - self.Ina - self.Ikdr - self.Isl) / self.cm
        self.output2 = self.output2 + self.dt * (self.Id / (1 - self.p) - self.gc * self.Ids /
                                              (1 - self.p) - self.Idl - self.Ica - self.Ikahp - self.Ikc) / self.cm
        return self.output

    def record(self):
        return self.output, self.output2

    def heav(self, v):
        if v >= 0:
            return 1
        else:
            return 0

# class HHNeuron(Neuron):
#     def __init__(self, manager, name, I):
#         super().__init__(manager, name=name)
#         self.I = I
#         self.vna = 50
#         self.vk = -77
#         self.vl = -54.4
#         self.gna = 120
#         self.gk = 36
#         self.gl = 0.3
#         self.c = 1
#         self.v = 0
#         self.m = 0
#         self.h = 0
#         self.n = 0
#         self.am = 0
#         self.bm = 0
#         self.ah = 0
#         self.bh = 0
#         self.an = 0
#         self.bn = 0
#
#     def function(self):
#         v = 0
#         SynapseI = 0
#         for i in range(len(self.inputs_tab)):
#             if self.inputs_tab[i] == "I":
#                 SynapseI += self.inputs[i]
#             else:
#                 v += self.inputs[i]
#         self.inputs.clear()
#         self.inputs.clear()
#
#         self.am = 0.1 * (v + 40) / (1 - math.exp(-(v + 40) / 10))
#         self.bm = 4 * math.exp(-(v + 65) / 18)
#         self.ah = 0.07 * math.exp(-(v + 65) / 20)
#         self.bh = 1 / (1 + math.exp(-(v + 35) / 10))
#         self.an = 0.01 * (v + 55) / (1 - math.exp(-(v + 55) / 10))
#         self.bn = 0.125 * math.exp(-(v + 65) / 80)
#         self.m = self.m + 0.01 * (self.am * (1 - self.m) - self.bm * self.m)
#         self.h = self.h + 0.01 * (self.ah * (1 - self.h) - self.bh * self.h)
#         self.n = self.n + 0.01 * (self.an * (1 - self.n) - self.bn * self.n)
#         self.output = v + 0.01 * (self.I -
#                                     self.gna * self.h * (v - self.vna) * math.pow(self.m, 3) -
#                                     self.gk * (v - self.vk) * math.pow(self.n, 4) -
#                                     self.gl * (v - self.vl)) / self.c
#         return self.output


class HHNeuron(Neuron):
    def __init__(self, manager, name, I, dt=0.01):
        super().__init__(manager, name=name)
        self.I = I
        self.vna = 120
        self.vk = -12
        self.vl = 10.6
        self.gna = 120
        self.gk = 36
        self.gl = 0.3
        self.c = 1
        self.v = 0
        self.m = 0
        self.h = 0
        self.n = 0
        self.am = 0
        self.bm = 0
        self.ah = 0
        self.bh = 0
        self.an = 0
        self.bn = 0
        self.m_ = 0
        self.n_ = 0
        self.h_ = 0
        self.dt = dt

    def function(self):
        v = 0
        Isyn = 0
        for i in range(len(self.inputs_tab)):
            if self.inputs_tab[i] == "I":
                Isyn += self.inputs[i]
            else:
                v += self.inputs[i]
        self.inputs.clear()

        self.am = 0.1 * (25 - v) / (math.exp((25 - v) / 10) - 1)
        self.bm = 4 * math.exp(-v / 18)
        self.ah = 0.07 * math.exp(-v / 20)
        self.bh = 1 / (1 + math.exp(30 - v) / 10)
        self.an = 0.01 * (10 - v) / ((math.exp(10 - v) / 10) - 1)
        self.bn = 0.125 * math.exp(-v / 80)
        self.m = self.m + self.dt * (self.am * (1 - self.m) - self.bm * self.m)
        self.h = self.h + self.dt * (self.ah * (1 - self.h) - self.bh * self.h)
        self.n = self.n + self.dt * (self.an * (1 - self.n) - self.bn * self.n)
        self.m_ = self.am / (self.am + self.bm)
        self.n_ = self.an / (self.an + self.bn)
        self.h_ = self.ah / (self.ah + self.bh)
        self.output = v + self.dt * (self.I + Isyn -
                                    self.gna * self.h * (v - self.vna) * math.pow(self.m, 3) -
                                    self.gk * (v - self.vk) * math.pow(self.n, 4) -
                                    self.gl * (v - self.vl)) / self.c
        return self.output

    def record(self):
        return self.output, self.m, self.h, self.n, self.m_, self.n_, self.h_, \
               self.gna * self.h * math.pow(self.m, 3), self.gk * math.pow(self.n, 4)



