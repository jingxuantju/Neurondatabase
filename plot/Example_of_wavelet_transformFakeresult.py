import pywt
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


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
        G_seq.append(data[0][0])

    return G_seq


# 小波
sampling_rate = 1024
t = np.arange(0, 1.0, 1.0 / sampling_rate)
f1 = 10
f2 = 20
f25 = 25
f3 = 30
f4 = 40
# 4
data0 = np.piecewise(t, [t < 1, t < 0.7, t < 0.3],
                     [lambda t: 0 * np.sin(2 * np.pi * f3 * t),
                      lambda t: 200 * np.sin(2 * np.pi * f2 * 5 * t),
                      lambda t: 0 * np.sin(2 * np.pi * f1 * t)])
data01 = np.piecewise(t, [t < 1, t < 0.7, t < 0.3],
                      [lambda t: 50 * np.sin(2 * np.pi * f2 * 10 * t),
                       lambda t: 300 * np.sin(2 * np.pi * f3 * 10 * t),
                       lambda t: 50 * np.sin(2 * np.pi * f2 * 10 * t)])
data02 = np.piecewise(t, [t < 1, t < 0.7, t < 0.3],
                      [lambda t: 80 * np.sin(2 * np.pi * f2 * 10 * t),
                       lambda t: 150 * np.sin(2 * np.pi * f1 * 10 * t),
                       lambda t: 80 * np.sin(2 * np.pi * f2 * 10 * t)])
data03 = np.piecewise(t, [t < 1, t < 0.7, t < 0.3],
                      [lambda t: 30 * np.sin(2 * np.pi * f2 * 10 * t),
                       lambda t: 60 * np.sin(2 * np.pi * f2 * 10 * t),
                       lambda t: 30 * np.sin(2 * np.pi * f2 * 10 * t)])
# 3
data1 = np.piecewise(t, [t < 1, t < 0.7, t < 0.3],
                     [lambda t: 0 * np.sin(2 * np.pi * f3 * t),
                      lambda t: 200 * np.sin(2 * np.pi * f2 * 0.5 * t),
                      lambda t: 0 * np.sin(2 * np.pi * f1 * t)])
kd = np.maximum(data1, 0)
data11 = np.piecewise(t, [t < 1, t < 0.72, t < 0.69, t < 0.31, t < 0.28],
                      [lambda t: 50 * np.sin(2 * np.pi * f2 * 10 * t),
                       lambda t: 230 * np.sin(2 * np.pi * f2 * 10 * t),
                       lambda t: 20 * np.sin(2 * np.pi * f3 * 10 * t),
                       lambda t: 230 * np.sin(2 * np.pi * f2 * 10 * t),
                       lambda t: 50 * np.sin(2 * np.pi * f2 * 10 * t)])
data12 = np.piecewise(t, [t < 1, t < 0.72, t < 0.69, t < 0.31, t < 0.28],
                      [lambda t: 90 * np.sin(2 * np.pi * f2 * 10 * t),
                       lambda t: 130 * np.sin(2 * np.pi * f1 * 10 * t),
                       lambda t: 30 * np.sin(2 * np.pi * f1 * 10 * t),
                       lambda t: 130 * np.sin(2 * np.pi * f1 * 10 * t),
                       lambda t: 90 * np.sin(2 * np.pi * f2 * 10 * t)])
data13 = np.piecewise(t, [t < 1, t < 0.72, t < 0.69, t < 0.31, t < 0.28],
                      [lambda t: 110 * np.sin(2 * np.pi * f2 * 10 * t),
                       lambda t: 130 * np.sin(2 * np.pi * f3 * 10 * t),
                       lambda t: 60 * np.sin(2 * np.pi * f2 * 10 * t),
                       lambda t: 130 * np.sin(2 * np.pi * f3 * 10 * t),
                       lambda t: 110 * np.sin(2 * np.pi * f2 * 10 * t)])
