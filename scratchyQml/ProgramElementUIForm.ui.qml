import QtQuick 2.4

Item {
    id: action
    width: 90
    height: 30
    property alias instruction: instruction.text
    property alias value: value.text
    property int listIndex: -1

    Rectangle {
        id: backgroundRect
        color: instruction.text == "Avance" ? "#7034a1" : instruction.text
                                              == "Tourne" ? "#dd9060" : instruction.text
                                                            == "Répete" ? "#21c24c" : "#000000"
        radius: 7
        anchors.topMargin: 3
        anchors.fill: parent

        Text {
            id: instruction
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
                text: qsTr("1.0")
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
    }
}
