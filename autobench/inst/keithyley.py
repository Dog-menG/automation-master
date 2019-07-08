from .gpib import GPIB


class Keithley2400(GPIB):
    # A class that defines and controls Keithley2400.
    KL = 'Keithley2400'

    def __init__(self, gpib_addr):
        """
        Initiate Keithley2400 GPIB interface
        :param gpib_addr: GPIB address, no need for the full resource name, type: int
        :rtype None
        """
        super(self.__class__, self).__init__(gpib_addr, "Keithley2400")

    def on_off(self, state):
        self.write('OUTP %s' % state)

    def read_one_data(self):
        """
        This command works exactly like FETCh?, except that it returns only the most recent reading.
        :rtype list
        """
        return self.query(':DATA?')

    def read_data(self):
        """
        This command is to set read_data mode.
        :rtype list
        """
        return self.query(':READ?')

    def read_buffer(self):
        """
        This command is used to read data stored in buffer.
        :rtype list
        """
        return self.query('TRACe:DATA?')

    def measure(self, measure_function):
        """
        This command is to choose measurement function.
        :param measure_function: function to be measured, type: str
        :rtype None
        """
        self.write(':MEAS:%s' % measure_function)

    def sense_function(self, sense_function):
        """
        This command is to choose sense function.
        :param sense_function: function to be sensed, type: str
        :rtype None
        """
        self.write(':SENS:FUNC "%s"' % sense_function)

    def sense_compliance(self, sense_function, level):
        """
        This command is uesd to set compliance for selected function.
        :param sense_function: function to be sensed, type: str
        :param level: Voltage level should be between -210 and 210, type: int
                      Current level should be between -1.05 and 1.05, type: float
        :rtype None
        """
        self.write(':SENS:%s:PROTection %s' % (sense_function, level))

    def source_voltage(self, voltage):
        """
        This command is used to set voltage.
        :param voltage: The voltage to be set, type: str
        :return: None
        :rtype: None
        """
        self.write(':SOUR:VOLT %s' % voltage)

    def source_function(self, source_function):
        """
        This command is used to select the source mode.
        :param source_function: function to source, type: str
        :rtype None
        """
        self.write(':SOUR:FUNCtion %s' % source_function)

    def source_mode(self, source_function, source_mode):
        """
        This command is used to select the source function and source mode.
        :param source_function: Voltage, Current, Memory, type: str
        :param source_mode: Fixed, list, sweep, type: str
        :rtype None
        """
        self.write(':SOUR:%s:MODE %s' % (source_function, source_mode))

    def fix_amplitute(self, source_function, amplitude):
        """
        This command is used to select the source function and amplitude for the fix mode.
        :param source_function: Voltage, Current, Memory, type: str
        :param amplitude: Voltage level should be between -210 and 210, type: int
                          Current level should be between -1.05 and 1.05, type: float
        :rtype None
        """
        self.write('SOUR:%s %s' % (source_function, amplitude))

    def range_mode(self, range_mode):
        """
        This command is used to select the range mode for the sweep.
        :param range_mode: best, auto, fixed type: str
        :rtype None
        """
        self.write(':SOUR:SWEep:RANGing %s' % range_mode)

    def sweep_mode(self, sweep_mode):
        """
        This command is used to select the scale for the sweep.
        :param sweep_mode: linear or logarithmic type: str
        :rtype None
        """
        self.write('SOUR:SWEep:SPACing %s' % sweep_mode)

    def start_stop(self, function_mode, start_number, stop_number, step):
        """
        This command is used to set start and stop point for the sweep for the function which is chosen.
        :param function_mode: Voltage or Current, type : str
        :param start_number: For Voltage mode, start values should be between -210V and 210V, type: int
                             For Current mode, start values should be between -1.05A and 1.05A, type: float
        :param stop_number: For Voltage mode, stop values should be between -210V and 210V, type: int
                            For Current mode, stop values should be between -1.05A and 1.05A, type: float
        :param step: For Voltage mode, step values should be between -210V and 210V, type: int
                     For Current mode, step values should be between -1.05A and 1.05A, type: float
        :rtype None
        """
        self.write('SOUR:%s:STARt %s' % (function_mode, start_number))
        self.write('SOUR:%s:STOP %s' % (function_mode, stop_number))
        self.write('SOUR:%s:STEP %s' % (function_mode, step))

    def center_span(self, function_mode, center_number, span_number, step):
        """
        This command is used to set center and span point for the sweep for the function which is chosen.
        :param function_mode: Voltage or Current, type : str
        :param center_number: For Voltage mode, center values should be between -210V and 210V, type: int
                              For Current mode, center values should be between -1.05A and 1.05A, type: float
        :param span_number: For Voltage mode, span values should be between -210V and 210V, type: int
                            For Current mode, span values should be between -1.05A and 1.05A, type: float
        :param step: For Voltage mode, step values should be between -210V and 210V, type: int
                     For Current mode, step values should be between -1.05A and 1.05A, type: float
        :rtype None
        """
        self.write('SOUR:%s:CENTer %s' % (function_mode, center_number))
        self.write('SOUR:%s:SPAN %s' % (function_mode, span_number))
        self.write('SOUR:%s:STEP %s' % (function_mode, step))

    def delay(self, time):
        """
        This command is used to manually set a delay (settling time) for the source.
        :param time: delay time should be between 0 and 999.999s, type: int
        :rtype None
        """
        self.write('SOUR:DElay %s' % time)

    def format(self, lst):
        """
        This command is used to set list format for sweep mode.
        :param lst: Voltage, Current, Resistance, Time, Status type: list
        :rtype None
        """
        self.write(':FORM:ELEM %s' % lst)

    def trigger_count(self, count):
        """
        This command is used to set trigger number.
        :parameter: trigger number from 1 to 2500, type: int
        :rtype None
        """
        self.write(':TRIG:COUN %s' % count)
