from autobench import log
from autobench.inst import scope
from autobench.inst import power
from autobench.inst import func_gen
from datetime import datetime
import time
import os
import pandas as pd




class Automotive(object):

    def __init__(self, scope_ip_address, fun_gen_gpib_address, power_gpib_address):
        self.log = log(self.__class__.__name__)
        self.scope = scope.Keysight(scope_ip_address)
        self.fun_gen = func_gen.Agilent81130A(fun_gen_gpib_address)
        self.power_supply = power.E3632_3_4A(power_gpib_address)

    def fun_gen_frequency(self, channel, frequency):
        self.fun_gen.freq(channel, frequency)

    def fun_gen_on_off(self, channel, status):
        self.fun_gen.on_off(channel, status)

    def fun_gen_vhigh_vlow(self, channel, vlow, vhigh):
        self.fun_gen.vhigh_vlow(channel, vlow, vhigh)

    def fun_gen_setup(self, channel, frequency, duty_cycle, vlow, vhigh):
        self.fun_gen_frequency(channel, frequency)
        self.fun_gen.duty_cycle(channel, duty_cycle)
        self.fun_gen_vhigh_vlow(channel, vlow, vhigh)

    def measure_and_save(self, source1, source2, source3, result, picture_name):
        self.scope_measure_delta_time(source3, source2)
        self.scope_measure_delta_time(source3, source1)
        self.scope_measure_time('FALLtime', source3)
        self.scope_measure_time('RISetime', source3)
        self.scope_measure('DUTYcycle', source3)
        self.scope_measure_time('FALLtime', source2)
        self.scope_measure_time('RISetime', source2)
        self.scope_measure('DUTYcycle', source2)
        self.scope_measure_time('FALLtime', source1)
        self.scope_measure_time('RISetime', source1)
        self.scope_measure('DUTYcycle', source1)
        self.scope.result_display_portion(40)
        self.scope_display_clear()
        time.sleep(2)
        result.append(self.scope.get_result())
        self.scope_save_picture(picture_name)
        return result

    def read_current(self):
        current = self.power_supply.read_current()
        return current

    def power_on_off(self, status):
        self.power_supply.on_off(status)

    def power_setup(self, range, voltage, current):
        self.power_supply.select_range(range)
        self.power_supply.set_voltage(voltage, current)

    def scope_setup(self, frequency, vdd, sample_rate, source1, source2, source3, edge, trigger_mode, run_mode):
        self.scope.run_mode(run_mode)
        self.scope_average_on_off('ON')
        time_scale = float(1 / (5*frequency))
        memory_depth = float(sample_rate * 10 * time_scale)
        trigger_level = float(vdd/2)
        self.scope.acquisition(memory_depth, sample_rate, time_scale)
        self.scope.source_on(source1)
        self.scope.source_on(source2)
        self.scope.source_on(source3)
        vertical_setup = self.scope_vertical_initial(source1)
        self.scope_vertical_setup(source1, vertical_setup[2].split('\n')[0], vertical_setup[1], vertical_setup[0])
        self.scope_vertical_setup(source2, vertical_setup[2].split('\n')[0], vertical_setup[1], vertical_setup[0])
        self.scope_vertical_setup(source3, vertical_setup[2].split('\n')[0], vertical_setup[1], vertical_setup[0])
        self.scope.trigger_setup(source1, edge, trigger_level, trigger_mode)
        self.scope.measure_statistics_setting('Mean')

    def scope_acquisition(self, frequency, sample_rate):
        time_scale = float(1 / (5 * frequency))
        memory_depth = float(sample_rate * 10 * time_scale)
        self.scope.acquisition(memory_depth, sample_rate, time_scale)

    def scope_average_on_off(self, mode):
        self.scope.average_mode_on_off(mode)

    def scope_display_clear(self):
        self.scope.clear_dispay()

    def scope_measure(self, measurement, source):
        self.scope.measure(measurement, source, direction='RISing')

    def scope_measure_clear(self):
        self.scope.measure_clear()

    def scope_measure_delta_time(self, input_source, output_source):
        self.scope.measure_delta_time(input_source, output_source)

    def scope_measure_time(self, measurement, source):
        self.scope.measure_time(measurement, source)

    def scope_measure_vertical(self, measurement, source):
        self.scope.measure_vertical(measurement, source)

    def scope_result_display_portion(self, portion_number):
        self.scope.result_display_portion(portion_number)

    def scope_save_picture(self, file_name):
        self.scope.screen_save(file_name)
        self.scope_measure_clear()
        self.scope_wait()

    def scope_trigger(self, source, vdd, edge, trigger_mode):
        trigger_level = float(vdd/2)
        self.scope.trigger_setup(source, edge, trigger_level, trigger_mode)

    def scope_vertical_initial(self, source):
        if 'FUNCtion' in source:
            self.scope.function_vertical_mode(source, 'AUTO')
            self.scope.function_vertical_mode(source, 'MANual')
        else:
            pass
        self.scope.auto_scale_vertical(source)
        self.scope_wait()
        self.scope_measure_vertical('VPP', source)
        self.scope_measure_vertical('VMAX', source)
        self.scope_measure_vertical('VMIN', source)
        time.sleep(2)
        vertical_setup = self.scope.get_result()
        self.scope_wait()
        self.scope.measure_clear()
        return vertical_setup

    def scope_vertical(self, source):
        if 'FUNCtion' in source:
            self.scope.function_vertical_mode(source, 'AUTO')
            self.scope.function_vertical_mode(source, 'MANual')
        else:
            pass
        self.scope_wait()
        self.scope_measure_vertical('VPP', source)
        self.scope_measure_vertical('VMAX', source)
        self.scope_measure_vertical('VMIN', source)
        time.sleep(2)
        vertical_setup = self.scope.get_result()
        self.scope_wait()
        self.scope.measure_clear()
        return vertical_setup

    def scope_vertical_setup(self, source, vertical, vtop, vbase):
        offset = (float(vtop) + float(vbase)) / 2
        self.scope.source_range_setup(source, float(vertical), offset)

    def scope_wait(self):
        status = self.scope.require_status().strip()
        while status != '1':
            status = str(self.scope.require_status().strip())

    def measure(self):
        # power supply setup
        voltage_range = 'LOW'; voltage = 3.3; current_compliance = 0.3
        self.power_on_off('OFF')
        self.power_setup(voltage_range, voltage, current_compliance)
        self.power_on_off('ON')
        time.sleep(0.1)

        # function generator setup
        channel = 1; frequency = 100.0; duty_cycle = 50; vlow = 0; vhigh = 3.3
        self.fun_gen_on_off(channel, 'OFF')
        self.fun_gen_setup(channel, frequency, duty_cycle, vlow, vhigh)
        self.fun_gen_on_off(channel, 'ON')
        time.sleep(0.1)

        # scope setup
        frequency = 100e6; vdd = 3.3; sample_rate = 10e9; source1 = 'CHANnel1'; source2 = 'CHANnel2'
        source3 = 'CHANnel3'; edge = 'POSitive'; trigger_mode = 'AUTO'; run_mode = 'RUN'
        self.scope_setup(frequency, vdd, sample_rate, source1, source2, source3, edge, trigger_mode, run_mode)

        # save index setup
        unit_number = 5; temp = 25
        path = r'J:\PRODUCT\CHAR\IDT5Pxxxxx\5PBxxxx\5PB11xx\5PB1104CMGI_AP669T-931_Automotive\ATE'
        save_path = path + r'\%sC' % temp
        if not os.path.isdir(save_path):
            os.mkdir(save_path)
        else:
            pass

        # voltages and frequencies loop
        frequencies = [40.0, 100.0, 156.25, 200.0]
        # frequencies = [10.0]

        if temp == 25:
            voltages = [3.3, 2.5, 1.8]
        elif temp == 125:
            voltages = [3.135, 2.375, 1.71]
        else:
            voltages = [3.465, 2.625, 1.89]

        # measurement
        for voltage in voltages:
            self.fun_gen_vhigh_vlow(channel, 0, voltage)
            self.power_setup(voltage_range, voltage, current_compliance)
            self.scope.thresholds_general_absolute('ALL', 0.8 * voltage, 0.5 * voltage, 0.2 * voltage)
            self.scope.thresholds_rfall_absolute('ALL', 0.8 * voltage, 0.5 * voltage, 0.2 * voltage)
            vertical_setup = self.scope_vertical('CHANnel1')
            self.scope_trigger('CHANnel1', voltage, 'POSitive', 'AUTO')
            self.scope_vertical_setup('CHANnel1', vertical_setup[2].split('\n')[0], vertical_setup[1], vertical_setup[0])
            self.scope_vertical_setup('CHANnel2', vertical_setup[2].split('\n')[0], vertical_setup[1], vertical_setup[0])
            self.scope_vertical_setup('CHANnel3', vertical_setup[2].split('\n')[0], vertical_setup[1], vertical_setup[0])
            # time.sleep(1)
            for frequency in frequencies:
                self.scope_acquisition(frequency*1e6, 10e9)
                self.fun_gen_frequency(channel, frequency)
                date_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
                save_picture_name = save_path + r'\Unit%s_%sC_%smV_%sMHz_%s' % (unit_number, temp,
                                                                             int(voltage*1000), int(frequency), date_time)
                result = []
                result = self.measure_and_save('CHANnel3', 'CHANnel2', 'CHANnel1', result, save_picture_name)
                time.sleep(1)
                classified_result = [y for x in result for y in x]
                classified_result.insert(0, str(frequency))
                classified_result.insert(0, str(voltage))
                classified_result.insert(0, str(temp))
                classified_result.insert(0, 'Unit' + str(unit_number))
                current = self.read_current()
                classified_result.append(current)
                classified_result.append(date_time)
                time.sleep(1)
                columns_name = ['Unit_number', 'Temperature(C)', 'Voltage(V)', 'Frequency(MHz)',
                                'CH3_Duty_cycle(%)', 'CH3_Rise_time(ps)', 'CH3_Fall_time(ps)',
                                'CH2_Duty_cycle(%)', 'CH2_Rise_time(ps)', 'CH2_Fall_time(ps)',
                                'Clkin_Duty_cycle(%)', 'Clkin_Rise_time(ps)', 'Clkin_Fall_time(ps)',
                                'In_to_CH3_skew(ns)', 'In_to_CH2_skew(ns)', 'current(mA)', 'date_time']
                classified_dataframe = pd.DataFrame(classified_result).transpose()
                classified_dataframe.columns = columns_name
                insert_row = pd.Series([''] * 17, index=columns_name)
                classified_dataframe['Output2_Duty_cycle(%)'] = float(classified_dataframe['Output2_Duty_cycle(%)'])
                classified_dataframe['Output2_Rise_time(ps)'] = float(classified_dataframe['Output2_Rise_time(ps)']) * 10e11
                classified_dataframe['Output2_Fall_time(ps)'] = float(classified_dataframe['Output2_Fall_time(ps)']) * 10e11
                classified_dataframe['Output0_Duty_cycle(%)'] = float(classified_dataframe['Output0_Duty_cycle(%)'])
                classified_dataframe['Output0_Rise_time(ps)'] = float(classified_dataframe['Output0_Rise_time(ps)']) * 10e11
                classified_dataframe['Output0_Fall_time(ps)'] = float(classified_dataframe['Output0_Fall_time(ps)']) * 10e11
                classified_dataframe['Clkin_Duty_cycle(%)'] = float(classified_dataframe['Clkin_Duty_cycle(%)'])
                classified_dataframe['Clkin_Rise_time(ps)'] = float(classified_dataframe['Clkin_Rise_time(ps)']) * 10e11
                classified_dataframe['Clkin_Fall_time(ps)'] = float(classified_dataframe['Clkin_Fall_time(ps)']) * 10e11
                classified_dataframe['In_to_Out2_skew(ns)'] = float(classified_dataframe['In_to_Out2_skew(ns)']) * 10e8
                classified_dataframe['In_to_Out0_skew(ns)'] = float(classified_dataframe['In_to_Out0_skew(ns)']) * 10e8
                classified_dataframe = classified_dataframe.append(insert_row, ignore_index=True)
                save_file_name = (save_path + r'\%sC.csv') % temp
                classified_dataframe.to_csv(save_file_name, index=False, mode='a')
                self.log.info('***************************************************************************************')
                self.log.info("Unit%s_%sC_%sV_%sMHz round is done." % (unit_number, temp, voltage, frequency))


def main():
    scope_ip_address = 'TCPIP0::157.165.147.88::inst0::INSTR'; fun_gen_gpib = 10; power_gpib = 20
    automotive = Automotive(scope_ip_address, fun_gen_gpib, power_gpib)
    automotive.measure()


if __name__ == '__main__':
    main()
