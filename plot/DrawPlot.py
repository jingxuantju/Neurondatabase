import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# list, string, string
def DrawHearMap(weight, plot_title, c_palette="Blues"):
    weight = weight.copy()
    weighta = np.array(weight)
    sns.heatmap(weighta, cmap=c_palette)
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.title(plot_title, fontdict={'family': 'SimHei', 'size': 16})
    font1 = {'family': 'Times New Roman', 'size': 16}
    plt.show()

def DrawLinkStackedBar(Cmap, plot_title):
    plt.yticks(fontproperties='Times New Roman', size=14)
    plt.xticks(fontproperties='Times New Roman', size=14)
    plt.title(plot_title, fontdict={'family': 'SimHei', 'size': 16})
    plt.show()