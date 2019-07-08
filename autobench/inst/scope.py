import visa
from autobench import log
import sys


class Keysight(object):
    # A class that defines and controls Keysight DSO-S 404A.

    def __init__(self, scope_address=0):
        """
        Initiate Keysight DSO-S 404A scope interface.
        :rtype None
        """
        self.log = log(self.__class__.__name__)
        try:
            if scope_address == 0:
                self.scope = visa.ResourceManager().open_resource(visa.ResourceManager().list_resources()[0])
                self.log.info('Scope opens successfully.')
            else:
                self.scope = visa.ResourceManager().open_resource(str(scope_address).split('\n')[0])
                self.log.info('Scope opens successfully.')
        except visa.Error:
            self.log.error('Scope fails to open.', exc_info=True)
            # sys.exit("I/O Error")
        self.scope.timeout = 60000
        self.scope.write(':MEASURE:CLEar')
        self.scope.write(':MARKer:MODE OFF')
        self.scope.write(':BLANk ALL')

    def advanced_tdly_trigger(self, arm, arm_slope, time_delay, slave, slave_slope, trigger_mode):
        """
        This command is set the delay mode to delay by time.
        :param arm: source of arming trigger, type: str
        :param arm_slope: slope of arming the trigger, type: str
        :param time_delay: delay time of a Delay By Time trigger event, type: str
        :param trigger: source of slave trigger, type: str
        :param trigger_slope: slope of arming the trigger, type: str
        :param trigger_mode: trigger mode of the selected source(auto, single, triggered), type: str
        :return: None
        :rtype: None
        """
        self.scope.write(':TRIGger:MODE ADVanced and')
        self.scope.write(':TRIGger:ADVanced:MODE DELay')
        self.scope.write(':TRIGger:ADVanced:DELay:MODE TDLY')
        self.scope.write(':TRIGger:ADVanced:DELay:TDLY:ARM:SOURce %s' % arm)
        self.scope.write(':TRIGger:ADVanced:DELay:TDLY:ARM:SLOPe %s' % arm_slope)
        self.scope.write(':TRIGger:ADVanced:DELay:TDLY:DELay %s' % time_delay)
        self.scope.write(':TRIGger:ADVanced:DELay:TDLY:TRIGger:SOURce %s' % slave)
        self.scope.write(':TRIGger:ADVanced:DELay:TDLY:TRIGger:SLOPe %s' %slave_slope)
        self.scope.write(':TRIGger:SWEep %s' % trigger_mode)
        self.run_mode('run')

    def auto_scale_channels(self, mode):
        """
        This command is used to select whether to apply autoscale to all of the input channels or just the input
        channels that are currently displayed.
        :param channel : All channels or the channels displayed on the screen, type: str
        :rtype: None
        """
        self.scope.write(':AUToscale:CHANnels %s' % mode)

    def auto_scale(self):
        """
        This command is used to set the oscilloscope to evaluate all input waveforms
        and find the optimum conditions for displaying the waveform.
        :rtype: None
        """
        self.scope.write(':AUToscale')

    def auto_scale_vertical(self, source):
        """
        This command is used to autoscales the vertical position and scaling for
        the corresponding channel without changing anything else.
        :param source: the source needs vertical auto-scale, type: str
        :rtype: None
        """
        self.scope.write(':AUToscale:VERTical %s' % source)

    def average_mode_on_off(self, mode):
        """
        This command is used to enable or disable averaging.
        :param mode: average on or off mode, type: str or int
        :return: None
        :rtype: None
        """
        self.scope.write(':ACQuire:AVERage %s' % mode)

    def source_on_off(self, source, state):
        """
        This command is used to turn on the selected channel.
        :param source: channel, function or histogram, type: str
        :param offset: state of the channel, type: str
        :return: None
        :rtype: None
        """
        self.scope.write(':%s:DISPlay %s' %(source, state))

    def memory_depth_auto_selection_status(self, status):
        """
        This command is used to enable or disable the automatic memory depth selection control.
        :param mode: memory depth selection status, type: str
        :return: None
        :rtype: None
        """
        self.scope.write(':ACQuire:POINts:AUTO %s' % status)

    def recall_setup(self, set_up_memory_number):
        """
        This command is used to recall a setup that was saved in one of the oscilloscope's setup memories.
        :param set_up_memory_number: Setup memory number 0 through 9, type: int.
        :return: None
        :rtype: None
        """
        self.scope.write(':RECall:SETup %s' % set_up_memory_number)

    def store_setup(self, set_up_memory_number):
        """
        This command is used to save the current oscilloscope setup in one of the setup memories.
        :param set_up_memory_number: Setup memory number 0 through 9, type: int.
        :return: None
        :rtype: None
        """
        self.scope.write(':STOEe:SETup %s' % set_up_memory_number)

    def thresholds_general_absolute(self, source, high, mid, low):
        """
        This command is used to set thresholds of rise and fall time for selected source
        :param source: all, channel, function or histogram, type: str
        :param high: high level of threshold, type: int or float
        :param mid: high level of threshold, type: int or float
        :param low: low level of threshold, type: int or float
        :rtype: None
        """
        # self.scope.write(':MEASure:THResholds:GENeral:METHod %s,ABSolute' % source)
        # self.scope.write(':MEASure:THResholds:GENeral:TOPBase:ABSolute %s,%s,%s,%s' % (source, high, mid, low))
        self.scope.write(':MEASure:THResholds:GENERal:METHod %s,ABSolute' % source)
        self.scope.write(':MEASure:THResholds:GENERal:ABSolute %s,%s,%s,%s' %(source, high, mid, low))

    def thresholds_general_percent(self, source, high, mid, low):
        """
        This command is used to set thresholds of rise and fall time for selected source
        :param source: channel, function or histogram, type: str
        :param high: high level of threshold, type: int or float
        :param middle: middle level of threshold, type: int or float
        :param low: low level of threshold, type: int or float
        :rtype: None
        """
        self.scope.write(':MEASure:THResholds:GENERal:METHod %s,PERCent' % source)
        self.scope.write(':MEASure:THResholds:GENeral:PERCent %s,%s,%s,%s' % (source, high, mid, low))

    def thresholds_rfall_absolute(self, source, high, mid, low):
        """
        This command is used to set thresholds of rise and fall time for selected source
        :param source: channel, function or histogram, type: str
        :param high: high level of threshold, type: int or float
        :param mid: high level of threshold, type: int or float
        :param low: low level of threshold, type: int or float
        :rtype: None
        """
        self.scope.write(':MEASure:THResholds:RFALl:METHod %s,ABSolute' % source)
        self.scope.write(':MEASure:THResholds:RFALl:ABSolute %s,%s,%s,%s' % (source, high, mid, low))

    def thresholds_rfall_percent(self, source, high, mid, low):
        """
        This command is used to set thresholds of rise and fall time for selected source
        :param source: channel, function or histogram, type: str
        :param high: high level of threshold, type: int or float
        :param middle: middle level of threshold, type: int or float
        :param low: low level of threshold, type: int or float
        :rtype: None
        """
        self.scope.write(':MEASure:THResholds:RFALl:METHod %s,PERCent' % source)
        self.scope.write(':MEASure:THResholds:RFALl:PERCent %s,%s,%s,%s' % (source, high, mid, low))

    def thresholds_query(self, mode, source):
        """
        This command is to ask the threshold of the scope
        :param mode: Percent of VDD level or absolute voltage, type: str
        :param source: channel, function or histogram, type: str
        :return: threshold of the scope
        :rtype: float
        """
        return self.scope.query(':MEASure:THResholds:%s? %s' % (mode, source))

    def source_on(self, source):
        """
        This command is used to turn on the selected source.
        :param source: channel, function or histogram, type: str
        :rtype: None
        """
        self.scope.write(':VIEW %s' % source)

    def source_scale_setup(self, source, offset, scale):
        """
        This command is used to set the offset and scale of selected source.
        :param source: channel, function or histogram, type: str
        :param offset: offset of the selected source, type: float
        :param scale:  scale of the selected source, type: float
        :rtype: None
        """
        self.scope.write(':%s:OFFSet %s' % (source, offset))
        self.scope.write(':%s:SCALe %s' % (source, scale))

    def source_range_setup(self, source, range, offset):
        """
        This command is used to set the offset and scale of selected source.
        :param source: channel, function or histogram, type: str
        :param range: range of the selected source, type: float
        :rtype: None
        """
        self.scope.write(':%s:RANGe %s' % (source, range))
        self.scope.write(':%s:OFFSet %s' % (source, offset))

    def histogram_setup(self, source, left_limit, right_limit, top_limit, bottom_limit):
        """
        This command is used to set the limit of histogram.
        :param source: channel, function or histogram, type: str
        :param left_limit: left limit of the selected source, type: float
        :param right_limit: right limit of the selected source, type: float
        :param top_limit: top limit of the selected source, type: float
        :param bottom_limit: bottom limit of the selected source, type: float
        :rtype: None
        """
        self.scope.write(':HISTogram:WINDow:SOURce %s' % source)
        self.scope.write(':HISTogram:WINDow:LLIMit %s' % left_limit)
        self.scope.write(':HISTogram:WINDow:RLIMit %s' % right_limit)
        self.scope.write(':HISTogram:WINDow:TLIMit %s' % top_limit)
        self.scope.write(':HISTogram:WINDow:BLIMit %s' % bottom_limit)

    def acquisition(self, memory_depth, sample_rate, timescale, memory_depth_auto_mode='ON'):
        """
        This command is used to set the acquisition parameters of the scope.
        :param memory_depth: memory_depth of the scope, type; float(scientific notation form)
        :param sample_rate: sample_rate of the scope, type(scientific notation form)
        :param timescale: timescale of the scope, type(scientific notation form)
        :param memory_depth_auto_mode: status of selecting memory_depth, type: str.
        :rtype: None
        """
        if memory_depth_auto_mode == 'ON':
            self.scope.write(':ACQuire:SRATe %s' % sample_rate)
            self.scope.write(':TIMebase:SCALe %s' % timescale)
        else:
            self.scope.write(':ACQuire:SRATe %s' % sample_rate)
            self.scope.write(':ACQuire:POINts %s' % memory_depth)
            self.scope.write(':TIMebase:SCALe %s' % timescale)

    def sample_rate(self, sample_rate):
        """
        This command is used to set the sampling rate of the scope
        :param sample_rate: sample_rate of the scope, type(scientific notation form)
        :return: None
        :rtype: None
        """
        self.scope.write(':ACQuire:SRATe %s' % sample_rate)

    def memory_depth(self, memory_depth):
        """
        This command is used to set the memory_depth of the scope
        :param memory_depth: memory_depth of the scope, type(scientific notation form)
        :return: None
        :rtype: None
        """
        self.scope.write(':ACQuire:POINts %s' % memory_depth)

    def timescale(self, timescale):
        """
        This command is used to set the timescale of the scope
        :param timescale: timescale of the scope, type(scientific notation form)
        :return: None
        :rtype: None
        """
        self.scope.write(':TIMebase:SCALe %s' % timescale)

    def trigger_setup(self, channel, edge, level, trigger_mode):
        """
        This command is used to setup the trigger parameter of selected channel.
        :param channel: channel to be used, type: int
        :param edge: trigger edge of the selected source (positive and negative), type: str
        :param level: trigger level of the selected source positive and negative), type: float
        :param trigger_mode: trigger mode of the selected source(auto, single, triggered), type: str
        :rtype: None
        """
        self.scope.write(':TRIGger:EDGE:SOURce %s' % channel)
        self.scope.write(':TRIGger:EDGE:SLOPe %s' % edge)
        self.scope.write(':TRIGger:LEVel %s,%s' % (channel, level))
        self.scope.write(':TRIGger:SWEep %s' % trigger_mode)
        self.run_mode('run')

    def result_display_portion(self, portion_number):
        """
        This command is used to specify the size of the Results pane in the oscilloscope display.
        :param portion_number: Results pane proportion number, type: float
        :return: None
        :rtype: None
        """
        self.scope.write(':DISPlay:PROPortion:RESults %s' % portion_number)

    def run_mode(self, mode):
        """
        This command is used to set the acquisition status.
        :param mode: Run, stop or single, type: str
        :rtype: None
        """
        self.scope.write(':%s' % mode)

    def screen_save(self, path):
        """
        This command is used to save the screen.
        :param path: the path to save the screen, type: str
        :return: None
        :rtype: None
        """
        self.scope.write(':DISK:SAVE:IMAGe "%s",PNG,SCR,OFF,INVERT' % path)
        self.wait()

    def waveform_save(self, source, path, file_format, header):
        """
        This command is used to save the waveform of selected source.
        :param source: selected source(channel, function, histogram), rtype: str
        :param path: the path to save the waveform of the selected source, rtype: str
        :param file_format: format of the save file(BIN | CSV | INTernal | TSV | TXT | H5 | H5INt), type: str
        :param header: Status of header of the waveform, str: str
        :return: None
        :rtype: None
        """
        self.scope.write(':DISK:SAVE:WAVeform %s,"%s" ,%s,%s' % (source, path, file_format, header))
        self.wait()

    def measure_vertical(self, measurement, source):
        """
        This command is used to measure parameter of the selected source.
        :param measurement: parameter to be measured, type: str
        :param source: channel, function or histogram, type: str
        :return: None
        :rtype: None
        """
        self.scope.write(':MEASure:%s %s' % (measurement, source))

    def measure(self, measurement, source, direction='RISing'):
        """
        This command is used to measure parameter of the selected source.
        :param measurement: parameter to be measured, type: str
        :param source: channel, function or histogram, type: str
        :param direction: rising edge or falling edge, type: str
        :return: None
        """
        self.scope.write(':MEASure:%s %s, %s' % (measurement, source, direction))

    def measure_all_edges(self, status):
        """
        This command is used to specify whether a single edge or all edges in the acquisition are used for horizontal measurements.
        :param status: Whether to measure all edges or not, type: str
        :return: None
        """
        self.scope.write(':ANALyze:AEDGes %s' % status)

    def measure_time(self, measurement, source):
        """
        This command is used to measures the rise time or fall time of the first displayed edge.
        :param measurement: RISetime of FALLtime, type: str
        :param source: channel, function or histogram, type: str
        :return: None
        :rtype: None
        """
        self.scope.write(':MEASure:%s %s' % (measurement, source))

    def measure_clear(self):
        """
        This command is used to clears the measurement results from the screen and
         disables all previously enabled measurements.
        :rtype: None
        """
        self.scope.write(':MEASURE:CLEar')

    def measure_delta_time(self, input_source, output_source):
        """
        This command is used to measure skew between the selected sources.
        :param input_source: channel, function or histogram, type: str
        :param output_source: channel, function or histogram, type: str
        :return: None
        """
        self.scope.write(":MEASure:DELTatime %s,%s" %(input_source, output_source))

    def measure_edge(self, status):
        """
        This command is used to specify whether a single edge or all edges in the acquisition
        are used for horizontal measurements.
        :param status: On or off, type: str
        :rtype: None
        """
        self.scope.write(':ANALyze:AEDGes %s' % status)

    def measure_histogram(self, measurement, source):
        """
        This command is used to  measure parameter of the selected source of the histogram.
        :param measurement: parameter to be measured, type: str
        :param source: channel, function or histogram, type: str
        :rtype: None
        """
        self.scope.write(':MEASure:HISTogram:%s %s' % (measurement, source))

    def measure_name(self, measurement_number):
        """
        This command is used to return the name of the corresponding measurement.
        :param source: the measurement number of the measurement you want to know about, type: int
        :rtype: str
        """
        return self.scope.query(':MEASurement%s:NAME?' % measurement_number)

    def measure_statistics_setting(self, statistics_mode):
        """
        This command is used to set the statistics mode.
        :param statistics_mode: statistics mode
              :ON/ CURRent/ MAXimum/ MEAN/ MINimum /STDDev, type: str
        :return: None
        :rtype: None
        """
        self.scope.write(':MEASure:STATistics %s' % statistics_mode)

    def get_result(self):
        """
        This command is used to ask the continuously displayed measurements.
        :return: Statistics result
        :rtype: list
        """
        result = self.scope.query(':MEASure:RESults?').split(',')
        self.wait()
        return result

    def function_single(self, source, function, operand):
        """
        This command is used to set the function of one operand.
        :param source: the selected function(unction1 to function16), type: str
        :param function: the function to be measured, type: str
        :param operand: the operand of the function to be measured, type: str
        :rtype: None
        """
        self.scope.write(':%s:%s %s' % (source, function, operand))

    def function_measure_trend(self, function_number, measurement_number):
        """
        This command is used to get the trend of certain measurement.
        :param source: the selected function(unction1 to function16), type: str
        :param function: the function to be measured, type: str
        :param operand1: the operand of the function to be measured, type: str
        :param operand2: the operand of the function to be measured, type: str
        :rtype: None
        """
        self.scope.write(":FUNCtion%s:MTRend MEAS%s" %(function_number, measurement_number))
        self.wait()

    def function_double(self, source, function, operand1, operand2):
        """
        This command is used to set the function of one operand.
        :param source: the selected function(unction1 to function16), type: str
        :param function: the function to be measured, type: str
        :param operand1: the operand of the function to be measured, type: str
        :param operand2: the operand of the function to be measured, type: str
        :rtype: None
        """
        self.scope.write(':%s:%s %s,%s' % (source, function, operand1, operand2))

    def function_name(self, function_number):
        """
        This command is used to return the currently defined source(s) for the function.
        :param function_number: the function number of the function you want to know, type: str
        :rtype: str
        """
        return self.scope.query(':FUNCtion%s?' % (function_number))

    def function_vertical_mode(self, source, mode):
        """
        This command is used to set the vertical scaling mode of the specified function to either AUTO or MANual
        :param source: source to change the mode, type: str
        :param mode: vertical scaling mode, type: str
        :return: None
        :rtype: None
        """
        self.scope.write(':%s:VERTical %s' % (source, mode))

    def marker_set(self, marker_mode):
        """
        This command is used to set the marker mode.
        :param marker_mode: off or manual, waveform, measurement, type: str
        :rtype: None
        """
        self.scope.write(':MARKer:MODE %s' % marker_mode)

    def marker_source(self, source1, source2):
        """
        This command is used to set the source for the Ax and Ay markers of selected source.
        :param source1: channel, function or histogram, type: str
        :param source2: channel, function or histogram, type: str
        :rtype: None
        """
        self.scope.write(':MARKer:X1Y1source %s' % source1)
        self.scope.write(':MARKer:X2Y2source %s' % source2)

    def marker_horizontal(self, x1, x2):
        """
        This command is used to set the Ax horizontal position, and moves the Ax marker
        to the specified time with respect to the trigger time.
        :param x1: x1 position, type: float(scientific notation form)
        :param x2: x2 position, type: float(scientific notation form)
        :rtype: None
        """
        self.scope.write(':MARKer:X1Position %s' % x1)
        self.scope.write(':MARKer:X2Position %s' % x2)

    def marker_vertical(self, y1, y2):
        """
        This command is used to set the vertical position, and moves the Ax marker
        to the specified time with respect to the trigger time.
        :param y1: y1 position, type: float(scientific notation form)
        :param y2: y2 position, type: float(scientific notation form)
        :rtype: None
        """
        self.scope.write(':MARKer:Y1Position %s' % y1)
        self.scope.write(':MARKer:Y2Position %s' % y2)

    def marker_delta(self, direction):
        """
        This command is used to get the current measurement unit difference between the markers of horizonal or vertical
        :param direction: x(horizonal) or y(vertical), type: str
        :rtype: None
        """
        return self.scope.query(':MARKer:%sDELta?' % direction)

    def query_measure_statistic(self):
        """
        This command is used to query returns of the current statistics mode.
        :return: current statistics mode.
        :rtype: list
        """
        return self.scope.query(':MEASure:STATistics?')

    def header(self, status):
        """
        This command is used to  specify whether the instrument will output a header for query responses.
        :param status: status of the header (on or off), type: str
        :rtype: None
        """
        self.scope.write(':SYSTem:HEADer %s' % status)

    def wait(self):
        """
        This command is used to wait until the previous command is done.
        :rtype: None
        """
        status = self.require_status().strip()
        while status != '1':
            status = str(self.require_status().strip())

    def reset(self):
        """
        This command is used to perform a default setup
        :rtype: None
        """
        self.scope.write('*RST')

    def clear(self):
        """
        This command is used to clear all status and error registers.
        :rtype: None
        """
        self.scope.write('*CLS')

    def require_status(self):
        """
        This command is used to query  the operation complete bit in the Standard Event Status Register.
        :rtype: unicode
        """
        return self.scope.query("*OPC?")

    def clear_dispay(self):
        """
        This command is used to clear the display and resets all associated measurements.
        """
        self.scope.write(':CDISplay')


