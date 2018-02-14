#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import AlgoElement
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtProperty, pyqtSlot, pyqtSignal
from PyQt5.QtQml import qmlRegisterType, QQmlApplicationEngine
from RobotItf import RobotItf

# FIXME
sys.path.append("./libpomp/python")
import pomp

# source : http://ceg.developpez.com/tutoriels/pyqt/qt-quick-python/02-interaction-qml-python/

class RobotController(RobotItf, QObject):

    def __init__(self, client):
        RobotItf.__init__(self, RobotItf.LOCAL_POMP_ADDRESS, "client")
        self.client = client

    def onStateReceived(self, x, y, cap, vx, vy, vang):
        print(x, y, cap, vx, vy, vang)

    def onInstructionReceived(self, instruction, value):
        self.client.onInstructionReceived(instruction, value)

class ScratchyApp (QObject):
    algorithmChanged = pyqtSignal()
    onInstructionReceived = pyqtSignal()

    def __init__(self, context, parent=None):
        super(ScratchyApp, self).__init__(parent)
        pomp.looper.prepareLoop()
        self.win = parent
        # Recherche d'un enfant appelé myButton dont le signal clicked sera connecté à la fonction test3
        #self.win.findChild(QObject, "myButton").clicked.connect(self.test3)
        self.ctx = context
        self._algorithm = AlgoElement.Algorithm(parent)
        self.filename = None
        self._robotController = RobotController(self)

    def onInstructionReceived(self, instruction, value):
        print ("instruction OK received from Robot")

    @pyqtSlot(str)
    def save(self, fileName):
        if fileName:
            self.filename = fileName.replace("file:///","/")
        if self.filename:
            open(self.filename, "w").write(self._algorithm.dump())

    @pyqtSlot(str)
    def open(self, fileName):
        if fileName:
            self.filename = fileName.replace("file:///","/")
            self._algorithm.load(open(self.filename, "r").read())

    @pyqtSlot()
    def timer(self):
        pomp.looper.stepLoop()
        pass

    @pyqtProperty(AlgoElement.Algorithm, notify=algorithmChanged)
    def algorithm(self):
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value):
        self._algorithm = value
        self.algorithmChanged.emit()

    @algorithm.setter
    def algorithm(self, value):
        self._algorithm = value
        self.algorithmChanged.emit()

    @pyqtSlot(str, float)
    def sendInstruction(self, instruction, value):
        self._robotController.sendInstruction(instruction, value)

if __name__ == "__main__":
    qmlRegisterType(AlgoElement.ProgramElement, 'Scratchy', 1, 0, 'ProgramElement')
    qmlRegisterType(AlgoElement.Algorithm, 'Scratchy', 1, 0, 'Algorithm')
    qmlRegisterType(RobotController, 'Scratchy', 1, 0, 'RobotController')

    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    scratchy = ScratchyApp(engine)
    engine.rootContext().setContextProperty('scratchyApp', scratchy)
    engine.load('./scratchyQml/main.qml')
    if engine.rootObjects():
        win = engine.rootObjects()[0]
        win.show()
        ret = app.exec_()
        scratchy.destroy()
        pomp.looper.exitLoop()
        sys.exit(ret)
