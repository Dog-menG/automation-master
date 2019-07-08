from autobench.inst import power, scope, func_gen, stanford_research_systems_CG635
from autobench import email_txt_msg
from autobench import log
import os, time


class OE(object):
    """ This class is used to check 9ZX21910D_AP711T_O17, Whether output stops after removing input and asserting OE."""

    def __init__(self, power_gpib, synthesizer_gpib, function_generator_gpib):
        self.log = log(self.__class__.__name__)
        # self.scope = scope.Keysight()
        self.power = power.E3646A(power_gpib)
        self.function_generator = func_gen.Agilent81130A(function_generator_gpib)
        self.synthesizer = stanford_research_systems_CG635.CG635(synthesizer_gpib)

    def power_on_off(self, status):
        self.power.on_off(status)

    def power_setup(self, range, channel, voltage, current_limit):
        self.power.select_range(range)
        self.power.select_channel(channel)
        self.power.set_voltage(voltage, current_limit)

    def function_generator_on_off(self, channel, status):
        self.function_generator.on_off(channel, status)

    def function_generator_setup(self, channel, frequency, duty_cycle, vhigh, vlow):
        self.function_generator.freq(channel, frequency)
        self.function_generator.duty_cycle(channel, duty_cycle)
        self.function_generator.vhigh_vlow(channel, vlow, vhigh)

    def synthesizer_on_off(self, status):
        self.synthesizer.run(status)

    def synthesizer_setup(self, frequency, vhigh, vlow):
        self.synthesizer.frequency(frequency)
        self.synthesizer.cmos_output(vlow, vhigh)

    def scope_horizontal_setup(self, memory_depth, sample_rate, time_scale):
        self.scope.acquisition(memory_depth, sample_rate, time_scale)

    def scope_trigger_setup(self, source, trigger_edge, trigger_level, trigger_mode):
        self.scope.trigger_setup(source, trigger_edge, trigger_level, trigger_mode)

    def scope_run_mode(self, run_mode):
        self.scope.run_mode(run_mode)

    def scope_setup(self, memory_depth, sample_rate, time_scale, source1, offset1, scale1, source2, offset2, scale2,
                    source3, offset3, scale3, trigger_edge, trigger_level, trigger_mode, run_mode):
        self.scope_horizontal_setup(memory_depth, sample_rate, time_scale)
        self.scope.source_on(source1)
        self.scope.source_scale_setup(source1, offset1, scale1)
        self.scope.source_on(source2)
        self.scope.source_scale_setup(source2, offset2, scale2)
        self.scope.source_on(source3)
        self.scope.source_scale_setup(source3, offset3, scale3)
        self.scope_trigger_setup(source2, trigger_edge, trigger_level, trigger_mode)
        self.scope_run_mode(run_mode)

    def scope_save_screen(self, save_name):
        self.scope.screen_save(save_name)

    def pre_test_setup(self):
        # Function generator setup
        function_generator_channel = 1; function_generator_frequency = 100; function_generator_duty_cycle = 50
        function_generator_vhigh = 0.8; function_generator_vlow = 0
        self.function_generator_on_off(function_generator_channel, 'OFF')
        self.function_generator_setup(function_generator_channel, function_generator_frequency,
                                      function_generator_duty_cycle, function_generator_vlow, function_generator_vhigh)
        self.function_generator_on_off(function_generator_channel, 'ON')

        # Power supply setup
        power_range = 'Low'; power_channel = 1; power_voltage = 3.3; power_current_compliance = 0.6
        self.power_on_off('OFF')
        self.power_setup(power_range, power_channel, power_voltage, power_current_compliance)
        self.power_on_off('ON')

        # Synthesizer setup
        synthesizer_ferquency = 10; synthesizer_vhigh = 3.3; synthesizer_vlow = 0
        self.synthesizer_on_off(0)
        self.synthesizer_setup(synthesizer_ferquency, synthesizer_vhigh, synthesizer_vlow)

        # Scope setup
        # scope_memory_depth = 10e3; scope_sample_rate = 10e9; scope_timescale = 10e-9
        # scope_source1 = 'CHANnel1'; scope_offset1 = -1; scope_scale1 = 0.5
        # scope_source2 = 'CHANnel3'; scope_offset2 = 1; scope_scale2 = 0.5
        # scope_source3 = 'CHANnel4'; scope_offset3 = 1.65; scope_scale3 = 1.5
        # scope_trigger_edge = 'POSITive'; scope_trigger_level = 1.65; scope_trigger_mode = 'AUTO'
        # scope_run_mode = 'RUN'
        # self.scope_setup(scope_memory_depth, scope_sample_rate, scope_timescale,
        #                  scope_source1, scope_offset1, scope_scale1,
        #                  scope_source2, scope_offset2, scope_scale2,
        #                  scope_source3, scope_offset3, scope_scale3,
        #                  scope_trigger_edge, scope_trigger_level, scope_trigger_mode, scope_run_mode)
        # self.scope.wait()

    def check_oe_function(self):
        # Change scope horizontal and trigger setup
        # test_memory_depth = 40e6; test_sample_rate = 100e9; test_time_scale = 400e-6
        # test_trigger_source = 'CHANnel1';test_trigger_edge = 'Negative'
        # test_trigger_level = 0.4; test_trigger_mode = 'TRIGgered'
        # self.scope_horizontal_setup(test_memory_depth, test_sample_rate, test_time_scale)
        # self.scope_trigger_setup(test_trigger_source, test_trigger_edge, test_trigger_level, test_trigger_mode)

        # Turn off function generator
        function_generator_channel = 1
        self.function_generator_on_off(function_generator_channel, 'OFF')

        # Add 400us time delay
        time.sleep(0.0004)

        # Assert OE signal
        self.synthesizer_on_off(1)

        # # Wait for the scope to trigger
        # run_mode = 'STOP'
        # self.scope.wait()
        # self.scope_run_mode(run_mode)

def main():
    power_gpib = 18; synthesizer_gpib = 23; function_generator_gpib = 7
    check_OE = OE(power_gpib, synthesizer_gpib, function_generator_gpib)


    # check pre_test setup and environment
    check_OE.pre_test_setup()
    # raw_input("Press Enter to continue...")

    # check OE function after input stops and OE asserts
    check_OE.check_oe_function()

    # save the screen
    # path = r'S:\9ZX2xxx\9ZX21901\9ZX21901DKLF_AP711T-017Released\Outputs_stop_with_input_deassert_then_OE_stops'
    # name = 'differential_output_OE_pin_controls'
    # os.chdir(path)
    # filename = r"%s\%s" % (path, name)
    # print filename
    # check_OE.scope_save_screen(filename)

if __name__ == '__main__':
    main()