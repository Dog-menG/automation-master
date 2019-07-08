from autobench.i2c.aa_i2c import AAReadWrite
from autobench.inst.keithyley import Keithley2400
from autobench import log
import time


class LVDS_Aardvark(object):
    """This class is used to communicate with part using Aardvark."""
    def __init__(self,power_address, i2c_address):
        self.log = log(self.__class__.__name__)
        self.keithley = Keithley2400(power_address)
        self.dut_i2c = AAReadWrite(0, i2c_address, True)
        self.dut_i2c.length = 1

    def keithley_on_off(self, status):
        self.keithley.on_off(status)

    def keithley_setup(self, voltage, function, current):
        self.keithley.source_voltage(voltage)
        self.keithley.sense_compliance(function, current)

    def i2c_read(self, start_address, length):
        return list(self.dut_i2c.aa_read_i2c(start_address, length))

    def i2c_write(self, start_address, register_values):
        self.dut_i2c.aa_write_i2c(start_address, register_values)

    def i2c_close(self):
        self.dut_i2c.close()

    def lvds_500MHz(self):
        self.keithley_on_off('OFF')
        keithley_voltage = 1.8; keithley_compliance_function = 'CURRent'; keithley_current = 0.3
        self.keithley_setup(keithley_voltage, keithley_compliance_function, keithley_current)
        time.sleep(2)
        self.keithley_on_off('ON')
        time.sleep(1)
        # change Output0 source from PLL1 to PLL2.
        self.i2c_write(0x14, [0x06])
        self.log.info('change Output0 source from PLL1 to PLL2.')
        # change fractional divider from 0.5 to 0.(PLL from 6.25GHz to 6GHz.)
        self.i2c_write(0x41, [0x00])
        self.log.info('change fractional divider from 0.5 to 0.(PLL from 6.25GHz to 6GHz.)')
        time.sleep(0.5)
        # recalibration.
        self.i2c_write(0x58, [0xAE])
        time.sleep(0.5)
        self.i2c_write(0x58, [0x2E])
        self.log.info('recalibration.')
        time.sleep(0.5)
        # enable doubler of PLL2.
        self.i2c_write(0x50, [0x3C])
        self.log.info('enable doubler of PLL2.')
        time.sleep(0.5)
        # change PLL2 feedback divider to 60.
        self.i2c_write(0x40, [0x3C])
        self.log.info('change PLL2 feedback divider to 60.')
        time.sleep(0.5)
        # change PLL2 source from PLL1 to Xtal.
        self.i2c_write(0x2A, [0x04])
        self.log.info('change PLL2 source from PLL1 to Xtal.')
        time.sleep(0.5)
        # change output0 divider to 60.
        self.i2c_write(0x17, [0x0C])
        self.log.info('hange output0 divider to 12.')
        # Turn off Output1.
        self.i2c_write(0x24, [0x00])
        self.log.info('Turn off Output1.')
        # Turn off PLL1.
        self.i2c_write(0x32, [0x1D])
        self.log.info('Turn off PLL1.')
        # close Aardvark
        self.i2c_close()

    def lvds_539p0625MHz(self):
        self.keithley_on_off('OFF')
        keithley_voltage = 1.8; keithley_compliance_function = 'CURRent'; keithley_current = 0.3
        self.keithley_setup(keithley_voltage, keithley_compliance_function, keithley_current)
        self.keithley_on_off('ON')
        time.sleep(2)
        # change Output0 source from PLL1 to PLL2.
        self.i2c_write(0x14, [0x06])
        self.log.info('change Output0 source from PLL1 to PLL2.')
        # change PLL2 source from PLL1 to Xtal.
        self.i2c_write(0x2A, [0x04])
        self.log.info('change PLL2 source from PLL1 to Xtal.')
        time.sleep(0.5)
        # enable doubler of PLL2.
        self.i2c_write(0x50, [0x3C])
        self.log.info('enable doubler of PLL2.')
        time.sleep(0.5)
        # change PLL2 fractional feedback divider to 59.296875.
        self.i2c_write(0x40, [0x3B, 0x13])
        self.log.info('change PLL2 feedback divider to 59.296875.')
        time.sleep(0.5)
        # recalibration.
        self.i2c_write(0x58, [0xAE])
        time.sleep(0.5)
        self.i2c_write(0x58, [0x2E])
        self.log.info('recalibration.')
        time.sleep(0.5)
        # change output0 divider to 11.
        self.i2c_write(0x17, [0x0B])
        self.log.info('hange output0 divider to 11.')
        # optimize charge_pump and loop filter.
        self.i2c_write(0x52, [0x66])
        self.i2c_write(0x54, [0x18])
        self.log.info('optimize charge_pump and loop filter.')
        # Turn off Output1.
        self.i2c_write(0x24, [0x00])
        self.log.info('Turn off Output1.')
        # Turn off PLL1.
        self.i2c_write(0x32, [0x1D])
        self.log.info('Turn off PLL1.')
        # close Aardvark
        self.i2c_close()

    def lvds_554p6875MHz(self):
        self.keithley_on_off('OFF')
        keithley_voltage = 1.8; keithley_compliance_function = 'CURRent'; keithley_current = 0.3
        self.keithley_setup(keithley_voltage, keithley_compliance_function, keithley_current)
        self.keithley_on_off('ON')
        time.sleep(2)
        # change Output0 source from PLL1 to PLL2.
        self.i2c_write(0x14, [0x06])
        self.log.info('change Output0 source from PLL1 to PLL2.')
        # change PLL2 source from PLL1 to Xtal.
        self.i2c_write(0x2A, [0x04])
        self.log.info('change PLL2 source from PLL1 to Xtal.')
        time.sleep(0.5)
        # enable doubler of PLL2.
        self.i2c_write(0x50, [0x3C])
        self.log.info('enable doubler of PLL2.')
        time.sleep(0.5)
        # change PLL2 fractional feedback divider to 61.015625.
        self.i2c_write(0x40, [0x3D, 0x01])
        self.log.info('change PLL2 feedback divider to 61.015625.')
        time.sleep(0.5)
        # recalibration.
        self.i2c_write(0x58, [0xAE])
        time.sleep(0.5)
        self.i2c_write(0x58, [0x2E])
        self.log.info('recalibration.')
        time.sleep(0.5)
        # change output0 divider to 11.
        self.i2c_write(0x17, [0x0B])
        self.log.info('hange output0 divider to 11.')
        # optimize charge_pump and loop filter.
        self.i2c_write(0x52, [0x66])
        self.i2c_write(0x54, [0x18])
        self.log.info('optimize charge_pump and loop filter.')
        # Turn off Output1.
        self.i2c_write(0x24, [0x00])
        self.log.info('Turn off Output1.')
        # Turn off PLL1.
        self.i2c_write(0x32, [0x1D])
        self.log.info('Turn off PLL1.')
        # close Aardvark
        self.i2c_close()


def main():
    lvds = LVDS_Aardvark(24, 0x09)
    frequency = 554.6875
    if frequency == 500:
        lvds.lvds_500MHz()
    elif frequency == 539.0625:
        lvds.lvds_539p0625MHz()
    elif frequency == 554.6875:
        lvds.lvds_554p6875MHz()


if __name__ == '__main__':
    main()