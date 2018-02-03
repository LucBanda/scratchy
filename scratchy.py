#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

import UImainwindow

class UIScratchy(UImainwindow.Ui_MainWindow):
    pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UIScratchy()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

