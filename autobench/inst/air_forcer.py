from .gpib import GPIB
from autobench import log
import time

class Air_forcer(GPIB):
    # A class that defines and controls air_forcer.

    def __init__(self, gpib_addr=10):
        """
        Initiate Agilent 81130A GPIB interface
        :param gpib_addr: GPIB address, no need for the full resource name, type: int
        :rtype None
        """
        super(self.__class__, self).__init__(gpib_addr, 'Air_forcer')

    def set_temperature(self, set_point):
        """
        This command is used to set the working temperature
        :param set_point:the temperature (-75 to 225), type: float
        :return: None
        """
        self.write('SP%s' % set_point)

    def requery_set_temperature(self):
        """
        This command is used to request the systems current temperature setpoint.
        :rtype: str
        """
        return self.query('?SP')

    def request_DUT_temperature(self):
        """
        This command is used to requset DUT temperature (Exact when the DUT temperature turns off/disable manually,
        it reads the last valid DUT temperature).
        :rtype: str
        """
        return self.query('?TD')

    def halt_the_program(self):
        """
        This command is used to halt the program
        :return: None
        """
        self.write('HL')

    def contine_the_program(self):
        """
        This command is used to continue the program
        :return: None
        """
        self.write('CN')

    def temperature_set(self, set_point):
        while self.request_DUT_temperature()!= set_point:
            continue
        time.sleep(10)