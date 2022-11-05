# libraries
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rc
import pandas as pd
import scipy.io as scio

plusFile = 'lianjiejuzhen.mat'
data = scio.loadmat(plusFile)
Csn_ge = data['Csn_ge']
Csn_gi = data['Csn_gi']
Cge_sn = data['Cge_sn']
Cge_gi = data['Cge_gi']
Cge_ge = data['Cge_ge']
Cgi_tc = data['Cgi_tc']

S_sn_ge = sum(sum(Csn_ge))
S_sn_gi = sum(sum(Csn_gi))
S_ge_sn = sum(sum(Cge_sn))
S_ge_gi = sum(sum(Cge_gi))
S_ge_ge = sum(sum(Cge_ge))
S_gi_tc = sum(sum(Cgi_tc))

# y-axis in bold
rc('font', weight='bold')

# Values of each group
sn_src = [0, S_sn_ge, S_sn_gi, 0]
ge_src = [S_ge_sn, S_ge_ge, S_ge_gi, 0]
gi_src = [0, 0, 0, S_gi_tc]
tc_src = [0, 0, 0, 0, 0]

# Heights of bars1 + bars2
bars = np.add(sn_src, ge_src).tolist()

# The position of the bars on the x-axis
r = ['STN', 'GPE', 'GPI', 'TC']

# Names of group and bar width
names = ['A', 'B', 'C', 'D', 'E']
barWidth = 1

# Create brown bars
plt.bar(r, sn_src, color='mistyrose', edgecolor='white', width=barWidth)
# Create green bars (middle), on top of the first ones
plt.bar(r, ge_src, bottom=sn_src, color='indianred', edgecolor='white', width=barWidth)
# Create green bars (top)
plt.bar(r, gi_src, bottom=bars, color='lightsteelblue', edgecolor='white', width=barWidth)

# Custom X axis

plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.title('各核团连接关系', fontdict={'family': 'SimHei', 'size': 16})
plt.xlabel("目的核团", fontdict={'family': 'SimHei', 'size': 14})
plt.ylabel("源核团", fontdict={'family': 'SimHei', 'size': 14})

# Show graphic
plt.show()