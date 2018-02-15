import QtQuick 2.4
import QtQuick.Controls 1.4

Item {
    id: debugToolBar
    width: 300
    height: 50
    property alias playButton: playButton

    Rectangle {
        id: rectangle
        visible: true
        gradient: Gradient {
            GradientStop {
                position: 0
                color: "#c5e25d"
            }

            GradientStop {
                position: 1
                color: "#4d5d14"
            }
        }
        anchors.fill: parent

        Rectangle {
            id: rectangle1
            x: 30
            width: 50
            height: 50
            color: "#9a9f37"
            visible: parent.visible
            anchors.top: parent.top
            anchors.topMargin: 0

            MouseArea {
                id: playButton
                visible: parent.visible
                anchors.fill: parent

                Image {
                    id: image
                    width: 30
                    height: 30
                    visible: parent.visible
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.verticalCenter: parent.verticalCenter
                    source: "Play_groen.png"
                }
            }
        }
    }
}
