import QtQuick 2.4
import QtQuick.Extras 1.4

Item {
    width: 200
    height: 200

    Image {
        id: image
        clip: true
        fillMode: Image.PreserveAspectFit
        anchors.fill: parent
        source: "robot.png"
    }
}
