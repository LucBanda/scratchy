from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


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
