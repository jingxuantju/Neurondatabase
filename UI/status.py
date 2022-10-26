from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from matplotlib.backends.backend_template import FigureCanvas

from neuron.neuron import *
from neuron.realNeuron import *
from neuron.comp import *
import sys
from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimSun']
matplotlib.rcParams['axes.unicode_minus']=False
import random
from UI.globalV import *
from plot.DrawPlot import *
import scipy.io as scio
from plot.DrawNetworkMap import *

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        qfile_ddna = QFile("DDNA.ui")
        qfile_ddna.open(QFile.ReadOnly)
        qfile_ddna.close()
        self.ui = QUiLoader().load(qfile_ddna)
        self.ui.setWindowTitle('神经元模型智能库')


class NewWindow(QWidget):
    def __init__(self):
        super().__init__()
        qfile_argument = QFile("argument.ui")
        qfile_argument.open(QFile.ReadOnly)
        qfile_argument.close()
        self.ui = QUiLoader().load(qfile_argument)
        self.ui.setWindowTitle('配置参数')
        self.ui.ackButton.clicked.connect(self.ui.close)


    def insertNeuron(self):
        value = newWin.ui.nameEdit.text()
        window.ui.table.insertRow(0)
        window.ui.table.setItem(0, 0, QTableWidgetItem(value))


class NewWindow1(QWidget):
    def __init__(self):
        super().__init__()
        qfile_argument = QFile("data.ui")
        qfile_argument.open(QFile.ReadOnly)
        qfile_argument.close()
        self.ui = QUiLoader().load(qfile_argument)
        self.ui.setWindowTitle('可视化分析')


    def insertNeuron(self):
        value = newWin.ui.nameEdit.text()
        window.ui.table.insertRow(0)
        window.ui.table.setItem(0, 0, QTableWidgetItem(value))

# class MyFigure(FigureCanvas):
#     def __init__(self, width=5, height=4, dpi=100):
#         # 第一步：创建一个创建Figure
#         self.fig = Figure(figsize=(width, height), dpi=dpi)
#         # 第二步：在父类中激活Figure窗口
#         super(MyFigure, self).__init__(self.fig)  # 此句必不可少，否则不能显示图形
#
#     def drawCos(self):
#         F = MyFigure(3, 3, 100)
#         axes = F.fig.add_subplot(111)
#         t = np.arange(0.0, 5.0, 0.01)
#         s = np.cos(2 * np.pi * t)
#         axes.plot(t, s)
#         F.fig.suptitle("cos")



def changeArgumentA():
    value = newWin.ui.aEdit.text()
    window.ui.labela.setText(value)

def changeArgumentB():
    value = newWin.ui.bEdit.text()
    window.ui.labelb.setText(value)

def changeArgumentC():
    value = newWin.ui.cEdit.text()
    window.ui.labelc.setText(value)

def changeArgumentD():
    value = newWin.ui.dEdit.text()
    window.ui.labeld.setText(value)

def changeArgumentname():
    value = newWin.ui.nameEdit.text()
    window.ui.labelname.setText(value)

def changeArgumentI():
    value = newWin.ui.IEdit.text()
    window.ui.labelI.setText(value)

def newIz():
    I = eval(window.ui.labelI.text())
    a = eval(window.ui.labela.text())
    b = eval(window.ui.labelb.text())
    c = eval(window.ui.labelc.text())
    d = eval(window.ui.labeld.text())
    name = window.ui.labelname.text()
    comp1 = IzhikevichNeuron(manager, name, I, a, b, c, d)


def showsynpase():
    plusFile1 = "D:\FPGA\ku\simulink\plot\chushihua.mat"
    data1 = scio.loadmat(plusFile1)
    DrawHearMap(np.random.random((10,10)), "突触权值", c_palette="Blues")

