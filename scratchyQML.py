#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import AlgoElement
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtProperty, pyqtSlot, pyqtSignal
from PyQt5.QtQml import qmlRegisterType, QQmlApplicationEngine

from RobotModel import RobotController

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


class Interpreter(QObject):
    instructionDone = pyqtSignal(int, str, float, arguments = ['pc', 'instruction', 'value'])
    stopped = pyqtSignal()

    def __init__(self, parent, algorithm, robotController):
        super(Interpreter, self).__init__(parent)
        self.algorithm = algorithm
        self.robotController = robotController
        self.PC = 0

    @pyqtSlot()
    def start(self):
        self.PC = -1
        self.next()

    @pyqtSlot()
    def next(self):
        self.PC += 1
        if self.PC < len(self.algorithm._elementList):
            self.algorithm._elementList[self.PC].executing = True
            self.robotController.sendInstruction(self.algorithm._elementList[self.PC].instruction,
                                                 self.algorithm._elementList[self.PC].value)

    def onInstructionReceived(self, instruction, value):
        self.algorithm._elementList[self.PC].executing = False
        self.instructionDone.emit(self.PC, instruction, value)
        if self.PC == len(self.algorithm._elementList):
            self.stopped.emit()

class ScratchyApp(QObject):
    algorithmChanged = pyqtSignal()
    interpreterChanged = pyqtSignal()
    robotControllerChanged = pyqtSignal()

    def __init__(self, context, parent=None):
        super(ScratchyApp, self).__init__(parent)
        pomp.looper.prepareLoop(QtPompLoop())
        self.win = parent
        # Recherche d'un enfant appelé myButton dont le signal clicked sera connecté à la fonction test3
        # self.win.findChild(QObject, "myButton").clicked.connect(self.test3)
        self.ctx = context
        self._algorithm = AlgoElement.Algorithm(parent)
        self.filename = None
        self._robotController = RobotController(self)
        self._interpreter = Interpreter(self, self._algorithm, self._robotController)
        self._robotController.client = self._interpreter

    def onInstructionDone(self, pc, instruction, value):
        print("instruction OK received from Robot :", pc, instruction, value)
        self.instructionDone.emit(pc, instruction, value)

    def onStopped(self):
        print ("END")

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

    @pyqtProperty(Interpreter, notify=interpreterChanged)
    def interpreter(self):
        return self._interpreter
    @interpreter.setter
    def interpreter(self, value):
        self._interpreter = value
        self.interpreterChanged.emit()

    @pyqtProperty(AlgoElement.Algorithm, notify=algorithmChanged)
    def algorithm(self):
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value):
        self._algorithm = value
        self.algorithmChanged.emit()


    @pyqtSlot(str, float)
    def sendInstruction(self, instruction, value):
        self._robotController.sendInstruction(instruction, value)

    def destroy(self):
        self._robotController.stop()

if __name__ == "__main__":
    qmlRegisterType(AlgoElement.ProgramElement, 'Scratchy', 1, 0, 'ProgramElement')
    qmlRegisterType(AlgoElement.Algorithm, 'Scratchy', 1, 0, 'Algorithm')
    qmlRegisterType(RobotController, 'Scratchy', 1, 0, 'RobotController')
    qmlRegisterType(Interpreter, 'Scratchy', 1, 0, 'Interpreter')
    qmlRegisterType(ScratchyApp, 'Scratchy', 1, 0, 'ScratchyApp')

    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    scratchy = ScratchyApp(engine)

    engine.rootContext().setContextProperty('scratchyApp', scratchy)
    engine.load('./scratchyQml/main.qml')
    ret = 0

    if engine.rootObjects():
        win = engine.rootObjects()[0]
        win.show()
        ret = app.exec_()
    scratchy.destroy()
    pomp.looper.exitLoop()
    sys.exit(ret)
