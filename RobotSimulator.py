#!/usr/bin/env python3

import sys, logging
import optparse
import threading
import math

# FIXME
sys.path.append("./libpomp/python")
import pomp


ROBOT_PROTOCOL_VERSION = 1

ROBOT_EVT_IDENT = 1
ROBOT_EVT_TELEMETRY = 2
ROBOT_MSG_INSTRUCTION = 3

ROBOT_EVT_FORMAT_TELEMETRY = "%f%f%f%f%f%f"   # x, y, cap, vx, vy, vang
ROBOT_MSG_FORMAT_INSTRUCTION = "%s%f"       # instruction: value


SAMPLE_RATE = 200 * 1000    # Samples every 200ms

#===============================================================================
#===============================================================================
_USAGE = (
    "usage: %prog [<options>] <ctrladdr>\n"
    "Connect to a ishtar server\n"
    "\n"
    "  <options>: see below\n"
    "  <ctrladdr> : control address\n"
    "  <dataport> : data port\n"
    "\n"
    "<ctrladdr> format:\n"
    "  inet:<addr>:<port>\n"
    "  inet6:<addr>:<port>\n"
    "  unix:<path>\n"
    "  unix:@<name>\n"
)

#===============================================================================
#===============================================================================
class RobotController(pomp.EventHandler):
    def __init__(self, addr):
        self.pompCtx = pomp.Context(self)
        (family, addr) = pomp.parseAddr(addr)
        self.pompCtx.listen(family, addr)
        self.timerHandler = pomp.looper.Handler(self.onTimer)
        self.timer = None
        self.x = 0.0
        self.y = 0.0
        self.cap = 0.0
        self.vy = 0.0
        self.vx = 0.0
        self.vang = 0.0
        self.avanceLeftIter = -1
        self.tourneLeftIter = -1
        self.shouldLoopStatus = False

    def stop(self):
        self.pompCtx.stop()

    def onConnected(self, ctx, conn):
        # Send connection request
        logging.info("Connected")
        self.shouldLoopStatus = True
        self.setupTimer()

    def onDisconnected(self, ctx, conn):
        # Clear internal state
        logging.info("Disconnected")
        self.shouldLoopStatus = False
        self.cancelTimer()

    def recvMessage(self, ctx, conn, msg):
        if msg.msgid == ROBOT_MSG_INSTRUCTION:
            (instruction, value) = msg.read(ROBOT_MSG_FORMAT_INSTRUCTION)
            if instruction == "Avance":
                self.avance(value)
            if instruction == "Tourne":
                self.tourne(value)


    def avance(self, distance):
        self.vx = math.sin(self.cap)
        self.vy = math.cos(self.cap)
        self.avanceLeftIter = distance * 10.0 + 1

    def tourne(self, angle):
        self.vang =  math.radians(30)
        self.tourneLeftIter = math.radians(angle) * 10.0 / self.vang


    def setupTimer(self):
        assert self.timer is None
        self.timer = threading.Timer(0.1, self.timerHandler.post, [None])
        self.timer.start()

    def cancelTimer(self):
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

    def onTimer(self, req):
        if self.avanceLeftIter > 0:
            self.avanceLeftIter -= 1
            if self.avanceLeftIter <= 0:
                self.vx = 0.0
                self.vy = 0.0
        if self.tourneLeftIter > 0:
            self.tourneLeftIter -= 1.0
            if self.tourneLeftIter < 0:
                self.vang = 0.0

        self.cap += self.vang / 10.0
        self.x += self.vx / 10.0
        self.y += self.vy / 10.0
        self.pompCtx.send(ROBOT_EVT_TELEMETRY, ROBOT_EVT_FORMAT_TELEMETRY, self.x, self.y, self.cap, self.vx, self.vy, self.vang)
        if self.shouldLoopStatus:
            self.timer = None
            self.setupTimer()

#===============================================================================
#===============================================================================
def main():
    (options, args) = parseArgs()
    setupLog(options)

    try:
        pomp.looper.prepareLoop()
        robot = RobotController(args[0])
        while (True):
            pomp.looper.stepLoop()
        robot.stop()
    except KeyboardInterrupt:
        pomp.looper.exitLoop()
    sys.exit(0)

#===============================================================================
#===============================================================================
def parseArgs():
    # Setup parser
    parser = optparse.OptionParser(usage=_USAGE)

    parser.add_option("-q", "--quiet",
        dest="quiet",
        action="store_true",
        default=False,
        help="be quiet")

    parser.add_option("-v", "--verbose",
        dest="verbose",
        action="store_true",
        default=False,
        help="verbose output")

    # Parse arguments
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("Bad number or arguments")
    return (options, args)

#===============================================================================
#===============================================================================
def setupLog(options):
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s][%(asctime)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stderr)
    logging.addLevelName(logging.CRITICAL, "C")
    logging.addLevelName(logging.ERROR, "E")
    logging.addLevelName(logging.WARNING, "W")
    logging.addLevelName(logging.INFO, "I")
    logging.addLevelName(logging.DEBUG, "D")

    # Setup log level
    if options.quiet == True:
        logging.getLogger().setLevel(logging.CRITICAL)
    elif options.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

#===============================================================================
#===============================================================================
if __name__ == "__main__":
    main()
