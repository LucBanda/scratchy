#!/usr/bin/env python3

import logging
import math
import optparse
import sys
import threading

from RobotItf import RobotItf

# FIXME
sys.path.append("./libpomp/python")
import pomp

#===============================================================================
#===============================================================================
class RobotSimulator(RobotItf):
    STATE_DECIMATION = 1
    def __init__(self, addrString):
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
        self.currentInstruction = ("", 0)
        self.decimator = self.STATE_DECIMATION
        RobotItf.__init__(self, addrString, "server")

    def destroy(self):
        self.cancelTimer()
        self.stop()

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

    def onInstructionReceived(self, instruction, value):
        self.currentInstruction = (instruction,value)
        logging.debug(instruction, value)
        if (instruction == "Avance"):
            self.vx = value * math.sin(self.cap)
            self.vy = value * math.cos(self.cap)
            logging.debug(self.vx, self.vy)
            self.avanceLeftIter = abs(value) * 10.0
        elif (instruction == "Tourne"):
            self.vang =  math.radians(30)
            self.tourneLeftIter = math.radians(value) * 10.0 / self.vang

    def setupTimer(self):
        self.timer = None
        self.timer = threading.Timer(0.1, self.timerHandler.post, [None])
        self.timer.start()

    def cancelTimer(self):
        if self.timer is not None:
            self.timer.cancel()
            self.timer = None

    def onTimer(self, req):
        if self.avanceLeftIter >= 0:
            self.avanceLeftIter -= 1
            if self.avanceLeftIter < 0:
                self.vx = 0.0
                self.vy = 0.0
                self.sendInstruction(self.currentInstruction[0], self.currentInstruction[1])

        if self.tourneLeftIter >= 0:
            self.tourneLeftIter -= 1.0
            if self.tourneLeftIter < 0:
                self.vang = 0.0
                self.sendInstruction(self.currentInstruction[0], self.currentInstruction[1])

        self.cap += self.vang / 10.0
        self.x += self.vx / 10.0
        self.y += self.vy / 10.0
        if self.decimator == 0:
            self.decimator = self.STATE_DECIMATION
            logging.debug("%f %f %f %f %f %f", self.x, self.y, self.cap, self.vx, self.vy, self.vang)
            self.sendState(self.x, self.y, math.degrees(self.cap), self.vx, self.vy, math.degrees(self.vang))
        self.decimator -= 1
        if self.shouldLoopStatus:
            self.timer = None
            self.setupTimer()

# ===============================================================================
# ===============================================================================
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
def main():
    (options, args) = parseArgs()
    setupLog(options)

    try:
        pomp.looper.prepareLoop()
        robot = RobotSimulator(args[0])
        while (True):
            pomp.looper.stepLoop()
    except KeyboardInterrupt:
        robot.destroy()
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
