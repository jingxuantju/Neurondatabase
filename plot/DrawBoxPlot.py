# libraries & dataset
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.io as scio

# set a grey background (use sns.set_theme() if seaborn version 0.11.0 or above)
sns.set(style="darkgrid")
# df = sns.load_dataset('iris')

SpikeFile = 'spknew.mat'
data = scio.loadmat(SpikeFile)
Spike2 = data['spk2']
Spike3 = data['spk3']
Spike4 = data['spk4']
Spike5 = data['spk5']
Spike6 = data['spk6']

average2 = np.mean(Spike2, axis=1) * 1000
average3 = np.mean(Spike3, axis=1) * 1000
average4 = np.mean(Spike4, axis=1) * 1000
average5 = np.mean(Spike5, axis=1) * 1000
average6 = np.mean(Spike6, axis=1) * 1000
a1 = {'l2': average2, 'l3': average3, 'l4': average4, 'l5': average5, 'l6': average6}
ac = np.vstack((average2, average3, average4, average5, average6))
my_pal = {"l2": "g", "l3": "b", "l4": "m", "l5": "g", "l6": "b"}

df = pd.DataFrame(a1)
df.plot.box()
plt.grid(linestyle="--", alpha=0.3)
plt.ylabel('放电率（Hz）', fontdict={'family': 'SimHei', 'size': 14})
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.title('各核团放电率', fontdict={'family': 'SimHei', 'size': 16})
# df = pd.DataFrame(ac, index=['l2', 'l3', 'l4', 'l5', 'l6'])
# sns.boxplot(x=['l2', 'l3', 'l4', 'l5', 'l6'], y=df, palette=my_pal)
plt.show()
