#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import AlgoElement
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtProperty
from PyQt5.QtQml import qmlRegisterType, QQmlApplicationEngine

# source : http://ceg.developpez.com/tutoriels/pyqt/qt-quick-python/02-interaction-qml-python/

class ScratchyApp (QObject):
    def __init__(self, context, parent=None):
        super(ScratchyApp, self).__init__(parent)
        # Recherche d'un enfant appelé myButton dont le signal clicked sera connecté à la fonction test3
        self.win = parent
        #self.win.findChild(QObject, "myButton").clicked.connect(self.test3)
        self.ctx = context
        self._algorithm = AlgoElement.Algorithm(parent)

    # Premier test de communication : propriétés contextuelles.
    # @pyqtSlot(QVariant, QVariant)
    # def test1(self, login, password):
        #txt = self.verifConnection(login, password)
        # Transmission du résultat comme une propriété nommée retour
        # self.ctx.setContextProperty("retour", txt)
        # return 0

    # Deuxième test de communication : création d'une fonction ayant pour type de retour un QVariant (obligatoire ici pour que QML sache l'interpréter).
    @pyqtProperty(AlgoElement.Algorithm)
    def algorithm(self):
        return self._algorithm

    @algorithm.setter
    def algorithm(self, value):
        self._algorithm = value

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
    engine.load('../scratchyQml/main.qml')
    if engine.rootObjects():
        win = engine.rootObjects()[0]
        win.show()
        sys.exit(app.exec_())