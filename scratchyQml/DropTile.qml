import QtQuick 2.0

DropArea {
    id: dragTarget

    property alias dropProxy: dragTarget
    property alias keys: dragTarget.keys
    property alias color: dropRectangle.color
    property bool disabled: false
    signal droppedProxy(var element, int x, int y)
    width: 64; height: 64
    keys:[]

    onDropped: {
            dragTarget.droppedProxy(dragTarget.drag.source, dragTarget.drag.x, dragTarget.drag.y)
    }

    Rectangle {
        id: dropRectangle
        anchors.fill: parent
        states: [
            State {
                when: dragTarget.containsDrag && !disabled
                PropertyChanges {
                    target: dropRectangle
                    color: "lightgrey"
                }
            }
        ]
    }
}
