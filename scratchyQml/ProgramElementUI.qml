import QtQuick 2.4

ProgramElementUIForm {
    id: dragableProgramElement

    Drag.active: mouseArea.drag.active
    Drag.dragType: Drag.Automatic

    MouseArea {
        id: mouseArea
        width: 40
        hoverEnabled: true
        anchors.rightMargin: 35
        anchors.fill: parent
        drag.target:dragableProgramElement
    }
}
