#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout
import sys
import libpomp

import ui.UIscratchy as UIscratchy

import AlgoElement

class UIScratchy(UIscratchy.Ui_MainWindow):
    def setupUi(self, MainWindow):
        UIscratchy.Ui_MainWindow.setupUi(self,MainWindow)
        self.actionAvancer.triggered.connect(self.addMove)
        self.actionTourner.triggered.connect(self.addTurn)
        self.actionBoucle.triggered.connect(self.addLoop)
        self.algorithmWidget = AlgoElement.AlgorithmWidget(self.centralwidget)
        self.layout = QVBoxLayout(self.centralwidget)
        self.layout.addWidget(self.algorithmWidget)

    def addMove(self):
        element = AlgoElement.Move(1)
        self.algorithmWidget.addAlgoElement(element)


    def addTurn(self):
        element = AlgoElement.Turn(90)
        self.algorithmWidget.addAlgoElement(element)


    def addLoop(self):
        element = AlgoElement.Loop(2, [AlgoElement.Move(1)])
        self.algorithmWidget.addAlgoElement(element)

def show_dialog():
    pass

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UIScratchy()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

