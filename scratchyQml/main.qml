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
            console.log (algorithmDropTile.keys)
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

    Timer  {
        interval: 10
        repeat:true
        running:true
        onTriggered: { scratchyApp.timer() }
    }

    MainForm {
        id: mainForm

        algorithmDropTile.onDroppedProxy: {
            if (element.listIndex === -1) {
                scratchyApp.algorithm.addElement(element.instruction, element.value, x, y)
            } else {
                scratchyApp.algorithm.updateElement(element.listIndex, element.instruction, element.value, x, y)
            }
        }

        playButton.onClicked: {
            scratchyApp.interpreter.start()
        }

        ListModel {
            id: fakeModel
            ListElement { instruction: "Avance"; value: 8 }
            ListElement { instruction: "Tourne"; value: 5 }
        }
        ListView {
            id: algorithmView
            parent:algorithmDropTile
            x: 0
            y: 0
            width: 110
            height: 160
            boundsBehavior: Flickable.StopAtBounds
            spacing: -2
            //model:fakeModel
            model: scratchyApp.algorithm.elementList
            onModelChanged: {
                console.log("model changed")
                if (scratchyApp.algorithm.elementList.length > 0) {
                    console.log(scratchyApp.algorithm.elementList[0].x, scratchyApp.algorithm.elementList[0].y)
                    algorithmView.x = scratchyApp.algorithm.elementList[0].x
                    algorithmView.y= scratchyApp.algorithm.elementList[0].y
                }
            }
            delegate: DropArea {
                id: targetArea

                width: programElement.width
                height: programElement.height
                onDropped: {
                    scratchyApp.algorithm.nextElementIndex(index+1)
                }
                ProgramElementUI {
                    id:programElement
                    instruction:model.instruction
                    value:model.value
                    listIndex: index
                    onValueChanged: model.value = Number(value)
                    states: [
                        State {
                            when: targetArea.containsDrag
                            PropertyChanges {
                                target: algorithmDropTile
                                disabled: true
                            }
                            PropertyChanges {
                                target: programElement
                                color:'grey'
                            }
                        }
                    ]
                }
            }
            onCountChanged: {
                /* calculate ListView dimensions based on content */
                var root = algorithmView.visibleChildren[0]
                var listViewHeight = 0
                var listViewWidth = 0

                // iterate over each delegate item to get their sizes
                for (var i = 0; i < root.visibleChildren.length; i++) {
                    listViewHeight += root.visibleChildren[i].height
                    listViewWidth  = Math.max(listViewWidth, root.visibleChildren[i].width)
                }

                algorithmView.height = listViewHeight
                algorithmView.width = listViewWidth
            }

        }

        function print_debug(str) {
            debugTextField.text += str + "\n"
        }

        anchors.fill: parent
    }
}
