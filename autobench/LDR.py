from autobench.inst import power, func_gen, scope
from autobench.i2c.aa_i2c import AAReadWrite
from autobench import log
import pandas as pd
import os, time
"marvell"


class LDR(object):
    # jun gou
    """This class is used to measure LDR of AP711T"""
    def __init__(self, power_gpib, fun_gen_gpib, i2c_address):
        self.log = log(self.__class__.__name__)
        self.power = power.E3646A(power_gpib)
        self.scope = scope.Keysight()
        self.scope.timeout = 600000
        self.fun_gen = func_gen.Agilent81130A(fun_gen_gpib)
        self.dut_i2c = AAReadWrite(0, i2c_address, True)
        self.dut_i2c.length = 1

    def i2c_read(self, start_address, length):
        return list(self.dut_i2c.aa_read_i2c(start_address, length))

    def i2c_write(self, start_address, resigster_values):
        self.dut_i2c.aa_write_i2c(start_address, resigster_values)

    def i2c_close(self):
        self.dut_i2c.close()

    def power_on_off(self, status):
        self.power.on_off(status)

    def power_setup(self, channel, voltage, current):
        self.power.select_channel(channel)
        self.power.set_voltage(voltage, current)

    def fun_on_off(self, channel, status):
        self.fun_gen.on_off(channel, status)

    def fun_setup(self, channel, duty_cycle, frequency, vlow, vhigh):
        self.fun_gen.duty_cycle(channel, duty_cycle)
        self.fun_gen.freq(channel, frequency)
        self.fun_gen.vhigh_vlow(channel, vlow, vhigh)

    def scope_display_clear(self):
        self.scope.clear_dispay()
        self.scope.wait()

    def scope_run_mode(self, run_mode):
        self.scope.run_mode(run_mode)

    def scope_vertical_full_swing(self, source):
        self.scope.auto_scale_vertical(source)
        self.scope_wait()
        time.sleep(5)
        self.scope.measure_vertical('VPP', source)
        vertical = self.scope.get_result()[4]
        self.scope_wait()
        self.scope.measure_vertical('VTOP', source)
        vtop = self.scope.get_result()[4]
        self.scope_wait()
        self.scope.measure_vertical('VBASE', source)
        vbase = self.scope.get_result()[4]
        self.scope_wait()
        offset = (float(vtop) + float(vbase)) / 2
        self.scope.source_range_setup(source, vertical, offset)

    def scope_threshold_abosulte(self, source, thre_high, thre_mid, thre_low):
        self.scope.thresholds_general_absolute(source, thre_high, thre_mid, thre_low)

    def scope_trend_measure(self, function_number, measurement_number, trend_status):
        self.scope.function_measure_trend(function_number, measurement_number)
        self.scope.source_on_off(function_number, trend_status)

    def scope_measure(self, measurement, source):
        self.scope.measure(measurement, source)

    def scope_save_waveform(self, source, file_name, file_type, header):
        self.scope.waveform_save(source, file_name, file_type, header)

    def scope_wait(self):
        status = self.scope.require_status().strip()
        while status != '1':
            status = str(self.scope.require_status().strip())

    def scope_setup(self, memory_depth, sample_rate, time_scale, source, edge, trigger_level,
                    trigger_mode, run_mode, status):
        self.scope.source_on(source)
        self.scope.run_mode('RUN')
        self.scope_display_clear()
        self.scope_vertical_full_swing(source)
        self.scope.measure_clear()
        self.scope.acquisition(memory_depth, sample_rate, time_scale)
        self.scope.trigger_setup(source, edge, trigger_level, trigger_mode)
        self.scope_run_mode(run_mode)
        self.scope.measure_all_edges(status)

    def LDR_measure(self):

        # Scope setup
        memory_depth = 40e6; sample_rate = 20e9; time_scale = 200e-6
        source = 'CHANnel2'
        edge = 'RISing'; trigger_level = 0; trigger_mode = 'TRIGgered'; run_mode = 'RUN'; all_edge_status = 'ON'
        thre_high = 0.15; thre_mid = 0; thre_low = -0.15
        measurement = 'PERiod'; function_number = 2; measurement_number = 1; trend_status = 'ON'
        self.scope_threshold_abosulte(source, thre_high, thre_mid, thre_low)

        # save_name&path_setting
        path = r'S:\9ZXLxxx\9ZXL19xx_AP711T\9ZXL19xxDKLF_AP711T-026\1930_LDR\input_file'
        os.chdir(path)
        output = 0
        unit_number = 7

        # get input from input_file
        input = pd.read_excel('85C_9FGV1006_spread_on_VDDIO=3.135V.xlsx')
        loop_number = len(input.index)

        for i in range(0,loop_number):
            power_supply = str(input.iloc[i][0]).split(',')
            channel1 = int(power_supply[0]); voltage1 = float(power_supply[1]); current1 = power_supply[2]

            function_generator = str(input.iloc[i][1]).split(',')
            fun_channel = function_generator[0]; fun_frequency = function_generator[1]; fun_duty_cycle = function_generator[2]
            fun_vhigh = function_generator[3]; fun_vlow = function_generator[4]

            Aardvark = str(input.iloc[i][2]).split(',')
            register_values = []
            start_address = Aardvark[0]; register_values.append(int(Aardvark[1],16))

            temp = str(input.iloc[i][3]); save_path = str(input.iloc[i][4])
            part = str(input.iloc[i][5]); Label = str(input.iloc[i][6])
            time.sleep(0.1)

            # power supply setup
            self.power_on_off('OFF')
            self.power_setup(channel1, voltage1, current1)
            self.power_on_off('ON')

            # scope setup
            self.scope_setup(memory_depth, sample_rate, time_scale, source, edge, trigger_level, trigger_mode, run_mode,
                             all_edge_status)
            self.scope_wait()

            # function generator setup
            self.fun_setup(fun_channel, fun_duty_cycle, fun_frequency, fun_vhigh, fun_vlow)
            self.fun_on_off(fun_channel, 'ON')
            time.sleep(0.1)

            # LDR measure
            self.scope_display_clear()
            self.i2c_write(start_address, register_values)
            self.scope_measure(measurement, source)
            self.scope_wait()
            self.scope_trend_measure(function_number, measurement_number, trend_status)
            self.scope_wait()
            time.sleep(5)
            measure_run_mode = 'Single'
            self.scope_run_mode(measure_run_mode)
            self.scope_wait()
            time.sleep(5)

        # Waveform save
            waveform_source = 'FUNCtion2'
            path_file_name = r"%s\%smV_%sC_%s_Unit%s_output%s_%s" % (save_path, int(voltage1*1000), temp, part, unit_number, output, Label)
            # path_file_name = r"%s\%smV_%sC_%s_Unit%s_%s" % (save_path, int(voltage1 * 1000), temp, part, unit_number, Label)
            file_type = 'TXT'
            Header_status = 'OFF'
            self.scope_save_waveform(waveform_source, path_file_name, file_type, Header_status)
            self.scope_wait()
            time.sleep(2)
            self.log.info('This round is done.')

        self.i2c_close()

def main():
    power_gpib = 18; fun_gen_gpib = 7; i2c_address = 0x6C
    LDR_measure = LDR(power_gpib, fun_gen_gpib, i2c_address)
    LDR_measure.LDR_measure()

if __name__ == "__main__":
    main()
