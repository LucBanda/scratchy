# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/luc/scratchy/scratchy/ui/AlgorithmWidget.ui'
#
# Created: Sun Feb  4 13:28:31 2018
#      by: PyQt5 UI code generator 5.3.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(657, 438)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.dockWidget = QtWidgets.QDockWidget(Form)
        self.dockWidget.setObjectName("dockWidget")
        self.dockWidgetContents = QtWidgets.QWidget()
        self.dockWidgetContents.setObjectName("dockWidgetContents")
        self.widget = QtWidgets.QWidget(self.dockWidgetContents)
        self.widget.setGeometry(QtCore.QRect(230, 140, 97, 107))
        self.widget.setObjectName("widget")
        self.algoLayout = QtWidgets.QVBoxLayout(self.widget)
        self.algoLayout.setContentsMargins(0, 0, 0, 0)
        self.algoLayout.setObjectName("algoLayout")
        self.dockWidget.setWidget(self.dockWidgetContents)
        self.verticalLayout.addWidget(self.dockWidget)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

