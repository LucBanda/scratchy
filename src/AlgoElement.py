from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout
from PyQt5 import QtWidgets

class AlgorithmWidget(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self, parent)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.formLayout = QtWidgets.QFormLayout(self)
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.formLayout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.algo = Algorithm()

    def displayAlgorithm(self):
        self.clear()
        i = 0
        for progElem in self.algo.instructionList:
            i+=1
            newButton = QtWidgets.QPushButton(progElem.ActionString, self)
            self.formLayout.setWidget(i, QtWidgets.QFormLayout.LabelRole, newButton)

    def addAlgoElement(self, algoElement):
        self.algo.instructionList.append(algoElement)
        self.displayAlgorithm()

    def clear(self):
        #clear layout
        for i in reversed(range(self.formLayout.count())):
            self.formLayout.itemAt(i).widget().setParent(None)


class Algorithm():
    def __init__(self):
        self.instructionList = []

class ProgramElement():
    def __init__(self, dict):
        self.needsEnd = False
        self.elementDict = dict

class Move(ProgramElement):
    defaultDistance = 1.0

    def __init__(self, targetDistance):
        ProgramElement.__init__(self, {"MOVE":targetDistance})
        self.ActionString = "Move " + str(self.elementDict["MOVE"]) + " m"

class Turn(ProgramElement):
    defaultRotationAngle = 90

    def __init__(self, rotationAngle):
        ProgramElement.__init__(self, {"TURN":rotationAngle})
        self.ActionString = "Turn " + str(self.elementDict["TURN"]) + "°"


class Loop(ProgramElement):
    defaultIterations = 2

    def __init__(self, iterations, actions):
        ProgramElement.__init__(self, {"LOOP":(iterations, actions)})
        self.ActionString = "Repeat " + str(self.elementDict["LOOP"][0])
