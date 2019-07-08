import pyvisa
import time
from autobench import log
import logging
import sys


class GPIB(object):
    """MMT GPIB Control"""

    def __init__(self, gpib_addr, instr_name=""):
        self.addr = gpib_addr
        self.name = instr_name
        self.log = log(self.__class__.__name__)
        try:
            self.inst = pyvisa.ResourceManager().open_resource("GPIB0::" + str(gpib_addr) + '::INSTR')
            self.inst.timeout = 50000
            self.logger("Device Opened")
        except pyvisa.Error:
            self.logger("GPIB Failed to Open", lvl=3)
            sys.exit("GPIB Failed VISA Error")

    def write(self, command):
        self.inst.write(command)

    def query(self, command):
        return self.inst.query(command)

    def ask(self, command):
        return self.inst.ask(command)

    def read(self):
        return self.inst.read()

    def clear(self):
        self.inst.write("*CLS")

    def logger(self, message, lvl=1):
        """
        GPIB Logger
        :param message: Log Message
        :param lvl: 0:DEBUG 1:INFO 2:WARN 3:ERROR
        """
        if self.name:
            if lvl == 0:
                self.log.debug("[GPIB:" + str(self.addr) + "] __" + self.name + "__:" + message)
            elif lvl == 1:
                self.log.info("[GPIB:" + str(self.addr) + "] __" + self.name + "__:" + message)
            elif lvl == 2:
                self.log.warning("[GPIB:" + str(self.addr) + "] __" + self.name + "__:" + message)
            elif lvl == 3:
                self.log.error("[GPIB:" + str(self.addr) + "] __" + self.name + "__:" + message, exc_info=True)
        else:
            if lvl == 0:
                self.log.debug("[GPIB:" + str(self.addr) + "]: " + message)
            elif lvl == 1:
                self.log.info("[GPIB:" + str(self.addr) + "]: " + message)
            elif lvl == 2:
                self.log.warning("[GPIB:" + str(self.addr) + "]: " + message)
            elif lvl == 3:
                self.log.error("[GPIB:" + str(self.addr) + "]: " + message, exc_info=True)

    def close(self):
        self.inst.close()

