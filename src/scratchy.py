#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QVBoxLayout, QFileDialog

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
        self.actionNouveau.triggered.connect(self.nouveau)
        self.actionOuvrir.triggered.connect(self.openFileNameDialog)
        self.actionSauver.triggered.connect(self.saveFileDialog)
        self.algorithmWidget = AlgoElement.AlgorithmWidget(self.centralwidget)
        self.layout = QVBoxLayout(self.centralwidget)
        self.layout.addWidget(self.algorithmWidget)

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(None, "Open Script", "",
                                                  "Scratchy Files (*.schy)", options=options)
        if fileName:
            self.nouveau()
            self.algorithmWidget.algo = AlgoElement.loadAlgorithm(open(fileName,'r').read())
            self.algorithmWidget.displayAlgorithm()


    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(None, "Save Script", "",
                                                  "Scratchy File (*.schy)", options=options)
        if fileName:
            open(fileName, "w").write(self.algorithmWidget.algo.dump())

    def nouveau(self):
        self.algorithmWidget.setParent(None)
        self.algorithmWidget = AlgoElement.AlgorithmWidget(self.centralwidget)
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

