import QtQuick 2.4

Item {
    id: action
    width: 90
    height: 30
    property alias backgroundRectColor: backgroundRect.color
    property alias value: value.text
    property string instruction: "Avance"
    property int listIndex: -1
    property bool executing: false
    property bool selected: false

    Rectangle {
        id: backgroundRect

        radius: 7
        anchors.topMargin: 3
        anchors.fill: parent

        border.color: "#80e142"
        border.width: executing ? 3 : 0

        Text {
            id: instructionText
            x: 10
            y: 0
            text: qsTr("Avance")
            anchors.topMargin: 0
            anchors.leftMargin: 10
            verticalAlignment: Text.AlignVCenter
            anchors.fill: parent
            fontSizeMode: Text.Fit
            horizontalAlignment: Text.AlignLeft
            font.pixelSize: 12
        }

        Rectangle {
            id: inputRect
            width: 25
            color: "#ffffff"
            radius: 5
            anchors.right: parent.right
            anchors.rightMargin: 5
            anchors.top: parent.top
            anchors.topMargin: 5
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 5

            TextInput {
                id: value
                text: qsTr("1")
                anchors.topMargin: 2
                horizontalAlignment: Text.AlignHCenter
                anchors.fill: parent
                font.pixelSize: 12
            }
        }
    }

    Rectangle {
        id: rectangle
        width: 13
        height: 5
        color: backgroundRect.color
        radius: 3
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 22
        anchors.left: parent.left
        anchors.leftMargin: 10
        anchors.top: parent.top
        anchors.topMargin: 0
        border.width: 0
    }
    states: [
        State {
            name: "Avance"
            when: instruction == "Avance"

            PropertyChanges {
                target: instructionText
                text: qsTr("Avance")
            }

            PropertyChanges {
                target: backgroundRect
                color: selected ? "grey" : "#7034a1"
            }

            PropertyChanges {
                target: value
                text: qsTr("1")
            }
        },
        State {
            name: "Tourne"
            when: instruction === "Tourne"

            PropertyChanges {
                target: instructionText
                text: qsTr("Tourne")
            }

            PropertyChanges {
                target: backgroundRect
                color: selected ? "grey" : "#dd9060"
            }

            PropertyChanges {
                target: value
                text: qsTr("90")
            }
        },
        State {
            name: "Répète"
            when: instruction === "Répete"
            PropertyChanges {
                target: instructionText
                text: qsTr("Répete")
            }

            PropertyChanges {
                target: backgroundRect
                color: selected ? "grey" : "#21c24c"
            }

            PropertyChanges {
                target: value
                text: qsTr("2")
            }
        }
    ]
}
