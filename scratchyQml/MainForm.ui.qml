import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.1

Item {
    id: item1
    width: 1024
    height: 800
    property alias debugTextField: debugTextField
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

        ProgramElementUI {
            id: defaultAvance
            anchors.left: parent.left
            anchors.leftMargin: -8
        }

        ProgramElementUI {
            id: defaultTourne
            y: 4
            color: "#dd9060"
            anchors.left: parent.left
            anchors.leftMargin: -8
            value: "90"
            instruction: "Tourne"
            anchors.verticalCenterOffset: 40
            anchors.verticalCenter: defaultAvance.verticalCenter
        }

        ProgramElementUI {
            id: defaultLoop
            color: "#21c24c"
            anchors.left: parent.left
            anchors.leftMargin: -8
            anchors.top: defaultTourne.bottom
            anchors.topMargin: 40
            value: "2"
            instruction: "Répete"
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
