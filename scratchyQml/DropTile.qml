import QtQuick 2.0

DropArea {
    id: dragTarget

    property alias dropProxy: dragTarget
    property alias color: dropRectangle.color
    signal droppedProxy(var element, int x, int y)
    width: 64; height: 64

    onDropped: {
        if (!dragTarget.drag.source.accepted) {
            dragTarget.droppedProxy(dragTarget.drag.source, dragTarget.drag.x, dragTarget.drag.y)
        }
    }

    Rectangle {
        id: dropRectangle
        anchors.fill: parent
        states: [
            State {
                when: dragTarget.containsDrag
                PropertyChanges {
                    target: dropRectangle
                    color: "lightgrey"
                }
            }
        ]
    }
}
