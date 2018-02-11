import QtQuick 2.0

DropArea {
    id: dragTarget

    property alias dropProxy: dragTarget

    width: 64; height: 64

    onDropped: {
        console.log("dropped " + dragTarget.parent)
        //dragTarget.drag.source.parent.parent = dragTarget.parent
        var component = Qt.createComponent("ProgramElementUI.qml");
        component.createObject(dragTarget.parent, {"instruction": dragTarget.drag.source.instruction,
                                                   "color": dragTarget.drag.source.color,
                                                   "value": dragTarget.drag.source.value,
                                                   "x": dragTarget.drag.x,
                                                   "y": dragTarget.drag.y});


    }
    MouseArea {
        id: targetMouseArea
        anchors.fill: parent
    }

    Rectangle {
        id: dropRectangle

        anchors.fill: parent

        states: [
            State {
                when: dragTarget.containsDrag
                PropertyChanges {
                    target: dropRectangle
                    color: "grey"
                }
            }
        ]
    }
}
