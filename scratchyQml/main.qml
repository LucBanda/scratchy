import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Dialogs 1.2

ApplicationWindow {
    visible: true
    width: 1200
    height: 700
    title: qsTr("Scratchy")

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
                    scratchyApp.algorithm.clear()
                    mainForm.debugTextField.text = ""
                }
            }
        }
    }

    property alias debugToolBar: mainForm.debugToolBar
    property alias algorithmDropTile: mainForm.algorithmDropTile
    property alias playButton: mainForm.playButton
    property alias robot: mainForm.robot
    property double xOrig: mainForm.robotPlayground.width / 2
    property double yOrig: mainForm.robotPlayground.height / 2
    property double rotateAngle: 0.0

    Rotation {
        id: rotation
        origin.x: robot.width/2
        origin.y: robot.height/2
        angle: rotateAngle
    }

    Connections {
        target: scratchyApp.robotController

        onConnectedChanged: {
            debugToolBar.visible = scratchyApp.robotController.connected
        }
        onStatusChanged: {
            robot.x = xOrig + scratchyApp.robotController.xRobot*2
            robot.y = yOrig - scratchyApp.robotController.yRobot*2
            rotateAngle = scratchyApp.robotController.capRobot
            robot.transform = rotation
        }
    }

    Connections {
        target: scratchyApp.interpreter

        onStopped: {
            mainForm.print_debug("STOP")
        }
        onInstructionDone: {
            mainForm.print_debug("fini : " + pc + " " + instruction + " " + value)
            scratchyApp.interpreter.next()
        }
    }

    MainForm {
        id: mainForm

        algorithmDropTile.onDroppedProxy: {
            if (element.listIndex === -1) {
                    scratchyApp.algorithm.addElement(element.programElement.instruction, element.programElement.value, x, y)
            } else {
                scratchyApp.algorithm.updateElement(element.listIndex, element.programElement.instruction, element.programElement.value, x, y)
            }
        }

        playButton.onClicked: {
            scratchyApp.interpreter.start()
        }

        ListModel {
            id: fakeModel
            Component.onCompleted: {
                append({ "instruction": "Répete", "value": 5, "childs":[
                           {"instruction": "Avance", "value": 8, "childs":[]},
                           { "instruction": "Répete", "value": 5, "childs":[
                                       {"instruction": "Avance", "value": 8, "childs":[]},
                                       {"instruction": "Tourne", "value": 180, "childs":[]}
                                   ]},
                           {"instruction": "Tourne", "value": 180, "childs":[]},
                           { "instruction": "Répete", "value": 5, "childs":[
                                       {"instruction": "Avance", "value": 8, "childs":[]},
                                       {"instruction": "Tourne", "value": 180, "childs":[]}
                                   ]},

                                   ]})
            }
        }

        Component {
            id:recursableDelegate
            ProgramElementUI {
                id:programElementUi
                property int programElementIndex: index
                programElement: model
                listIndex: programElementIndex

                onValueChanged: { model.value = Number(value) }
                onAddAfter: { model.context.addAfter(index, element.programElement.instruction, element.programElement.value, x, y) }
                onAddInside: { model.context.addElementAtIndex(0, element.programElement.instruction, element.programElement.value, x, y) }
                childListView.model: model.childs
                childListView.delegate: recursableDelegate
            }
        }

        ListView {
            id: algorithmView
            parent:algorithmDropTile
            x: 0
            y: 0
            height: count > 0 ? contentItem.childrenRect.height : 0
            spacing: -2
            //model:fakeModel
            model: scratchyApp.algorithm.elementList
            onModelChanged: {
                if (scratchyApp.algorithm.elementList.length > 0) {
                    algorithmView.x = scratchyApp.algorithm.x
                    algorithmView.y = scratchyApp.algorithm.y
                }
            }
            delegate: recursableDelegate

        }

        function print_debug(str) {
            debugTextField.text += str + "\n"
        }

        anchors.fill: parent
    }
}
