import visa
import sys
from autobench import log


class M1(object):
    # A class that defines and controls M1

    def __init__(self):
        """
        Initiate log of class.
        :rtype None
        """
        self.log = log(self.__class__.__name__)

    def open(self):
        try:
            self.scope = visa.ResourceManager('@py')
            self.M1 = self.scope.open_resource('TCPIP0::157.165.147.162::8001::SOCKET')
            self.log.info('M1 opens successfully.')
        except visa.Error:
            self.log.error('M1 fails to open.', exc_info=True)
            sys.exit("I/O Error")

    def measure(self):
        self.open()
        self.M1.write('<M1RemoteCommand ApplicationKey="RemoteClient"><PerformAcquisition RunType="LiveSingle" /></M1RemoteCommand>')

    def status(self):
        self.open()
        status = self.M1.write('<M1RemoteCommand ApplicationKey="RemoteClient"><Ping /></M1RemoteCommand>')
        return status

    def clear(self):
        self.open()
        self.M1.write('<M1RemoteCommand ApplicationKey="RemoteClient"><ClearAllData /></M1RemoteCommand>')

    def start_test(self, name, save_file):
        self.open()
        self.M1.write('<M1RemoteCommand ApplicationKey="RemoteClient"><StartTest Name="%s" SaveReports="%s" /></M1RemoteCommand>' % (name, save_file))

    def end_test(self, file_name):
        self.open()
        self.M1.write('<M1RemoteCommand ApplicationKey="RemoteClient"><EndTest ReportFile="%s" /></M1RemoteCommand>' % file_name)

    def measurement_type(self, measurement_type):
        self.open()
        self.M1.write('<M1RemoteCommand ApplicationKey="RemoteClient"><MeasurementType="%s"/></M1RemoteCommand>' % measurement_type)

    def create_char_mgrview(self):
        self.open()
        self.M1.write('<M1RemoteCommand ApplicationKey="RemoteClient"><CreateCharMgrView ViewID="CharMgr" MeasurementType="SUPER_MAQ" Val1="-1 "Val2="-1" DblVal="0" /></M1RemoteCommand>')
        self.log.info('It creates char manager view')

    def set_threshold(self, type, value, channel, Pct):
        self.open()
        if type == 0:
            self.M1.write('<M1RemoteCommand ApplicationKey="RemoteClient"><SetHighThreshold Value="%s" ChannelID="%s" Pct="%s" /></M1RemoteCommand>' % (value, channel, Pct))
            self.log.info('It is OK')
        elif type == 1:
            self.M1.write('<M1RemoteCommand ApplicationKey="RemoteClient"><SetMidThreshold Value="%s" ChannelID="%s" Pct="%s" /></M1RemoteCommand>' % (value, channel, Pct))
        elif type == 2:
            self.M1.write('<M1RemoteCommand ApplicationKey="RemoteClient"><SetLowThreshold Value="%s" ChannelID="%s" Pct="%s" /></M1RemoteCommand>' % (value, channel, Pct))
        elif type == 3:
            self.M1.write('<M1RemoteCommand ApplicationKey="RemoteClient"><SetHysteresisThreshold Value="%s" ChannelID="%s" /></M1RemoteCommand>' % (value, channel))
        else:
            self.log.warn('The input is invalid')

    def add_measurement(self, measurement):
        self.open()
        self.M1.write()

    # #TODO NEED TO IMPLEMENT M1

a = M1()
a.create_char_mgrview()
test.write('<M1RemoteCommand ApplicationKey="RemoteClient"><CreateHistogramView ViewID="tCKavg" AnalysisID="tCKavg" MeasurementType="CLOCK_FREQUENCY" Val1="2" Val2="-1" DblVal="-1" /></M1RemoteCommand>')