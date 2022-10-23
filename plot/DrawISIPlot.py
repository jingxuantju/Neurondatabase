# libraries & dataset
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.io as scio



SpikeFile = 'spknew.mat'
data = scio.loadmat(SpikeFile)
Spike2 = data['spk2']

# set a grey background (use sns.set_theme() if seaborn version 0.11.0 or above)
sns.set(style="darkgrid")
df = sns.load_dataset('iris')
# df = pd.DataFrame(Spike2)

# Narrower bandwidth
sns.kdeplot(df, shade=True, bw=0.05, color='olive') # if using seaborn < 0.11.0
plt.show()