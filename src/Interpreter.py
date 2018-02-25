from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty


class Debugger(QObject):
    stoppedChanged = pyqtSignal()
    pausedChanged = pyqtSignal()
    playChanged = pyqtSignal()
    pendingChanged = pyqtSignal()

    def __init__(self, parent, robotController):
        super(Debugger, self).__init__(parent)
        self._paused = False
        self._stopped = True
        self._play = False
        self._pending = False
        self.cpu = CPU(self, robotController)

    def load(self, algorithm):
        self.algorithm = algorithm
        self.cpu.load(algorithm)

    @pyqtProperty(bool, notify=pendingChanged)
    def pending(self):
        return self._pending
    @pending.setter
    def pending(self, value):
        self._pending = value
        self.pendingChanged.emit()

    @pyqtProperty(bool, notify=pausedChanged)
    def paused(self):
        return self._paused
    @paused.setter
    def paused(self, value):
        self._paused = value
        self.pausedChanged.emit()

    @pyqtProperty(bool, notify=playChanged)
    def play(self):
        return self._play
    @play.setter
    def play(self, value):
        self._play = value
        self.playChanged.emit()

    @pyqtProperty(bool, notify=stoppedChanged)
    def stopped(self):
        return self._stopped
    @stopped.setter
    def stopped(self, value):
        self._stopped = value
        self.stoppedChanged.emit()

    @pyqtSlot()
    def start(self):
        self.play = True
        self.stopped = False
        self.paused = False
        #load main function
        self.cpu.load(self.algorithm.functionList[0])
        self.cpu.execute()
        self.pending = True

    @pyqtSlot()
    def step(self):
        self.paused = True
        self.play = False
        self.stopped = False
        self.cpu.execute()
        self.pending = True

    @pyqtSlot()
    def stop(self):
        self.stopped = True
        self.play = False
        self.paused = False

    @pyqtSlot()
    def pause(self):
        self.stopped = False
        self.play = False
        self.paused = True

    def onInstructionDone(self, instruction):
        self.pending = False
        if (self.paused):
            return
        if (self.stopped):
            self.cpu.load(self.algorithm._elementList)
            return
        if self.play:
            self.cpu.execute()

    def onProgramDone(self):
        self.stopped = True
        self.paused = False
        self.play = False
        self.cpu.load(self.algorithm._elementList)


class CPU:
    def __init__(self, client, robotController):
        self.client = client
        self.robotController = robotController
        robotController.client = self
        self.program = None
        self.executionList = None
        self.pc = None
        self.pcStack = None

    def load(self, program):
        self.program = program
        self.executionList = program
        self.pc = 0
        self.pcStack = []
        self.loopCount = 1


    def execute(self):
        if self.pc < len(self.executionList):
            inst = self.executionList[self.pc].instruction
            val = self.executionList[self.pc].value
            self.executionList[self.pc].executing = True

            if (inst == "Répete"):
                self.pcStack.append((self.executionList, self.pc, self.loopCount))
                self.executionList = self.executionList[self.pc]._childs
                self.pc = 0
                self.loopCount = val
                self.execute()
            else:
                self.robotController.sendInstruction(inst, val)


    def onInstructionReceived(self, instruction, value):
        self.executionList[self.pc].executing = False
        self.pc += 1
        if self.pc == len(self.executionList):
            #finished current execution thread, decrease current loop number
            self.loopCount -= 1
            if self.loopCount > 0:
                #if we still need to loop, only reset the pc and stay in the same executionList
                self.pc = 0
            elif len(self.pcStack)>0:
                #if we are finised with the loop, and there is something in stack unstack everything
                self.executionList, self.pc, self.loopCount = self.pcStack.pop()
                self.onInstructionReceived(self.executionList[self.pc].instruction,
                                           self.executionList[self.pc].value)
                return
            else:
                # everything finished
                self.client.onProgramDone()
        self.client.onInstructionDone(self.executionList[self.pc-1])
