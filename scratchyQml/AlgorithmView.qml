import QtQuick 2.0
import Scratchy 1.0

Item {
    property Algorithm algorithm

    Component {
        id:recursableDelegate
        ProgramElementUI {
            id:programElementUi
            programElement: model.context
            listIndex: index

            onAddAfter: { model.context.addAfter(index, element.programElement.instruction, element.programElement.value, x, y) }
            onAddInside: { model.context.addElementAtIndex(0, element.programElement.instruction, element.programElement.value, x, y) }
            childListView.model: model.childs
            childListView.delegate: recursableDelegate
        }
    }

    DropTile {
        id: algorithmDropTile
        color: "#fffcee"
        anchors.fill: parent

        onDroppedProxy: {
            if (element.listIndex === -1) {
                if (algorithm.functionList.length > 0) {
                    algorithm.addElementToFunction("func"+algorithm.functionList.length, element.programElement.instruction, element.programElement.value, x, y)
                } else {
                    algorithm.addElementToFunction("main", element.programElement.instruction, element.programElement.value, x, y)
                }
            } else {
                algorithm.updateFunction(element.listIndex, element.programElement.instruction, element.programElement.value, x, y)
            }
        }

        Repeater{
            id: algorithmView
            model: algorithm.functionList

            ListView {
                id:functionView
                x: modelData.x
                y: modelData.y
                spacing: -2
                model: elementList
                height: contentHeight
                delegate: recursableDelegate
            }
        }
    }
}
