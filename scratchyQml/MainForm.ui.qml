import QtQuick 2.5
import QtQuick.Controls 1.4
import QtQuick.Layouts 1.1

Item {
    id: item1
    width: 1024
    height: 800
    property alias algorithmView: algorithmView
    property alias algorithmDropTile: algorithmDropTile
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
            anchors.left: parent.left
            anchors.leftMargin: 2
            anchors.top: defaultAvance.bottom
            anchors.topMargin: 15
            value: "90"
            instruction: "Tourne"
        }

        ProgramElementUI {
            id: defaultLoop
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
            id: algorithmDropTile
            anchors.fill: parent

            ListView {
                id: algorithmView
                x: 0
                y: 0
                width: 110
                height: 160
                boundsBehavior: Flickable.StopAtBounds
                spacing: 2
                delegate: Item {
                    x: 5
                    width: 80
                    height: 40
                    Row {
                        id: row1
                        Rectangle {
                            width: 40
                            height: 40
                            color: colorCode
                        }

                        Text {
                            text: name
                            anchors.verticalCenter: parent.verticalCenter
                            font.bold: true
                        }
                        spacing: 10
                    }
                }
                model: ListModel {
                    ListElement {
                        name: "Grey"
                        colorCode: "grey"
                    }

                    ListElement {
                        name: "Red"
                        colorCode: "red"
                    }

                    ListElement {
                        name: "Blue"
                        colorCode: "blue"
                    }

                    ListElement {
                        name: "Green"
                        colorCode: "green"
                    }
                }
            }
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