def ISI():
    if __name__ == '__main__':
        SpikeFile = 'D:\FPGA\ku\simulink\plot\spknew.mat'
        data = scio.loadmat(SpikeFile)
        Spike2 = data['spk2']
        n0 = np.load('D:\FPGA\ku\simulink\plot\pd0.npz')
        V_STN_array = n0['V_STN_array']
        V_GPE_array = n0['V_GPE_array']
        V_GPI_array = n0['V_GPI_array']
        V_TH_array = n0['V_TH_array']
        t_span = 12000
        real_t_span = 1200
        data_t_span = len(V_STN_array)

        SPK_STN = np.where(V_STN_array > 10, 1, 0)
        SPK_GPE = np.where(V_GPE_array > 10, 1, 0)
        SPK_GPI = np.where(V_GPI_array > 10, 1, 0)
        SPK_TH = np.where(V_TH_array > 10, 1, 0)

        Splot = 1
        Lplot = 0
        Nneuron = 10
        lw = 0.3
        if (Splot):
            plt.scatter(0, 0, s=2, c='b', label="GPE")
            plt.scatter(0, 0, s=2, c='r', label="STN")
            plt.scatter(0, 0, s=2, c='g', label="GPI")
            plt.scatter(0, 0, s=2, c='y', label="TC")
        if (Lplot):
            plt.plot([0, 0], [0.01, 0.01], c='lightsalmon', linewidth=lw, label="STN")
            plt.plot([0, 0], [0.01, 0.01], c='lightskyblue', linewidth=lw, label="GPE")
            plt.plot([0, 0], [0.01, 0.01], c='plum', linewidth=lw, label="GPI")
            plt.plot([0, 0], [0.01, 0.01], c='lightgreen', linewidth=lw, label="TC")
        for i in range(Nneuron):
            s2_idx = np.nonzero(SPK_STN[i, :])
            idzero = [0]
            ids = s2_idx[0].tolist()
            idall = np.hstack((idzero, ids))
            idy = np.diff(idall)
            if (Lplot):
                plt.plot(s2_idx[0], idy, c='lightsalmon', linewidth=lw)
            if (Splot):
                for indexs in s2_idx:
                    plt.scatter(indexs, idy, s=2, c='r')
        for i in range(Nneuron):
            s2_idx = np.nonzero(SPK_GPE[i, :])
            idzero = [0]
            ids = s2_idx[0].tolist()
            idall = np.hstack((idzero, ids))
            idy = np.diff(idall)
            if (Lplot):
                plt.plot(s2_idx[0], idy, c='lightskyblue', linewidth=lw)
            if (Splot):
                for indexs in s2_idx:
                    plt.scatter(indexs, idy, s=2, c='b')
        for i in range(Nneuron):
            s2_idx = np.nonzero(SPK_GPI[i, :])
            idzero = [0]
            ids = s2_idx[0].tolist()
            idall = np.hstack((idzero, ids))
            idy = np.diff(idall)
            if (Lplot):
                plt.plot(s2_idx[0], idy, c='plum', linewidth=lw)
            if (Splot):
                for indexs in s2_idx:
                    plt.scatter(indexs, idy, s=2, c='g')
        for i in range(Nneuron):
            s2_idx = np.nonzero(SPK_TH[i, :])
            idzero = [0]
            ids = s2_idx[0].tolist()
            idall = np.hstack((idzero, ids))
            idy = np.diff(idall)
            if (Lplot):
                plt.plot(s2_idx[0], idy, c='lightgreen', linewidth=lw)
            if (Splot):
                for indexs in s2_idx:
                    plt.scatter(indexs, idy, s=2, c='y')

        plt.ylabel('ISI时间（ms）', fontdict={'family': 'SimHei', 'size': 14})
        plt.xlabel('时间（ms）', fontdict={'family': 'SimHei', 'size': 14})
        plt.yticks(fontproperties='Times New Roman', size=14)
        plt.xticks(fontproperties='Times New Roman', size=14)
        plt.title('ISI', fontdict={'family': 'SimHei', 'size': 16})
        font1 = {'family': 'Times New Roman', 'size': 16}
        legend = plt.legend(prop=font1)
        plt.show()

