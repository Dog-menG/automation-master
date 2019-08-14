from autobench.inst import power, scope, func_gen
from autobench import email_txt_msg
from autobench.i2c.aa_i2c import AAReadWrite
from autobench import log
import time


class VCO_tune(object):

    def __init__(self, power_gpib, fun_gen_gpib, i2c_address=0x6C):
        self.log = log(self.__class__.__name__)
        self.power = power.E3646A(power_gpib)
        self.scope = scope.Keysight()
        self.fun_gen = func_gen.Agilent81130A(fun_gen_gpib)
        self.dut_i2c.length = 1
        self.dut_i2c = AAReadWrite(0, i2c_address, True)

    def power_setup(self, channel, range, voltage, current):
        self.power.select_channel(channel)
        self.power.select_range(range)
        self.power.set_voltage(voltage, current)

    def power_on_off(self, status):
        self.power.on_off(status)

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
        self.scope.source_setup(source1, offset, scale)
        self.scope.trigger_setup(source1, edge, trigger_level, trigger_mode)
        self.scope.source_on(source2)
        self.scope.source_setup(source2, offset, scale)
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

    def measure(self):
        # power supply setup
        power_channel = 1; power_range = 'LOW'
        power_voltage = 3.3; power_current = 0.2
        self.power_on_off(False)
        self.power_setup(power_channel, power_range, power_voltage, power_current)
        self.power_on_off(True)

        #function_generator setup
        fun_gen_channel = 1; fun_gen_frequency = 100; fun_gen_duty_cycle = 50
        fun_gen_high = 0.8; fun_gen_low = 0
        self.fun_on_off(fun_gen_channel, 'OFF')
        self.fun_setup(fun_gen_channel, fun_gen_frequency, fun_gen_duty_cycle, fun_gen_high, fun_gen_low)
        self.fun_on_off(fun_gen_channel, 'ON')

        #scope setup
        scope_memory_depth = 10e3; scope_sample_rate = 10e9; scope_timescale = 10e-9; source1 = 'Channel1'
        source2 = 'Channel3'; scope_offset = 0; scope_scale = 0.25; scope_trigger_edge = 'Rising'
        scope_trigger_level = 0; scope_trigger_mode = 'AUTO'; scope_run_mode = 'Run'; scope_threshold_mode = 'PERCent'
        scope_threshold_high = 80; scope_threshold_mid = 50; scope_threshold_low = 20
        self.scope_setup(scope_memory_depth, scope_sample_rate, scope_timescale, source1, source2, scope_offset,
                         scope_scale, scope_trigger_edge, scope_trigger_level, scope_trigger_mode, scope_run_mode)
        self.scope_threshold(source1, source2, scope_threshold_mode, scope_threshold_high, scope_threshold_mid,
                             scope_threshold_low)

        #measurement
        fb_result = []
        out_result = []
        fb_skew = [[0x01], [0x02], [0x03], [0x04], [0x05], [0x06], [0x07]]
        out_skew = [[0x10], [0x20], [0x30], [0x40], [0x50], [0x60], [0x70]]
        self.log.info('The I2O of PLL mode is %s ps.' % self.measure_delta_time(source1, source2))
        fb_result.append(self.measure_delta_time(source1, source2))
        out_result.append(self.measure_delta_time(source1, source2))
        for code in fb_skew:
            self.i2c_write(23, [0xC6])
            self.i2c_write(8, code)
            self.i2c_write(44, [0x00])
            time.sleep(0.3)
            self.i2c_write(44, [0x80])
            time.sleep(0.3)
            self.i2c_write(23, [0xC4])
            time.sleep(0.3)
            self.log.info('The delay to corresponding code is %s ps.' % self.measure_delta_time(source1, source2))
            fb_result.append(self.measure_delta_time(source1, source2))
        for code in out_skew:
            self.i2c_write(23, [0xC6])
            self.i2c_write(8, code)
            self.i2c_write(44, [0x00])
            time.sleep(0.3)
            self.i2c_write(44, [0x80])
            time.sleep(0.3)
            self.i2c_write(23, [0xC4])
            time.sleep(0.3)
            self.log.info('The delay to corresponding code is %s ps.' % self.measure_delta_time(source1, source2))
            out_result.append(self.measure_delta_time(source1, source2))

        # email setup
        source = 'jun.gou@idt.com'; destination = 'jun.gou@idt.com'
        subject = 'The test is done.'; text = 'The test is done, please take care!'
        self.email_message(source, destination, subject, text)