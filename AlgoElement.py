from PyQt5.QtCore import QObject, pyqtProperty
from PyQt5.QtQml import qmlRegisterType, QQmlComponent, QQmlEngine, QQmlListProperty
from PyQt5.QtCore import pyqtSignal, pyqtSlot
import math

class ProgramElement(QObject):
    instructionChanged = pyqtSignal()
    valueChanged = pyqtSignal()
    executingChanged = pyqtSignal()
    childsChanged = pyqtSignal()

    def __init__(self, parent):
        QObject.__init__(self, parent)
        self._parent = parent
        self._instruction = ""
        self._value = 0
        self._childs = []
        self._executing = False

    @pyqtProperty(QObject)
    def context(self):
        return self

    @pyqtProperty(str, notify=instructionChanged)
    def instruction(self):
        return self._instruction

    @pyqtProperty(float, notify=valueChanged)
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if value != "" and not math.isnan(value):
            if self._value != value:
                self._value = value
                self.valueChanged.emit()

    @pyqtProperty(QQmlListProperty, notify=childsChanged)
    def childs(self):
        return QQmlListProperty(ProgramElement, self, self._childs)

    @pyqtProperty(bool, notify=executingChanged)
    def executing(self):
        return self._executing

    @executing.setter
    def executing(self, value):
        self._executing = value
        self.executingChanged.emit()

    @pyqtSlot(int, str, str)
    def addAfter(self, index, inst, value):
        self._parent.addElementAtIndex(index+1, inst, value)

    @pyqtSlot(int, str, str)
    def addElementAtIndex(self, index, inst, value):
        element = newElement(self, inst, value)
        self._childs.insert(index, element)
        self.childsChanged.emit()

def newElement(parent, inst, value):
    element = ProgramElement(parent)
    element._instruction = inst
    element.value = float(value)
    return element

class Algorithm(QObject):
    elementListChanged = pyqtSignal()

    def __init__(self, parent):
        QObject.__init__(self, parent)
        self._elementList = []
        self._x = 0
        self._y = 0

    def dump(self):
        string = ""
        if len(self._elementList) > 0:
            string += 'position.x:' + str(self._x) + "\n"
            string += 'position.y:' + str(self._y) + "\n"
        for element in self._elementList:
            string += element.instruction + ":" + str(element.value) + "\n"
        return string

    def load(self, string):
        self._elementList = []
        for element in string.split('\n'):
            if element:
                inst, val = element.split(':')
                if inst == "position.x":
                    self._x = int(val)
                    continue
                if inst == "position.y":
                    self._y = int(val)
                    continue
                newElement = ProgramElement(None)
                newElement.instruction = inst
                newElement.value = float(val)
                self._elementList.append(newElement)
                self.elementListChanged.emit()

    @pyqtProperty(int)
    def x(self):
        return self._x

    @pyqtProperty(int)
    def y(self):
        return self._y

    @pyqtSlot()
    def clear(self):
        self._elementList = []
        self.elementListChanged.emit()

    @pyqtSlot(str, str, int, int)
    def addElement(self, inst, value, x, y):
        self._x = x
        self._y = y
        self.addElementAtIndex(0, inst, value)

    def addElementAtIndex(self, index, inst, value):
        element = newElement(self, inst, value)
        self._elementList.insert(index, element)
        self.elementListChanged.emit()

    @ pyqtSlot(int, str, str, int, int)
    def updateElement(self, index, inst, value, x, y):
        self._elementList[index]._instruction = inst
        self._elementList[index]._value = float(value)
        self._x = x
        self._y = y
        self.elementListChanged.emit()


    @pyqtProperty(QQmlListProperty, notify=elementListChanged)
    def elementList(self):
        return QQmlListProperty(ProgramElement, self, self._elementList)

    @elementList.setter
    def elementList(self, value):
        self._elementList = value
        self.elementListChanged.emit()