import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.1

Item {
    id: item1
    width: 1024
    height: 800
    property alias defaultLoop: defaultLoop
    property alias defaultTourne: defaultTourne
    property alias defaultAvance: defaultAvance
    property alias debugTextField: debugTextField
    property alias algorithmGroupBox: algorithmGroupBox
    property alias actionGroupBox: actionGroupBox

    GroupBox {
        id: actionGroupBox
        width: 110
        anchors.left: videoFrame.right
        anchors.leftMargin: 0
        anchors.bottom: robotPosition.top
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
        }

        ProgramElementUI {
            id: defaultTourne
            color: "#dd9060"
            anchors.left: parent.left
            anchors.leftMargin: 2
            anchors.top: defaultAvance.bottom
            anchors.topMargin: 15
            value: "90"
            instruction: "Tourne"
        }

        ProgramElementUI {
            id: defaultLoop
            color: "#21c24c"
            anchors.left: parent.left
            anchors.leftMargin: 2
            anchors.top: defaultTourne.bottom
            anchors.topMargin: 15
            value: "2"
            instruction: "Répete"
        }
    }

    Rectangle {
        id: robotPosition
        color: "#f0fff7"
        radius: 10
        border.color: "#3be97e"
        border.width: 1
        anchors.right: algorithmGroupBox.left
        anchors.rightMargin: 0
        anchors.top: videoFrame.bottom
        anchors.topMargin: 0
        anchors.left: parent.left
        anchors.leftMargin: 0
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 0
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
        id: algorithmGroupBox
        color: "#fffcee"
        radius: 10
        anchors.left: actionGroupBox.right
        anchors.leftMargin: 0
        anchors.bottom: rectangle.top
        anchors.bottomMargin: 0
        anchors.top: parent.top
        anchors.topMargin: 0
        anchors.right: parent.right
        anchors.rightMargin: 0

        DropTile {
            id: dropTile
            anchors.fill: parent
        }
    }

    Rectangle {
        id: rectangle
        y: 622
        height: 200
        color: "#f0f0ff"
        border.color: "#4819d4"
        anchors.left: robotPosition.right
        anchors.leftMargin: 0
        anchors.right: parent.right
        anchors.rightMargin: 0
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 0

        Text {
            id: debugTextField
            text: qsTr("Text")
            anchors.fill: parent
            font.pixelSize: 12
        }
    }
}
