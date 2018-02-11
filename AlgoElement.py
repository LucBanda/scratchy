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
    elementListChanged = pyqtSignal()

    def __init__(self, parent):
        QObject.__init__(self, parent)
        self._elementList = []

    def dump(self):
        string = ""
        for element in self._elementList:
            string += element.instruction + ":" + str(element.value) + "\n"
        return string

    def load(self, string):
        self._elementList = []
        for element in string.split('\n'):
            if element:
                inst, val = element.split(':')
                newElement = ProgramElement(None)
                newElement.instruction = inst
                newElement.value = float(val)
                self._elementList.append(newElement)
                self.elementListChanged.emit()


    @pyqtSlot(str, str, QObject, int, int)
    def addElement(self, inst, value, parent, x, y):
        print(inst + ' ' + value + ' ' + str(x) + ' ' + str(y))
        element = ProgramElement(self)
        element.instruction = inst
        element.value = float(value)
        self._elementList.append(element)
        self.elementListChanged.emit()

    @pyqtProperty(QQmlListProperty, notify=elementListChanged)
    def elementList(self):
        return QQmlListProperty(ProgramElement, self, self._elementList)

    @elementList.setter
    def elementList(self, value):
        self._elementList = value
        self.elementListChanged.emit()