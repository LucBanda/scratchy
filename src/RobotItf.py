import sys
# FIXME
sys.path.append("./libpomp/python")
import pomp

ROBOT_EVT_TELEMETRY = 1
ROBOT_MSG_INSTRUCTION = 2

ROBOT_EVT_FORMAT_TELEMETRY = "%f%f%f%f%f%f"   # x, y, cap, vx, vy, vang
ROBOT_MSG_FORMAT_INSTRUCTION = "%s%f"       # instruction: value

class RobotItf(pomp.EventHandler):
    LOCAL_POMP_ADDRESS = "inet:127.0.0.1:5000"

    def __init__(self, addrString, role="server"):
        (family, addr) = pomp.parseAddr(addrString)
        self.pompCtx = pomp.Context(self)
        self.role = role
        if self.role == "server":
            self.pompCtx.listen(family, addr)
        elif self.role == "udp":
            self.pompCtx.bind(family, addr)
        else:
            self.pompCtx.connect(family, addr)

    def recvMessage(self, ctx, conn, msg):
        if msg.msgid == ROBOT_MSG_INSTRUCTION:
            (instruction, value) = msg.read(ROBOT_MSG_FORMAT_INSTRUCTION)
            self.onInstructionReceived(instruction, value)
        if msg.msgid == ROBOT_EVT_TELEMETRY:
            (x, y, cap, vx, vy, vang) = msg.read(ROBOT_EVT_FORMAT_TELEMETRY)
            self.onStateReceived(x, y, cap, vx, vy, vang)

    def stop(self):
        self.pompCtx.stop()

    def onConnected(self, ctx, conn):
        pass

    def onDisconnected(self, ctx, conn):
        pass

    def onStateReceived(self, x, y, cap, vx, vy, vang):
        pass

    def onInstructionReceived(self, instruction, value):
        pass

    def sendState(self, x, y, cap, vx, vy, vang):
        self.pompCtx.send(ROBOT_EVT_TELEMETRY, ROBOT_EVT_FORMAT_TELEMETRY, x, y, cap, vx, vy, vang)

    def sendInstruction(self, instruction, value):
        self.pompCtx.send(ROBOT_MSG_INSTRUCTION, ROBOT_MSG_FORMAT_INSTRUCTION, instruction, value)
