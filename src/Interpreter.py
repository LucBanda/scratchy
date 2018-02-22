from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class Interpreter(QObject):
    instructionDone = pyqtSignal(int, str, float, arguments = ['pc', 'instruction', 'value'])
    stopped = pyqtSignal()

    def __init__(self, parent, executionList, robotController):
        super(Interpreter, self).__init__(parent)
        self.executionList = executionList
        self._parent = parent
        self.robotController = robotController
        self.subInterpreter = None
        self.loopCount = 0
        self.PC = 0

    @pyqtSlot()
    def start(self):
        self.PC = -1
        self.next()

    @pyqtSlot()
    def next(self):
        if (self.subInterpreter):
            self.subInterpreter.next()
            return
        self.PC += 1
        if self.PC == len(self.executionList):
            self._parent.finishedExecutionList()
            return
        if self.PC < len(self.executionList):
            inst = self.executionList[self.PC].instruction
            val = self.executionList[self.PC].value
            self.executionList[self.PC].executing = True
            if (inst != "Répete"):
                self.robotController.sendInstruction(inst, val)
            else:
                self.loopCount = val
                self.subInterpreter = Interpreter(self, self.executionList[self.PC].childs, self.robotController)
                self.robotController.client = self.subInterpreter
                self.subInterpreter.start()


    def finishedExecutionList(self):
        self.loopCount -= 1
        if (self.loopCount == 0):
            self.subInterpreter = None
            self.robotController.client = self
            self.next()
        else:
            self.subInterpreter = Interpreter(self, self.executionList[self.PC].childs, self.robotController)
            self.robotController.client = self.subInterpreter
            self.subInterpreter.start()


    def onInstructionReceived(self, instruction, value):
        if (self.subInterpreter):
            self.subInterpreter.next()
            return
        self.executionList[self.PC].executing = False
        self.next()
        self.instructionDone.emit(self.PC, instruction, value)

