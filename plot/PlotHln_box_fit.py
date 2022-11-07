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
import scipy.io

V1D = scipy.io.loadmat('HLN1L.mat')
V1L = V1D["V1L"][0]
V1N = V1D["V1N"][0]
V2N = V1D["V2N"][0]
V2NM = V1D["V2NM"][0]
V3N = V1D["V3N"][0]
V3NM = V1D["V3NM"][0]
V4N = V1D["V4N"][0]
V4NM = V1D["V4NM"][0]

df1 = pd.DataFrame({"1L": V1L, "1N": V1N, '2N': V2N, "2N-M": V2NM,
                    "3N": V3N, "3N-M": V3NM, '4N': V4N, "4N-M": V4NM})

V1D = scipy.io.loadmat('HLN1N.mat')
V1L = V1D["V1L"][0]
V1N = V1D["V1N"][0]
V2N = V1D["V2N"][0]
V2NM = V1D["V2NM"][0]
V3N = V1D["V3N"][0]
V3NM = V1D["V3NM"][0]
V4N = V1D["V4N"][0]
V4NM = V1D["V4NM"][0]

df2 = pd.DataFrame({"1L": V1L, "1N": V1N, '2N': V2N, "2N-M": V2NM,
                    "3N": V3N, "3N-M": V3NM, '4N': V4N, "4N-M": V4NM})

V1D = scipy.io.loadmat('HLN2N.mat')
V1L = V1D["V1L"][0]
V1N = V1D["V1N"][0]
V2N = V1D["V2N"][0]
V2NM = V1D["V2NM"][0]
V3N = V1D["V3N"][0]
V3NM = V1D["V3NM"][0]
V4N = V1D["V4N"][0]
V4NM = V1D["V4NM"][0]

df3 = pd.DataFrame({"1L": V1L, "1N": V1N, '2N': V2N, "2N-M": V2NM,
                    "3N": V3N, "3N-M": V3NM, '4N': V4N, "4N-M": V4NM})

V1D = scipy.io.loadmat('HLN2NM.mat')
V1L = V1D["V1L"][0]
V1N = V1D["V1N"][0]
V2N = V1D["V2N"][0]
V2NM = V1D["V2NM"][0]
V3N = V1D["V3N"][0]
V3NM = V1D["V3NM"][0]
V4N = V1D["V4N"][0]
V4NM = V1D["V4NM"][0]

df4 = pd.DataFrame({"1L": V1L, "1N": V1N, '2N': V2N, "2N-M": V2NM,
                    "3N": V3N, "3N-M": V3NM, '4N': V4N, "4N-M": V4NM})

V1D = scipy.io.loadmat('HLN3N.mat')
V1L = V1D["V1L"][0]
V1N = V1D["V1N"][0]
V2N = V1D["V2N"][0]
V2NM = V1D["V2NM"][0]
V3N = V1D["V3N"][0]
V3NM = V1D["V3NM"][0]
V4N = V1D["V4N"][0]
V4NM = V1D["V4NM"][0]

df5 = pd.DataFrame({"1L": V1L, "1N": V1N, '2N': V2N, "2N-M": V2NM,
                    "3N": V3N, "3N-M": V3NM, '4N': V4N, "4N-M": V4NM})

V1D = scipy.io.loadmat('HLN3NM.mat')
V1L = V1D["V1L"][0]
V1N = V1D["V1N"][0]
V2N = V1D["V2N"][0]
V2NM = V1D["V2NM"][0]
V3N = V1D["V3N"][0]
V3NM = V1D["V3NM"][0]
V4N = V1D["V4N"][0]
V4NM = V1D["V4NM"][0]

df6 = pd.DataFrame({"1L": V1L, "1N": V1N, '2N': V2N, "2N-M": V2NM,
                    "3N": V3N, "3N-M": V3NM, '4N': V4N, "4N-M": V4NM})

V1D = scipy.io.loadmat('HLN4N.mat')
V1L = V1D["V1L"][0]
V1N = V1D["V1N"][0]
V2N = V1D["V2N"][0]
V2NM = V1D["V2NM"][0]
V3N = V1D["V3N"][0]
V3NM = V1D["V3NM"][0]
V4N = V1D["V4N"][0]
V4NM = V1D["V4NM"][0]

df7 = pd.DataFrame({"1L": V1L, "1N": V1N, '2N': V2N, "2N-M": V2NM,
                    "3N": V3N, "3N-M": V3NM, '4N': V4N, "4N-M": V4NM})

V1D = scipy.io.loadmat('HLN4NM.mat')
V1L = V1D["V1L"][0]
V1N = V1D["V1N"][0]
V2N = V1D["V2N"][0]
V2NM = V1D["V2NM"][0]
V3N = V1D["V3N"][0]
V3NM = V1D["V3NM"][0]
V4N = V1D["V4N"][0]
V4NM = V1D["V4NM"][0]

df8 = pd.DataFrame({"1L": V1L, "1N": V1N, '2N': V2N, "2N-M": V2NM,
                    "3N": V3N, "3N-M": V3NM, '4N': V4N, "4N-M": V4NM})

fig1 = plt.figure()
# subplot(241)
subplot(421)
ax1 = sns.boxplot(data=df1, orient="h")
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.xlabel('放电率（Hz）', fontdict={'family': 'SimHei', 'size': 14})
plt.xlim(0, 1)
subplot(422)
# fig2 = plt.figure(figsize=(4, 4))
ax2 = sns.boxplot(data=df2, orient="h")
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.xlabel('拟合能力', fontdict={'family': 'SimHei', 'size': 14})
plt.xlim(0, 1)
# fig3 = plt.figure(figsize=(4, 4))
subplot(423)
ax3 = sns.boxplot(data=df3, orient="h")
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.xlabel('放电率（Hz）', fontdict={'family': 'SimHei', 'size': 14})
plt.xlim(0, 1)
# fig1.tight_layout()
# fig4 = plt.figure(figsize=(4, 4))
subplot(424)
ax4 = sns.boxplot(data=df4, orient="h")
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.xlabel('放电率（Hz）', fontdict={'family': 'SimHei', 'size': 14})
plt.xlim(0, 1)
# fig5 = plt.figure(figsize=(4, 4))
subplot(425)
ax5 = sns.boxplot(data=df5, orient="h")
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.xlabel('放电率（Hz）', fontdict={'family': 'SimHei', 'size': 14})
plt.xlim(0, 1)

# fig6 = plt.figure(figsize=(4, 4))
subplot(426)
ax6 = sns.boxplot(data=df6, orient="h")
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.xlabel('放电率（Hz）', fontdict={'family': 'SimHei', 'size': 14})
plt.xlim(0, 1)
subplot(427)
# fig7 = plt.figure(figsize=(4, 4))
ax7 = sns.boxplot(data=df7, orient="h")
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.xlabel('拟合能力', fontdict={'family': 'SimHei', 'size': 14})
plt.xlim(0, 1)
# fig8 = plt.figure(figsize=(4, 4))
subplot(428)
ax8 = sns.boxplot(data=df8, orient="h")
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.xlabel('拟合能力', fontdict={'family': 'SimHei', 'size': 14})
plt.xlim(0, 1)