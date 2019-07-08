import visa
from autobench import log
import sys


class Switch(object):
    # A class that defines and controls Agilent 34890A switch.

    def __init__(self, TCP_IP_address):
        """
        Initiate Agilent 34890A switch interface and set timeout timing.
        :rtype None
        """
        self.log = log(self.__class__.__name__)
        try:
            self.switch = visa.ResourceManager().open_resource("TCPIP::" + TCP_IP_address +'::INSTR')
            self.log.info('Switch opens successfully.')
        except visa.Error:
            self.log.error('Switch fails to open.', exc_info=True)
            sys.exit("I/O Error")
        self.switch.timeout = 10000

    def switch_open(self, channels):
        """
        This command is to open the given channel or channels.
        :param channels: input channels to open, eg, (@1101), (@1103, 1104), (@2304:2615,1911), type: str
        :return: None
        """
        self.switch.write('ROUTe:OPEN %s' % channels)

    def switch_close(self, channels):
        """
        This command is to close the given channel or channels.
        :param channels: input channels to close, eg, (@1101), (@1103, 1104), (@2304:2615,1911), type: str
        :return: None
        """
        self.switch.write('ROUTe:CLOSe %s' % channels)