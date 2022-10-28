import pandas as pd
import numpy as np
from pylab import *
from neuron.layer import *
import scipy.io as scio
import copy


def Gaussian_Noise(seql=100, mx=0, sigma=4):
    """
    :param sigma: 方差
    :param seql: 序列长度
    :param mx: 噪声均值
    """
    mean = np.array([mx])
    cov = np.eye(1) * sigma

    G_seq = []
    for i in range(seql):
        data = np.random.multivariate_normal(mean, cov, 1)
        G_seq.append(data)

    return G_seq
