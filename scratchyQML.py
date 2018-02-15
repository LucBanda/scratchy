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

    xChanged = pyqtSignal()
    yChanged = pyqtSignal()
    capChanged = pyqtSignal()
    vxChanged = pyqtSignal()
    vyChanged = pyqtSignal()
    vangChanged = pyqtSignal()
    connectedChanged = pyqtSignal()
    lastInstructionChanged = pyqtSignal()

    def __init__(self, parent):
        QObject.__init__(self, parent)
        RobotItf.__init__(self, RobotItf.LOCAL_POMP_ADDRESS, "client")
        self._connected = False
        self._x = 0.0
        self._y = 0.0
        self._cap  = 0.0
        self._vx = 0.0
        self._vy = 0.0
        self._vang = 0.0
        self._lastInstruction = AlgoElement.ProgramElement(None)

    @pyqtProperty(bool, notify=connectedChanged)
    def connected(self):
        return self._connected
    @connected.setter
    def connected(self, value):
        self._connected = value
        self.connectedChanged.emit()

    @pyqtProperty(float, notify=xChanged)
    def x(self):
        return self._x
    @x.setter
    def x(self, value):
        self._x = value
        self.xChanged.emit()

    @pyqtProperty(float, notify=yChanged)
    def y(self):
        return self._y
    @y.setter
    def y(self, value):
        self._y = value
        self.yChanged.emit()

    @pyqtProperty(float, notify=capChanged)
    def cap(self):
        return self._cap
    @cap.setter
    def cap(self, value):
        self._cap = value
        self.capChanged.emit()

    @pyqtProperty(float, notify=vxChanged)
    def vx(self):
        return self._vx
    @vx.setter
    def vx(self, value):
        self._vx = value
        self.vxChanged.emit()

    @pyqtProperty(float, notify=vyChanged)
    def vy(self):
        return self._vy
    @vy.setter
    def vy(self, value):
        self._vy = value
        self.vyChanged.emit()

    @pyqtProperty(float, notify=vangChanged)
    def vang(self):
        return self._vang
    @vang.setter
    def vang(self, value):
        self._vang = value
        self.vangChanged.emit()

    @pyqtProperty(AlgoElement.ProgramElement, notify = lastInstructionChanged)
    def lastInstruction(self):
        return self._lastInstruction

    @lastInstruction.setter
    def lastInstruction(self, value):
        self._lastInstruction = value
        self.lastInstructionChanged.emit()

    def onConnected(self, ctx, conn):
        self.connected = True

    def onDisconnected(self, ctx, conn):
        self.connected = False

    def onStateReceived(self, x, y, cap, vx, vy, vang):
        self.x = x
        self.y = y
        self.cap = cap
        self.vx = vx
        self.vy = vy
        self.vang = vang

    def onInstructionReceived(self, instruction, value):
        newInst = AlgoElement.ProgramElement(None)
        newInst.instruction = instruction
        newInst.value = value
        self.lastInstruction = newInst


class ScratchyApp (QObject):
    algorithmChanged = pyqtSignal()
    onInstructionReceived = pyqtSignal()
    robotControllerChanged = pyqtSignal()

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

    @pyqtProperty(RobotController, notify=robotControllerChanged)
    def robotController(self):
        return self._robotController

    @robotController.setter
    def robotController(self, value):
        self._robotController = value
        self.robotControllerChanged.emit()

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
