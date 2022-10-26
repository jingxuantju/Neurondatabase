import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.io as scio
from neuron.neuron import *

n0 = np.load('pd0.npz')
n1 = np.load('pd1.npz')
V_STN_array = n0['V_STN_array']
V_GPE_array = n0['V_GPE_array']
V_GPI_array = n0['V_GPI_array']
V_TH_array = n0['V_TH_array']
V1_STN_array = n1['V1_STN_array']
V1_GPE_array = n1['V1_GPE_array']
V1_GPI_array = n1['V1_GPI_array']
V1_TH_array = n1['V1_TH_array']
t_span = 12000
real_t_span = 1200
data_t_span = len(V_STN_array)

Nn = 100
t_span = 12000
real_t_span = 1200
data_t_span = len(V_STN_array)

V_mean_stn = np.mean(V_STN_array, axis=0)
V_mean_gpe = np.mean(V_GPE_array, axis=0)
V_mean_gpi = np.mean(V_GPI_array, axis=0)
V_mean_th = np.mean(V_TH_array, axis=0)
V1_mean_stn = np.mean(V1_STN_array, axis=0)
V1_mean_gpe = np.mean(V1_GPE_array, axis=0)
V1_mean_gpi = np.mean(V1_GPI_array, axis=0)
V1_mean_th = np.mean(V1_TH_array, axis=0)

fig1 = plt.figure(figsize=(6, 8), dpi=100)
plt.title('正常', fontdict={'family': 'SimHei', 'size': 14})
plt.subplot(411)
plt.plot(V_mean_stn, c='k', linewidth=2)
plt.xlim(2000, t_span)
plt.ylim(-70, -45)
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.ylabel('STN', fontdict={'family': 'SimHei', 'size': 14})
plt.subplot(412)
plt.plot(V_mean_gpe, c='k', linewidth=2)
plt.xlim(2000, t_span)
plt.ylim(-70, -54)
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.ylabel('GPE', fontdict={'family': 'SimHei', 'size': 14})
plt.subplot(413)
plt.plot(V_mean_gpi, c='k', linewidth=2)
plt.xlim(2000, t_span)
plt.ylim(-70, -40)
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.ylabel('GPI', fontdict={'family': 'SimHei', 'size': 14})
plt.subplot(414)
plt.plot(V_mean_th, c='k', linewidth=2)
plt.xlim(2000, t_span)
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.ylabel('TH', fontdict={'family': 'SimHei', 'size': 14})
# plt.show()

fig2 = plt.figure(figsize=(6, 8), dpi=100)
plt.title('PD', fontdict={'family': 'SimHei', 'size': 14})
plt.subplot(411)
plt.plot(V1_mean_stn, c='k', linewidth=2)
plt.xlim(2000, t_span)
plt.ylim(-70, -45)
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.ylabel('STN', fontdict={'family': 'SimHei', 'size': 14})
plt.subplot(412)
plt.plot(V1_mean_gpe, c='k', linewidth=2)
plt.xlim(2000, t_span)
plt.ylim(-70, -54)
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.ylabel('GPE', fontdict={'family': 'SimHei', 'size': 14})
plt.subplot(413)
plt.plot(V1_mean_gpi, c='k', linewidth=2)
plt.xlim(2000, t_span)
plt.ylim(-70, -40)
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.ylabel('GPI', fontdict={'family': 'SimHei', 'size': 14})
plt.subplot(414)
plt.plot(V1_mean_th, c='k', linewidth=2)
plt.xlim(2000, t_span)
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.ylabel('TH', fontdict={'family': 'SimHei', 'size': 14})