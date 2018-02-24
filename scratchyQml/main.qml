import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Dialogs 1.2
import Scratchy 1.0

ApplicationWindow {
    visible: true
    width: 1200
    height: 700
    title: qsTr("Scratchy")

    ScratchyApp {
        id: scratchyApp
        objectName: 'scratchyApp'
    }

    FileDialog {
            id: fileDialog
            nameFilters: ["scratchy files (*.sch)"]
            onAccepted: {
                if (fileDialog.selectExisting)
                    scratchyApp.open(fileUrl)
                else
                    scratchyApp.save(fileUrl)
            }
        }

    menuBar: MenuBar {
        Menu {
            title: qsTr("File")
            MenuItem {
                text: qsTr("&Ouvrir...")
                onTriggered: {
                    fileDialog.selectExisting = true
                    fileDialog.open()
                }
            }
            MenuItem {
                text: qsTr("&Enregistrer")
                onTriggered: {
                    fileDialog.selectExisting = false
                    scratchyApp.save(null)
                }
            }
            MenuItem {
                text: qsTr("&Enregistrer sous...")
                onTriggered: {
                    fileDialog.selectExisting = false
                    fileDialog.open()
                }
            }
            MenuItem {
                text: qsTr("Exit")
                onTriggered: Qt.quit();
            }
        }
        Menu {
            title: qsTr("Algorithme")
            MenuItem {
                text: qsTr("&Efface")
                onTriggered: {
                    scratchyApp.clear()
                    mainForm.debugTextField.text = ""
                }
            }
        }
    }

    Connections {
        target: scratchyApp.scratchyDebugger

        onStopped: {
            mainForm.print_debug("STOP")
        }
        onInstructionDone: {
            mainForm.print_debug("fini : " + pc + " " + instruction + " " + value)
        }
    }

    MainForm {
        id: mainForm
        scratchyApp: scratchyApp
        robotController: scratchyApp.robotController

        anchors.fill: parent

        function print_debug(str) {
            debugTextField.text += str + "\n"
        }
    }
}
