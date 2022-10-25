# library
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Create a dataset
df = pd.DataFrame(np.random.random((10,10)), columns=["a","b","c","d","e","f","g","h","i","j"])

# plot using a color palette
# sns.heatmap(df, cmap="YlGnBu")
# sns.heatmap(df, cmap="BuPu")
# sns.heatmap(df, cmap="Greens")
sns.heatmap(df, cmap="Blues")
plt.yticks(fontproperties='Times New Roman', size=14)
plt.xticks(fontproperties='Times New Roman', size=14)
plt.title('权值矩阵', fontdict={'family': 'SimHei', 'size': 16})
font1 = {'family': 'Times New Roman', 'size': 16}
# cb = plt.colorbar(prop=font1)
# cb = plt.colorbar(mappable=map, cax=None, ax=None)
# for l in cb.ax.yaxis.get_ticklabels():
#     l.set_family('Times New Roman')

# legend = plt.legend(prop=font1)
# plt.xticks(xr, range(200, real_t_span, 200))
# plt.ylabel('STN', fontdict={'family': 'SimHei', 'size': 14})  # label = name of label
plt.show()