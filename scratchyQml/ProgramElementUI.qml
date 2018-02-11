import QtQuick 2.4

ProgramElementUIForm {
    id: dragableProgramElement
    Drag.active: mouseArea.drag.active
    Drag.dragType: Drag.Automatic

    MouseArea {
        id: mouseArea
        anchors.fill: parent
        drag.target:dragableProgramElement
    }
}
