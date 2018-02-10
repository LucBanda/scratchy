import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Dialogs 1.2
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.0
import Scratchy 1.0

ApplicationWindow {
    visible: true
    width: 1200
    height: 700
    title: qsTr("Scratchy")

    menuBar: MenuBar {
        Menu {
            title: qsTr("File")
            MenuItem {
                text: qsTr("&Open")
                onTriggered: console.log("Open action triggered");
            }
            MenuItem {
                text: qsTr("&Save")
                onTriggered: console.log("Save action triggered");
            }
            MenuItem {
                text: qsTr("Exit")
                onTriggered: Qt.quit();
            }
        }
    }

    MainForm {
        moveButton.onClicked: {
            scratchyApp.algorithm.addElement("Move", 1.0)
            var str
            for (var elem in scratchyApp.algorithm.elementList) {
                str += scratchyApp.algorithm.elementList[elem].instruction + "\n"
            }
            debugTextField.text = str
        }

        anchors.fill: parent
    }
}