# 2
data2 = np.piecewise(t, [t < 1, t < 0.7, t < 0.3],
                     [lambda t: 0 * np.sin(2 * np.pi * f3 * t),
                      lambda t: -6,
                      lambda t: 0 * np.sin(2 * np.pi * f1 * t)])
data21 = np.piecewise(t, [t < 1, t < 0.72, t < 0.69, t < 0.31, t < 0.28],
                      [lambda t: 50 * np.sin(2 * np.pi * f2 * 10 * t),
                       lambda t: 130 * np.sin(2 * np.pi * f2 * 10 * t),
                       lambda t: 20 * np.sin(2 * np.pi * f3 * 10 * t),
                       lambda t: 130 * np.sin(2 * np.pi * f2 * 10 * t),
                       lambda t: 50 * np.sin(2 * np.pi * f2 * 10 * t)])
data22 = 0.03 * kd * np.piecewise(t, [t < 1, t < 0.72, t < 0.69, t < 0.31, t < 0.28],
                                  [lambda t: 90 * np.sin(2 * np.pi * f2 * 10 * t),
                                   lambda t: 130 * np.sin(2 * np.pi * f1 * 10 * t),
                                   lambda t: 30 * np.sin(2 * np.pi * f2 * 10 * t),
                                   lambda t: 130 * np.sin(2 * np.pi * f1 * 10 * t),
                                   lambda t: 90 * np.sin(2 * np.pi * f2 * 10 * t)])
data23 = np.piecewise(t, [t < 1, t < 0.72, t < 0.69, t < 0.31, t < 0.28],
                      [lambda t: 110 * np.sin(2 * np.pi * f2 * 10 * t),
                       lambda t: 130 * np.sin(2 * np.pi * f3 * 10 * t),
                       lambda t: 60 * np.sin(2 * np.pi * f2 * 10 * t),
                       lambda t: 130 * np.sin(2 * np.pi * f3 * 10 * t),
                       lambda t: 110 * np.sin(2 * np.pi * f2 * 10 * t)])
# 1
data3 = np.piecewise(t, [t < 1, t < 0.7, t < 0.3],
                     [lambda t: 0 * np.sin(2 * np.pi * f3 * t),
                      lambda t: 6,
                      lambda t: 0 * np.sin(2 * np.pi * f1 * t)])
data31 = np.piecewise(t, [t < 1, t < 0.72, t < 0.69, t < 0.31, t < 0.28],
                      [lambda t: 50 * np.sin(2 * np.pi * f2 * 10 * t),
                       lambda t: 230 * np.sin(2 * np.pi * f2 * 10 * t),
                       lambda t: 120 * np.sin(2 * np.pi * f2 * 10 * t),
                       lambda t: 230 * np.sin(2 * np.pi * f2 * 10 * t),
                       lambda t: 50 * np.sin(2 * np.pi * f2 * 10 * t)])
data32 = np.piecewise(t, [t < 1, t < 0.72, t < 0.69, t < 0.31, t < 0.28],
                      [lambda t: 90 * np.sin(2 * np.pi * f2 * 10 * t),
                       lambda t: 130 * np.sin(2 * np.pi * f1 * 10 * t),
                       lambda t: 80 * np.sin(2 * np.pi * f1 * 10 * t),
                       lambda t: 130 * np.sin(2 * np.pi * f1 * 10 * t),
                       lambda t: 90 * np.sin(2 * np.pi * f2 * 10 * t)])
data33 = np.piecewise(t, [t < 1, t < 0.72, t < 0.69, t < 0.31, t < 0.28],
                      [lambda t: 110 * np.sin(2 * np.pi * f2 * 10 * t),
                       lambda t: 130 * np.sin(2 * np.pi * f3 * 10 * t),
                       lambda t: 60 * np.sin(2 * np.pi * f2 * 10 * t),
                       lambda t: 130 * np.sin(2 * np.pi * f3 * 10 * t),
                       lambda t: 110 * np.sin(2 * np.pi * f2 * 10 * t)])

