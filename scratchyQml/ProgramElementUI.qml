import QtQuick 2.4

Item {
    id: root
    property alias instruction: dragableProgramElement.instruction
    property alias value: dragableProgramElement.value
    property alias listIndex: dragableProgramElement.listIndex
    property alias executing: dragableProgramElement.executing
    property alias selected: dragableProgramElement.selected

    width: dragableProgramElement.width
    height: dragableProgramElement.height

    ProgramElementUIForm {
        id: dragableProgramElement
        anchors.fill: parent
        property int listIndex: -1
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
}
