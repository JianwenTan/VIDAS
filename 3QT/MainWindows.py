import sys

from UI import listOne

from PyQt5.QtWidgets import QApplication,QWidget,QMainWindow


if __name__ == '__main__':
    #   创建QApplication类的实例
    app = QApplication(sys.argv)
    #   创建对象
    mainWindow = QMainWindow()
    #   创建UI界面
    List_One = listOne.Ui_MainWindow()
    List_One.setupUi(mainWindow)

    mainWindow.show()


    # 进入程序的主循环，并通过exit函数确保主循环安全结束(该释放资源的一定要释放)
    sys.exit(app.exec_())
