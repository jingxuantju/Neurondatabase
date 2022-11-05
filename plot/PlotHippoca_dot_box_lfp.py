from simulink.component import Component, Manager
import math
import numpy as np
from neuron.neuron import *
import pywt
import pandas as pd
import seaborn as sns
from pylab import *
from neuron.layer import *
import scipy.io as scio
import copy
import cv2
import matplotlib.gridspec as gridspec
from scipy import misc
# import imageio
num = 20
real_t_span = 1000

n0 = np.load('ng_v5.npz')
ng1_array = n0['ng1_array']
ng2_array = n0['ng2_array']
ng3_array = n0['ng3_array']
ng4_array = n0['ng4_array']
ng5_array = n0['ng5_array']
t_span = 10000

SPK_ng1 = np.where(ng1_array > 10, 1, 0)
SPK_ng2 = np.where(ng2_array > 10, 1, 0)
SPK_ng3 = np.where(ng3_array > 10, 1, 0)
SPK_ng4 = np.where(ng4_array > 10, 1, 0)
SPK_ng5 = np.where(ng5_array > 10, 1, 0)

SS_ng1 = np.sum(SPK_ng1, axis=0)
SS_ng2 = np.sum(SPK_ng2, axis=0)
SS_ng3 = np.sum(SPK_ng3, axis=0)
SS_ng4 = np.sum(SPK_ng4, axis=0)
SS_ng5 = np.sum(SPK_ng5, axis=0)

SS_1 = []
SS_2 = []
SS_3 = []
SS_4 = []
SS_5 = []
window = 50
tw1 = math.floor(len(SS_ng1) / window)
tw2 = math.floor(len(SS_ng2) / window)
tw3 = math.floor(len(SS_ng3) / window)
tw4 = math.floor(len(SS_ng4) / window)
tw5 = math.floor(len(SS_ng5) / window)
s0 = np.zeros(tw1)
for i in range(tw1):
    ps1 = 0
    ps2 = 0
    ps3 = 0
    ps4 = 0
    ps5 = 0
    for j in range(window):
        ps1 += SS_ng1[window*i+j]
        ps2 += SS_ng2[window*i+j]
        ps3 += SS_ng3[window*i+j]
        ps4 += SS_ng4[window*i+j]
        ps5 += SS_ng5[window*i+j]
    SS_1.append(ps1)
    SS_2.append(ps2)
    SS_3.append(ps3)
    SS_4.append(ps4)
    SS_5.append(ps5)

# TODO：这里是正确的对应关系，但名字起乱了
df1 = pd.DataFrame({"ng5": SS_3, "ng4": SS_4, 'ng3': SS_5, "ng2": SS_2, "ng1": SS_1})
# df1.keys()
df2 = df1.stack()
new_df = df2.rename_axis(index=['hetuan', 'FiringRate'])
new_df1 = new_df.reset_index(level=[0, 1], name='value')

# Get the index of a scatter map
indexX_1 = []
indexY_1 = []
indexX_2 = []
indexY_2 = []
indexX_3 = []
indexY_3 = []
indexX_4 = []
indexY_4 = []
indexX_5 = []
indexY_5 = []
for j in range(num):
    for t in range(t_span):
        if SPK_ng1[j][t] == 1:
            indexX_1.append(t)
            indexY_1.append(j)
    for t in range(t_span):
        if SPK_ng2[j][t] == 1:
            indexX_2.append(t)
            indexY_2.append(j+20)
    for t in range(t_span):
        if SPK_ng3[j][t] == 1:
            indexX_3.append(t)
            indexY_3.append(j+80)
    for t in range(t_span):
        if SPK_ng4[j][t] == 1:
            indexX_4.append(t)
            indexY_4.append(j+40)
    for t in range(t_span):
        if SPK_ng5[j][t] == 1:
            indexX_5.append(t)
            indexY_5.append(j+60)
