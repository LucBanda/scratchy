# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/luc/scratchy/scratchy/ui/mainwindow.ui'
#
# Created: Sat Feb  3 23:58:04 2018
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(804, 479)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.VideoWidget = QtWidgets.QGraphicsView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.VideoWidget.sizePolicy().hasHeightForWidth())
        self.VideoWidget.setSizePolicy(sizePolicy)
        self.VideoWidget.setSizeIncrement(QtCore.QSize(0, 0))
        self.VideoWidget.setBaseSize(QtCore.QSize(0, 0))
        self.VideoWidget.setObjectName("VideoWidget")
        self.horizontalLayout_2.addWidget(self.VideoWidget)
        self.CommandsTable = QtWidgets.QTableWidget(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CommandsTable.sizePolicy().hasHeightForWidth())
        self.CommandsTable.setSizePolicy(sizePolicy)
        self.CommandsTable.setMinimumSize(QtCore.QSize(120, 0))
        self.CommandsTable.setMaximumSize(QtCore.QSize(120, 16777215))
        self.CommandsTable.setObjectName("CommandsTable")
        self.CommandsTable.setColumnCount(0)
        self.CommandsTable.setRowCount(0)
        self.horizontalLayout_2.addWidget(self.CommandsTable)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.locationView = QtWidgets.QGraphicsView(self.centralwidget)
        self.locationView.setObjectName("locationView")
        self.verticalLayout.addWidget(self.locationView)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.AlgoView = QtWidgets.QGraphicsView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AlgoView.sizePolicy().hasHeightForWidth())
        self.AlgoView.setSizePolicy(sizePolicy)
        self.AlgoView.setMinimumSize(QtCore.QSize(20, 250))
        self.AlgoView.setMaximumSize(QtCore.QSize(16000, 16777215))
        self.AlgoView.setObjectName("AlgoView")
        self.verticalLayout_2.addWidget(self.AlgoView)
        self.DebugView = QtWidgets.QTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DebugView.sizePolicy().hasHeightForWidth())
        self.DebugView.setSizePolicy(sizePolicy)
        self.DebugView.setMinimumSize(QtCore.QSize(100, 0))
        self.DebugView.setMaximumSize(QtCore.QSize(16777215, 150))
        self.DebugView.setObjectName("DebugView")
        self.verticalLayout_2.addWidget(self.DebugView)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 804, 27))
        self.menubar.setObjectName("menubar")
        self.menuFichier = QtWidgets.QMenu(self.menubar)
        self.menuFichier.setObjectName("menuFichier")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOuvrir = QtWidgets.QAction(MainWindow)
        self.actionOuvrir.setObjectName("actionOuvrir")
        self.actionSauver = QtWidgets.QAction(MainWindow)
        self.actionSauver.setObjectName("actionSauver")
        self.menuFichier.addAction(self.actionOuvrir)
        self.menuFichier.addAction(self.actionSauver)
        self.menubar.addAction(self.menuFichier.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFichier.setTitle(_translate("MainWindow", "Fichier"))
        self.actionOuvrir.setText(_translate("MainWindow", "Ouvrir..."))
        self.actionSauver.setText(_translate("MainWindow", "Sauver..."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

