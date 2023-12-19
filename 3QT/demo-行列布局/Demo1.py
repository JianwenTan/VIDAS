from PyQt5.QtWidgets import QApplication, QLineEdit, QLabel, QFormLayout, QHBoxLayout, QVBoxLayout
from PyQt5 import QtWidgets


class FormLayout(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('表单+水平+垂直布局综合演示')
        # 添加标签
        label1 = QLabel('label1')
        label2 = QLabel('label2')
        label3 = QLabel('label3')
        label4 = QLabel('label4')
        # 添加行编辑器
        lineEdit1 = QLineEdit()
        lineEdit2 = QLineEdit()
        lineEdit3 = QLineEdit()
        lineEdit4 = QLineEdit()
        # 添加表单布局
        gridlayout1 = QFormLayout()
        gridlayout2 = QFormLayout()
        gridlayout3 = QFormLayout()
        gridlayout4 = QFormLayout()
        gridlayout1.addRow(label1, lineEdit1)
        gridlayout2.addRow(label2, lineEdit2)
        gridlayout3.addRow(label3, lineEdit3)
        gridlayout4.addRow(label4, lineEdit4)
        # 添加水平布局
        hbox = QHBoxLayout()
        hbox.addLayout(gridlayout1)
        hbox.addLayout(gridlayout2)
        # 添加垂直布局
        vbox = QVBoxLayout()
        vbox.addLayout(gridlayout3)
        vbox.addLayout(gridlayout4)
        # 添加布局
        vlayout = QVBoxLayout()  # 整个程序的灵魂,将QVBoxLayout改成QHBoxLayout可以改变hbox和vbox的布局从垂直布局到水平布局
        vlayout.addLayout(hbox)
        vlayout.addLayout(vbox)
        self.setLayout(vlayout)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    qb = FormLayout()
    qb.show()
    sys.exit(app.exec_())
