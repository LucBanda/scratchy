import QtQuick 2.0

DropArea {
    id: dragTarget

    property alias dropProxy: dragTarget
    signal droppedProxy(var element, int x, int y)
    width: 64; height: 64

    onDropped: {
        /*var component = Qt.createComponent("ProgramElementUI.qml");
        var instance = component.createObject(null, {"instruction": dragTarget.drag.source.instruction,
                                                   "color": dragTarget.drag.source.color,
                                                   "value": dragTarget.drag.source.value,
                                                   "x": dragTarget.drag.x,
                                                   "y": dragTarget.drag.y});*/

        dragTarget.droppedProxy(dragTarget.drag.source, dragTarget.drag.x, dragTarget.drag.y)
    }

    Rectangle {
        id: dropRectangle
        anchors.fill: parent
        color: parent.parent.color
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
