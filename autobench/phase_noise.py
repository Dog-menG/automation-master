# from autobench.inst import power, pn_machine, SMA100A
from autobench import email_txt_msg
# from i2c.aa_i2c import AAReadWrite
from autobench import log
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import *
import sys
import time


class Phase_noise_measure(object):
    def __init__(self, power_gpib,  i2c_address, sma100a_address=28, E5052=17):
        # self.log = log(self.__class__.__name__)
        # self.dut_i2c = AAReadWrite(0, i2c_address, True)
        # self.power = power.E3646A(power_gpib)
        # # self.SMA100A = SMA100A.SMA100A(sma100a_address)
        # self.phase_noise = pn_machine.E5052(E5052)
        self.Gui = QWidget()
        self.hbox = QHBoxLayout()
        self.topleft = QFrame()
        self.topmid = QFrame()
        self.topright = QFrame()
        self.bottomleft = QFrame()
        self.bottomright = QFrame()
        self.power_channel = QLineEdit(self.topleft)
        self.power_range = QLineEdit(self.topleft)
        self.power_voltage = QLineEdit(self.topleft)
        self.power_current = QLineEdit(self.topleft)
        self.phase_noise_band = QLineEdit(self.topmid)
        self.phase_noise_if_gain = QLineEdit(self.topmid)
        self.phase_noise_rf_attenuation = QLineEdit(self.topmid)
        self.phase_noise_BDmarker_start = QLineEdit(self.topmid)
        self.phase_noise_BDmarker_stop = QLineEdit(self.topmid)
        self.aardvark_write_register = QLineEdit(self.topright)
        self.aardvark_write_value = QLineEdit(self.topright)
        self.aardvark_read_register = QLineEdit(self.topright)
        self.aardvark_read_length = QLineEdit(self.topright)
        self.aardvark_read_value = QTextEdit(self.topright)
        self.show_file_name = QLineEdit(self.bottomleft)
        self.show_path = QLineEdit(self.bottomleft)
        self.temperature = QLineEdit(self.bottomleft)
        self.part_font_unit = QLineEdit(self.bottomleft)
        self.phase_noise_rms_jitter = QLineEdit(self.bottomleft)
        self.sma100a_frequency = QLineEdit(self.bottomright)
        self.sma100a_level = QLineEdit(self.bottomright)
        self.wenzel_frequency = QLineEdit(self.bottomright)
        self.ui()

    def ui(self):
        # Power panel GUI setup
        power_lable = QLabel('Power_setup_panel', self.topleft)
        power_lable.setGeometry(20, 20, 150, 150)
        power_channel_label = QLabel('Power_channel', self.topleft)
        power_channel_label.setGeometry(30, 150, 75, 30)
        self.power_channel.setGeometry(150, 150, 75, 30)
        self.power_channel.setText('1')
        power_range_label = QLabel('Power_range', self.topleft)
        power_range_label.setGeometry(30, 200, 75, 30)
        self.power_range.setGeometry(150, 200, 75, 30)
        self.power_range.setText('LOW')
        power_voltage_label = QLabel('Power_voltage', self.topleft)
        power_voltage_label.setGeometry(30, 250, 75, 30)
        self.power_voltage.setGeometry(150, 250, 75, 30)
        self.power_voltage.setText('3.3')
        power_current_label = QLabel('Power_current', self.topleft)
        power_current_label.setGeometry(30, 300, 75, 30)
        self.power_current.setGeometry(150, 300, 75, 30)
        self.power_current.setText('0.3')
        power_notification = QTextEdit(self.topleft)
        power_note = """This is power panel, it is used for power setting.

E3646A is the selected source, power GPIB address is 19.

Power Channel should be 1 or 2.

Power range LOW(0-8V), HIGH(0-20V).

Power voltage is the voltage to use.

Power current is the current compliance.
                """
        power_notification.setText(power_note)
        power_notification.setGeometry(250, 80, 180, 250)
        self.topleft.setFrameShape(QFrame.StyledPanel)
        self.topleft.setGeometry(0, 0, 750, 700)

        # Phase noise instrument panel GUI setup
        phase_noise_lable = QLabel('Phase_noise_panel', self.topmid)
        phase_noise_lable.setGeometry(20, 20, 150, 150)
        phase_noise_label = QLabel('Phase_noise_band', self.topmid)
        phase_noise_label.setGeometry(20, 135, 150, 30)
        self.phase_noise_band.setGeometry(180, 135, 75, 30)
        self.phase_noise_band.setText('2')
        phase_noise_if_gain_label = QLabel('Phase_noise_IF_Gain', self.topmid)
        phase_noise_if_gain_label.setGeometry(20, 180, 150, 30)
        self.phase_noise_if_gain.setGeometry(180, 180, 75, 30)
        self.phase_noise_if_gain.setText('50')
        phase_noise_rf_attenuation_label = QLabel('Phase_noise_RF_Attenuation', self.topmid)
        phase_noise_rf_attenuation_label.setGeometry(20, 225, 150, 30)
        self.phase_noise_rf_attenuation.setGeometry(180, 225, 75, 30)
        self.phase_noise_rf_attenuation.setText('0')
        phase_noise_BDmarker_start_label = QLabel('Phase_noise_BDmarker_start', self.topmid)
        phase_noise_BDmarker_start_label.setGeometry(20, 270, 150, 30)
        self.phase_noise_BDmarker_start.setGeometry(180, 270, 75, 30)
        self.phase_noise_BDmarker_start.setText('12e3')
        phase_noise_BDmarker_stop_label = QLabel('Phase_noise_BDmarker_stop', self.topmid)
        phase_noise_BDmarker_stop_label.setGeometry(20, 315, 150, 30)
        self.phase_noise_BDmarker_stop.setGeometry(180, 315, 75, 30)
        self.phase_noise_BDmarker_stop.setText('20e6')
        phase_noise_notification = QTextEdit(self.topmid)
        phase_noise_note = """This is phase noise panel, it is used for phase noise setting.

E5052 is the selected source, power GPIB address is 23.

Phase noise band should be 1(10M-41M) or 2(99M-1G).

Phase noise if gain is intermediate frequency gain.

Phase noise rf attenuation is input attenuation.

Phase noise BDmarker start is the start frequency of Band Marker.

Phase noise BDmarker stop is the stop frequency of Band Marker.
                        """
        phase_noise_notification.setText(phase_noise_note)
        phase_noise_notification.setGeometry(280, 60, 180, 300)
        self.topmid.setFrameShape(QFrame.StyledPanel)
        self.topmid.setGeometry(0, 0, 750, 700)

        # Aardvark GUI setup
        aardvark_lable = QLabel('Aardvark_setup_panel', self.topright)
        aardvark_lable.setGeometry(20, 20, 150, 150)
        aardvark_write_register_label = QLabel('Aardvark_write_register', self.topright)
        aardvark_write_register_label.setGeometry(20, 135, 150, 30)
        self.aardvark_write_register.setText('0')
        self.aardvark_write_register.setGeometry(180, 135, 75, 30)
        aardvark_write_value_label = QLabel('Aardvark_write_value', self.topright)
        aardvark_write_value_label.setGeometry(20, 180, 150, 30)
        self.aardvark_write_value.setText('0xCE')
        self.aardvark_write_value.setGeometry(180, 180, 75, 30)
        aardvark_read_register_label = QLabel('Aardvark_read_register', self.topright)
        aardvark_read_register_label.setGeometry(20, 225, 150, 30)
        self.aardvark_read_register.setText('0')
        self.aardvark_read_register.setGeometry(180, 225, 75, 30)
        aardvark_read_length_label = QLabel('Aardvark_read_length', self.topright)
        aardvark_read_length_label.setGeometry(20, 270, 150, 30)
        self.aardvark_read_length.setText('1')
        self.aardvark_read_length.setGeometry(180, 270, 75, 30)
        aardvark_read_value_label = QLabel('Aardvark_read_value', self.topright)
        aardvark_read_value_label.setGeometry(80, 320, 150, 30)
        self.aardvark_read_value.setGeometry(20, 350, 230, 50)
        self.topright.setFrameShape(QFrame.StyledPanel)
        self.topright.setGeometry(0, 0, 750, 700)
        aardvark_notification = QTextEdit(self.topright)
        aardvark_note = """This is Aardvark panel, it is used for Aardvark setting.

Aardvark is the selected source.

Aardvark write address is the start address to write to Aardvark.

Aardvark write value is the value to write to Aardvark.

Aardvark read address is the start address to read from Aardvark.

Aardvark read length is how many bytes read from Aardvark.

Aardvark read value shows the values read from Aardvark.
                                """
        aardvark_notification.setText(aardvark_note)
        aardvark_notification.setGeometry(280, 60, 180, 300)
        self.topright.setFrameShape(QFrame.StyledPanel)
        self.topright.setGeometry(0, 0, 750, 700)

        # Main window GUI setup
        run_button = QPushButton('Run', self.bottomleft)
        run_button.clicked.connect(self.run)
        run_button.setGeometry(50, 50, 75, 30)
        Open_file_button = QPushButton('Open_file', self.bottomleft)
        Open_file_button.clicked.connect(self.open_file)
        Open_file_button.setGeometry(175, 50, 75, 30)
        self.show_file_name.setGeometry(300, 50, 400, 30)
        select_path_button = QPushButton('Select_path', self.bottomleft)
        select_path_button.clicked.connect(self.select_path)
        select_path_button.setGeometry(50, 135, 75, 30)
        self.show_path.setGeometry(180, 135, 520, 30)
        self.show_path.setText(r'S:\ '.strip())
        temperature_label = QLabel('Temperature', self.bottomleft)
        temperature_label.setGeometry(50, 220, 75, 30)
        self.temperature.setGeometry(175, 220, 75, 30)
        self.temperature.setText('25C')
        part_font_unit_label = QLabel('Part_Font_Unit', self.bottomleft)
        part_font_unit_label.setGeometry(300, 220, 100, 30)
        self.part_font_unit.setGeometry(400, 220, 300, 30)
        Phase_noise_rms_jitter_label = QLabel('Phase_noise_rms_jitter', self.bottomleft)
        Phase_noise_rms_jitter_label.setGeometry(50, 305, 125, 30)
        self.phase_noise_rms_jitter.setGeometry(180, 305, 150, 30)
        self.bottomleft.setFrameShape(QFrame.StyledPanel)
        self.bottomleft.setGeometry(700, 700, 400, 400)

        # SMA100A Function Generator GUI setup
        sma100a_lable = QLabel('SMA100A_Or_Wenzel_panel', self.bottomright)
        sma100a_lable.setGeometry(300, 40, 150, 20)
        sma100a_frequency_label = QLabel('SMA100A_Frequency', self.bottomright)
        sma100a_frequency_label.setGeometry(20, 100, 150, 30)
        self.sma100a_frequency.setGeometry(180, 100, 75, 30)
        self.sma100a_frequency.setText('100MHz')
        sma100a_level_label = QLabel('SMA100A_Level', self.bottomright)
        sma100a_level_label.setGeometry(20, 200, 150, 30)
        self.sma100a_level.setGeometry(180, 200, 75, 30)
        self.sma100a_level.setText('0.8V')
        wenzel_frequency_label = QLabel('Wenzel_Frequency', self.bottomright)
        wenzel_frequency_label.setGeometry(20, 300, 150, 30)
        self.wenzel_frequency.setGeometry(180, 300, 75, 30)
        self.wenzel_frequency.setText('100MHz')
        self.bottomright.setFrameShape(QFrame.StyledPanel)
        self.bottomright.setGeometry(700, 700, 400, 400)
        sma100a_notification = QTextEdit(self.bottomright)
        sma100a_note = """This is SMA100A or Wenzel panel, it is used for function generator setting.

SMA100A is the selected source.

SMA100A frequency is the input frequency.

SMA100A level is the input amplitude.

Wenzel frequency is the input frequency.

Using either SMA100A or Wenzel.
                                        """
        sma100a_notification.setText(sma100a_note)
        sma100a_notification.setGeometry(280, 100, 400, 230)

        splitter1 = QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(self.topleft)
        splitter1.addWidget(self.topmid)
        splitter1.addWidget(self.topright)
        splitter1.resize(300, 400)

        splitter2 = QSplitter(QtCore.Qt.Horizontal)
        splitter2.addWidget(self.bottomleft)
        splitter2.addWidget(self.bottomright)
        splitter2.resize(300, 400)

        splitter3 = QSplitter(QtCore.Qt.Vertical)
        splitter3.addWidget(splitter1)
        splitter3.addWidget(splitter2)

        self.hbox.addWidget(splitter3)
        self.Gui.setLayout(self.hbox)
        self.Gui.setWindowTitle('Phase_Noise_Measurement')
        self.Gui.showMaximized()

    def power_setup(self, channel, ran, voltage, current):
        self.power.select_channel(channel)
        self.power.select_range(ran)
        self.power.set_voltage(voltage, current)

    def power_on_off(self, status):
        self.power.on_off(status)

    def sma100a_setup(self, frequency, amplitude):
        self.SMA100A.rf_frequency(frequency)
        self.SMA100A.rf_output_level(amplitude)

    def sma100a_on_off(self, status):
         self.SMA100A.rf_out_state(status)

    def i2c_read(self, start_address, length):
        return list(self.dut_i2c.aa_read_i2c(start_address, length))

    def i2c_write(self, start_address, register_values):
        self.dut_i2c.aa_write_i2c(start_address, register_values)

    def phase_noise_setup(self, if_gain=50, rf_attenuation=0):
        self.phase_noise.trigger_continuous(0)
        self.phase_noise.spurious(2)
        self.phase_noise.if_gain(if_gain)
        self.phase_noise.rf_attenuation(rf_attenuation)

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
            for i in range(0,8):
                self.phase_noise.turn_on_off_marker(i,'ON')
        elif band == 2:
            self.phase_noise.band_select(3)
            self.phase_noise.stop_frequency(3)
            self.phase_noise.set_BDmarker(1,BDmarker_start, BDmarker_stop)
            self.phase_noise.set_marker(1, 100)
            self.phase_noise.set_marker(2, 1e3)
            self.phase_noise.set_marker(3, 1e4)
            self.phase_noise.set_marker(4, 1e5)
            self.phase_noise.set_marker(5, 1e6)
            self.phase_noise.set_marker(6, 5e6)
            self.phase_noise.set_marker(7, 1e7)
            self.phase_noise.set_marker(8, 2e7)
            for i in range(0,9):
                self.phase_noise.turn_on_off_marker(i,'ON')
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

    def email_message(self, source, destination, subject, text):
        self.email = email_txt_msg.Email_Txt_Msg()
        self.email.send_msg(source, destination, subject, text)

    def run(self):
        # power supply setup
        power_channel = self.power_channel.text(); power_range = self.power_range.text()
        power_voltage = self.power_voltage.text(); power_current = self.power_current.text()
        self.power_on_off('OFF')
        self.power_setup(power_channel, power_range, power_voltage, power_current)
        self.power_on_off('ON')
        time.sleep(0.5)

        # # SMA100A setup
        # sma100a_frequency = self.sma100a_frequency.text(); sma100a_amplitude = self.sma100a_level.text()
        # self.sma100a_on_off(0)
        # self.sma100a_setup(sma100a_frequency, sma100a_amplitude)
        # self.sma100a_on_off(1)

        #Aardvark setup
        aardvark_write_register = int(self.aardvark_write_register.text()) + 128
        aardvark_write_value = []
        aardvark_write_value.append(int(str(self.aardvark_write_value.text().split(',')[0]),16))
        # print aardvark_write_value
        aardvark_read_register = int(self.aardvark_read_register.text()) + 128
        aardvark_read_length = int(self.aardvark_read_length.text())
        self.i2c_write(aardvark_write_register, aardvark_write_value)
        time.sleep(1)
        aardvark_read_value = self.i2c_read(aardvark_read_register, aardvark_read_length)
        self.aardvark_read_value.setText(str(hex(aardvark_read_value[0])))
        time.sleep(3)

        # phase noise setup
        phase_noise_if_gain = self.phase_noise_if_gain.text()
        phase_noise_rf_attenutaion = self.phase_noise_rf_attenuation.text()
        phase_noise_band = int(self.phase_noise_band.text())
        phase_noise_BDmarker_start = str(self.phase_noise_BDmarker_start.text())
        phase_noise_BDmarker_stop = str(self.phase_noise_BDmarker_stop.text())
        self.phase_noise_setup(phase_noise_if_gain, phase_noise_rf_attenutaion)
        self.phase_noise_band_marker(phase_noise_band, phase_noise_BDmarker_start, phase_noise_BDmarker_stop)
        self.phase_noise_measure()
        self.path = self.show_path.text()
        rms_jitter = '%.3f' % (float(self.phase_noise_get_rms_jitter()) * 10e14)
        csv_name = r'"%s\%s_%sV_%s_%s_to_%s_%sf.csv"' \
                   % (self.path, self.temperature.text(), self.power_voltage.text(), self.part_font_unit.text(),
                      phase_noise_BDmarker_start, phase_noise_BDmarker_stop, rms_jitter)
        png_name = r'"%s\%s_%sV_%s_%s_to_%s_%sf.png"' \
                   % (self.path, self.temperature.text(), self.power_voltage.text(), self.part_font_unit.text(),
                      phase_noise_BDmarker_start, phase_noise_BDmarker_stop, rms_jitter)
        save_csv_name = r"%s" % csv_name
        save_png_name = r"%s" % png_name
        # print save_csv_name
        # print save_png_name
        self.phase_noise_save_csv_png(save_csv_name, save_png_name)
        self.phase_noise_rms_jitter.setText(rms_jitter)

        # # email setup
        # source = 'jun.gou@idt.com'; destination = 'jun.gou@idt.com'
        # subject = 'The test is done.'; text = 'The test is done, please take care!'
        # self.email_message(source, destination, subject, text)

    def select_path(self):
        self.path = str(QFileDialog.getExistingDirectory(self.bottomleft, "Select Directory", 'S:\9ZXLxxx\9ZXL1951-1952\9ZXL1951_1952D_AP711T-010\PN'))
        reply = QMessageBox.question(self.bottomleft, 'Message',
            'Do you want to select the path?', QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.No:
            self.select_path()
        else:
            self.show_path.setText(self.path)

    def open_file(self):
        fileName = QFileDialog.getOpenFileName(self.bottomleft, 'OpenFile')
        reply = QMessageBox.question(self.bottomleft, 'Message',
            'Do you open this file?', QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.No:
            self.open_file()
        else:
            self.show_file_name.setText(fileName)
            input = []
            file = open(fileName, 'r')
            for line in file:
                input.append(line)
            for i in range(0,len(input)):
                # print input[i]
                print (1)


def main():
    app = QApplication(sys.argv)
    ex = Phase_noise_measure(18, 0x6C)
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()