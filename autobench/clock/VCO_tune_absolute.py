from autobench.inst import power, scope, func_gen
from autobench import email_txt_msg
from autobench.i2c.aa_i2c import AAReadWrite
from autobench import log
import time


class VCO_tune(object):

    def __init__(self, power_gpib1, power_gpib2, fun_gen_gpib, i2c_address=0x6C):
        self.log = log(self.__class__.__name__)
        self.power1 = power.E3646A(power_gpib1)
        self.power2 = power.E3631A(power_gpib2)
        self.scope = scope.Keysight()
        self.fun_gen = func_gen.Agilent81130A(fun_gen_gpib)
        self.dut_i2c = AAReadWrite(0, i2c_address, True)
        self.dut_i2c.length = 1

    def power1_setup(self, channel, range, voltage, current):
        self.power1.select_channel(channel)
        self.power1.select_range(range)
        self.power1.set_voltage(voltage, current)

    def power1_on_off(self, status):
        self.power1.on_off(status)

    def power2_setup(self, channel, voltage, current):
        self.power2.set_voltage(channel, voltage, current)

    def power2_on_off(self, status):
        self.power2.on_off(status)

    def fun_setup(self, channel, frequency, duty_cycle, vhigh, vlow):
        self.fun_gen.freq(channel, frequency)
        self.fun_gen.duty_cycle(channel, duty_cycle)
        self.fun_gen.vhigh_vlow(channel, vlow, vhigh)

    def fun_on_off(self, channel, status):
        self.fun_gen.on_off(channel, status)

    def i2c_write(self, start_address, resigster_values):
        self.dut_i2c.aa_write_i2c(start_address, resigster_values)

    def scope_setup(self, memory_depth, sample_rate, time_scale, source1, source2, offset, scale, edge, trigger_level,
                    trigger_mode, run_mode):
        self.scope.measure_clear()
        self.scope.acquisition(memory_depth, sample_rate, time_scale)
        self.scope.source_on(source1)
        self.scope.source_scale_setup(source1, offset, scale)
        self.scope.trigger_setup(source1, edge, trigger_level, trigger_mode)
        self.scope.source_on(source2)
        self.scope.source_scale_setup(source2, offset, scale)
        self.scope.trigger_setup(source2, edge, trigger_level, trigger_mode)
        self.scope.run_mode(run_mode)

    def scope_threshold(self, source1, source2, mode, thre_high, thre_mid, thre_low):
        self.scope.thresholds_general(mode, source1, thre_high, thre_mid, thre_low)
        self.scope.thresholds_general(mode, source2, thre_high, thre_mid, thre_low)

    def measure_delta_time(self, input_source, output_source):
        self.scope.measure_clear()
        self.scope.measure_delta_time(input_source, output_source)
        time.sleep(0.5)
        return self.scope.get_result()[4]

    def email_message(self, source, destination, subject, text):
        self.email = email_txt_msg.Email_Txt_Msg()
        self.email.send_msg(source, destination, subject, text)

    def setup(self,voltage):
        # power supply1 setup
        power1_channel = 1; power1_range = 'LOW'
        power1_voltage = voltage; power1_current = 0.2
        self.power1_setup(power1_channel, power1_range, power1_voltage, power1_current)
        # self.power1_on_off(False)
        self.power1_on_off(True)

        # power supply2 setup
        power2_channel = 2; power2_voltage = 3.3; power2_current = 0.2
        self.power2_setup(power2_channel, power2_voltage, power2_current)
        self.power1_on_off(True)

        #function_generator setup
        fun_gen_channel = 1; fun_gen_frequency = 100; fun_gen_duty_cycle = 50
        fun_gen_high = 0.8; fun_gen_low = 0
        self.fun_on_off(fun_gen_channel, 'OFF')
        self.fun_setup(fun_gen_channel, fun_gen_frequency, fun_gen_duty_cycle, fun_gen_high, fun_gen_low)
        self.fun_on_off(fun_gen_channel, 'ON')

        #scope setup
        scope_memory_depth = 10e3; scope_sample_rate = 10e9; scope_timescale = 10e-9; self.source1 = 'Channel1'
        self.source2 = 'Channel3'; scope_offset = 0; scope_scale = 0.25; scope_trigger_edge = 'Rising'
        scope_trigger_level = 0; scope_trigger_mode = 'AUTO'; scope_run_mode = 'Run'; scope_threshold_mode = 'PERCent'
        scope_threshold_high = 80; scope_threshold_mid = 50; scope_threshold_low = 20
        self.scope_setup(scope_memory_depth, scope_sample_rate, scope_timescale, self.source1, self.source2, scope_offset,
                         scope_scale, scope_trigger_edge, scope_trigger_level, scope_trigger_mode, scope_run_mode)
        self.scope_threshold(self.source1, self.source2, scope_threshold_mode, scope_threshold_high, scope_threshold_mid,
                             scope_threshold_low)

    def measure(self, temperature, voltage):
        #csv file
        summary = open("skew_tune.csv", "ab")
        summary.writelines('This is with %sC_%sV\n' % (temperature, voltage))

        #measurement
        self.power1_on_off('OFF')
        time.sleep(1)
        self.power1_on_off('ON')
        time.sleep(1)
        fb_skew = [[0x00],[0x01], [0x02], [0x03], [0x04], [0x05], [0x06], [0x07]]
        for i in range(0,8):
            self.i2c_write(137, fb_skew[i])
            time.sleep(2)
            self.log.info('The delay to corresponding code %s is %s ps.'
                          % (fb_skew[i] ,float(self.measure_delta_time(self.source1, self.source2))*1e12))
            summary.writelines('The delay to corresponding code %s is %s ps.\n'
                          % (fb_skew[i] ,float(self.measure_delta_time(self.source1, self.source2))*1e12))
            self.power2_on_off('OFF')
            self.power2_on_off('ON')
            time.sleep(2)
            self.log.info('After PD then power up. The delay to corresponding code %s is %s ps.'
                          % (fb_skew[i] ,float(self.measure_delta_time(self.source1, self.source2))*1e12))
            summary.writelines('After PD then power up. The delay to corresponding code %s is %s ps.\n'
                          % (fb_skew[i] ,float(self.measure_delta_time(self.source1, self.source2))*1e12))

        # # email setup
        # source = 'jun.gou@idt.com'; destination = 'jun.gou@idt.com'
        # subject = 'The test is done.'; text = 'The test is done, please take care!'
        # self.email_message(source, destination, subject, text)


def email():
    source = 'jun.gou@idt.com'; destination = 'jun.gou@idt.com'
    subject = 'The test is done.'; text = 'The test is done, please take care!'
    email_txt_msg.Email_Txt_Msg().send_msg(source, destination, subject, text)


def main():
    vco_tune = VCO_tune(19,18,7)
    temperature = 25
    voltage = 3.3
    vco_tune.setup(voltage)
    vco_tune.measure(temperature, voltage)


if __name__ == '__main__':
    main()
