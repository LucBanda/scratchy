import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Dialogs 1.2
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.0
//import Scratchy 1.0

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
        /*algorithmGroupBox.children: [
            ProgramElementUI{instruction: "Avance"}
        ]*/

        anchors.fill: parent
    }
}
