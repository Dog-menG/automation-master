from .gpib import GPIB


class Agilent81130A(GPIB):
    # A class that defines and controls function generator.
    fun_gen = '81130A'

    def __init__(self, gpib_addr=10):
        """
        Initiate Agilent 81130A GPIB interface
        :param gpib_addr: GPIB address, no need for the full resource name, type: int
        :rtype None
        """
        super(self.__class__, self).__init__(gpib_addr, '81130A')

    def on_off(self, channel, status):
        """
        This command is used to turn on or off the function generator.
        :param channel: output channel1 or channel2
        :type: int
        :param status: the status of outputs, type: str
        :rtype None
        """
        self.write(':OUTP%s %s' % (channel, status))
        self.write(':OUTP%s:COMP %s' % (channel, status))

    def freq(self, channel, frequency):
        """
        This command is used to set frequency
        :param channel: output channel1 or channel2, type: int
        :param frequency: output frequency, type: float
        :rtype None
        """
        self.write(':FREQuency%s %sMHz' % (channel, frequency))

    def period(self, channel, period):
        """
        This command is used to set period
        :param channel: output channel1 or channel2, type: int
        :param period: output period, type: float
        :rtype None
        """
        self.write(':PULSe:PERiod%s %sNS' % (channel, period))

    def duty_cycle(self, channel, duty_cycle):
        """
        This command is used to set duty_cycle
        :param channel: output channel1 or channel2, type: int
        :param duty_cycle: output duty_cycle, type: float
        :rtype None
        """
        self.write(':PULSe:DCYCle%s %s' % (channel, duty_cycle))

    def width(self, channel, width):
        """
        This command is used to set width
        :param channel: output channel1 or channel2, type: int
        :param width: output period, type: float
        :rtype None
        """
        self.write(':PULSeL:WIDTh%s %sNS' % (channel, width))

    def vhigh_vlow(self, channel, low, high):
        """
        This command is used to set vhigh and vlow of the signal
        :param channel: output channel1 or channel2, type: int
        :param low: vlow, type: float
        :param high: vhigh, type: float
        :rtype None
        """
        # if high < low:
        #     raise self.logger('High voltage should be larger than low voltage.', lvl=2)
        # else:
        self.write(':VOLTage%s:LOW %sV' % (channel, low))
        self.write(':VOLTage%s:HIGH %sV' % (channel, high))

    def arm_trigger_edge(self, edge):
        """
        This command is used to select the trigger level for the arming signal
        :param edge: positive or negative, type: str
        :return: None
        :rtype: None
        """
        self.write(':ARM:SENS %s' % edge)

    def arm_trigger_mode(self, mode):
        """
        This command is used to select the arming mode.
        :param mode: STARTED mode or GATED mode, type: str
        :return: None
        :rtype: None
        """
        self.write(':ARM:MODE %s' % mode)

    def arm_trigger_source(self, source):
        """
        This command is used to select the arming source.
        :param source: Source of arming signal, type: str
        :return: None
        :rtype: None
        """
        self.write(':ARM:SOUR %s' % source)

    def amplitude_offset(self, amplitude, offset, channel):
        """
        This command is used to set amplitude and offset of the signal
        :param channel: output channel1 or channel2, type: int
        :param amplitude: signal amplitude, type: float
        :param offset: signal offset, type: float
        :rtype: None
        """
        self.write(':VOLTage%s %sV' % (channel, amplitude))
        self.write(':VOLTage%s:OFFset %sV' % (channel, offset))

    def digital_loop_number(self, number):
        """
        This command is used to set up a counted loop across one or more segments.
        :param number: loop count numbers, type: int
        :return: None
        :rtype: None
        """
        self.write(':DIG:PATT:LOOP %s' % number)

    def digital_loop_start_segment(self, start_segment):
        """
        This command is used to set up the first segment within a counted loop.
        :param start_segment:  srart segment, type: int
        :return: None
        :rtype: None
        """
        self.write(':DIG:PATT:LOOP:STAR %s' % start_segment)

    def digital_loop_length(self, length):
        """
        This command is used to set the number of segments to be repeated within the counted loop.
        :param length: 1 | 2 | 3 | 4, type: int
        :return: None
        :rtype: None
        """
        self.write(':DIG:PATT:LOOP:LENG %s' % length)

    def digital_pattern_on_off(self, status):
        """
        This command is used to enable or disable the pattern mode.
        :param status: On | OFF | 1 | 0
        :return: None
        :rtype: None
        """
        self.write(':DIG:PATT %s' % status)

    def digital_segment_data(self, segment_number, segment_data):
        """
        This command is used to set a segment's data for one or all channels starting from Bit1.
        :param segment_number: 1 | 2 | 3 | 4, type: int
        :param segment_data: data, type: str
        :return: None
        :rtype: None
        """
        self.write(':DIG:PATT:SEGM%s:DATA %s' %(segment_number, segment_data))

    def digital_segment_length(self, segment_number, segment_length):
        """
        This command is used to set up the number of bits within a segment.
        :param segment_number: 1 | 2 | 3 | 4, type: int
        :param segment_length: length within a segment 0 to 65504, type: int
        :return: None
        :rtype: None
        """
        self.write(':DIG:PATT:SEGM%s:LENG %s' %(segment_number, segment_length))

    def digital_segment_type(self, segment_number, segment_type):
        """
        This command is used to set the type of the segment for one channel.
        :param segment_number: 1 | 2 | 3 | 4, type: int
        :param segment_type: DATA | PRBS | HIGH | LOW
        :return: None
        :rtype: None
        """
        self.write(':DIG:PATT:SEGM%s:TYPE %s' %(segment_number, segment_type))

    def digital_sign_format(self, data_format):
        """
        This command is used to set the data format of channels1 and 2.
        :param data_format: RZ | NRZ | R1
        :return: None
        :rtype: None
        """
        self.write(':DIG:SIGN:FORM %s' % data_format)

    def serial_data_stream(self, channel, data, frequency, high, low):
        """
        This command is used to data stream.
        :param channel: output channel1 or channel2, type: int
        :param data: data stream, type: list
        :param frequency: data frequency, type:float
        :param high: signal vhigh, type: float
        :param low: signal vlow, type: float
        :rtype None
        """
        self.write(':DIGital:PATTern:STATe ON')
        self.write(':DIGital:SIGNal:FORMat NRZ')
        self.write(':DIGital:PATTern:SEGMent1:DATA1 %s' % data)
        self.freq(channel, frequency)
        self.vhigh_vlow(channel, low, high)

    def reset(self):
        """
        This command is used to reset 81130A function generator.
        :rtype None
        """
        self.write('*RST')

    def function_generator_setting(self, channel, frequency, duty_cycle, vlow, vhigh, status):
        """
        This command is used to set function generator.
        :param channel: output channel1 or channel2, type: int
        :param frequency: output frequency, type: float
        :param duty_cycle: output duty_cycle, type: float
        :param vhigh: high voltage, type: float
        :param vlow: low voltage, type: float
        :param status: output status, type: str
        :rtype None
        """
        self.freq(channel, frequency)
        self.duty_cycle(channel, duty_cycle)
        self.vhigh_vlow(channel, vlow, vhigh)
        self.on_off(channel, status)