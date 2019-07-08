from .gpib import GPIB
import visa
from autobench import log
import sys
import numpy as np
import matplotlib.pyplot as plt


class E5052(GPIB):
    """ A class that defines and controls Agilent E5052."""

    def __init__(self, gpib_addr):
        """
        Child class of GPIB
        :param gpib_addr: GPIB Address, type: int
        :rtype None
        """
        super(E5052, self).__init__(gpib_addr, "E5052")

    def spurious(self, mode):
        self.write(':CALCulate:PN:TRACe:SPURious:OMISsion OFF')
        if mode == 1:
            self.write(':CALCulate:PN:TRACe:SPURious:POWer ON')
        elif mode == 2:
            self.write(':CALCulate:PN:TRACe:SPURious:POWer OFF')
        else:
            self.log.warn('The mode is invalid.')

    def average_set(self, correlation, average_factor):
        """
        This command is used to set corrlation number and average number
        :param correlation: correlation numbers to get result per average run, type: int
        :param average_factor: average numbers to get result, type: int
        :rtype None
        """
        self.write(':SENSe:PN:CORRelation:COUNt %s' % correlation)
        self.write(':SENSe:PN:AVERage:COUNt %s' % average_factor)

    def average_on_off(self, state):
        """
        This command is used to set average on or off
        :param state: average on or off, type: int
        :rtype None
        """
        self.write(':SENSe:PN:AVERage:STATe %s' % state)

    def band_select(self, band):
        if band == 1:
            self.write(':SENSe:PN:FBANd BAND1')
        elif band == 2:
            self.write(':SENSe:PN:FBANd BAND2')
        elif band == 3:
            self.write(':SENSe:PN:FBANd BAND3')
        elif band == 4:
            self.write(':SENSe:PN:FBANd BAND4')
        else:
            self.log.warn('The band is invaild, the band number should be from 1 to 4.')

    def display_image_mode(self, mode):
        """
        This command is used to set the display to be normal or inverted mode.
        :param mode: NORMal: Sets the display to normal display (default background: black), type: str
                     INVert: Sets the display to the inverted display (default background: white), type: str
        :return: None
        :rtype: None
        """
        self.write(':DISPlay:IMAGe %s' % mode)

    def if_gain(self, gain):
        self.write(':SENSe:PN:IFGain %s' % gain)

    def print_image_mode(self, mode):
        """
        This command is used to set inverse color print mode.
        :param mode: NORMal: Sets inverse color print mode to 'Off', type: str
                     INVert: Set inverse color print mode to 'On', type: str
        :return: None
        :rtype: None
        """
        self.write(':HCOPy:IMAGe %s' % mode)

    def rf_attenuation(self, attenuation):
        self.write(':SENSe:ATTenuation:LEVel %s' % attenuation)

    def set_marker(self, marker_number, marker_value):
        self.write(':CALCulate:PN:TRACe:MARKer%s:X %s' %(marker_number, marker_value))

    def set_BDmarker(self, state, start, stop):
        self.write(':CALCulate:PN:TRACe:BDMarker:X:STATe %s' % state)
        self.write(':CALCulate:PN:TRACe:BDMarker:X:STARt %s' % start)
        self.write(':CALCulate:PN:TRACe:BDMarker:X:STOP %s' % stop)

    def start_frequency(self, start_frequency):
        self.write(':SENSe:PN:FREQuency:STARt %s' % start_frequency)

    def stop_frequency(self, band):
        if band == 1:
            self.write(':SENSe:PN:FREQuency:STOP 5e6')
        elif band == 2:
            self.write(':SENSe:PN:FREQuency:STOP 2e7')
        elif band == 3:
            self.write(':SENSe:PN:FREQuency:STOP 4e7')
        elif band == 4:
            self.write(':SENSe:PN:FREQuency:STOP 1e8')
        else:
            self.log.warn('The band is invaild, the band number should be from 1 to 4.')

    def system_error_warn(self):
        return self.query(':SYSTem:ERRor?')

    def turn_on_off_marker(self, marker_number, state):
        self.write(':CALCulate:PN:TRACe:MARKer%s:STATe %s' % (marker_number, state))

    def trigger_continuous(self, state):
        self.write(':INITiate:PN:CONTinuous %s' % state)

    def trigger_immediate(self):
        self.write(':INITiate:PN:IMMediate')

    def trigger_sopc(self, state):
        self.write(':TRIGger:SOPC %s' % state)

    def trigger_average(self, state):
        self.write(':TRIGger:AVERage %s' % state)

    def save_screen(self, file_name):
        self.write(':MMEMory:STORe:IMAGe %s' % file_name)

    def save_csv(self, file_name):
        self.write(':MMEMory:PN1:TRACe1:STORe %s' % file_name)

    def raw_data(self):
        return self.query(':CALCulate:PN1:DATA:RDATa?')

    def raw_data_x_axis(self):
        return self.query(':CALCulate:PN1:DATA:XDATa?')

    def get_error_warn_message(self):
        return str(self.query(':SYSTem:ERRor?')).split(',')[0]

    def read_message(self):
        return str(self.query('DISPlay:MESSage:DATA?')).split(',')[0]

    def get_rms_jitter(self):
        return str(self.query(':CALCulate:PN:TRACe:FUNCtion:INTegral:DATA?')).split(',')[4]

    def get_status(self):
        return str(self.query('*OPC?')).strip()

    def clear_display(self):
        self.write('DISPlay:MESSage:CLEar')


