from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
import sys

class Stats(QWidget):

    def __init__(self):
        # 从文件中加载UI定义

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        qfile_ddna = QFile("DDNA.ui")
        qfile_ddna.open(QFile.ReadOnly)
        qfile_ddna.close()

        self.ui = QUiLoader().load(qfile_ddna)
        self.ui.LIFButton.clicked.connect(self.handleCalc)

    def handleCalc(self):
        print("1")
        QMessageBox.about(self.ui, '选择参数',
                    '请选择输入电流')




app = QApplication([])
stats = Stats()
stats.ui.show()
app.exec_()
