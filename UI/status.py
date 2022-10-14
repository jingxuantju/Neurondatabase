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

class MyFigure(FigureCanvas):
    def __init__(self, width=5, height=4, dpi=100):
        # 第一步：创建一个创建Figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        # 第二步：在父类中激活Figure窗口
        super(MyFigure, self).__init__(self.fig)  # 此句必不可少，否则不能显示图形

    def drawCos(self):
        F = MyFigure(3, 3, 100)
        axes = F.fig.add_subplot(111)
        t = np.arange(0.0, 5.0, 0.01)
        s = np.cos(2 * np.pi * t)
        axes.plot(t, s)
        F.fig.suptitle("cos")



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
    newWin.ui.aEdit.textChanged.connect(changeArgumentA)
    newWin.ui.bEdit.textChanged.connect(changeArgumentB)
    newWin.ui.cEdit.textChanged.connect(changeArgumentC)
    newWin.ui.dEdit.textChanged.connect(changeArgumentD)
    newWin.ui.nameEdit.textChanged.connect(changeArgumentname)
    newWin.ui.IEdit.textChanged.connect(changeArgumentI)



    # 显示窗口
    window.ui.IZButton.clicked.connect(newWin.ui.show)


    newWin.ui.ackButton.clicked.connect(newWin.insertNeuron)
    newWin.ui.ackButton.clicked.connect(newIz)
    window.ui.applyButton.clicked.connect(run)
    window.ui.deleteButton.clicked.connect(delete)

    # 运行应用，并监听事件
    app.exec_()
