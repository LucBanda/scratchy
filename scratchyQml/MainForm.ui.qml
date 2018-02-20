import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.1

Item {
    id: item1
    width: 1024
    height: 800
    property alias robotPlayground: robotPlayground
    property alias robotY: robot.y
    property alias robotX: robot.x
    property alias robot: robot
    property alias debugToolBar: debugToolBar
    property alias algorithmDropTile: algorithmDropTile
    property alias defaultLoop: defaultLoop
    property alias defaultTourne: defaultTourne
    property alias defaultAvance: defaultAvance
    property alias debugTextField: debugTextField
    property alias actionGroupBox: actionGroupBox
    property alias playButton: debugToolBar.playButton

    GroupBox {
        id: actionGroupBox
        width: 110
        anchors.left: videoFrame.right
        anchors.leftMargin: 0
        anchors.bottom: robotPlayground.top
        anchors.bottomMargin: 0
        anchors.top: parent.top
        anchors.topMargin: 0

        Layout.fillHeight: true
        Layout.fillWidth: false
        Layout.preferredWidth: 100
        Layout.maximumWidth: 100

        title: qsTr("Actions")

        ProgramElementUI {
            id: defaultAvance
            anchors.left: parent.left
            anchors.leftMargin: 2
            anchors.top: parent.top
            anchors.topMargin: 5
            programElement: Item {
                property string instruction:"Avance"
                property string value: "1"
                property bool executing: false
            }
        }

        ProgramElementUI {
            id: defaultTourne
            anchors.left: parent.left
            anchors.leftMargin: 2
            anchors.top: defaultAvance.bottom
            anchors.topMargin: 15
            programElement: Item {
                property string instruction:"Tourne"
                property string value: "90"
                property bool executing: false
            }
        }

        ProgramElementUI {
            id: defaultLoop
            anchors.left: parent.left
            anchors.leftMargin: 2
            anchors.top: defaultTourne.bottom
            anchors.topMargin: 15
            programElement: Item {
                property string instruction:"Répete"
                property string value: "2"
                property bool executing: false
            }
        }
    }

    Rectangle {
        id: robotPlayground
        color: "#f0fff7"
        radius: 10
        border.color: "#3be97e"
        border.width: 1
        anchors.right: algorithmDropTile.left
        anchors.rightMargin: 0
        anchors.top: videoFrame.bottom
        anchors.topMargin: 0
        anchors.left: parent.left
        anchors.leftMargin: 0
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 0

        RobotForm {
            id: robot
            x: 180
            y: 228
            width: 30
            height: 30
        }
    }

    Rectangle {
        id: videoFrame
        width: videoFrame.height * 4.0 / 3.0
        height: 250
        color: "#727272"
        anchors.top: parent.top
        anchors.topMargin: 0
        anchors.left: parent.left
        anchors.leftMargin: 0
    }


    Rectangle {
        id: rectangle
        y: 622
        width: algorithmDropTile.width
        height: 200
        color: "#f0f0ff"
        border.color: "#4819d4"
        anchors.left: robotPlayground.right
        anchors.leftMargin: 0
        anchors.right: parent.right
        anchors.rightMargin: 0
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 0

        Text {
            id: debugTextField
            text: qsTr("")
            anchors.fill: parent
            font.pixelSize: 12
        }
    }
    DropTile {
        id: algorithmDropTile
        color: "#fffcee"
        anchors.bottom: rectangle.top
        anchors.bottomMargin: 0
        anchors.left: actionGroupBox.right
        anchors.leftMargin: 0
        anchors.right: parent.right
        anchors.rightMargin: 0
        anchors.top: parent.top
        anchors.topMargin: 0

        DebugToolBarForm {
            id: debugToolBar
            x: 51
            y: 510
            width: 300
            height: 50
            visible: false
            anchors.right: parent.right
            anchors.rightMargin: 30
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 30
        }
    }
}