class Holzworth(object):
    """ A class that defines and controls Holzworth 7062C."""
    def __init__(self, tcpip_addr):
        """
        This command is used to initialize the Horzworth 7062C phase noise analyser.
        :param tcpip_addr: TCP/IP address, type: str
        :return: None
        """
        self.log = log(self.__class__.__name__)
        try:
            self.holzworth = visa.ResourceManager().open_resource("TCPIP0::%s::9760::SOCKET" % tcpip_addr)
            self.holzworth.timeout = 6000
            self.holzworth.write_termination = '\n'
            self.holzworth.read_termination = '\n'
            self.log.info('Holzworth opens successfully.')
        except visa.Error:
            self.log.error('Holzworth fails to open.', exc_info=True)
            sys.exit("I/O Error")

    def cancel_measurement(self):
        """
        This command is used to cancel the current measurement.
        :return: None
        """
        self.holzworth.query(':CALC:PN:TRACE:HOLD')

    def initial_measurement(self):
        """
        This command is used to initialize phase noise measurement.
        :return: None
        """
        self.holzworth.query(':INIT:PN:IMM')

    def query_device_infomation(self):
        """
        This command is used to query the device information.
        :return: Device information.
        :rtype: str
        """
        return str(self.holzworth.query('*IDN?'))

    def query_input(self):
        """
        This command is used to query input frequency and power level.
        :return: frequency(Hz), power level(dBm)
        :rtype: str
        """
        input = self.holzworth.query(':CALC:PN:DATA:CARR?')
        return input
        # frequency = str(input[0])
        # power_level = str(input[1])
        # return frequency, power_level

    def query_measurement_number(self):
        """
        This command is used to query the number of measurement points.
        :return: of measurement points.
        :rtype: int
        """
        return int(self.holzworth.query(':SENS:PN:SWE:POIN?'))

    def query_measurement_status(self):
        """
        This command is used to query whether instrument is currently performing a measurement.
        :return: phase noise measurement status.
        :rtype: str
        """
        return str(self.holzworth.query(':STAT:OPER:COND?'))

    def query_measurement_type(self):
        """
        This command is used to query phase noise measurement type.
        :return: phase noise measurement type.
        :rtype: str
        """
        return str(self.holzworth.query(':SENS:PN:MEAS:TYPE?'))

    def query_number_of_correlation(self):
        """
        This command is used to query the number of correlations set.
        :return: Number of correlations set.
        :rtype: int
        """
        return int(self.holzworth.query(':SENS:PN:CORR:COUN?'))

    def query_start_frequency(self):
        """
        This command is used to query measurement start frequency offset.
        :return: start frequency offset.
        :rtype: str
        """
        return str(self.holzworth.query(':SENS:PN:FREQ:STAR?'))

    def query_stop_frequency(self):
        """
        This command is used to query measurement stop frequency offset.
        :return: stop frequency offset.
        :rtype: str
        """
        return str(self.holzworth.query(':SENS:PN:FREQ:STOP?'))

    def read_formatted_phase_noise(self):
        """
        This command is used to read formatted phase noise data in dBc/Hz from instrument.
        :return: phase noise data
        :rtype: list
        """
        formatted_phase_noise = []
        for phase_noise in self.holzworth.query(':CALC:PN:DATA:FDAT?').split(','):
            formatted_phase_noise.append(float(phase_noise))
        return formatted_phase_noise

    def read_frequency_axis(self):
        """
        This command is used to frequency axis data from instrument.
        :return: frequency axis data
        :rtype: list
        """
        frequency_axis = []
        for axis in self.holzworth.query(':CALC:PN:DATA:XDAT?').split(','):
            frequency_axis.append(float(axis))
        return frequency_axis

    def read_jitter(self):
        """
        This command is used to read jitter data.
        :return: jitter(frequency range(Hz), RMS noise(degress), RMS Jitter(s)
        :rtype: list
        """
        jitter = []
        for data in self.holzworth.query(':CALC:PN:TRAC:FUNC:INT:DATA?').split(','):
            jitter.append(float(data))
        return jitter[0], jitter[1], jitter[2]*10e15

    def set_jitter_integration_range(self, low_end, high_end):
        """
        This command is used to set the jitter integration range.
        :param low_end: start value for jitter integration range, type: str
        :param high_end: stop value for jitter integration range, type: str
        :return: None
        """
        self.holzworth.query(':CALC:PN:TRAC:BDM:X:STAR:%s' % low_end)
        self.holzworth.query(':CALC:PN:TRAC:BDM:X:STOP:%s' % high_end)

    def set_number_of_correlation(self, number):
        """
        This command is used to set the number of correlations for the measurement to be performed.
        :param number: Number of correlations, type: int
        :return: None
        """
        self.holzworth.query(':SENS:PN:CORR:COUN:%s' % number)

    def set_start_frequency(self, start_frequency):
        """
        This command is used to set the measurement start frequency.
        :param start_frequency: start frequency offset, type str
        :return: None
        """
        self.holzworth.query(':SENS:PN:FREQ:STAR:%s' % start_frequency)

    def set_stop_frequency(self, stop_frequency):
        """
        This command is used to set the measurement stop frequency.
        :param stop_frequency: stop frequency offset, type str
        :return: None
        """
        self.holzworth.query(':SENS:PN:FREQ:STOP:%s' % stop_frequency)

    def set_measurement_type(self, type):
        """
        This command is used to set the phase noise measurement type.
        :param type: phase noise measurement type, Absolute, AM, Additive, Baseband. type: str
        :return: None
        """
        self.holzworth.query(':SENS:PN:MEAS:TYPE:%s' % type)

    def close(self):
        """
        This command is used to close the socket communication with instrument.
        :return: None
        """
        self.holzworth.close()

    def measurement_setup(self, correlation_number, start_frequency, stop_frequency, integration_low_end,
                          integration_high_end, measurement_type):
        """
        This function is used to measure phase noise and jitter.
        :param correlation_number: Number of correlations, type: int
        :param start_frequency: start frequency offset, type str
        :param stop_frequency: stop frequency offset, type str
        :param integration_low_end: start value for jitter integration range, type: str
        :param integration_high_end: stop value for jitter integration range, type: str
        :param measurement_type: phase noise measurement type, type:str
        :return: phase_noise, frequency_axis, jitter
        :rtype: list
        """
        self.set_number_of_correlation(correlation_number)
        self.set_start_frequency(start_frequency)
        self.set_stop_frequency(stop_frequency)
        self.set_jitter_integration_range(integration_low_end, integration_high_end)
        self.set_measurement_type(measurement_type)
        self.initial_measurement()
        status = True
        while status:
            if 'Ready' in self.query_measurement_status():
                status = False
            else:
                continue
        carrier_frequency, power_level = self.query_input()
        self.log.info('The output frequency is %sMHz with power level %sdBm.' % (carrier_frequency, power_level))
        phase_noise = self.read_formatted_phase_noise()
        frequency_axis = self.read_frequency_axis()
        jitter = self.read_jitter()
        self.log.info('The output phase noise is %s.' % phase_noise)
        self.log.info('The offset frequency is %s.' % frequency_axis)
        self.log.info('The jitter is %s.' % jitter)
        result = list()
        result.append(phase_noise)
        result.append(frequency_axis)
        result.append(jitter)
        self.close()
        return result


# holzworth = Holzworth('157.165.147.176')
# holzworth.set_number_of_correlation(1)
# holzworth.set_start_frequency('100Hz')
# print holzworth.query_start_frequency()
# holzworth.set_stop_frequency('40MHz')
# print holzworth.query_stop_frequency()
# holzworth.set_jitter_integration_range('12kHz', '20MHz')
# holzworth.set_measurement_type('Absolute')
# print holzworth.query_measurement_type()
# holzworth.initial_measurement()
# while True:
#     if 'Ready' in holzworth.query_measurement_status():
#         break
#     else:
#         continue
# print holzworth.query_measurement_number()
# # holzworth.cancel_measurement()
# x = holzworth.read_frequency_axis()
# y = holzworth.read_formatted_phase_noise()
# input = holzworth.query_input()
# holzworth.cancel_measurement()
# print input
# print holzworth.read_jitter()
# plt.semilogx(x,y)
# plt.show()