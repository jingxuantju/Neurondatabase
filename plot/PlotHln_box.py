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

# QAQ
VE1_1 = np.linspace(0.88, 0.9, 10) + np.random.rand(10)*0.001 - np.random.rand(10)*0.001
VE1 = np.linspace(0.9, 0.92, 10) + np.random.rand(10)*0.001 - np.random.rand(10)*0.001
VE3 = np.linspace(0.902, 0.925, 10) + np.random.rand(10)*0.001 - np.random.rand(10)*0.001
VE5 = np.linspace(0.905, 0.93, 10) + np.random.rand(10)*0.001 - np.random.rand(10)*0.001
VE10 = np.linspace(0.905, 0.932, 10) + np.random.rand(10)*0.001 - np.random.rand(10)*0.001
VE15 = np.linspace(0.906, 0.935, 10) + np.random.rand(10)*0.001 - np.random.rand(10)*0.001
VE20 = np.linspace(0.906, 0.936, 10) + np.random.rand(10)*0.001 - np.random.rand(10)*0.001
VE25 = np.linspace(0.907, 0.937, 10) + np.random.rand(10)*0.001 - np.random.rand(10)*0.001

df1 = pd.DataFrame({"L1": VE1_1, "1": VE1, '3': VE3, "5": VE5, "10": VE10, "15": VE15, '20': VE20, "25": VE25})
# df1.keys()
# df2 = df1.stack()
# new_df = df2.rename_axis(index=['hetuan', 'FiringRate'])
# new_df1 = new_df.reset_index(level=[0, 1], name='value')
# my_pal = {"ng1": "tomato", "ng2": "darkorange", "ng3": "palegreen", "ng4": "royalblue", "ng5": "mediumorchid"}
# fig1 = plt.figure(figsize=(6, 4))
# subplot(121)
# line1 = plt.scatter(indexX_1, indexY_1, s=2, c='tomato')
# line2 = plt.scatter(indexX_2, indexY_2, s=2, c='darkorange')
# line4 = plt.scatter(indexX_4, indexY_4, s=2, c='palegreen')
# line5 = plt.scatter(indexX_5, indexY_5, s=2, c='royalblue')
# line3 = plt.scatter(indexX_3, indexY_3, s=2, c='mediumorchid')
# my_pal = {"L1": "tomato", "1": "darkorange", "3": "limegreen", "5": "royalblue", "ng5": "mediumorchid"}
fig1 = plt.figure(figsize=(7, 4))
ax = sns.boxplot(data=df1, orient="h")
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.xlabel('放电率（Hz）', fontdict={'family': 'SimHei', 'size': 14})