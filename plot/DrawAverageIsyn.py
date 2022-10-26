import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.io as scio
from neuron.neuron import *


nv = np.load('pd0_v.npz')
ni = np.load('pd0_i.npz')
V_STN_array = nv['V_STN_array']
V_GPE_array = nv['V_GPE_array']
V_GPI_array = nv['V_GPI_array']
V_TH_array = nv['V_TH_array']
SYN_stn_gpe_array = ni['SYN_stn_gpe_array']
SYN_stn_gpi_array = ni['SYN_stn_gpi_array']
SYN_gpe_stn_array = ni['SYN_gpe_stn_array']
SYN_gpe_gpi_array = ni['SYN_gpe_gpi_array']
SYN_gpe_gpe_array = ni['SYN_gpe_gpe_array']
SYN_gpi_tc_array = ni['SYN_gpi_tc_array']
Nn = 100
t_span = 12000
real_t_span = 1200
data_t_span = len(V_STN_array)

Itot_stn_gpe = np.sum(SYN_stn_gpe_array, axis=0)
Ilfp_stn_gpe = Itot_stn_gpe / Nn

Itot_stn_gpi = np.sum(SYN_stn_gpi_array, axis=0)
Ilfp_stn_gpi = Itot_stn_gpi / Nn

Itot_gpe_stn = np.sum(SYN_gpe_stn_array, axis=0)
Ilfp_gpe_stn = Itot_gpe_stn / Nn

Itot_gpe_gpi = np.sum(SYN_gpe_gpi_array, axis=0)
Ilfp_gpe_gpi = Itot_gpe_gpi / Nn

Itot_gpe_gpe = np.sum(SYN_gpe_gpe_array, axis=0)
Ilfp_gpe_gpe = Itot_gpe_gpe / Nn

Itot_gpi_tc = np.sum(SYN_gpi_tc_array, axis=0)
Ilfp_gpi_tc = Itot_gpi_tc / Nn

Ilfp = (Ilfp_stn_gpe + Ilfp_stn_gpi + Ilfp_gpe_stn + Ilfp_gpe_gpi + Ilfp_gpe_gpe + Ilfp_gpi_tc)/6

fig1 = plt.figure(figsize=(6, 8), dpi=100)
plt.subplot(311)
plt.plot(Ilfp_stn_gpe, c='tomato', linewidth=2)
plt.xlim(2000, t_span)
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.ylabel('STN_GPE', fontdict={'family': 'SimHei', 'size': 14})
plt.subplot(312)
plt.plot(Ilfp_stn_gpi, c='plum', linewidth=2)
plt.xlim(2000, t_span)
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.ylabel('STN_GPI', fontdict={'family': 'SimHei', 'size': 14})
# plt.subplot(313)
# plt.plot(Ilfp_gpe_stn, c='royalblue', linewidth=2)
# plt.xlim(2000, t_span)
# plt.yticks(fontproperties='Times New Roman', size=14)
# plt.xticks(fontproperties='Times New Roman', size=14)
# plt.ylabel('GPE_STN', fontdict={'family': 'SimHei', 'size': 14})
plt.subplot(313)
plt.plot(Ilfp_gpi_tc, c='gold', linewidth=2)
plt.xlim(2000, t_span)
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.ylabel('GPI_TC', fontdict={'family': 'SimHei', 'size': 14})
# plt.show()
fig2 = plt.figure(figsize=(6, 3), dpi=100)
plt.plot(Ilfp, c='lightgreen', linewidth=2)
plt.xlim(2000, t_span)
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.ylabel('总电流', fontdict={'family': 'SimHei', 'size': 14})