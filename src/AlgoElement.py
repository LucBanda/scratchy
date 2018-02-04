from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
import ui.UIAlgorithmWidget

class AlgorithmWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        self.ui = ui.UIAlgorithmWidget.Ui_Form()
        self.ui.setupUi(self)
        self.algo = Algorithm()

    def displayAlgorithm(self):
        self.clear()
        for progElem in self.algo.instructionList:
            sampleButton_1 = progElem.getWidget()
            self.ui.algoLayout.addWidget(sampleButton_1)

    def addAlgoElement(self, algoElement):
        self.algo.instructionList.append(algoElement)
        self.displayAlgorithm()

    def clear(self):
        #clear layout
        for i in reversed(range(self.ui.algoLayout.count())):
            self.ui.algoLayout.itemAt(i).widget().setParent(None)

class Algorithm():
    def __init__(self):
        self.instructionList = []

class ProgramElement():
    def __init__(self, dict):
        self.needsEnd = False
        self.elementDict = dict

    def getWidget(self):
        pass

class Move(ProgramElement):
    defaultDistance = 1.0

    def __init__(self, targetDistance):
        ProgramElement.__init__(self, {"MOVE":targetDistance})

    def getWidget(self):
        return QPushButton("Move " + str(self.elementDict["MOVE"]) + " m")

class Turn(ProgramElement):
    defaultRotationAngle = 90

    def __init__(self, rotationAngle):
        ProgramElement.__init__(self, {"TURN":rotationAngle})

    def getWidget(self):
        return QPushButton("Turn " + str(self.elementDict["TURN"]) + "°")


class Loop(ProgramElement):
    defaultIterations = 2

    def __init__(self, iterations, actions):
        ProgramElement.__init__(self, {"LOOP":(iterations, actions)})

    def getWidget(self):
        return QPushButton("Repeat " + str(self.elementDict["LOOP"][0]))
