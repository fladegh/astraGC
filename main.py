import sys
from PyQt5 import QtWidgets
from core.astra import Astra


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    astra = Astra(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
