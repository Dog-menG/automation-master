from autobench.inst import power, scope
from autobench.i2c.aa_i2c import AAReadWrite
from autobench import log
import time


class Output_Check(object):

    def __init__(self, power_gpib1, power_gpib2, i2c_address=0x6C):
        self.log = log(self.__class__.__name__)
        self.power1 = power.E3646A(power_gpib1)
        self.power2 = power.E3631A(power_gpib2)
        self.scope = scope.Keysight()
        self.dut_i2c = AAReadWrite(0, i2c_address, True)
        self.read_address = 0x80
        self.dut_i2c.length = 51

    def power1_setup(self, channel, range, voltage, current):
        self.power1.select_channel(channel)
        self.power1.select_range(range)
        self.power1.set_voltage(voltage, current)

    def power1_on_off(self, status):
        self.power1.on_off(status)

    def power2_setup(self, channel, voltage, current):
        self.power2.set_voltage(channel, voltage, current)

    def power2_on_off(self, status):
        self.power1.on_off(status)

    def i2c_read(self, read_address, read_length):
        return list(self.dut_i2c.aa_read_i2c(read_address, read_length))

    def scope_setup(self, memory_depth, sample_rate, time_scale, source, offset, scale, edge, trigger_level,
                    trigger_mode, run_mode, thre_mode, thre_high, thre_mid, thre_low):
        self.scope.measure_clear()
        self.scope.acquisition(memory_depth, sample_rate, time_scale)
        self.scope.source_on(source)
        self.scope.source_scale_setup(source, offset, scale)
        self.scope.trigger_setup(source, edge, trigger_level, trigger_mode)
        self.scope.thresholds_general(thre_mode, source, thre_high, thre_mid, thre_low)
        self.scope.run_mode(run_mode)

    def scope_measure_frequency(self, measurement, source, edge):
        self.scope.measure_clear()
        return float(self.scope.measure(measurement, source, edge)) / 10e5

    def function_check(self):
        # power supplies setup
        power1_chanel = 1; power1_voltage = 3.3; power1_current = 0.4; power1_range = 'LOW'
        power2_channel = 1; power2_voltage = 3.3; power2_current = 0.1
        self.power1_on_off('OFF')
        self.power2_on_off('OFF')
        self.power1_setup(power1_chanel, power1_range, power1_voltage, power1_current)
        self.power2_setup(power2_channel, power2_voltage, power2_current)
        self.power1_on_off('ON')
        self.power2_on_off('ON')

        # scope setup
        scope_memory_depth = 10e3; scope_sample_rate = 10e9; scope_timescale = 10e-9; source = 'Channel1'
        scope_offset = 0; scope_scale = 0.25; scope_trigger_edge = 'Rising'
        scope_trigger_level = 0; scope_trigger_mode = 'AUTO'; scope_run_mode = 'Run'
        scope_threshold_mode = 'PERCent'; scope_threshold_high = 80; scope_threshold_mid = 50; scope_threshold_low = 20
        self.scope_setup(scope_memory_depth, scope_sample_rate, scope_timescale, source, scope_offset,
                         scope_scale, scope_trigger_edge, scope_trigger_level, scope_trigger_mode, scope_run_mode,
                         scope_threshold_mode, scope_threshold_high, scope_threshold_mid, scope_threshold_low)
        scope_measurement = 'FREQuency'; scope_measurement_source = 'Channel1'; scope_measurement_edge = 'RISing'
        result = True
        while result:
            self.power2_on_off('OFF')
            time.sleep(1)
            frequency = self.scope_measure_frequency(scope_measurement, scope_measurement_source, scope_measurement_edge)
            self.log.info('Now the frequency of 9ZML1232F is %s MHz' % frequency)
            if frequency < 90 or frequency > 110:
                aardvark_read_value = self.i2c_read(self.read_address, self.dut_i2c.length)
                for i in range(0, len(aardvark_read_value)):
                    aardvark_read_value[i] = str(hex(aardvark_read_value[i]))
                self.log.info('The read back is %s' % aardvark_read_value)
                result = False
            else:
                self.log.info('The output of 9ZML1232F is still present and normal.')
                self.power2_on_off('ON')
                time.sleep(1)
                result = True


def main():
    power_gpib1 = 18
    power_gpib2 = 19
    ZML = Output_Check(power_gpib1, power_gpib2)
    ZML.function_check()


if __name__ == '__main__':
    main()

