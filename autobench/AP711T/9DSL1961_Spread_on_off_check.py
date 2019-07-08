from autobench.inst import power, scope, func_gen
from autobench import email_txt_msg
from autobench.i2c.aa_i2c import AAReadWrite
from autobench import log
import time


class spread_check(object):

    def __init__(self, power_gpib1, fun_gen_gpib, scope_address, i2c_address=0x6C):
        self.log = log(self.__class__.__name__)
        self.power1 = power.E3646A(power_gpib1)
        self.scope = scope.Keysight(scope_address)
        self.fun_gen = func_gen.Agilent81130A(fun_gen_gpib)
        self.dut_i2c = AAReadWrite(0, i2c_address, True)
        self.dut_i2c.length = 1

    def power1_setup(self, channel, range, voltage, current):
        self.power1.select_channel(channel)
        self.power1.select_range(range)
        self.power1.set_voltage(voltage, current)

    def power1_on_off(self, status):
        self.power1.on_off(status)

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
        self.scope.run_mode(run_mode)

    def scope_threshold(self, source1, thre_high, thre_mid, thre_low):
        self.scope.thresholds_general_absolute(source1, thre_high, thre_mid, thre_low)

    def measure(self, measurement, source):
        self.scope.measure_clear()
        self.scope.measure(measurement, source)
        time.sleep(0.5)
        return self.scope.get_result()[4]

    def email_message(self, source, destination, subject, text):
        self.email = email_txt_msg.Email_Txt_Msg()
        self.email.send_msg(source, destination, subject, text)

    def environment_setup(self, voltage):
        # power supply1 setup
        power1_channel = 1; power1_range = 'LOW'
        power1_voltage = voltage; power1_current = 0.2
        self.power1_setup(power1_channel, power1_range, power1_voltage, power1_current)
        self.power1_on_off(False)
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
        self.scope_threshold(self.source1, scope_threshold_high, scope_threshold_mid, scope_threshold_low)

    def test(self, mode):
        test_result = True
        while test_result:
            summary = open("mode_change_check.csv", "ab")
            if mode == 'spread_off':
                summary.writelines('This checks bp to spread off mode.\n')
                self.i2c_write(128, [0x54])
                time.sleep(1)
                self.i2c_write(137, [0x35])
                frequency = float(self.measure('FREQuency', 'Channel1')) / 10e5
                self.log.info('Now the frequency is %s MHz.' % frequency)
                summary.writelines('Now the frequency is %s MHz.\n' % frequency)
                difference = frequency - 100.0
                if difference < 1:
                    self.log.info('It is successful to change from BP to spread off.')
                    summary.writelines('It is successful to change from BP to spread off.\n')
                    self.power1_on_off('OFF')
                    time.sleep(0.1)
                    self.power1_on_off('ON')
                    test_result = True
                else:
                    self.log.info('It fails to change from BP to spread off.')
                    summary.writelines('It fails to change from BP to spread off.\n')
                    test_result = False
            else:
                summary.writelines('This checks bp to -0.5SS mode.\n')
                self.i2c_write(128, [0x54])
                time.sleep(1)
                self.i2c_write(137, [0xF5])
                frequency = float(self.measure('FREQuency', 'Channel1')) / 10e5
                self.log.info('Now the frequency is %s MHz.' % frequency)
                summary.writelines('Now the frequency is %s MHz.\n' % frequency)
                difference = frequency - 100.0
                if difference < 1:
                    self.log.info('It is successful to change from BP to -0.5SS mode.')
                    summary.writelines('It is successful to change from BP to -0.5SS mode.\n')
                    self.power1_on_off('OFF')
                    time.sleep(0.1)
                    self.power1_on_off('ON')
                    test_result = True
                else:
                    self.log.info('It fails to change from BP to -0.5SS mode.')
                    summary.writelines('It fails to change from BP to -0.5SS mode.\n')
                    test_result = False

#         # email setup
#         source = 'jun.gou@idt.com'; destination = 'jun.gou@idt.com'
#         subject = 'The test is done.'; text = 'The test is done, please take care!'
#         self.email_message(source, destination, subject, text)
#
#
# def email():
#     source = 'jun.gou@idt.com'; destination = 'jun.gou@idt.com'
#     subject = 'The test is done.'; text = 'The test is done, please take care!'
#     email_txt_msg.Email_Txt_Msg().send_msg(source, destination, subject, text)


def main():
    power_gpib1 = 19; fun_gen_gpib = 7; scope_address = 'TCPIP0::157.165.147.87::inst0::INSTR'
    voltage = 3.3
    Spread_check = spread_check(power_gpib1,fun_gen_gpib,scope_address)
    Spread_check.environment_setup(voltage)
    Spread_check.test('spread_off')


if __name__ == '__main__':
    main()
