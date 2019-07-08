from autobench.inst import func_gen, power
from autobench.inst.scope import Keysight
from autobench import log
from i2c.aa_i2c import AAReadWrite
import csv, os, time
import pandas as pd


class SweepFrequency(object):

    def __init__(self, power_gpib, func_gen_gpib, i2c_address):
        self.log = log(self.__class__.__name__)
        self.power = power.E3646A(power_gpib)
        self.function = func_gen.Agilent81130A(func_gen_gpib)
        self.myscope = Keysight()
        self.dut_i2c = AAReadWrite(0, i2c_address, True)
        self.dut_i2c.length = 1

    def fun_frequency(self, channel, frequency):
        self.function.freq(channel, frequency)

    def fun_on_off(self, channel, status):
        self.function.on_off(channel, status)

    def i2c_read(self, start_address, length):
        return list(self.dut_i2c.aa_read_i2c(start_address, length))

    def i2c_write(self, start_address, resigster_values):
        self.dut_i2c.aa_write_i2c(start_address, resigster_values)

    def power_setup(self, channel, power_range, voltage, current):
        self.power.select_channel(channel)
        self.power.select_range(power_range)
        self.power.set_voltage(voltage, current)

    def power_on_off(self, status):
        self.power.on_off(status)

    def scope_display_clear(self):
        self.myscope.clear_dispay()
        self.myscope.wait()

    def scope_measure(self, source, frequency, duty_cycle, slew_rate, cycle_jitter, rising_edge, falling_edge):
        self.myscope.measure_clear()
        self.myscope.measure(source, duty_cycle, rising_edge)
        self.myscope.measure(source, frequency, rising_edge)
        self.myscope.measure(source, slew_rate, rising_edge)
        self.myscope.measure(source, slew_rate, falling_edge)
        self.myscope.measure(source, cycle_jitter, rising_edge)
        self.scope_wait()
        time.sleep(2)
        return self.myscope.get_result()

    def scope_save_screen(self, path):
        self.myscope.screen_save(path)

    def scope_setup(self, memory_depth, sample_rate, time_scale, source, offset, edge, trigger_level,
                    trigger_mode, run_mode, status):
        self.myscope.source_on(source)
        self.scope_display_clear()
        self.scope_vertical_full_swing(source, offset)
        self.myscope.measure_clear()
        self.myscope.acquisition(memory_depth, sample_rate, time_scale)
        self.myscope.trigger_setup(source, edge, trigger_level, trigger_mode)
        self.myscope.run_mode(run_mode)
        self.myscope.measure_all_edges(status)

    def scope_threshold(self, source, mode, thre_high, thre_mid, thre_low):
        self.myscope.thresholds_general(mode, source, thre_high, thre_mid, thre_low)

    def scope_vertical_full_swing(self, source, offset):
        self.myscope.measure(source, 'VPP')
        vertical = self.myscope.get_result()[4]
        self.myscope.source_range_setup(source, vertical, offset)

    def scope_wait(self):
        status = self.myscope.require_status().strip()
        while status != '1':
            status = str(self.myscope.require_status().strip())

    def sweep(self):
        unit_number = 1;output = 0

        # Scope setup
        memory_depth = 40e6; sample_rate = 20e9; time_scale = 200e-6
        scope_source = 'CHANnel1'; offset = 0
        trigger_edge = 'RISing'; trigger_level = 0; trigger_mode = 'TRIGgered'; run_mode = 'RUN'
        measure_all_edge_status = 'ON'
        thre_high = 0.15; thre_mid = 0; thre_low = -0.15; thre_mode = 'ABSolute'
        measurement1 = 'FREQuency'; measurement2 = 'DUTYcycle'; measurement3 = 'SLEWrate'
        measurement4 = 'CTCJitter'; rising_edge = 'RISing'; falling_edge = 'FALLing'
        self.scope_setup(memory_depth, sample_rate, time_scale, scope_source, offset, trigger_edge, trigger_level,
                         trigger_mode, run_mode, measure_all_edge_status)
        self.scope_threshold(scope_source, thre_mode, thre_high, thre_mid, thre_low)
        self.scope_wait()

        path = r'S:\9ZXLxxx\9ZXL12xx_AP711T\9ZXL12xxE_AP711T-021\LvInput'
        os.chdir(path)
        input = pd.read_excel('test.xlsx')
        loop_number = len(input.index)

        for i in range(0,loop_number):
            # Power supply setup
            power_supply = str(input.iloc[i][0]).split(',')
            voltage_range = 'Low'
            voltage1 = power_supply[0]; current_compliance1 = power_supply[1]
            voltage2 = power_supply[2]; current_compliance2 = power_supply[3]
            self.power_setup(1, voltage_range, voltage1, current_compliance1)
            self.power_setup(1, voltage_range, voltage2, current_compliance2)
            self.power_on_off('OFF')
            self.power_on_off('OM')

            # Function Generator setup
            function_generator = str(input.iloc[i][1]).split(',')
            fun_channel = function_generator[0]; frequency = function_generator[1]; duty_cycle = function_generator[2]
            vhigh = function_generator[3]; vlow = function_generator[4]
            self.function.function_generator_setting(fun_channel, frequency, duty_cycle, vlow, vhigh, 'ON')

            # save_name&path_setting
            temp = str(input.iloc[i][2]); path = str(input.iloc[i][3]); part = str(input.iloc[i][4])

            #  Sweep frequency of BP mode
            self.function.freq(fun_channel, frequency)
            result = self.scope_measure(scope_source, measurement1, measurement2, measurement3, measurement4, rising_edge, falling_edge)
            with open("test.csv", "ab") as res:
                writer = csv.writer(res, delimiter=",")
                writer.writerow(result)
            time.sleep(1)
            path_file_name = r"%s\%smV_%sC_%sMHz_%s_Unit%s_output%s" % (path, int(voltage1 * 1000), temp, frequency, part, unit_number, output)
            self.scope_save_screen(path)
            self.scope_wait()
            self.log.info('Sweep of %sMHz is done' % frequency)
        self.log.info('It is finished.')


def main():
    power_gpib = 18; func_gpib = 7; i2c_address = '0x6C'
    BP_sweep_frequency = SweepFrequency(power_gpib, func_gen, i2c_address)
    BP_sweep_frequency.sweep()

if __name__ == '__main__':
    main()