# Gen Gaussian Noise
noise1 = Gaussian_Noise(seql=sampling_rate, mx=0, sigma=500)
noise2 = Gaussian_Noise(seql=sampling_rate, mx=0, sigma=500)
noise3 = Gaussian_Noise(seql=sampling_rate, mx=0, sigma=500)
noise4 = Gaussian_Noise(seql=sampling_rate, mx=0, sigma=500)

data00 = data01 + data02 + noise1 + data03
data20 = data21 + data22 + noise2 + data23
data10 = data11 + data12 + noise3 + data13
data30 = data31 + data32 + noise4 + data33

wavename = 'cgau8'
totalscal = 256
fc = pywt.central_frequency(wavename)
cparam = 2 * fc * totalscal
scales = cparam / np.arange(totalscal, 1, -1)
[cwtmatr1, frequencies1] = pywt.cwt(data00, scales, wavename, 1.0 / sampling_rate)
[cwtmatr2, frequencies2] = pywt.cwt(data10, scales, wavename, 1.0 / sampling_rate)
[cwtmatr3, frequencies3] = pywt.cwt(data20, scales, wavename, 1.0 / sampling_rate)
[cwtmatr4, frequencies4] = pywt.cwt(data30, scales, wavename, 1.0 / sampling_rate)
fig1 = plt.figure(figsize=(9, 4))
grid = plt.GridSpec(3, 2, top=0.9, bottom=0.15, wspace=0.5, hspace=0.1)
plt.subplot(grid[0, 0])
plt.plot(t, data0)
plt.axis('off')
plt.subplot(grid[1:3, 0])
plt.contourf(t, frequencies1, abs(cwtmatr1))
plt.xticks([0.0, 0.2, 0.4, 0.6, 0.8, 0.99], [0, 1000, 2000, 3000, 4000, 5000])
plt.yticks([10, 167, 333, 500], [10, 20, 30, 40])
plt.ylabel("频率(Hz)", fontdict={'family': 'SimHei', 'size': 14})
plt.xlabel("时间(ms)", fontdict={'family': 'SimHei', 'size': 14})
plt.subplot(grid[0, 1])
plt.plot(t, data2)
plt.axis('off')
plt.subplot(grid[1:3, 1])
plt.contourf(t, frequencies2, abs(cwtmatr2))
plt.xticks([0.0, 0.2, 0.4, 0.6, 0.8, 0.99], [0, 1000, 2000, 3000, 4000, 5000])
plt.yticks([10, 167, 333, 500], [10, 20, 30, 40])
plt.ylabel("频率(Hz)", fontdict={'family': 'SimHei', 'size': 14})
plt.xlabel("时间(ms)", fontdict={'family': 'SimHei', 'size': 14})
fig2 = plt.figure(figsize=(9, 4))
plt.subplot(grid[0, 0])
plt.plot(t, data1)
plt.axis('off')
plt.subplot(grid[1:3, 0])
plt.contourf(t, frequencies3, abs(cwtmatr3))
plt.xticks([0.0, 0.2, 0.4, 0.6, 0.8, 0.99], [0, 1000, 2000, 3000, 4000, 5000])
plt.yticks([10, 167, 333, 500], [10, 20, 30, 40])
plt.ylabel("频率(Hz)", fontdict={'family': 'SimHei', 'size': 14})
plt.xlabel("时间(ms)", fontdict={'family': 'SimHei', 'size': 14})
plt.subplot(grid[0, 1])
plt.plot(t, data3)
plt.axis('off')
plt.subplot(grid[1:3, 1])
plt.contourf(t, frequencies4, abs(cwtmatr4))
plt.xticks([0.0, 0.2, 0.4, 0.6, 0.8, 0.99], [0, 1000, 2000, 3000, 4000, 5000])
plt.yticks([10, 167, 333, 500], [10, 20, 30, 40])
plt.ylabel("频率(Hz)", fontdict={'family': 'SimHei', 'size': 14})
plt.xlabel("时间(ms)", fontdict={'family': 'SimHei', 'size': 14})
# plt.subplots_adjust(hspace=0.4)
# fig2.tight_layout()
plt.show()
