from AlgoElement import ProgramElement
from PyQt5.QtCore import QObject, pyqtProperty, pyqtSignal

from RobotItf import RobotItf


class RobotController(RobotItf, QObject):
    xRobotChanged = pyqtSignal()
    yRobotChanged = pyqtSignal()
    capRobotChanged = pyqtSignal()
    vxRobotChanged = pyqtSignal()
    vyRobotChanged = pyqtSignal()
    vangRobotChanged = pyqtSignal()
    connectedChanged = pyqtSignal()
    lastInstructionChanged = pyqtSignal()
    statusChanged = pyqtSignal()

    def __init__(self, parent):
        QObject.__init__(self, parent)
        RobotItf.__init__(self, RobotItf.LOCAL_POMP_ADDRESS, "client")
        self._connected = False
        self._x = 0.0
        self._y = 0.0
        self._cap = 0.0
        self._vx = 0.0
        self._vy = 0.0
        self._vang = 0.0
        self._lastInstruction = ProgramElement(None)
        self.client = None

    @pyqtProperty(bool, notify=connectedChanged)
    def connected(self):
        return self._connected

    @connected.setter
    def connected(self, value):
        self._connected = value
        self.connectedChanged.emit()

    @pyqtProperty(float, notify=xRobotChanged)
    def xRobot(self):
        return self._x

    @xRobot.setter
    def xRobot(self, value):
        self._x = value
        self.xRobotChanged.emit()

    @pyqtProperty(float, notify=yRobotChanged)
    def yRobot(self):
        return self._y

    @yRobot.setter
    def yRobot(self, value):
        self._y = value
        self.yRobotChanged.emit()

    @pyqtProperty(float, notify=capRobotChanged)
    def capRobot(self):
        return self._cap

    @capRobot.setter
    def capRobot(self, value):
        self._cap = value
        self.capRobotChanged.emit()

    @pyqtProperty(float, notify=vxRobotChanged)
    def vxRobot(self):
        return self._vx

    @vxRobot.setter
    def vxRobot(self, value):
        self._vx = value
        self.vxRobotChanged.emit()

    @pyqtProperty(float, notify=vyRobotChanged)
    def vyRobot(self):
        return self._vy

    @vyRobot.setter
    def vyRobot(self, value):
        self._vy = value
        self.vyRobotChanged.emit()

    @pyqtProperty(float, notify=vangRobotChanged)
    def vangRobot(self):
        return self._vang

    @vangRobot.setter
    def vangRobot(self, value):
        self._vang = value
        self.vangRobotChanged.emit()

    @pyqtProperty(ProgramElement, notify=lastInstructionChanged)
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
        self.xRobot = x
        self.yRobot = y
        self.capRobot = cap
        self.vxRobot = vx
        self.vyRobot = vy
        self.vangRobot = vang

    def onInstructionReceived(self, instruction, value):
        newInst = ProgramElement(None)
        newInst._instruction = instruction
        newInst._value = value
        self.lastInstruction = newInst
        if self.client:
            self.client.onInstructionReceived(instruction, value)

