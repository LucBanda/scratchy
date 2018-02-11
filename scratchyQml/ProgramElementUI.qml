import QtQuick 2.4

Item {
    id: root
    property alias color: form.backgroundRect
    property alias instruction: form.instruction
    property alias value: form.value
    width: 90
    height: 30

    Rectangle {
        property alias color: form.backgroundRect
        property alias instruction: form.instruction
        property alias value: form.value
        property alias mouseX: mouseArea.mouseX
        property alias mouseY: mouseArea.mouseX

        width: 90
        height: 30

        id:rectangleToDrag

        anchors.fill: parent
        Drag.active: mouseArea.drag.active
        Drag.dragType: Drag.Automatic
        Drag.hotSpot.x: 32
        Drag.hotSpot.y: 32
        states: State {
            when: mouseArea.drag.active
            ParentChange { target: rectangleToDrag; parent: root }
            AnchorChanges { target: rectangleToDrag; anchors.verticalCenter: undefined; anchors.horizontalCenter: undefined }
        }

        ProgramElementUIForm {
            id: form
            MouseArea {
                id: mouseArea
                anchors.fill: parent
                drag.target:rectangleToDrag
                onReleased: console.log("Dragged " + rectangleToDrag.parent + rectangleToDrag.Drag.target)
            }

            anchors.fill: parent
        }
    }
}
