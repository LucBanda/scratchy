from PyQt5.QtCore import QObject, pyqtProperty
from PyQt5.QtQml import qmlRegisterType, QQmlComponent, QQmlEngine, QQmlListProperty
from PyQt5.QtCore import pyqtSignal, pyqtSlot

class ProgramElement(QObject):
    instructionChanged = pyqtSignal()
    valueChanged = pyqtSignal()

    def __init__(self, parent):
        QObject.__init__(self, parent)
        self._parent = None
        self._instruction = ""
        self._value = 0
        self._childs = []

    @pyqtProperty(str, notify=instructionChanged)
    def instruction(self):
        return self._instruction

    @instruction.setter
    def instruction(self, value):
        self._instruction = value
        self.instructionChanged.emit()

    @pyqtProperty(float, notify=valueChanged)
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self.valueChanged.emit()

    @pyqtProperty(QQmlListProperty)
    def childs(self):
        return QQmlListProperty(ProgramElement, self, self._childs)

    @childs.setter
    def childs(self, value):
        self._childs = value


class Algorithm(QObject):

    algorithmChanged = pyqtSignal()

    def __init__(self, parent):
        QObject.__init__(self, parent)
        self._elementList = []

    @pyqtSlot(str, float)
    def addElement(self, str, value):
        element = ProgramElement(self)
        element.instruction = str
        element.value = value
        self._elementList.append(element)
        self.algorithmChanged.emit()


    @pyqtProperty(QQmlListProperty, notify=algorithmChanged)
    def elementList(self):
        return QQmlListProperty(ProgramElement, self, self._elementList)

    @elementList.setter
    def elementList(self, value):
        self._elementList = value
        self.algorithmChanged.emit()