#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import AlgoElement
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtProperty, pyqtSlot, pyqtSignal
from PyQt5.QtQml import qmlRegisterType, QQmlApplicationEngine

# source : http://ceg.developpez.com/tutoriels/pyqt/qt-quick-python/02-interaction-qml-python/

class ScratchyApp (QObject):
    algorithmChanged = pyqtSignal()

    def __init__(self, context, parent=None):
        super(ScratchyApp, self).__init__(parent)
        self.win = parent
        # Recherche d'un enfant appelé myButton dont le signal clicked sera connecté à la fonction test3
        #self.win.findChild(QObject, "myButton").clicked.connect(self.test3)
        self.ctx = context
        self._algorithm = AlgoElement.Algorithm(parent)

    @pyqtSlot(str)
    def save(self, fileName):
        if fileName:
            self.filename = fileName.replace("file:///","/")
        if self.filename:
            open(self.filename, "w").write(self._algorithm.dump())

    @pyqtSlot(str)
    def open(self, fileName):
        if fileName:
            self.filename = fileName.replace("file:///","/")
            self._algorithm.load(open(self.filename, "r").read())


    # Premier test de communication : propriétés contextuelles.
    # @pyqtSlot(QVariant, QVariant)
    # def test1(self, login, password):
        #txt = self.verifConnection(login, password)
        # Transmission du résultat comme une propriété nommée retour
        # self.ctx.setContextProperty("retour", txt)
        # return 0

    @pyqtProperty(AlgoElement.Algorithm, notify=algorithmChanged)
    def algorithm(self):
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value):
        self._algorithm = value
        self.algorithmChanged.emit()

    # Troisième test de communication : modification directe d'un composant QML.
    #def test3(self):
        # Recherche des enfants par leur attribut objectName, récupération de la valeur de leur propriété text
    #    login = self.win.findChild(QObject, "myLogin").property("text")
    #    password = self.win.findChild(QObject, "myPassword").property("text")
    #    txt = self.verifConnection(login, password)
    #    self.win.findChild(QObject, "labelCo").setProperty("text", txt)
    #    return 0

if __name__ == "__main__":
    qmlRegisterType(AlgoElement.ProgramElement, 'Scratchy', 1, 0, 'ProgramElement')
    qmlRegisterType(AlgoElement.Algorithm, 'Scratchy', 1, 0, 'Algorithm')
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    scratchy = ScratchyApp(engine)
    engine.rootContext().setContextProperty('scratchyApp', scratchy)
    engine.load('./scratchyQml/main.qml')
    if engine.rootObjects():
        win = engine.rootObjects()[0]
        win.show()
        sys.exit(app.exec_())
