from simulink.component import Component, Manager
import math
import numpy as np
from neuron.neuron import *
from pylab import *
from neuron.layer import *
import scipy.io as scio
import copy
import cv2
import matplotlib.gridspec as gridspec
from scipy import misc
# import imageio

t_span = 2000
real_t_span = 200

n0 = np.load('ng_v.npz')
ng1_array = n0['ng1_array']
ng2_array = n0['ng2_array']
ng3_array = n0['ng3_array']

SPK_ng1 = np.where(ng1_array > 10, 1, 0)
SPK_ng2 = np.where(ng2_array > 10, 1, 0)
SPK_ng3 = np.where(ng3_array > 10, 1, 0)

# Get the index of a scatter map
indexX_1 = []
indexY_1 = []
indexX_2 = []
indexY_2 = []
indexX_3 = []
indexY_3 = []
for j in range(100):
    # for t in range(2000, t_span):
    for t in range(t_span):
        if SPK_ng1[j][t] == 1:
            indexX_1.append(t)
            indexY_1.append(j)
    for t in range(t_span):
        if SPK_ng2[j][t] == 1:
            indexX_2.append(t)
            indexY_2.append(j)
    for t in range(t_span):
        if SPK_ng3[j][t] == 1:
            indexX_3.append(t)
            indexY_3.append(j)

xr = range(1000, t_span, 1000)
fig1 = plt.figure(figsize=(6, 8), dpi=100)
gs = gridspec.GridSpec(15, 2)
plt.subplot(321)
# plt.title('(a) pd=0')
line1 = plt.scatter(indexX_1, indexY_1, s=2, c='k')
plt.xlim(1000, t_span)
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.xticks(xr, range(100, real_t_span, 200))
plt.ylabel('ng1', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
plt.subplot(322)
line2 = plot(ng1_array[10], c='k')
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.xlim(1000, t_span)
plt.xticks(xr, range(100, real_t_span, 200))
plt.xlabel('时间(ms)', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
plt.ylabel('ng1膜电位(mV)', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
plt.subplot(323)
line3 = plt.scatter(indexX_2, indexY_2, s=2, c='k')
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.xlim(1000, t_span)
plt.xticks(xr, range(100, real_t_span, 200))
plt.ylabel('ng2', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
# plt.title('(b) pd=0')
plt.subplot(324)
line4 = plot(ng2_array[10], c='k')
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.xlim(1000, t_span)
plt.xticks(xr, range(100, real_t_span, 200))
plt.xlabel('时间(ms)', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
plt.ylabel('ng2膜电位(mV)', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
plt.subplot(325)
line5 = plt.scatter(indexX_3, indexY_3, s=2, c='k')
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.xlim(1000, t_span)
plt.xticks(xr, range(100, real_t_span, 200))
plt.ylabel('ng3', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
plt.subplot(326)
line6 = plot(ng3_array[10], c='k')
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.xlim(1000, t_span)
plt.xticks(xr, range(100, real_t_span, 200))
plt.xlabel('时间(ms)', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
plt.ylabel('ng3膜电位(mV)', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
fig1.tight_layout()
plt.show()













