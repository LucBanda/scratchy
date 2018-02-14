import QtQuick 2.5
import QtQuick.Controls 1.4

ApplicationWindow {
    visible: true
    width: 1200
    height: 700
    title: qsTr("Scratchy")

    /*FileDialog {
            id: fileDialog
            nameFilters: ["scratchy files (*.sch)"]
            onAccepted: {
                if (fileDialog.selectExisting)
                    scratchyApp.open(fileUrl)
                else
                    scratchyApp.save(fileUrl)
            }
        }
*/
    menuBar: MenuBar {
        Menu {
            title: qsTr("File")
            MenuItem {
                text: qsTr("&Open")
                onTriggered: {
                    fileDialog.selectExisting = true
                    fileDialog.open()
                }
            }
            MenuItem {
                text: qsTr("&Save")
                onTriggered: {
                    fileDialog.selectExisting = false
                    scratchyApp.save(null)
                }
            }
            MenuItem {
                text: qsTr("&Save As")
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
    }

    MainForm {
        Timer  {
            interval: 100
            repeat:true
            running:true
            onTriggered: {scratchyApp.timer()}
        }
        algorithmDropTile.onDroppedProxy: {
            console.log("Proxy is ok with component : " + element.instruction + " " + element.value + " " + element.listIndex)
            if (element.listIndex == -1) {
                scratchyApp.algorithm.addElement(element.instruction, element.value, x, y)
            } else {
                scratchyApp.algorithm.updateElement(element.listIndex, element.instruction, element.value, x, y)
            }
            print_algorithm()
        }
        debugToolBar.playButton.onClicked: {
            console.log("sending instruction")
            scratchyApp.sendInstruction(scratchyApp.algorithm.elementList[0].instruction, scratchyApp.algorithm.elementList[0].value)
        }

        algorithmView.spacing: -2
        algorithmView.model: scratchyApp.algorithm.elementList
        algorithmView.delegate: ProgramElementUI {
            instruction:model.instruction
            value:model.value
            listIndex: index
        }
        algorithmView.onModelChanged: {
            console.log("this is my line, settings at : " + scratchyApp.algorithm.elementList[0].x + " " + scratchyApp.algorithm.elementList[0].y)
            algorithmView.x = scratchyApp.algorithm.elementList[0].x
            algorithmView.y= scratchyApp.algorithm.elementList[0].y
        }

        algorithmView.onCountChanged: {
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
