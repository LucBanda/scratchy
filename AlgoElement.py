from PyQt5.QtCore import QObject, pyqtProperty
from PyQt5.QtQml import qmlRegisterType, QQmlComponent, QQmlEngine, QQmlListProperty
from PyQt5.QtCore import pyqtSignal, pyqtSlot

class ProgramElement(QObject):
    instructionChanged = pyqtSignal()
    valueChanged = pyqtSignal()
    xChanged = pyqtSignal()
    yChanged = pyqtSignal()

    def __init__(self, parent):
        QObject.__init__(self, parent)
        self._parent = None
        self._instruction = ""
        self._value = 0
        self._childs = []
        self._x = 0
        self._y = 0

    @pyqtProperty(str, notify=instructionChanged)
    def instruction(self):
        return self._instruction

    @instruction.setter
    def instruction(self, value):
        self._instruction = value
        self.instructionChanged.emit()

    @pyqtProperty(int, notify=xChanged)
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value
        print ("x is now : " + str(self._x))
        self.xChanged.emit()

    @pyqtProperty(int, notify=yChanged)
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value
        self.yChanged.emit()

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


    @pyqtSlot(str, str, int, int)
    def addElement(self, inst, value, x, y):
        print(inst + ' ' + value + ' ' + ' ' + str(x) + ' ' + str(y))
        element = ProgramElement(self)
        element.x = x
        element.y = y
        element.instruction = inst
        element.value = float(value)
        self._elementList.append(element)
        self.elementListChanged.emit()

    @pyqtSlot(int, str, str, int, int)
    def updateElement(self, index, inst, value, x, y):
        print(str(index) + ' ' + inst + ' ' + value + ' ' + str(x) + ' ' + str(y))
        self._elementList[index].instruction = inst
        self._elementList[index].value = float(value)
        self._elementList[index].x = x
        self._elementList[index].y = y
        self.elementListChanged.emit()

    @pyqtProperty(QQmlListProperty, notify=elementListChanged)
    def elementList(self):
        return QQmlListProperty(ProgramElement, self, self._elementList)

    @elementList.setter
    def elementList(self, value):
        self._elementList = value
        self.elementListChanged.emit()