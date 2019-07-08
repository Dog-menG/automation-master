from autobench.i2c.aa_i2c import AAReadWrite
from autobench.inst.pn_machine import E5052
from autobench.inst.power import E3646A, E3631A
from autobench import log
import pandas as pd
import os, time


class pn_check(object):
    """This class is used to communicate with part using Aardvark."""
    def __init__(self, e3646_power_address, e3631_power_address, i2c_address, e5052_address=17):
        self.log = log(self.__class__.__name__)
        self.phase_noise = E5052(e5052_address)
        self.power_3646 = E3646A(e3646_power_address)
        self.power_3631 = E3631A(e3631_power_address)
        self.dut_i2c = AAReadWrite(0, i2c_address, True)
        self.dut_i2c.length = 1

    def i2c_read(self, start_address, length):
        return list(self.dut_i2c.aa_read_i2c(start_address, length))

    def i2c_write(self, start_address, register_values):
        self.dut_i2c.aa_write_i2c(start_address, register_values)

    def i2c_close(self):
        self.dut_i2c.close()

    def phase_noise_setup(self, if_gain=50, rf_attenuation=0, mode='NORMal'):
        self.phase_noise.trigger_continuous(0)
        self.phase_noise.spurious(1)
        self.phase_noise.if_gain(if_gain)
        self.phase_noise.rf_attenuation(rf_attenuation)
        self.phase_noise.print_image_mode(mode)

    def phase_noise_band_marker(self, band, BDmarker_start, BDmarker_stop):
        self.phase_noise.start_frequency(100)
        if band == 1:
            self.phase_noise.band_select(1)
            self.phase_noise.stop_frequency(1)
            self.phase_noise.set_BDmarker(1, BDmarker_start, BDmarker_stop)
            self.phase_noise.set_marker(1, 100)
            self.phase_noise.set_marker(2, 1e3)
            self.phase_noise.set_marker(3, 1e4)
            self.phase_noise.set_marker(4, 1e5)
            self.phase_noise.set_marker(5, 1e6)
            self.phase_noise.set_marker(6, 5e6)
            for i in range(0, 8):
                self.phase_noise.turn_on_off_marker(i, 'ON')
        elif band == 2:
            self.phase_noise.band_select(3)
            self.phase_noise.stop_frequency(3)
            self.phase_noise.set_BDmarker(1, BDmarker_start, BDmarker_stop)
            self.phase_noise.set_marker(1, 100)
            self.phase_noise.set_marker(2, 1e3)
            self.phase_noise.set_marker(3, 1e4)
            self.phase_noise.set_marker(4, 1e5)
            self.phase_noise.set_marker(5, 1e6)
            self.phase_noise.set_marker(6, 5e6)
            self.phase_noise.set_marker(7, 1e7)
            self.phase_noise.set_marker(8, 2e7)
            for i in range(0, 9):
                self.phase_noise.turn_on_off_marker(i, 'ON')
        else:
            self.log.warn('The input is invalid.')

    def phase_noise_measure(self):
        self.phase_noise.clear_display()
        self.phase_noise.trigger_sopc(1)
        self.phase_noise.trigger_average(1)
        self.phase_noise.trigger_immediate()
        self.phase_noise.trigger_continuous(0)
        self.phase_noise.average_onoff(1)
        self.phase_noise.average_set(2, 16)
        self.phase_noise.trigger_continuous(1)
        status = self.phase_noise.get_status()
        while status != '+1':
            status = self.phase_noise.get_status()
        self.phase_noise.trigger_continuous(0)

    def phase_noise_get_rms_jitter(self):
        return self.phase_noise.get_rms_jitter()

    def phase_noise_save_csv_png(self, csv_name, png_name):
        self.phase_noise.save_csv(csv_name)
        self.phase_noise.save_screen(png_name)

    def e3646_power_on_off(self, status):
        self.power_3646.on_off(status)

    def e3646_power_setup(self, channel, voltage, current):
        self.power_3646.select_channel(channel)
        self.power_3646.set_voltage(voltage, current)

    def e3631_power_on_off(self, status):
        self.power_3631.on_off(status)

    def e3631_power_setup(self, channel, voltage, current):
        self.power_3631.set_voltage(channel, voltage, current)

    def run(self):
        # E5052 phase noise set up
        phase_noise_if_gain = 50; phase_noise_rf_attenuation = 5; phase_noise_print_mode = 'INVert'
        phase_noise_band = 2; phase_noise_BDmarker_start = 12e3; phase_noise_BDmarker_stop = 20e6

        # power set up
        e3646_channel = 1; e3646_voltage = 3.3; e3646_current = 0.4
        e3631_channel = 1; e3631_voltage = 3.3; e3631_current = 0.4

        # setting file path and save path
        path = r'J:\PRODUCT\CHAR\IDT8Pxxxxxx\8P49N3xx_VELO\8P49N344(AK721T-J13)\PN_001_HCSL\test_larry\input_file'
        save_path = r'J:\PRODUCT\CHAR\IDT8Pxxxxxx\8P49N3xx_VELO\8P49N344(AK721T-J13)\PN_001_HCSL\test_larry\revb_board_50ohm_termination\soldered_no_caps'
        os.chdir(path)

        # get input from input_file
        input = pd.read_excel('Output1.xlsx')
        loop_number = len(input.index)

        # # power configuration
        # self.e3646_power_on_off('OFF')
        # self.e3631_power_on_off('OFF')
        self.e3646_power_setup(e3646_channel, e3646_voltage, e3646_current)
        self.e3631_power_setup(e3631_channel, e3631_voltage, e3631_current)
        self.e3646_power_on_off('ON')
        self.e3631_power_on_off('ON')
        time.sleep(0.5)

        self.i2c_write(10, [0x05])
        for i in range(0, loop_number):
            Aardvark = str(input.iloc[i][0]).split(',')
            register_values = []
            start_address = Aardvark[0]
            for n in range(0, len(Aardvark[1].split(' '))):
                register_values.append(int(Aardvark[1].split(' ')[n], 16))

            temp = str(input.iloc[i][1]); output = str(input.iloc[i][2]); label = str(input.iloc[i][3])
            time.sleep(0.1)

            # Aardvark write
            self.i2c_write(start_address, register_values)
            time.sleep(2)

            # Phase noise measurement
            self.phase_noise_setup(phase_noise_if_gain, phase_noise_rf_attenuation, phase_noise_print_mode)
            self.phase_noise_band_marker(phase_noise_band, phase_noise_BDmarker_start, phase_noise_BDmarker_stop)
            self.phase_noise_measure()
            rms_jitter = '%.3f' % (float(self.phase_noise_get_rms_jitter()) * 10e14)
            mark_start = phase_noise_BDmarker_start/1e3
            mark_stop = phase_noise_BDmarker_stop/1e6
            csv_name = r'"%s\3.3V_%sC_%s_%sk_to_%sM_%s_%sf.csv"' \
                       % (save_path, temp, output, mark_start, mark_stop, label, rms_jitter)
            png_name = r'"%s\3.3V_%sC_%s_%sk_to_%sM_%s_%sf.png"' \
                       % (save_path, temp, output, mark_start, mark_stop, label, rms_jitter)
            time.sleep(0.1)
            save_csv_name = r"%s" % csv_name
            save_png_name = r"%s" % png_name
            self.phase_noise_save_csv_png(save_csv_name, save_png_name)
            self.log.info('The %s round is finished' % i)
            self.log.info('The phase noise is %sf.' % rms_jitter)
            time.sleep(2)
        self.i2c_close()


def main():
    e3646_power_gpib = 18; e3631_power_gpib = 19; i2c_address = 0x09
    phase_noise_check = pn_check(e3646_power_gpib, e3631_power_gpib, i2c_address)
    phase_noise_check.run()


if __name__ == "__main__":
    main()
