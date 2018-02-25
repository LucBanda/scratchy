import QtQuick 2.4
import QtQuick.Controls 1.4
import Scratchy 1.0

Item {
    id: action
    width: 90
    height: 30 + childListRect.height + (programElement.instruction == "Répete"? 10:0)
    property alias childListView: childListView
    property ProgramElement programElement

    property int listIndex: -1
    property bool accepted: false

    signal addAfter(var element)
    signal addInside(var element)

    Drag.active: mouseArea.drag.active
    Drag.dragType: Drag.Automatic

    DropArea {
        id: targetArea
        width: backgroundRect.width
        height: backgroundRect.height
        onDropped: { drag.source.accepted = true; action.addAfter(targetArea.drag.source) }
    }
    DropArea {
        id: insideTargetArea
        width: 0
        height: 0
        onDropped: { drag.source.accepted = true; action.addInside(insideTargetArea.drag.source) }
    }

    MouseArea {
        id: mouseArea
        width: 40
        hoverEnabled: true
        anchors.rightMargin: 35
        anchors.fill: parent
        drag.target:action
        onPressed: {

            parent.grabToImage(function(result) {
                parent.Drag.imageSource = result.url
        })}
    }

    Rectangle {
        id: backgroundRect
        height: 27

        radius: 7
        anchors.topMargin: 3
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.rightMargin: 0
        anchors.left: parent.left
        anchors.leftMargin: 0

        border.color: "#80e142"
        border.width: programElement.executing ? 3 : 0

        Text {
            id: instructionText
            x: 10
            y: 0
            text: qsTr("Avance")
            anchors.topMargin: 0
            anchors.leftMargin: 10
            anchors.fill: parent
            fontSizeMode: Text.Fit
            horizontalAlignment: Text.AlignLeft
            font.pixelSize: 12
        }

        Rectangle {
            id: inputRect
            width: 25
            height: 15
            color: "#ffffff"
            radius: 5
            anchors.right: parent.right
            anchors.rightMargin: 5
            anchors.top: parent.top
            anchors.topMargin: 5

            TextInput {
                id: value
                text: programElement.value
                onTextChanged: if (text) programElement.value = text
                anchors.topMargin: 2
                horizontalAlignment: Text.AlignHCenter
                anchors.fill: parent
                font.pixelSize: 12
            }
        }
    }
    Rectangle {
        id: childListRect
        width:90
        height:childListView.contentHeight
        anchors.right: parent.right
        anchors.top: backgroundRect.bottom
        anchors.left:backgroundRect1.right
        anchors.rightMargin: 0
        anchors.topMargin: 0
        anchors.leftMargin: 0
        visible: true
        color: "transparent"
        ListView {
            id:childListView
            anchors.fill:parent
            height: contentHeight
        }
    }

    Rectangle {
        id: rectangle
        width: 13
        height: 5
        color: backgroundRect.color
        radius: 3
        anchors.left: parent.left
        anchors.leftMargin: 10
        anchors.top: parent.top
        anchors.topMargin: 0
        border.width: 0
    }
    Rectangle {
        id: backgroundRect1
        x: 0
        y: 0
        width: 10
        color: "#00000000"
        radius: 0
        anchors.bottom: backgroundRect2.top
        anchors.bottomMargin: 0
        visible: false
        border.color: "#80e142"
        anchors.topMargin: 0
        anchors.top: backgroundRect.bottom
        border.width: programElement.executing ? 3 : 0
        anchors.leftMargin: 0
        anchors.left: parent.left
    }

    Rectangle {
        id: backgroundRect2
        y: -6
        height: 0
        color: insideTargetArea.containsDrag ? "grey" : backgroundRect.color
        radius: 7
        border.color: "#80e142"
        border.width: programElement.executing ? 3 : 0
        visible: false
        anchors.bottomMargin: 0
        anchors.rightMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 90
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
    }
    states: [
        State {
            name: "Avance"
            when: programElement.instruction == "Avance"

            PropertyChanges {
                target: instructionText
                text: qsTr("Avance")
            }

            PropertyChanges {
                target: backgroundRect
                color: targetArea.containsDrag ? "grey" : "#7034a1"
            }
        },
        State {
            name: "Tourne"
            when: programElement.instruction === "Tourne"

            PropertyChanges {
                target: instructionText
                text: qsTr("Tourne")
                anchors.topMargin: 4
            }

            PropertyChanges {
                target: backgroundRect
                color: targetArea.containsDrag ? "grey" : "#dd9060"
            }
        },
        State {
            name: "Répète"
            when: programElement.instruction === "Répete"
            PropertyChanges {
                target: instructionText
                text: qsTr("Répete")
                anchors.topMargin: 4
            }

            PropertyChanges {
                target: backgroundRect
                color: insideTargetArea.containsDrag ? "grey" : "#c0d6c4"
                radius: 7
                anchors.bottomMargin: 0
            }

            PropertyChanges {
                target: action
                visible: true

            }

            PropertyChanges {
                target: backgroundRect1
                height: 27
                color: backgroundRect.color
                anchors.bottomMargin: -2
                anchors.leftMargin: 0
                anchors.topMargin: -5
                visible: true
            }

            PropertyChanges {
                target: backgroundRect2
                height: 10
                color: targetArea.containsDrag ? "grey" : "#c0d6c4"
                radius: 3
                border.color: backgroundRect.color
                anchors.bottomMargin: 0
                visible: true
            }

            PropertyChanges {
                target: targetArea
                x: backgroundRect2.x
                y: backgroundRect2.y
                width: backgroundRect2.width
                height: backgroundRect2.height
            }

            PropertyChanges {
                target: insideTargetArea
                width: backgroundRect.width
                height: backgroundRect.height
            }
            PropertyChanges {
                target: childListRect
                visible: true
            }

            PropertyChanges {
                target: childListView
                interactive: false
            }

        }
    ]
}
