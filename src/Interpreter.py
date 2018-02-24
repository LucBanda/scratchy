from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, pyqtProperty


class Debugger(QObject):
    stopChanged = pyqtSignal()
    pauseChanged = pyqtSignal()
    playChanged = pyqtSignal()

    def __init__(self, parent, robotController):
        super(Debugger, self).__init__(parent)
        self._pause = False
        self._stop = True
        self._play = False
        self.cpu = CPU(self, robotController)

    def load(self, algorithm):
        self.algorithm = algorithm
        self.cpu.load(algorithm._elementList)

    @pyqtProperty(bool, notify=pauseChanged)
    def pause(self):
        return self._pause
    @pause.setter
    def pause(self, value):
        self._pause = value
        self.pauseChanged.emit()

    @pyqtProperty(bool, notify=playChanged)
    def play(self):
        return self._play
    @play.setter
    def play(self, value):
        self._play = value
        self.playChanged.emit()

    @pyqtProperty(bool, notify=stopChanged)
    def stop(self):
        return self._stop
    @stop.setter
    def stop(self, value):
        self._stop = value
        if self._stop:
            self.cpu.load(self.algorithm._elementList)
        self.stopChanged.emit()

    @pyqtSlot()
    def start(self):
        self.play = True
        self.stop = False
        self.pause = False
        self.cpu.execute()

    @pyqtSlot()
    def step(self):
        self.pause = True
        self.play = False
        self.stop = False
        self.cpu.execute()

    def onInstructionDone(self, instruction):
        if (self.pause):
            return
        if (self.stop):
            self.cpu.load(self.algorithm._elementList)
            return
        if self.play:
            self.cpu.execute()

    def onProgramDone(self):
        self.stop = True
        self.pause = False
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
