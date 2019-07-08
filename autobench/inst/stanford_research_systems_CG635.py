from .gpib import GPIB


class CG635(GPIB):
    """GPIB Control of Stanford research systems CG635."""

    def __init__(self, CG635_gpib_addr=23):
        super(CG635, self).__init__(CG635_gpib_addr, "CG635")

    def cmos_output(self, low_voltage, high_voltage):
        """
        This command is used to set voltage level of CMOS outputs.
        :param low_voltage: CMOS low voltage, type: float
        :param high_voltage: CMOS high voltage, type: float
        :return: None
        """
        self.write('CMOS 0, %s' % low_voltage)
        self.write('CMOS 1, %s' % high_voltage)

    def Q_output(self, low_voltage, high_voltage):
        """
        This command is used to set voltage level of Q outputs.
        :param low_voltage: Q output low voltage, type: float
        :param high_voltage: Q output high voltage, type: float
        :return: None
        """
        self.write('QOUT 0, %s' % low_voltage)
        self.write('QOUT 1, %s' % high_voltage)

    def standard_cmos(self, standard_level):
        """
        This command is used to choose the standard CMOS output level.
        :param standard_level: 0 (1.2V standard CMOS level), type: int
                               1 (1.8V standard CMOS level), type: int
                               2 (2.5V standard CMOS level), type: int
                               3 (3.3V standard CMOS level), type: int
                               4 (5.0V standard CMOS level), type: int
        :return: None
        """
        self.write('STDC %s' % standard_level)

    def standard_Q(self, standard_level):
        """
        This command is used to choose the standard Q output level.
        :param standard_level: 0 ECL levels , type: int
                               1 +7 dBm levels , type: int
                               2 LVDS levels , type: int
                               3 PECL 3.3 V levels , type: int
                               4 PECL 5.0 V levels , type: int
        :return: None
        """
        self.write('STDQ %s' % standard_level)

    def frequency(self, frequency):
        """
        This command is used to set the frequency of the instrument.
        :param frequency: Frequency of the instrument, type: float
        :return: None
        """
        self.write('FREQ %s' % frequency)

    def phase(self, phase):
        """
        This command is used to set the frequency of the instrument.
        :param phase: phase of the instrument, type: float
        :return: None
        """
        self.write('PHAS %s' % phase)

    def run(self, run_state):
        """
        This command is used to set the running state of outputs.
        :param run_state: 0(stop) or 1(run), type: int
        :return: none
        """
        self.write('RUNS %s' % run_state)

    def show_display(self, display_state):
        """
        This command is used to set the current state of the display.
        :param display_state: 0 (display off), type: int
                              1 (display on), type: int
        :return: None
        """
        self.write('SHDP %s' % display_state)

    def stop_level(self, stop_state):
        """
        This command is used to set the level at the output in the stopped state.
        :param stop_state: 0 (stop level low), type: int
                           1 (stop level high), type: int
                           2 (stop level toggled), type: int
        :return:
        """
        self.write('SLVL %s' % stop_state)