# my_pal = {"ng1": "tomato", "ng2": "darkorange", "ng3": "palegreen", "ng4": "royalblue", "ng5": "mediumorchid"}
# fig1 = plt.figure(figsize=(6, 4))
# subplot(121)
# line1 = plt.scatter(indexX_1, indexY_1, s=2, c='tomato')
# line2 = plt.scatter(indexX_2, indexY_2, s=2, c='darkorange')
# line4 = plt.scatter(indexX_4, indexY_4, s=2, c='palegreen')
# line5 = plt.scatter(indexX_5, indexY_5, s=2, c='royalblue')
# line3 = plt.scatter(indexX_3, indexY_3, s=2, c='mediumorchid')
my_pal = {"ng1": "tomato", "ng2": "darkorange", "ng3": "limegreen", "ng4": "royalblue", "ng5": "mediumorchid"}
fig1 = plt.figure(figsize=(7, 4))
subplot(121)
line1 = plt.scatter(indexX_1, indexY_1, s=2, c=my_pal['ng1'])
line2 = plt.scatter(indexX_2, indexY_2, s=2, c=my_pal['ng2'])
line3 = plt.scatter(indexX_3, indexY_3, s=2, c=my_pal['ng5'])
line4 = plt.scatter(indexX_4, indexY_4, s=2, c=my_pal['ng4'])
line5 = plt.scatter(indexX_5, indexY_5, s=2, c=my_pal['ng3'])
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.xlim(2000, t_span)
xr = range(2000, t_span, 2000)
plt.xticks(xr, range(200, 1000, 200))
plt.xlabel('时间（ms）', fontdict={'family': 'SimHei', 'size': 14})
plt.ylabel('神经元索引', fontdict={'family': 'SimHei', 'size': 14})
subplot(122)
ax = sns.boxplot(data=df1, orient="h", palette=my_pal)
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.xlabel('放电率（Hz）', fontdict={'family': 'SimHei', 'size': 14})

# Caculate LFP
V_mean_1 = np.mean(ng1_array, axis=0)
V_mean_2 = np.mean(ng2_array, axis=0)
V_mean_3 = np.mean(ng3_array, axis=0)
V_mean_4 = np.mean(ng4_array, axis=0)
V_mean_5 = np.mean(ng5_array, axis=0)

V_mean_e = (V_mean_1 + V_mean_2 + V_mean_4 + V_mean_5) / 4
V_mean_all = (V_mean_1 + V_mean_2 + V_mean_3 + V_mean_4 + V_mean_5) / 5

fig2 = plt.figure(figsize=(6, 6))
plt.subplot(211)
l1 = plot(V_mean_e,c='b')
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.xlabel('时间(ms)', fontdict={'family': 'SimHei', 'size': 14})
plt.ylabel('兴奋性核团LFP(mV)', fontdict={'family': 'SimHei', 'size': 14})
plt.xlim(2000, t_span)
plt.ylim(-72, -58)
plt.xticks(xr, range(200, 1000, 200))
plt.subplot(212)
l2 = plot(V_mean_3,c='r')
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.xlabel('时间(ms)', fontdict={'family': 'SimHei', 'size': 14})
plt.ylabel('抑制性核团LFP(mV)', fontdict={'family': 'SimHei', 'size': 14})
plt.xlim(2000, t_span)
plt.ylim(-70, -45)
plt.xticks(xr, range(200, 1000, 200))
# plt.subplot(313)
# l3 = plot(V_mean_all)
# plt.yticks(fontproperties='Times New Roman', size=14)
# plt.xticks(fontproperties='Times New Roman', size=14)
# plt.xlabel('时间(ms)', fontdict={'family': 'SimHei', 'size': 14})
# plt.ylabel('ng1 LFP(mV)', fontdict={'family': 'SimHei', 'size': 14})
# plt.xlim(2000, t_span)
# plt.xticks(xr, range(200, 1000, 200))
fig2.tight_layout()

# # Caculate LFP
# V_mean_1 = np.mean(ng1_array, axis=0)
# V_mean_2 = np.mean(ng2_array, axis=0)
# V_mean_3 = np.mean(ng3_array, axis=0)

# sampling_rate = 1024
# wavename = 'cgau8'
# totalscal = 256
# fc = pywt.central_frequency(wavename)
# cparam = 2 * fc * totalscal
# scales = cparam / np.arange(totalscal, 1, -1)
# [cwtmatr1, frequencies1] = pywt.cwt(V_mean_1, scales, wavename, 1.0 / sampling_rate)
# [cwtmatr2, frequencies2] = pywt.cwt(V_mean_2, scales, wavename, 1.0 / sampling_rate)
# [cwtmatr3, frequencies3] = pywt.cwt(V_mean_3, scales, wavename, 1.0 / sampling_rate)
# fig2 = plt.figure(figsize=(6, 8), dpi=100)
# plt.subplot(311)
# plt.contourf(range(t_span), frequencies1, abs(cwtmatr1))
# plt.subplot(312)
# plt.contourf(range(t_span), frequencies2, abs(cwtmatr2))
# plt.subplot(313)
# plt.contourf(range(t_span), frequencies3, abs(cwtmatr3))
# fig2.tight_layout()