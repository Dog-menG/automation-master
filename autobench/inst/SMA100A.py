from .gpib import GPIB


class SMA100A(GPIB):
    # A class that defines and controls SMA100A function generator.

    def __init__(self, gpib_addr):
        """
        Initiate SMA100A GPIB interface
        :param gpib_addr: GPIB address, no need for the full resource name, type: int
        :rtype None
        """
        super(self.__class__, self).__init__(gpib_addr, 'SMA100A')

    def rf_frequency(self, frequency):
        """
        This command is used to set rf output frequency
        :param frequency: rf output frequency, type: str
        :rtype None
        """
        self.write(':SOURce:FREQuency %s' % frequency)

    def rf_output_level(self, level):
        """
        This command is used to set rf output level
        :param level: rf output level, type: int
        :rtype None
        """
        self.write(':SOURce:POWer %s' % level)

    def clk_synthesis_frequency(self, frequency):
        """
        This command is used to set clock synthesis frequency
        :param frequency: synthesis output frequency, type: str
        :rtype None
        """
        self.write(':CSYNthesis:FREQuency %s' % frequency)

    def clk_synthesis_offset(self, offset):
        """
        This command is used to set clock synthesis offset
        :param frequency: synthesis output frequency, type: str
        :rtype None
        """
        self.write(':CSYNthesis:OFFset %s' % offset)

    def rf_out_state(self, state):
        """
        This command is used to set rf output state
        :param state: rf output state, type: int
        :rtype None
        """
        self.write(':OUTPut %s' % state)

    def clk_synthesis_state(self, state):
        """
        This command is used to set clock synthesis output state
        :param state: rf output state, type: int
        :rtype None
        """
        self.write(':CSYNthesis:STATe %s' % state)

    def clk_synthesis_offset_state(self, offset_state):
        """
        This command is used to set clock synthesis offset output state
        :param state: rf output state, type: int
        :rtype None
        """
        self.write(':CSYNthesis:OFFSet:STATe %s' % offset_state)