import QtQuick 2.0
import Scratchy 1.0

Item {
    property Algorithm algorithm

    Component {
        id:recursableDelegate
        ProgramElementUI {
            id:programElementUi
            property int programElementIndex: index
            programElement: model
            listIndex: programElementIndex

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
                algorithm.addElement(element.programElement.instruction, element.programElement.value, x, y)
            } else {
                algorithm.updateElement(element.listIndex, element.programElement.instruction, element.programElement.value, x, y)
            }
        }

        ListView {
            id: algorithmView
            x: 0
            y: 0
            spacing: -2
            //model:fakeModel
            model: algorithm.elementList
            height: contentHeight
            onModelChanged: {
                if (algorithm.elementList.length > 0) {
                    algorithmView.x = scratchyApp.algorithm.x
                    algorithmView.y = scratchyApp.algorithm.y
                }
            }
            delegate: recursableDelegate
        }
    }
}