class Tektronix(object):
    # A class that defines and controls Tektronix DC74534.
    def __init__(self, scope_address = 0):
        """
        Initiate Tektronix DPO7354C scope interface and set timeout timing.
        :rtype None
        """
        self.log = log(self.__class__.__name__)
        try:
            if scope_address == 0:
                self.scope = visa.ResourceManager().open_resource(visa.ResourceManager().list_resources()[0])
                self.log.info('Scope opens successfully.')
            else:
                self.scope = visa.ResourceManager().open_resource(str(scope_address).split('\n')[0])
                self.log.info('Scope opens successfully.')
        except visa.Error:
            self.log.error('Scope fails to open.', exc_info=True)
            # sys.exit("I/O Error")
        self.timeout(60)

    def query_measurement_min(self, measurement_slot):
        """
        This command is used to get accumulated minimum value of specified measurement.
        :param measurement_slot: The measurement number to be queried, type: int
        :return: min value of the measurement
        :rtype: float
        """
        return float(self.scope.query('MEASUrement:MEAS%s:MINImum?' % measurement_slot))

    def query_measurement_mean(self, measurement_slot):
        """
        This command is used to get accumulated mean value of specified measurement.
        :param measurement_slot: The measurement number to be queried, type: int
        :return: mean value of the measurement
        :rtype: float
        """
        return float(self.scope.query('MEASUrement:MEAS%s:MEAN?' % measurement_slot))

    def query_measurement_max(self, measurement_slot):
        """
        This command is used to get accumulated max value of specified measurement.
        :param measurement_slot: The measurement number to be queried, type: int
        :return: max value of the measurement
        :rtype: float
        """
        return float(self.scope.query('MEASUrement:MEAS%s:MAXimum?' % measurement_slot))

    def query_measurement_current(self, measurement_slot):
        """
        This command is used to is calculated for the measurement specified by <x>, which ranges from 1 through 8
        :param measurement_slot: The measurement number to be queried, type: int
        :return: current value of the measurement
        :rtype: float
        """
        return float(self.scope.query('MEASUrement:MEAS%s:VALue?' % measurement_slot))

    def query_measurement_unit(self, measurement_slot):
        """
        This command is used to query the units associated with the specified measurement.
        :param measurement_slot: The measurement number to be queried, type: int
        :return: units
        :rtype: unicode
        """
        self.scope.query('MEASUrement:MEAS%s:UNIts?' % measurement_slot)

    def save_file_destination(self, file_destination):
        """
        This command is used to set the location where files to be saved.
        :param file_destination: the location where files to be saved, type: str
        :return: None
        :rtype: None
        """
        self.scope.write('SAVEON:FILE:DEST %s' % file_destination)

    def save_file_name(self, file_name):
        """
        This command is used to set queries the file name to use when the file type is set to Custom.
        :param file_name: the file name to be saved, type: str
        :return: None
        :rtype: None
        """
        self.scope.write('SAVEON:FILE:NAME %s' % file_name)

    def save_file_type(self, file_type):
        """
        This command is used to set whether to use the data and time as the file name or to use a custom file name.
        :param file_type: the saving method, type: srt
               1 AUTO: uses the date and time as the file name for the saved events.
               2 CUSTOM uses the file name that you specified.
        :return: None
        :rtype: None
        """
        self.scope.write('SAVEON:FILE:TYPE %s' % file_type)

    def save_images(self, save_status):
        """
        This command is used to whether to save a screen capture any of the following triggers occurs:
            1.Limit test failure - if set to On.
            2.Mask failure - if set to On.
            3.Trigger - if set to On.
        :param save_status: the status whether to save the image or not, type: int or str
                0 or OFF disable Save On Image.
                other integer values or ON enable Save On Image.
        :return: None
        :rtype: None
        """
        self.scope.write('SAVEON:IMAGe %s' % save_status)

    def set_absolute_threshold_level(self, high_level, middle1_level, middle2_level, low_level):
        """
        This command is used to set threshold levels of absolute mode. Setting high, mid and low commands affect the
        results of period, frequency, delay, and all cyclic measurements. Setting high and low commands the results of
        rise and fall measurements. Setting mid command affects the results of delay measurements.
        :param high_level: high reference level, type: float
        :param middle1_level: mid reference level of mid1(the from waveform when taking a delay measurement), type: float
        :param middle2_level: mid reference level of mid2(the from waveform when taking a delay measurement), type: float
        :param low_level: low reference level, type: float
        :return: None
        :rtype: None
        """
        self.scope.write('MEASUrement:REFLevel:ABSolute:HIGH %s' % high_level)
        self.scope.write('MEASUrement:REFLevel:ABSolute:MID1 %s' % middle1_level)
        self.scope.write('MEASUrement:REFLevel:ABSolute:MID2 %s' % middle2_level)
        self.scope.write('MEASUrement:REFLevel:ABSolute:LOW %s' % low_level)

    def set_certain_measurement_slot_absolute_threshold_level(self, measurement_slot, high_level,
                                                              middle1_level, middle2_level, low_level):
        """
        This command is used to set threshold levels of absolute mode. Setting high, mid and low commands affect the
        results of period, frequency, delay, and all cyclic measurements. Setting high and low commands the results of
        rise and fall measurements. Setting mid command affects the results of delay measurements.
        :param measurement_slot: specified measurement_slot to be changed, type: int
        :param high_level: high reference level, type: float
        :param middle1_level: mid reference level of mid1(the from waveform when taking a delay measurement), type: float
        :param middle2_level: mid reference level of mid2(the from waveform when taking a delay measurement), type: float
        :param low_level: low reference level, type: float
        :return: None
        :rtype: None
        """
        self.scope.write('MEASUrement:MEAS%s:REFLevel:ABSolute:HIGH %s' % (measurement_slot, high_level))
        self.scope.write('MEASUrement:MEAS%s:REFLevel:ABSolute:MID1 %s' % (measurement_slot, middle1_level))
        self.scope.write('MEASUrement:MEAS%s:REFLevel:ABSolute:MID2 %s' % (measurement_slot, middle2_level))
        self.scope.write('MEASUrement:MEAS%s:REFLevel:ABSolute:LOW %s' % (measurement_slot, low_level))

    def set_certain_measurement_slot_threshold_mode(self, measurement_slot, threshold_mode):
        """
        This command is used to specify the reference level units used for measurement calculations of immediate
        measurement.
        :param measurement_slot: specified measurement_slot to be changed, type: int
        :param threshold_mode: threshold_mode for the measurement, type: str
        :return: None
        :rtype: None
        """
        self.scope.write('MEASUrement:MEAS%s:REFLevel:METHod %s' % (measurement_slot, threshold_mode))

    def set_certain_measurement_slot_percent_threshold_level(self, measurement_slot, high_level,
                                                             middle1_level, middle2_level, low_level):
        """
        This command is used to set threshold levels of percent mode. Setting high, mid and low commands affect the
        results of period, frequency, delay, and all cyclic measurements. Setting high and low commands the results of
        rise and fall measurements. Setting mid command affects the results of delay measurements.
        :param measurement_slot: specified measurement_slot to be changed, type: int
        :param high_level: high reference level, type: float
        :param middle1_level: mid reference level of Mid1 which is for the first waveform specified, type: float
        :param middle2_level: mid reference level of Mid2 which is for the second waveform specified, type: float
        :param low_level: low reference level, type: float
        :return: None
        :rtype: None
        """
        self.scope.write('MEASUrement:MEAS%s:REFLevel:PERCent:HIGH %s' % (measurement_slot, high_level))
        self.scope.write('MEASUrement:MEAS%s:REFLevel:PERCent:MID1 %s' % (measurement_slot, middle1_level))
        self.scope.write('MEASUrement:MEAS%s:REFLevel:PERCent:MID2 %s' % (measurement_slot, middle2_level))
        self.scope.write('MEASUrement:MEAS%s:REFLevel:PERCent:LOW %s' % (measurement_slot, low_level))

    def set_delay_measurement_source(self, measurement_slot, target_source, reference_source):
        """
        This command is used to set the sources for phase and delay measurement.
        Source:
        CH<x> is an input channel waveform. The x variable can be expressed as an integer ranging from 1 through 4.
        MATH<y> is a math waveform. The y variable can be expressed as an integer ranging from 1 through 4.
        REF<x> is a reference waveform. The x variable can be expressed as an integer ranging from 1 through 4.
        HIStogram is a histogram. Histogram is valid only for source 1.
        :param measurement_slot: The measurement slot ranges from 1 to 8, type: int
        :param target_source: the target source, type: str
        :param reference_source: the reference source, type: str
        :return: None
        :rtype: None
        """
        self.scope.write('MEASUrement:MEAS%s:SOUrce1 %s' % (measurement_slot, target_source))
        self.scope.write('MEASUrement:MEAS%s:SOUrce2 %s' % (measurement_slot, reference_source))

    def set_immediate_percent_threshold_level(self, high_level, middle1_level, middle2_level, low_level):
        """
        This command is used to set threshold levels of percent mode. Setting high, mid and low commands affect the
        results of period, frequency, delay, and all cyclic measurements. Setting high and low commands the results of
        rise and fall measurements. Setting mid command affects the results of delay measurements of immediate channel.
        :param high_level: high reference level, type: float
        :param middle1_level: mid reference level of Mid1 which is for the first waveform specified, type: float
        :param middle2_level: mid reference level of Mid2 which is for the second waveform specified, type: float
        :param low_level: low reference level, type: float
        :return: None
        :rtype: None
        """
        self.scope.write('MEASUrement:IMMed:REFLevel:PERCent:HIGH %s' % high_level)
        self.scope.write('MEASUrement:IMMed:REFLevel:PERCent:MID1 %s' % middle1_level)
        self.scope.write('MEASUrement:IMMed:REFLevel:PERCent:MID2 %s' % middle2_level)
        self.scope.write('MEASUrement:IMMed:REFLevel:PERCent:LOW %s' % low_level)

    def set_immediate_absolute_threshold_level(self, high_level, middle1_level, middle2_level, low_level):
        """
        This command is used to set threshold levels of absolute mode. Setting high, mid and low commands affect the
        results of period, frequency, delay, and all cyclic measurements. Setting high and low commands the results of
        rise and fall measurements. Setting mid command affects the results of delay measurements.
        :param high_level: high reference level, type: float
        :param middle1_level: mid reference level of mid1(the from waveform when taking a delay measurement), type: float
        :param middle2_level: mid reference level of mid2(the from waveform when taking a delay measurement), type: float
        :param low_level: low reference level, type: float
        :return: None
        :rtype: None
        """
        self.scope.write('MEASUrement:IMMed:REFLevel:ABSolute:HIGH %s' % high_level)
        self.scope.write('MEASUrement:IMMed:REFLevel:ABSolute:MID1 %s' % middle1_level)
        self.scope.write('MEASUrement:IMMed:REFLevel:ABSolute:MID2 %s' % middle2_level)
        self.scope.write('MEASUrement:IMMed:REFLevel:ABSolute:LOW %s' % low_level)

    def set_immediate_threshold_mode(self, threshold_mode):
        """
        This command is used to specify the reference level units used for measurement calculations of immediate
        measurement.
        :param: threshold_mode: threshold_mode for the measurement, type: str
        :return: None
        :rtype: None
        """
        self.scope.write('MEASUrement:IMMed:REFLevel:METHod %s' % threshold_mode)

    def set_percent_threshold_level(self, high_level, middle1_level, middle2_level, low_level):
        """
        This command is used to set threshold levels of percent mode. Setting high, mid and low commands affect the
        results of period, frequency, delay, and all cyclic measurements. Setting high and low commands the results of
        rise and fall measurements. Setting mid command affects the results of delay measurements.
        :param high_level: high reference level, type: float
        :param middle1_level: mid reference level of Mid1 which is for the first waveform specified, type: float
        :param middle2_level: mid reference level of Mid2 which is for the second waveform specified, type: float
        :param low_level: low reference level, type: float
        :return: None
        :rtype: None
        """
        self.scope.write('MEASUrement:REFLevel:PERCent:HIGH %s' % high_level)
        self.scope.write('MEASUrement:REFLevel:PERCent:MID1 %s' % middle1_level)
        self.scope.write('MEASUrement:REFLevel:PERCent:MID2 %s' % middle2_level)
        self.scope.write('MEASUrement:REFLevel:PERCent:LOW %s' % low_level)

    def source_horizontal_setup(self, sampling_rate, time_scale, record_length):
        """
        This command is used to set the horizontal sampling_rate, time_scale and record_length for the specified channel.
        :param sampling_rate: sample rate in samples per second, type: float
        :param time_scale: horizontal scale in seconds per division, The horizontal scale is read only for Manual mode,
               type: float
        :param record_length: record length in samples, Manual mode lets you change the record length, while the record
               length is read only for Auto and Constant mode.type: int
        :return:
        """
        self.scope.write('HORizontal:MODE:SAMPLERate %s' % sampling_rate)
        self.scope.write('HORizontal:MODE:SCAle %s' % time_scale)
        self.scope.write('HORizontal:MODE:RECORDLENGTH %s' % record_length)

    def set_measurement(self, measurement_slot, measurement):
        """
        This command is used to the set measurement type defined for the specified measurement slot.
        Source:
        CH<x> is an input channel waveform. The x variable can be expressed as an integer ranging from 1 through 4.
        MATH<y> is a math waveform. The y variable can be expressed as an integer ranging from 1 through 4.
        REF<x> is a reference waveform. The x variable can be expressed as an integer ranging from 1 through 4.
        HIStogram is a histogram. Histogram is valid only for source 1.
        :param measurement_slot: The measurement slot ranges from 1 to 8, type: int
        :param measurement: measurement to be taken, type: str
        :return: None
        :rtype: None
        """
        self.scope.write('MEASUrement:MEAS%s:%s' % (measurement_slot, measurement))

    def set_measurement_source(self, measurement_slot, source):
        """
        This command is used to set the source for all single channel measurements.
        :param measurement_slot: The measurement slot ranges from 1 to 8, type: int
        :param source: source of specified measurement_slot, type: int
        :return: None
        """
        self.scope.write('MEASUrement:MEAS%s:SOUrce%s' % (measurement_slot, source))

    def set_threshold_mode(self, threshold_mode):
        """
        This command is used to specify the reference level units used for measurement calculations of immediate
        measurement.
        :param: threshold_mode: threshold_mode for the measurement, type: str
        :return: None
        :rtype: None
        """
        self.scope.write('MEASUrement:REFLevel:METHod %s' % threshold_mode)

    def source_vertical_setup(self, source, offset, scale):
        """
        This command is used to set the vertical scale and offset for the specified channel.
        :param source: selected channel number which should be ranged from 1 to 4, type: int
        :param offset: offset of the selected source, type: float
        :param scale: scale per vertical division of the selected source, type: float
        :return: None
        :rtype: None
        """
        self.scope.write('CH%s: %s' % (source, offset))
        self.scope.write('CH%s: %s' % (source, scale))

    def source_vertical_coupling(self, source, coupling_mode):
        """
        This command is used to set the input attenuator coupling setting for the specified channel.
        :param source: selected channel number which should be ranged from 1 to 4, type :int
        :param coupling_mode:  Input attenuator coupling setting, type: string
                                AC: set the specified channel to AC coupling.
                                DC: set the specified channel to DC coupling.
                                DCREJect: set DC Reject coupling when probes are attached that have that feature.
                                GND: set the specified channel to ground.
        :return:
        """
        self.scope.write('CH%s:coupling %s' % (source, coupling_mode))

    def timeout(self, time_out):
        """
        This command is used to set the global timeout in seconds. The default is 30 seconds.
        time_out: Timeout, it will be 0 through 500, type: float.
        :return: None
        :rtype: None
        """
        self.scope.write('EMail:TIMEOut %s' % time_out)
