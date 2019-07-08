from i2c.aa_i2c import AAReadWrite
from autobench import log

class Read_Write_check(object):
    """This class is used to check SMB block and Byte read&write mode."""

    def __init__(self, i2c_address):
        self.log = self.log = log(self.__class__.__name__)
        self.dut_i2c = AAReadWrite(0, i2c_address, True)

    def read_check(self, start_address, length, data, mode = 'Block'):
        """
        This function is used to check SMB Block and Byte read mode.
        :param start_address:Register start address. Block mode: most significant bit 0. Byte mode: most significant bit 1, type : int
        :param length: # of bytes to be read in this operation, type: int
        :param data: Data to compare with the read_back from the unit.
        :param mode: Mode to check, 'Byte' or "Block', default is 'Block', type: str
        :return: True if read_back matches data, False if read_back does not match data.
        :rtype: Boolean
        """
        # read_back = self.dut_i2c.aa_read_i2c(start_address, length)
        # print read_back[0]
        if mode == 'Byte':
            start_address = start_address + 128
            read_back = list(self.dut_i2c.aa_read_i2c(start_address, length))
            if read_back == data:
                self.log.info('Read_back matches the input, SMB Byte mode read is working.')
                return True
            else:
                self.log.info('Read_back does not match the input, SMB Byte mode read is not working.')
                self.log.info('The read_back is %s ' % read_back)
                self.log.info('The input data is %s' % data)
                return False
        elif mode == 'Block':
            read_back = list(self.dut_i2c.aa_read_i2c(start_address, length))
            if read_back == data:
                self.log.info('Read_back matches the input, SMB Block mode read is working.')
                return True
            else:
                self.log.info('Read_back does not match the input, SMB Block mode read is not working.')
                self.log.info('The read_back is %s ' % read_back)
                self.log.info('The input data is %s' % data)
                return False
        else:
            self.log.warn('The mode is neither Block or Byte mode, please check '
                          'and re-run the program again.')


test = Read_Write_check(0x6C)
test.read_check(0x00, 2, [0x08, 0xF0], 'Block')