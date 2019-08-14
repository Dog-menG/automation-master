from autobench.i2c.aa_i2c import AAReadWrite
from autobench import log
import time


class FLL_PLL(object):

    def __init__(self, i2c_address=0x58):
        self.log = log(self.__class__.__name__)
        self.dut_i2c = AAReadWrite(0, i2c_address, True)
        self.dut_i2c.length = 1

    def i2c_write(self, address, data_list):
        self.dut_i2c.aa_write_i2c(address, data_list)
        time.sleep(0.2)

    # def i2c_write_to_page_register(self, page_register):
    #     wrt_lst = []
    #     for i in range(1, len(page_register)/2):
    #         wrt_lst.insert(0, page_register[i:i+2])

    def i2c_close(self):
        self.dut_i2c.close()

    def lock_show(self):
        # Write to page 0x20100900
        self.i2c_write('0xFC', [0x00, 0x09, 0x10, 0x20])
        # Disable write protect
        self.i2c_write('0x01', [0x00])
        # Enable all modules
        self.i2c_write('0x04', [0x00*7])
        # Write to page 0x20100880
        self.i2c_write('0xFC', [0x00, 0x08, 0x10, 0x20])
        # Enable tds_pll_fb_div8
        self.i2c_write('0x94', [0x01])
        # Select test_mux1_sel as pll_fb_clk_div8
        self.i2c_write('0x84', [0x17])
        # Write to page 0x20100300
        self.i2c_write('0xFC', [0x00, 0x03, 0x10, 0x20])
        # Enable analog io mode(GPIO7), and set GPIO7 as output of test_mux1
        self.i2c_write('0x18', [0x08, 0x03])
        # Write to page 0x20100600
        self.i2c_write('0xFC', [0x00, 0x06, 0x10, 0x20])
        # Change PLL divider to 56 Dec
        self.i2c_write('0x07', [0x38])
        # Open PLL loop
        self.i2c_write('0x04', [0x64])
        # Close PLL loop
        self.i2c_write('0x04', [0x44])
        # Enable PLL calibration
        self.i2c_write('0x00', [0x01])
        # Write to page 0x20100880
        self.i2c_write('0xFC', [0x00, 0x08, 0x10, 0x20])
        # Disable resetting the FLL_counter and enable the logic block
        self.i2c_write('0x81', [0x3D])
        # Set FLL_rstb_div to be low
        self.i2c_write('0x81', [0x39])
        # Set FLL_rstb_div to be high
        self.i2c_write('0x81', [0x3D])
        # Write to page 0x20100300
        self.i2c_write('0xFC', [0X00, 0x03, 0x10, 0x20])
        # Bring FLL to GPIO0
        self.i2c_write('0x00', [0x08, 0x02])
        # close i2c
        self.i2c_close()

    def lock_not_show(self):
        # Write to page 0x20100900
        self.i2c_write('0xFC', [0x00, 0x09, 0x10, 0x20])
        # Disable write protect
        self.i2c_write('0x01', [0x00])
        # Enable all modules
        self.i2c_write('0x04', [0x00*7])
        # Write to page 0x20100880
        self.i2c_write('0xFC', [0x00, 0x08, 0x10, 0x20])
        # Enable tds_pll_fb_div8
        self.i2c_write('0x94', [0x01])
        # Write to page 0x20100600
        self.i2c_write('0xFC', [0x00, 0x06, 0x10, 0x20])
        # Change PLL divider to 56 Dec
        self.i2c_write('0x07', [0x38])
        # Open PLL loop
        self.i2c_write('0x04', [0x64])
        # Close PLL loop
        self.i2c_write('0x04', [0x44])
        # Enable PLL calibration
        self.i2c_write('0x00', [0x01])
        # Write to page 0x20100880
        self.i2c_write('0xFC', [0x00, 0x08, 0x10, 0x20])
        # Disable resetting the FLL_counter and enable the logic block
        self.i2c_write('0x81', [0x3D])
        # Set FLL_rstb_div to be low
        self.i2c_write('0x81', [0x39])
        # Set FLL_rstb_div to be high
        self.i2c_write('0x81', [0x3D])
        # close i2c
        self.i2c_close()


def main():
    i2c_address = 0x58
    PLL_FLL_show = FLL_PLL(i2c_address)
    PLL_FLL_show.lock_show()


if __name__ == "__main__":
    main()