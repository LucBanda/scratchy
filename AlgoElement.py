from PyQt5.QtCore import QObject, pyqtProperty
from PyQt5.QtQml import qmlRegisterType, QQmlComponent, QQmlEngine, QQmlListProperty
from PyQt5.QtCore import pyqtSignal, pyqtSlot
import math

class ProgramElement(QObject):
    instructionChanged = pyqtSignal()
    valueChanged = pyqtSignal()
    xChanged = pyqtSignal()
    yChanged = pyqtSignal()
    executingChanged = pyqtSignal()
    childsChanged = pyqtSignal()

    def __init__(self, parent):
        QObject.__init__(self, parent)
        self._parent = parent
        self.addAfterCb = None
        self._instruction = ""
        self._value = 0
        self._childs = []
        self._x = 0
        self._y = 0
        self._executing = False

    @pyqtProperty(QObject)
    def context(self):
        return self

    @pyqtProperty(str, notify=instructionChanged)
    def instruction(self):
        return self._instruction

    @pyqtProperty(int, notify=xChanged)
    def x(self):
        return self._x

    @pyqtProperty(int, notify=yChanged)
    def y(self):
        return self._y

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

    def addChild(self, index, child):
        self._childs.insert(index, child)
        self.childsChanged.emit()

    @pyqtProperty(bool, notify=executingChanged)
    def executing(self):
        return self._executing

    @executing.setter
    def executing(self, value):
        self._executing = value
        self.executingChanged.emit()

    @pyqtSlot(str, float, int, int)
    def addAfter(self, inst, value, x, y):
        print ("onAddAfter python : ", self.instruction, inst)
        self.addAfterCb(inst, value, x, y)

    @pyqtSlot(int, str, float, int, int)
    def addElementAtIndex(self, index, inst, value, x, y):
        element = newElement(self,
                             inst, value, x, y)
        element.addAfterCb = lambda inst, val, x, y: self.addElementAtIndex(index+1, inst, val, x, y)
        self._childs.insert(index, element)
        self.childsChanged.emit()

def newElement(parent, inst, value, x, y):
    element = ProgramElement(parent)
    element._x = x
    element._y = y
    element._instruction = inst
    print(inst, value, x, y)
    element.value = float(value)
    return element

class Algorithm(QObject):
    elementListChanged = pyqtSignal()

    def __init__(self, parent):
        QObject.__init__(self, parent)
        self._elementList = []

    def dump(self):
        string = ""
        if len(self._elementList) > 0:
            string += 'position.x:' + str(self._elementList[0].x) + "\n"
            string += 'position.y:' + str(self._elementList[0].y) + "\n"
        for element in self._elementList:
            string += element.instruction + ":" + str(element.value) + "\n"
        return string

    def load(self, string):
        self._elementList = []
        xFound = 0
        yFound = 0
        for element in string.split('\n'):
            if element:
                inst, val = element.split(':')
                if inst == "position.x":
                    xFound = int(val)
                    continue
                if inst == "position.y":
                    yFound = int(val)
                    continue
                newElement = ProgramElement(None)
                newElement.instruction = inst
                newElement.value = float(val)
                if len(self._elementList) == 0:
                    newElement.x = xFound
                    newElement.y = yFound
                self._elementList.append(newElement)
                self.elementListChanged.emit()

    @pyqtSlot()
    def clear(self):
        self._elementList = []
        self.elementListChanged.emit()

    @pyqtSlot(str, str, int, int)
    def addElement(self, inst, value, x, y):
        print("add element at ", 0, " : ", inst, value, x, y)
        self.addElementAtIndex(0, inst, value, x, y)

    def addElementAtIndex(self, index, inst, value, x, y):
        element = newElement(self, inst, value, x, y)
        element.addAfterCb = lambda inst, val, x, y: self.addElementAtIndex(index+1, inst, val, x, y)
        self._elementList.insert(index, element)
        self.elementListChanged.emit()

    @ pyqtSlot(int, str, str, int, int)
    def updateElement(self, index, inst, value, x, y):
        print("update element", index)
        self._elementList[index]._instruction = inst
        self._elementList[index]._value = float(value)
        self._elementList[index]._x = x
        self._elementList[index]._y = y
        self.elementListChanged.emit()


    @pyqtProperty(QQmlListProperty, notify=elementListChanged)
    def elementList(self):
        return QQmlListProperty(ProgramElement, self, self._elementList)

    @elementList.setter
    def elementList(self, value):
        self._elementList = value
        self.elementListChanged.emit()