def linkresult():

    plusFile = 'D:\FPGA\ku\simulink\plot\lianjiejuzhen.mat'
    data = scio.loadmat(plusFile)
    Csn_ge = data['Csn_ge'].tolist()
    Csn_gi = data['Csn_gi'].tolist()
    Cge_sn = data['Cge_sn'].tolist()
    Cge_gi = data['Cge_gi'].tolist()
    Cge_ge = data['Cge_ge'].tolist()
    Cgi_tc = data['Cgi_tc'].tolist()

    #    Start Plot
    lw = 0.2
    pointarea = 2
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    STN_dis, _ = Gaussian_Distribution(mx=5, my=5, mz=5, sigma=4, M=100)
    GPE_dis, _ = Gaussian_Distribution(mx=15, my=5, mz=5, sigma=4, M=100)
    GPI_dis, _ = Gaussian_Distribution(mx=5, my=15, mz=15, sigma=4, M=100)
    TH_dis, _ = Gaussian_Distribution(mx=15, my=15, mz=15, sigma=4, M=100)
    STN_x, STN_y, STN_z = STN_dis.T
    GPE_x, GPE_y, GPE_z = GPE_dis.T
    GPI_x, GPI_y, GPI_z = GPI_dis.T
    TH_x, TH_y, TH_z = TH_dis.T
    # Draw the dots
    for i in range(100):
        ax.scatter(STN_x[i], STN_y[i], STN_z[i], c='coral', s=pointarea)
        ax.scatter(GPE_x[i], GPE_y[i], GPE_z[i], c='royalblue', s=pointarea)
        ax.scatter(GPI_x[i], GPI_y[i], GPI_z[i], c='gold', s=pointarea)
        ax.scatter(TH_x[i], TH_y[i], TH_z[i], c='limegreen', s=pointarea)
    # Draw the edges
    for i in range(100):
        for j in range(100):
            if (Csn_ge[i][j] == 1):
                # if (stn_syn_gpe[i].E == 0):
                #     c_edge = 'lightsalmon'
                # else:
                c_edge = 'lightsalmon'
                ax.plot([STN_x[i], GPE_x[j]], [STN_y[i], GPE_y[j]], [STN_z[i], GPE_z[j]], c=c_edge, linewidth=lw)

            if (Csn_gi[i][j] == 1):
                # if (stn_syn_gpe[i].E == 0):
                #     c_edge = 'lightsalmon'
                # else:
                c_edge = 'lightsalmon'
                ax.plot([STN_x[i], GPI_x[j]], [STN_y[i], GPI_y[j]], [STN_z[i], GPI_z[j]], c=c_edge, linewidth=lw)
            if (Cge_sn[i][j] == 1):
                # if (stn_syn_gpe[i].E == 0):
                #     c_edge = 'lightsalmon'
                # else:
                c_edge = 'lightskyblue'
                ax.plot([GPE_x[i], STN_x[j]], [GPE_y[i], STN_y[j]], [GPE_z[i], STN_z[j]], c=c_edge, linewidth=lw)
            if (Cge_gi[i][j] == 1):
                # if (stn_syn_gpe[i].E == 0):
                #     c_edge = 'lightsalmon'
                # else:
                c_edge = 'lightskyblue'
                ax.plot([GPE_x[i], GPI_x[j]], [GPE_y[i], GPI_y[j]], [GPE_z[i], GPI_z[j]], c=c_edge, linewidth=lw)
            if (Cge_ge[i][j] == 1):
                # if (stn_syn_gpe[i].E == 0):
                #     c_edge = 'lightsalmon'
                # else:
                c_edge = 'lightskyblue'
                ax.plot([GPE_x[i], GPE_x[j]], [GPE_y[i], GPE_y[j]], [GPE_z[i], GPE_z[j]], c=c_edge, linewidth=lw)
            if (Cgi_tc[i][j] == 1):
                # if (stn_syn_gpe[i].E == 0):
                #     c_edge = 'lightsalmon'
                # else:
                c_edge = 'lightskyblue'
                ax.plot([GPE_x[i], TH_x[j]], [GPE_y[i], TH_y[j]], [GPE_z[i], TH_z[j]], c=c_edge, linewidth=lw)
    # plt.xticks([])
    # plt.yticks([])
    # plt.axis('off')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    plt.show()
    plt.savefig("NetworkMap.svg", dpi=300, format="png")

def run(result):
    result = manager.start_stimulation(10000)

    COMP4_RESULT = []
    COMP5_RESULT = []
    for dictionary in result:
        name = ''
        for key in dictionary:
            name = key
            break
        COMP4_RESULT.append(dictionary[name][0])
        COMP5_RESULT.append(dictionary[name][1])
    figure = plt.figure()
    plt.subplot(311)
    line1, = plt.plot(COMP4_RESULT)
    plt.xlabel('时间(ms)', fontsize=20)  # label = name of label
    plt.subplot(312)
    line2, = plt.plot(COMP5_RESULT)
    plt.subplot(313)
    line3, = plt.plot(COMP4_RESULT, COMP5_RESULT)
    figure.tight_layout()
    figure.show()
    plt.show()

    # canvas = FigureCanvas(figure)
    # gridlayout = QGridLayout(window.ui.groupBox)  # 继承容器groupBox
    # window.ui.graphicsView.addWidget(canvas, 0, 1)
    # canvas.draw()


def delete():
    manager = Manager()



if __name__ == '__main__':
    app = QApplication([])
    # 创建窗口
    window = MainWindow()
    window.ui.show()
    newWin = NewWindow()
    newWin1 = NewWindow1()
    newWin.ui.aEdit.textChanged.connect(changeArgumentA)
    newWin.ui.bEdit.textChanged.connect(changeArgumentB)
    newWin.ui.cEdit.textChanged.connect(changeArgumentC)
    newWin.ui.dEdit.textChanged.connect(changeArgumentD)
    newWin.ui.nameEdit.textChanged.connect(changeArgumentname)
    newWin.ui.IEdit.textChanged.connect(changeArgumentI)
    newWin1.ui.pushButton.clicked.connect(showsynpase)
    newWin1.ui.pushButton_4.clicked.connect(ISI)
    newWin1.ui.pushButton_6.clicked.connect(linkresult)



    # 显示窗口
    window.ui.IZButton.clicked.connect(newWin.ui.show)
    window.ui.basalButton.clicked.connect(newWin1.ui.show)


    newWin.ui.ackButton.clicked.connect(newWin.insertNeuron)
    newWin.ui.ackButton.clicked.connect(newIz)
    window.ui.applyButton.clicked.connect(run)
    window.ui.deleteButton.clicked.connect(delete)

    # 运行应用，并监听事件
    app.exec_()
