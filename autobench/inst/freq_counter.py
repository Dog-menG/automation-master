from .gpib import GPIB


class FreqCounter(GPIB):
    """GPIB Control of Agilent E53131A"""

    def __init__(self, gpib_addr):
        super(FreqCounter, self).__init__(gpib_addr, "E53131A")

    def read_freq(self, tar_freq, source):
        """
        Directly Read Frequency out from Assigned Channel
        :param tar_freq: Target Measurement Frequency, UNIT MHz
        :param source: Channel, either 1 or 2
        :return: A float value of the current reading
        """
        freq = self.query(':MEAS:FREQ? %s,1, (@%s)' % (tar_freq, source))
        return float(freq)

    def read_ratio(self, source1, source2):
        """
        Directly Read ratio out from Assigned Channels (source2 to source1)
        :param source: Channel, either 1 or 2
        :return: A float value of the current reading
        """
        ratio = self.query(':MEASure:FREQuency:RATio? , 1, 1, @%s, @%s' %(source1, source2))
        return ratio

    def get_status(self):
        """
        :return: A unicode value of the completion status
        """
        return str(self.query('*OPC?')).strip()



