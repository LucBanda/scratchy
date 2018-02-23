import QtQuick 2.4
import QtQuick.Extras 1.4
import Scratchy 1.0

Item {
    property RobotController robotController
    property int origX: 0
    property int origY: 0
    width: 30
    height: 30
    x: origX +  robotController.xRobot*2
    y: origY - robotController.yRobot*2

    Rotation {
        id: rotation
        origin.x: robot.width/2
        origin.y: robot.height/2
        angle: robotController.capRobot
    }

    Image {
        id: image
        clip: true
        fillMode: Image.PreserveAspectFit
        anchors.fill: parent
        source: "robot.png"
        transform: rotation
    }
}
