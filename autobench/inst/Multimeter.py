from .gpib import GPIB


class Multimeter(GPIB):

    def __init__(self, gpib_addr):
        """
        Child class of GPIB
        :param gpib_addr: GPIB Address, type: int
        :rtype None
        """
        super(Multimeter, self).__init__(gpib_addr, "Multimeter")

    def filter(self, bandwidth):
        """
        This command is used to set different ac filter.
        :param bandwidth: selected filter bandwidth 3 Hz to 300 kHz(7 seconds / reading), type: int
                                                    20 Hz to 300 kHz(1 reading / second), type: int
                                                    200 Hz to 300 kHz(10 readings / second), type: int
        :rtype None
        """
        self.write('DETector:BANDwidth %s' % bandwidth)

    def impedance_auto(self, status):
        """
        This command is used to set the status of automatic input resistance mode.
        :param status: On or off, type: str
        :rtype None
        """
        self.write('INPut:IMPedance:AUTO %s' % status)

    def measure_curr_vol(self, function, typ, ran, resolution):
        """
        This command is used to set the function and type of the measurement.
        :param function: current or voltage, type: str
        :param typ: AC or DC, type: str
        :param ran: range of voltage(100mV, 1V, 10V, 100V, 1000V), type: float
                    range of current(10mA, 100mA, 1A, 3A), type: float
        :param resolution: resolution of voltage(100nV, 100mV), type: float
                           resolution of current(10nA, 10mA), type: float
        :rtype None
        """
        self.query('MEASure:%s:%s? %s,%s' % (function, typ, ran, resolution))

    def measure_others(self, function):
        """
        This command is used to set the function and type of the measurement.
        :param function: resistance, frequency, period, continuity or diode , type: str
        :rtype None
        """
        self.query('MEASure:%s?' % function)

    def configure_curr_vol(self, function, typ, ran, resolution):
        """
        This command is used to configure the function and type of the measurement.
        :param function: current or voltage, type: str
        :param typ: AC or DC, type: str
        :param ran: range of voltage(100mV, 1V, 10V, 100V, 1000V), type: float
                    range of current(10mA, 100mA, 1A, 3A), type: float
        :param resolution: resolution of voltage(100nV, 100mV), type: float
                           resolution of current(10nA, 10mA), type: float
        :rtype None
        """
        self.write('CONFigure:%s:%s %s,%s' % (function, typ, ran, resolution))

    def configure_others(self, function):
        """
        This command is used to set the function and type of the measurement.
        :param function: resistance, frequency, period, continuity or diode , type: str
        :rtype None
        """
        self.write('CONFigure:%s' % function)

    def trigger_source(self, source):
        """
        This command is used to select the source from which the multimeter will accept a trigger.
        :param source: BUS or IMMediate or EXTernal, type: str
        :rtype None
        """
        self.write('TRIGger:SOURce %s' % source)

    def trigger_delay(self, delay):
        """
        This command is used to insert a trigger delay between the trigger signal and each sample that follows.
        :param delay: delay between the trigger signal and each sample that follows, type: int
        :rtype None
        """
        self.write('TRIGger:DELay %s' % delay)

    def trigger_count(self, count):
        """
        This command is used to set the number of triggers the multimeter will
        accept before returning to the idle state.
        :param count: trigger count, type: int
        :rtype None
        """
        self.write('TRIGger:COUNt %s' % count)

    def sample_count(self, count):
        """
        This command is used to set the number of readings (samples) the multimeter takes per trigger.
        :param count: trigger count, type: int
        :rtype None
        """
        self.write('SAMPle:COUNt %s' % count)

    def initiate(self):
        """
        This command is used to change the state of the triggering system from the idle state to the
        wait-for-trigger state.
        :rtype None
        """
        self.write('INITiate')

    def read_data(self):
        """
        This command is used to read data from the instrument.
        :rtype float
        """
        return self.query('Read?')

    def fetch_data(self):
        """
        This command is used to transfer readings stored in the multimeter internal memory by the
        INITiate command to the multimeter output buffer where you can read them into your bus controller.
        :rtype float
        """
        return self.query('FETCh?')

    def wait(self):
        """
        This command is used to query the status after commands are executed.
        :rtype: int
        """
        return self.query('*OPC?')