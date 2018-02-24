import QtQuick 2.4
import QtQuick.Controls 1.4
import Scratchy 1.0

Item {
    id: debugToolBar
    property RobotController robotController
    property Debugger scratchyDebugger

    width: 250
    height: 50

    Rectangle {
        id: rectangle
        color: "#bad9e5"
        radius: 20
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.rightMargin: 0
        visible: parent.visible

        Image {
            id: play
            y: 8
            width: 35
            height: 35
            anchors.left: parent.left
            anchors.leftMargin: 20
            anchors.verticalCenter: parent.verticalCenter
            source: "play.png"
            MouseArea {
                id: playButton
                visible: parent.visible
                anchors.fill: parent
                onClicked: scratchyDebugger.start()
            }
        }

        Image {
            id: pause
            y: 7
            width: 35
            height: 35
            anchors.left: step.right
            anchors.leftMargin: 20
            anchors.verticalCenter: parent.verticalCenter
            source: "pause.png"
            MouseArea {
                id: pauseButton
                visible: parent.visible
                anchors.fill: parent
                onClicked: scratchyDebugger.pause = true
            }
        }

        Image {
            id: stop
            y: 8
            width: 35
            height: 35
            anchors.left: pause.right
            anchors.leftMargin: 20
            anchors.verticalCenter: parent.verticalCenter
            source: "stop.png"
            MouseArea {
                id: stopButton
                visible: parent.visible
                anchors.fill: parent
                onClicked: scratchyDebugger.stop = true
            }
        }

        Image {
            id: step
            x: 76
            y: 7
            width: 35
            height: 35
            anchors.left: play.right
            anchors.leftMargin: 20
            anchors.verticalCenter: parent.verticalCenter
            source: "step.png"
            MouseArea {
                id: stepButton
                visible: parent.visible
                anchors.fill: parent
                onClicked: scratchyDebugger.step()
            }
        }
    }
}
