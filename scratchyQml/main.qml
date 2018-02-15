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


    Rotation {
        id: rotation
        origin.x: robot.x
        origin.y: robot.y
        angle: scratchyApp.robotController.capRobot
    }

    Connections {
        target: scratchyApp.robotController

        onConnectedChanged: {
            debugToolBar.visible = scratchyApp.robotController.connected
        }
        onStatusChanged: {
            console.log(scratchyApp.robotController.xRobot,
                        scratchyApp.robotController.yRobot,
                        xOrig,
                        yOrig)
            robot.x = scratchyApp.robotController.xRobot*10 + xOrig
            robot.y = scratchyApp.robotController.yRobot*10 + yOrig
            robot.transform = rotation

        }

    }
    Timer  {
        interval: 100
        repeat:true
        running:true
        onTriggered: {scratchyApp.timer()}
    }

    MainForm {
        id: mainForm

        algorithmDropTile.onDroppedProxy: {
            if (element.listIndex === -1) {
                scratchyApp.algorithm.addElement(element.instruction, element.value, x, y)
            } else {
                scratchyApp.algorithm.updateElement(element.listIndex, element.instruction, element.value, x, y)
            }
            print_algorithm()
        }

        playButton.onClicked: {
            console.log("sending")
            scratchyApp.sendInstruction(scratchyApp.algorithm.elementList[0].instruction, scratchyApp.algorithm.elementList[0].value)
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
            delegate: ProgramElementUI {
                instruction:model.instruction
                value:model.value
                listIndex: index
            }
            model: scratchyApp.algorithm.elementList
            onModelChanged: {
                        if (scratchyApp.algorithm.elementList.length > 0) {
                            algorithmView.x = scratchyApp.algorithm.elementList[0].x
                            algorithmView.y= scratchyApp.algorithm.elementList[0].y
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
        function print_algorithm() {
            debugTextField.text = ""
            for (var index in scratchyApp.algorithm.elementList) {
                var element = scratchyApp.algorithm.elementList[index]
                debugTextField.text += element.instruction + ": " + element.value + "\n"
            }
        }

        anchors.fill: parent
    }
}
