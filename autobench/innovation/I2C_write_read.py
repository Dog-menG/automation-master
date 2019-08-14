from autobench.i2c.aa_i2c import AAReadWrite
from autobench import log
import time
import datetime
import os
import pandas as pd

class TDC_Calibration(object):

    def __init__(self, i2c_address=0x58):
        self.log = log(self.__class__.__name__)
        self.dut_i2c = AAReadWrite(0, i2c_address, True)
        self.dut_i2c.length = 1
        self.dut_number = 6
        self.ANA_MISC = [0x00, 0x08, 0x10, 0x20]   # 0x20100880 && 0xFFFFFF00
        self.DIG_MISC = [0x00, 0x09, 0x10, 0x20]   # 0x20100900 && 0xFFFFFF00
        self.TDC_PLL = [0x00, 0x06, 0x10, 0x20]    # 0x20100600 && 0xFFFFFF00
        self.TDC0 = [0x00, 0x0B, 0x10, 0x20]       # 0x20100B80 && 0xFFFFFF00
        self.TDC1 = [0x00, 0x0C, 0x10, 0x20]       # 0x20100C00 && 0xFFFFFF00
        self.TDC0_data = [0x00, 0x80, 0x10, 0x20]  # 0x20108000 && 0xFFFFFF00
        self.TDC1_data = [0x00, 0x82, 0x10, 0x20]  # 0x20108200 && 0xFFFFFF00
        self.AFE1 = [0x00, 0x60, 0x10, 0x20]       # 0x20100680 && 0xFFFFFF00
        self.AFE2 = [0x00, 0x70, 0x10, 0x20]       # 0x20100700 && 0xFFFFFF00
        self.AFE3 = [0x00, 0x70, 0x10, 0x20]       # 0x20100780 && 0xFFFFFF00

    def i2c_write(self, address, data_list):
        self.dut_i2c.aa_write_i2c(address, data_list)
        data_list.pop(0)
        time.sleep(0.2)

    def i2c_read(self, start_address, length):
        return list(self.dut_i2c.aa_read_i2c(start_address, length))

    def i2c_close(self):
        self.dut_i2c.close()

    def enable_all_modules(self):
        # Write to page 0x20100900
        self.i2c_write('0xFC', self.DIG_MISC)
        time.sleep(0.1)
        # Disable write protect
        self.i2c_write('0x01', [0x00])
        time.sleep(0.1)
        # Enable all modules
        self.i2c_write('0x04', [0x00] * 8)
        time.sleep(0.1)

    def system_calibration(self, save_file):
        # Write to page 0x20100880
        self.i2c_write('0xFC', self.ANA_MISC)
        time.sleep(0.1)
        # Disable RX_top internal LDOs
        self.i2c_write('0x80', [0x00])
        time.sleep(0.1)
        # Enable RX_top internal LDOs
        self.i2c_write('0x80', [0x01])
        time.sleep(0.1)
        # Toggle bias_re_cal_trig to 1
        self.i2c_write('0x8C', [0x02])
        time.sleep(0.1)
        # Toggle bias re_cal_trig to 0
        self.i2c_write('0x8C', [0x00])
        time.sleep(0.1)
        # # Bypass bias calibration
        # self.i2c_write('0x8C', [0x01])
        # time.sleep(0.1)
        # # Change bias regulator code
        # self.i2c_write('0x8D', [0x00])
        # time.sleep(0.1)
        # read bias calibration status
        if bin(int(self.i2c_read(0x8F, 1)[0]))[2] == 0:
            bias_cal = True
        else:
            bias_cal = False
        # PLL calibration
        # Enable PLL FB div8 divider for testing
        self.i2c_write('0x94', [0x01])
        time.sleep(0.1)
        # Write to page 0x20100600
        self.i2c_write('0xFC', self.TDC_PLL)
        time.sleep(0.1)
        # Change PLL divider to Dec 56
        self.i2c_write('0x07', [0x38])
        time.sleep(0.1)
        # Open PLL loop
        self.i2c_write('0x04', [0x4C])
        time.sleep(0.1)
        # Close PLL loop
        self.i2c_write('0x04', [0x44])
        time.sleep(0.1)
        # Enable PLL calibration
        self.i2c_write('0x00', [0x01])
        time.sleep(0.1)
        # Read PLL lock status
        if int(self.i2c_read(0x02, 1)[0]) == 1:
            pll_lock = True
        else:
            pll_lock = False
        # FLL calibration
        # Write to page 0x20100880
        self.i2c_write('0xFC', self.ANA_MISC)
        time.sleep(0.1)
        # Enable FLL
        self.i2c_write('0x81', [0x3F])
        time.sleep(0.1)
        # Set FLL_rstb_counter to be low
        self.i2c_write('0x81', [0x3D])
        time.sleep(0.1)
        # Read FLL status
        if int(self.i2c_read(0x83, 1)[0]) == 0:
            fll = True
        else:
            fll = False
        # Write to page 0x20100680
        self.i2c_write('0xFC', self.AFE1)
        time.sleep(0.1)
        # Disable AFE1
        self.i2c_write('0x84', [0x08])
        # Write to page 0x20100700
        self.i2c_write('0xFC', self.AFE2)
        time.sleep(0.1)
        # Disable AFE2
        self.i2c_write('0x04', [0x08])
        # Write to page 0x20100700
        self.i2c_write('0xFC', self.AFE3)
        time.sleep(0.1)
        # Disable AFE3
        self.i2c_write('0x84', [0x08])
        status = '%s Bias calibration status: %s PLL lock status: %s FLL lock status: %s\n' \
                 % (datetime.datetime.now(), bias_cal, pll_lock, fll)
        save_file.writelines(status)
        print '%s Bias calibration status: %s PLL lock status: %s FLL lock status: %s\n' \
                 % (datetime.datetime.now(), bias_cal, pll_lock, fll)
        return save_file

    def tdc0_calibration(self, save_file):
        # Write to page 0x20100900
        self.i2c_write('0xFC', self.DIG_MISC)
        time.sleep(0.1)
        # TDC0_sw_rst = 1
        self.i2c_write('0x09', [0x01])
        time.sleep(0.1)
        # TDC0_sw_rst = 0
        self.i2c_write('0x09', [0x00])
        time.sleep(0.1)
        # Write to page 0x20100B80
        self.i2c_write('0xFC', self.TDC0)
        time.sleep(0.1)
        # Disable vernier line
        self.i2c_write('0x83', [0x00])
        time.sleep(0.1)
        # Enable vernier line
        self.i2c_write('0x83', [0xFF])
        time.sleep(0.1)
        # Data capture enable, raw data our enable, calibration enable
        self.i2c_write('0x80', [0xC1])
        time.sleep(0.1)
        # Data capture enable, raw data our enable, calibration disable
        self.i2c_write('0x80', [0xC0])
        time.sleep(0.1)
        self.tdc_data_process(self.TDC0_data)
        # Write to page 0x20108000
        self.i2c_write('0xFC', self.TDC0_data)
        time.sleep(0.1)
        tdc0_data = self.tdc_data_process(self.TDC0_data)
        tdc0 = pd.DataFrame(tdc0_data).transpose()
        tdc0.rename(index={0: 'TDC0'}, inplace=True)
        tdc0.columns = ['phase1', 'counter1', 'phase2', 'counter2', 'phase3', 'counter3', 'phase4', 'counter4',
                        'phase5', 'counter5', 'phase6', 'counter6', 'phase7', 'counter7', 'phase8', 'counter8']
        tdc0.to_csv(save_file, mode='a')
        return save_file

    def tdc1_calibration(self, save_file):
        # Write to page 0x20100900
        self.i2c_write('0xFC', self.DIG_MISC)
        time.sleep(0.1)
        # TDC0_sw_rst = 1
        self.i2c_write('0x09', [0x01])
        time.sleep(0.1)
        # TDC0_sw_rst = 0
        self.i2c_write('0x09', [0x00])
        time.sleep(0.1)
        # Write to page 0x20100C00
        self.i2c_write('0xFC', self.TDC1)
        time.sleep(0.1)
        # Disable vernier line
        self.i2c_write('0x03', [0x00])
        time.sleep(0.1)
        # Enable vernier line
        self.i2c_write('0x03', [0xFF])
        time.sleep(0.1)
        # Data capture enable, raw data our enable, calibration enable
        self.i2c_write('0x00', [0xC1])
        time.sleep(0.1)
        # Data capture enable, raw data our enable, calibration disable
        self.i2c_write('0x00', [0xC0])
        time.sleep(0.1)
        # Write to page 0x20108200
        tdc1_data = self.tdc_data_process(self.TDC1_data)
        tdc1 = pd.DataFrame(tdc1_data).transpose()
        tdc1.rename(index={0: 'TDC1'}, inplace=True)
        tdc1.columns = ['phase1', 'counter1', 'phase2', 'counter2', 'phase3', 'counter3', 'phase4', 'counter4',
                        'phase5', 'counter5', 'phase6', 'counter6', 'phase7', 'counter7', 'phase8', 'counter8']
        tdc1.to_csv(save_file, mode='a')
        return save_file

    def tdc_data_process(self, tdc_data_address):
        self.i2c_write('0xFC', tdc_data_address)
        time.sleep(0.1)
        phase1 = [hex(element) for element in self.i2c_read(0x12, 1)][0]
        counter1 = [hex(element) for element in self.i2c_read(0x18, 2)]
        counter1 = '0x' + counter1[1][2:] + counter1[0][2:]
        phase2 = [hex(element) for element in self.i2c_read(0x22, 1)][0]
        counter2 = [hex(element) for element in self.i2c_read(0x28, 2)]
        counter2 = '0x' + counter2[1][2:] + counter2[0][2:]
        phase3 = [hex(element) for element in self.i2c_read(0x32, 1)][0]
        counter3 = [hex(element) for element in self.i2c_read(0x38, 2)]
        counter3 = '0x' + counter3[1][2:] + counter3[0][2:]
        phase4 = [hex(element) for element in self.i2c_read(0x42, 1)][0]
        counter4 = [hex(element) for element in self.i2c_read(0x48, 2)]
        counter4 = '0x' + counter4[1][2:] + counter4[0][2:]
        phase5 = [hex(element) for element in self.i2c_read(0x52, 1)][0]
        counter5 = [hex(element) for element in self.i2c_read(0x58, 2)]
        counter5 = '0x' + counter5[1][2:] + counter5[0][2:]
        phase6 = [hex(element) for element in self.i2c_read(0x62, 1)][0]
        counter6 = [hex(element) for element in self.i2c_read(0x68, 2)]
        counter6 = '0x' + counter6[1][2:] + counter6[0][2:]
        phase7 = [hex(element) for element in self.i2c_read(0x72, 1)][0]
        counter7 = [hex(element) for element in self.i2c_read(0x78, 2)]
        counter7 = '0x' + counter7[1][2:] + counter7[0][2:]
        phase8 = [hex(element) for element in self.i2c_read(0x82, 1)][0]
        counter8 = [hex(element) for element in self.i2c_read(0x88, 2)]
        counter8 = '0x' + counter8[1][2:] + counter8[0][2:]
        tdc_processed_data = [phase1, counter1, phase2, counter2, phase3, counter3, phase4, counter4,
                              phase5, counter5, phase6, counter6, phase7, counter7, phase8, counter8]
        return tdc_processed_data

    def test(self):
        path = r'J:\PRODUCT\CHAR\DSSxxx\DSS203_AK769T-001\Aardvark\09_10_2018'
        os.chdir(path)
        file_name = 'Unit%s.csv' % self.dut_number
        save_file = open(file_name, 'a')
        iterate_number = 10
        self.enable_all_modules()
        for i in range(1, iterate_number + 1):
            save_file = self.system_calibration(save_file)
            save_file = self.tdc0_calibration(save_file)
            time.sleep(2)
        for i in range(1, iterate_number + 1):
            save_file = self.system_calibration(save_file)
            save_file = self.tdc1_calibration(save_file)
            time.sleep(2)
        save_file.writelines(' \n')
        self.i2c_close()


def main():
    i2c_address = 0x59
    test_aardvark = TDC_Calibration(i2c_address)
    test_aardvark.test()


if __name__ == "__main__":
    main()