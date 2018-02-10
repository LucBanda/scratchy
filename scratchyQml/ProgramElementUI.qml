import QtQuick 2.4

Item {
    id: actionWrapper
    property alias color: form.backgroundRect
    property alias instruction: form.instruction
    property alias value: form.value

    ProgramElementUIForm {
        id: form
    }
}
