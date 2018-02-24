#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys

from AlgoElement import ProgramElement, Algorithm
from PyQt5.QtCore import QObject, pyqtProperty, pyqtSlot, pyqtSignal
from PyQt5.QtQml import qmlRegisterType, QQmlApplicationEngine
from PyQt5.QtWidgets import QApplication
from RobotModel import RobotController
from Interpreter import Debugger

# FIXME
sys.path.append("./libpomp/python")
import pomp
from pomp.looper import _Loop


class QtPompLoop(_Loop, QObject):
    postSignal = pyqtSignal(object, object)

    def __init__(self):
        QObject.__init__(self)
        _Loop.__init__(self)
        self.postSignal.connect(self.handlerCb)

    def post(self, handler, req):
        self.postSignal.emit(handler, req)

    @pyqtSlot(object, object)
    def handlerCb(self, handler, req):
        handler.cb(req)

class ScratchyApp(QObject):
    algorithmChanged = pyqtSignal()
    scratchyDebuggerChanged = pyqtSignal()
    robotControllerChanged = pyqtSignal()

    def __init__(self, context, parent=None):
        super(ScratchyApp, self).__init__(parent)
        pomp.looper.prepareLoop(QtPompLoop())
        self.win = parent
        # Recherche d'un enfant appelé myButton dont le signal clicked sera connecté à la fonction test3
        # self.win.findChild(QObject, "myButton").clicked.connect(self.test3)
        self.ctx = context
        self._algorithm = Algorithm(parent)
        self.filename = None
        self._robotController = RobotController(self)
        self._debugger = Debugger(self, self._robotController)
        self._debugger.load(self._algorithm)

    @pyqtSlot(str)
    def save(self, fileName):
        if fileName:
            self.filename = fileName.replace("file:///", "/")
        if self.filename:
            open(self.filename, "w").write(self._algorithm.dump())

    @pyqtSlot(str)
    def open(self, fileName):
        if fileName:
            self.filename = fileName.replace("file:///", "/")
            self._algorithm.load(open(self.filename, "r").read())

    @pyqtProperty(RobotController, notify=robotControllerChanged)
    def robotController(self):
        return self._robotController

    @robotController.setter
    def robotController(self, value):
        self._robotController = value
        self.robotControllerChanged.emit()

    @pyqtProperty(Debugger, notify=scratchyDebuggerChanged)
    def scratchyDebugger(self):
        return self._debugger

    @scratchyDebugger.setter
    def scratchyDebugger(self, value):
        self._debugger = value
        self.scratchyDebuggerChanged.emit()

    @pyqtProperty(Algorithm, notify=algorithmChanged)
    def algorithm(self):
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value):
        self._algorithm = value
        self._debugger.load(self._algorithm)
        self.algorithmChanged.emit()


    @pyqtSlot(str, float)
    def sendInstruction(self, instruction, value):
        self._robotController.sendInstruction(instruction, value)

    @pyqtSlot()
    def clear(self):
        self._algorithm.clear()
        self._interpreter = Interpreter(self, self._algorithm._elementList, self._robotController)

    @pyqtSlot()
    def destroy(self):
        self._robotController.stop()

if __name__ == "__main__":
    qmlRegisterType(ProgramElement, 'Scratchy', 1, 0, 'ProgramElement')
    qmlRegisterType(Algorithm, 'Scratchy', 1, 0, 'Algorithm')
    qmlRegisterType(RobotController, 'Scratchy', 1, 0, 'RobotController')
    qmlRegisterType(Debugger, 'Scratchy', 1, 0, 'Debugger')
    qmlRegisterType(ScratchyApp, 'Scratchy', 1, 0, 'ScratchyApp')


    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    engine.load('./scratchyQml/main.qml')
    ret = 0

    if engine.rootObjects():
        win = engine.rootObjects()[0]
        win.show()
        ret = app.exec_()

    scratchyApp = engine.rootObjects()[0].findChildren(ScratchyApp)[0]
    scratchyApp.destroy()

    pomp.looper.exitLoop()
    sys.exit(ret)
