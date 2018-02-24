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
                visible: !shaderPlay.visible
                anchors.fill: parent
                onClicked: scratchyDebugger.start()
            }

            Rectangle {
                id: shaderPlay
                color: "#66ffffff"
                radius: 18
                visible: false
                anchors.fill: parent
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
                visible: !shaderPause.visible
                anchors.fill: parent
                onClicked: scratchyDebugger.pause()
            }

            Rectangle {
                id: shaderPause
                color: "#66ffffff"
                radius: 18
                visible: false
                anchors.fill: parent
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
                visible: !shaderStop.visible
                anchors.fill: parent
                onClicked: scratchyDebugger.stop()
            }

            Rectangle {
                id: shaderStop
                x: 2
                y: -9
                color: "#66ffffff"
                radius: 18
                anchors.fill: parent
                visible: false
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
                visible: !shaderStep.visible
                anchors.fill: parent
                onClicked: scratchyDebugger.step()
            }

            Rectangle {
                id: shaderStep
                x: 9
                y: 2
                color: "#66ffffff"
                radius: 18
                anchors.fill: parent
                visible: false
            }
        }
    }
    states: [
        State {
            name: "pending"
            when: scratchyDebugger.pending

            PropertyChanges {
                target: shaderPlay
                visible: true
            }

            PropertyChanges {
                target: shaderPause
                visible: false
            }

            PropertyChanges {
                target: shaderStop
                visible: true
            }

            PropertyChanges {
                target: shaderStep
                visible: true
            }

            PropertyChanges {
                target: playButton
                visible: !shaderPlay.visible
            }

            PropertyChanges {
                target: pauseButton
                visible: !shaderPause.visible
            }
        },
        State {
            name: "playing"
            when: scratchyDebugger.play && !scratchyDebugger.pending

            PropertyChanges {
                target: shaderPlay
                visible: true
            }

            PropertyChanges {
                target: shaderPause
                visible: false
            }

            PropertyChanges {
                target: shaderStop
                visible: false
            }

            PropertyChanges {
                target: shaderStep
                visible: true
            }
        },
        State {
            name: "paused"
            when: scratchyDebugger.paused && !scratchyDebugger.pending

            PropertyChanges {
                target: shaderPlay
                visible: false
            }

            PropertyChanges {
                target: shaderPause
                visible: true
            }

            PropertyChanges {
                target: shaderStop
                visible: false
            }

            PropertyChanges {
                target: shaderStep
                visible: false
            }
        },
        State {
            name: "Stopped"
            when: scratchyDebugger.stopped && !scratchyDebugger.pending

            PropertyChanges {
                target: shaderPause
                visible: true
            }

            PropertyChanges {
                target: shaderStop
                visible: true
            }
        }
    ]
}
