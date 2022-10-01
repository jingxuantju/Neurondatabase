from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
import sys


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        qfile_ddna = QFile("DDNA.ui")
        qfile_ddna.open(QFile.ReadOnly)
        qfile_ddna.close()
        self.ui = QUiLoader().load(qfile_ddna)
        self.ui.setWindowTitle('神经元模型智能库')
        self.ui.table = QTableWidget(5, 2)





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
        window.ui.table.insertRow(0)
        window.ui.table.setItem(0, 0, QTableWidgetItem('1'))
        window.ui.table.setItem(0, 1, QTableWidgetItem('2'))


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

def insortRow():
    value = newWin.ui.nameEdit.text()
    window.ui.table.insertRow(0)
    item = QTableWidgetItem()
    item.setText(value)
    window.ui.table.setItem(0, 0, item)

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
    newWin.ui.nameEdit.textChanged.connect(insortRow)
    newWin.ui.IEdit.textChanged.connect(changeArgumentI)



    # 显示窗口
    window.ui.IZButton.clicked.connect(newWin.ui.show)


    newWin.ui.ackButton.clicked.connect(newWin.insertNeuron)


    # 运行应用，并监听事件
    app.exec_()
