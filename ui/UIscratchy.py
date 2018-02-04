# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/luc/scratchy/scratchy/ui/scratchy.ui'
#
# Created: Sun Feb  4 19:09:27 2018
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 27))
        self.menubar.setObjectName("menubar")
        self.menuFichier = QtWidgets.QMenu(self.menubar)
        self.menuFichier.setObjectName("menuFichier")
        self.menuActions = QtWidgets.QMenu(self.menubar)
        self.menuActions.setObjectName("menuActions")
        MainWindow.setMenuBar(self.menubar)
        self.actionAvancer = QtWidgets.QAction(MainWindow)
        self.actionAvancer.setObjectName("actionAvancer")
        self.actionTourner = QtWidgets.QAction(MainWindow)
        self.actionTourner.setObjectName("actionTourner")
        self.actionBoucle = QtWidgets.QAction(MainWindow)
        self.actionBoucle.setObjectName("actionBoucle")
        self.menuActions.addAction(self.actionAvancer)
        self.menuActions.addAction(self.actionTourner)
        self.menuActions.addAction(self.actionBoucle)
        self.menubar.addAction(self.menuFichier.menuAction())
        self.menubar.addAction(self.menuActions.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFichier.setTitle(_translate("MainWindow", "Fichier"))
        self.menuActions.setTitle(_translate("MainWindow", "Actions"))
        self.actionAvancer.setText(_translate("MainWindow", "Avancer..."))
        self.actionTourner.setText(_translate("MainWindow", "Tourner..."))
        self.actionBoucle.setText(_translate("MainWindow", "Boucle..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

