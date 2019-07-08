from autobench.inst import power, stanford_research_systems_CG635, func_gen
from autobench.i2c.aa_i2c import AAReadWrite
from autobench import log
import time


class Write_Lock(object):
    # This function defines and verify write_lock function.
    def __init__(self, power_gpib1, power_gpib2, func_gen_gpib=10, CG635_gpib_addr=20, i2c_add=0x6c,):
        self.log = log(self.__class__.__name__)
        self.power1 = power.E3631A(power_gpib1)
        self.power2 = power.E3646A(power_gpib2)
        self.fun = func_gen.Agilent81130A(func_gen_gpib)
        self.lock_signal = stanford_research_systems_CG635.CG635(CG635_gpib_addr)
        self.dut_i2c = AAReadWrite(0, i2c_add, True)
        self.dut_i2c.bitrate = 100
        self.dut_i2c.aa_init()
        self.dut_i2c.length = 64

    def fun_set_up(self, channel, duty_cycle, vhigh, vlow, frequency, on_off_status):
        self.fun.duty_cycle(channel, duty_cycle)
        self.fun.vhigh_vlow(channel, vlow, vhigh)
        self.fun.freq(channel, frequency)
        self.fun.on_off(channel, on_off_status)

    def power1_setup(self, channel, voltage, current):
        self.power1.set_voltage(channel, voltage, current)

    def power2_setup(self, channel, ran, voltage, current):
        self.power2.select_channel(channel)
        self.power2.select_range(ran)
        self.power2.set_voltage(voltage, current)

    def power1_on_off(self, on_off_status):
        self.power1.on_off(on_off_status)

    def power2_on_off(self, on_off_status):
        self.power2.on_off(on_off_status)

    def research_system_setup(self, low_voltage, high_voltage, frequency):
        self.lock_signal.cmos_output(low_voltage, high_voltage)
        self.lock_signal.frequency(frequency)

    def research_system_on_off(self, run_state):
        self.lock_signal.run(run_state)

    def research_system_stop_level(self, stop_level):
        self.lock_signal.stop_level(stop_level)

    def i2c_write(self, byte, value):
        self.dut_i2c.aa_write_i2c(byte, value)

    def i2c_read(self, start_byte):
        return list(self.dut_i2c.aa_read_i2c(start_byte))

    def i2c_close(self):
        self.dut_i2c.close()

    def test_write_lock(self, write_byte):
        self.research_system_stop_level(0)
        self.i2c_write(0x80, write_byte)
        self.research_system_on_off(0)
        self.research_system_on_off(1)
        # self.research_system_on_off(0)
        # self.i2c_close()
        # self.power2_on_off(True)
        time.sleep(2)
        # result = self.i2c_read(0x80)
        # print result
        # self.log.info('The result is %s' % result)

def main():
    write_lock = Write_Lock(18, 19)
    # write_lock.power1_on_off(False)
    write_lock.power2_on_off(False)
    # write_lock.power1_setup(2, 3.3, 0.3)
    write_lock.power2_setup(1, 'low', 3.3, 0.1)
    write_lock.power2_on_off(True)
    time.sleep(0.1)
    write_lock.fun_set_up(1, 50, 0.8, 0, 100, 'on')
    write_lock.research_system_setup(3, 3.3, 500)
    write_byte = ['FF']*100
    write_lock.test_write_lock(write_byte)

if __name__ == '__main__':
    main()
