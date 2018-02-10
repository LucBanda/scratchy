import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.1

Item {
    id: item1
    width: 1024
    height: 800
    property alias debugTextField: debugTextField
    property alias loopButton: loopButton
    property alias turnButton: turnButton
    property alias moveButton: moveButton
    property alias algorithmGroupBox: algorithmGroupBox
    property alias actionGroupBox: actionGroupBox

    GroupBox {
        id: actionGroupBox
        width: 100
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

        Button {
            id: moveButton
            x: 4
            y: 10
            text: qsTr("Move")
        }

        Button {
            id: turnButton
            x: 4
            y: 44
            text: qsTr("Turn")
        }

        Button {
            id: loopButton
            x: 4
            y: 78
            text: qsTr("Loop")
        }
    }

    Rectangle {
        id: robotPosition
        color: "#ffffff"
        border.width: 5
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
        color: "#d4d4d4"
        anchors.left: actionGroupBox.right
        anchors.leftMargin: 0
        anchors.bottom: rectangle.top
        anchors.bottomMargin: 0
        anchors.top: parent.top
        anchors.topMargin: 0
        anchors.right: parent.right
        anchors.rightMargin: 0
    }

    Rectangle {
        id: rectangle
        y: 622
        height: 200
        color: "#ffffff"
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
