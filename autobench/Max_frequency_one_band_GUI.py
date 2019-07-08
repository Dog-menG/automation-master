from autobench.inst import func_gen, power
from autobench.inst.scope import Keysight
from autobench.i2c.aa_i2c import AAReadWrite
from autobench import log
from PyQt5 import QtWidgets, QtCore
import sys, csv, time, os


class MaxFrequency(object):

    def __init__(self, power_gpib, i2c_address, func_gen_gpib=7):
        self.log = log(self.__class__.__name__)
        self.dut_i2c = AAReadWrite(0, i2c_address, True)
        self.power = power.E3646A(power_gpib)
        self.function = func_gen.Agilent81130A(func_gen_gpib)
        self.myscope = Keysight()
        self.Gui = QtWidgets.QWidget()
        self.hbox = QtWidgets.QHBoxLayout()
        self.left = QtWidgets.QFrame()
        self.Power_channel1_voltage = QtWidgets.QLineEdit(self.left)
        self.Power_channel1_current_compliance = QtWidgets.QLineEdit(self.left)
        self.Power_channel2_voltage = QtWidgets.QLineEdit(self.left)
        self.Power_channel2_current_compliance = QtWidgets.QLineEdit(self.left)
        self.Fun_channel = QtWidgets.QLineEdit(self.left)
        self.Fun_frequency = QtWidgets.QLineEdit(self.left)
        self.Fun_duty_cycle = QtWidgets.QLineEdit(self.left)
        self.Fun_vhigh = QtWidgets.QLineEdit(self.left)
        self.Fun_vlow = QtWidgets.QLineEdit(self.left)
        self.Aardvark_write = QtWidgets.QLineEdit(self.left)
        self.Aardvark_write_register = QtWidgets.QLineEdit(self.left)
        self.Aardvark_read = QtWidgets.QTextEdit(self.left)
        self.mid = QtWidgets.QFrame()
        self.Scope_memory_depth = QtWidgets.QLineEdit(self.mid)
        self.Scope_sample_rate = QtWidgets.QLineEdit(self.mid)
        self.Scope_time_scale = QtWidgets.QLineEdit(self.mid)
        self.Scope_source = QtWidgets.QLineEdit(self.mid)
        self.Scope_source_offset = QtWidgets.QLineEdit(self.mid)
        self.Scope_source_scale = QtWidgets.QLineEdit(self.mid)
        self.Scope_source_thre_mode = QtWidgets.QLineEdit(self.mid)
        self.Scope_source_thre_high = QtWidgets.QLineEdit(self.mid)
        self.Scope_source_thre_mid = QtWidgets.QLineEdit(self.mid)
        self.Scope_source_thre_low = QtWidgets.QLineEdit(self.mid)
        self.Scope_trigger_edge = QtWidgets.QLineEdit(self.mid)
        self.Scope_trigger_level = QtWidgets.QLineEdit(self.mid)
        self.Scope_trigger_mode = QtWidgets.QLineEdit(self.mid)
        self.Scope_run_mode = QtWidgets.QLineEdit(self.mid)
        self.right = QtWidgets.QFrame()
        self.select_path_line = QtWidgets.QLineEdit(self.right)
        self.open_file_line = QtWidgets.QLineEdit(self.right)
        self.create_summary_file = QtWidgets.QLineEdit(self.right)
        self.temperature = QtWidgets.QLineEdit(self.right)
        self.unit = QtWidgets.QLineEdit(self.right)
        self.progress_bar = QtWidgets.QProgressBar(self.right)
        self.ui()

    def ui(self):
        # Power, function generator & Aardvark setup
        title_label = QtWidgets.QLabel('Power, function generator & Aardvark setup', self.left)
        title_label.setStyleSheet("font-weight:bold; font-size: 18px;")
        title_label.setGeometry(40, 20, 420, 150)
        power_channel1_voltage_label = QtWidgets.QLabel('Power_channel1_voltage', self.left)
        power_channel1_voltage_label.setGeometry(20, 200, 140, 30)
        self.Power_channel1_voltage.setText('3.3')
        self.Power_channel1_voltage.setGeometry(160, 200, 50, 30)
        power_channel1_current_compliance_label = QtWidgets.QLabel('Power_channel1_current_compliance', self.left)
        power_channel1_current_compliance_label.setGeometry(250, 200, 200, 30)
        self.Power_channel1_current_compliance.setText('0.3')
        self.Power_channel1_current_compliance.setGeometry(440, 200, 50, 30)
        power_channel2_voltage_label = QtWidgets.QLabel('Power_channel2_voltage', self.left)
        power_channel2_voltage_label.setGeometry(20, 280, 140, 30)
        self.Power_channel2_voltage.setText('3.3')
        self.Power_channel2_voltage.setGeometry(160, 280, 50, 30)
        power_channel2_current_compliance_label = QtWidgets.QLabel('Power_channel2_current_compliance', self.left)
        power_channel2_current_compliance_label.setGeometry(250, 280, 200, 30)
        self.Power_channel2_current_compliance.setText('0.6')
        self.Power_channel2_current_compliance.setGeometry(440, 280, 50, 30)
        fun_channel_label = QtWidgets.QLabel('Function_Generator_channel', self.left)
        fun_channel_label.setGeometry(95, 360, 150, 30)
        self.Fun_channel.setText('1')
        self.Fun_channel.setGeometry(250, 360, 50, 30)
        fun_frequency_label = QtWidgets.QLabel('Function_Generator_frequency', self.left)
        fun_frequency_label.setGeometry(20, 440, 150, 30)
        self.Fun_frequency.setText('100')
        self.Fun_frequency.setGeometry(170, 440, 50, 30)
        fun_duty_cycle_label = QtWidgets.QLabel('Function_Generator_Duty_cycle', self.left)
        fun_duty_cycle_label.setGeometry(250, 440, 200, 30)
        self.Fun_duty_cycle.setText('50')
        self.Fun_duty_cycle.setGeometry(440, 440, 50, 30)
        fun_vhigh_label = QtWidgets.QLabel('Function_Generator_Vhigh', self.left)
        fun_vhigh_label.setGeometry(20, 520, 150, 30)
        self.Fun_vhigh.setText('0.8')
        self.Fun_vhigh.setGeometry(170, 520, 50, 30)
        fun_vlow_label = QtWidgets.QLabel('Function_Generator_Vlow', self.left)
        fun_vlow_label.setGeometry(250, 520, 200, 30)
        self.Fun_vlow.setText('0')
        self.Fun_vlow.setGeometry(440, 520, 50, 30)
        aardvark_write_label = QtWidgets.QLabel('Aardvark_write', self.left)
        aardvark_write_label.setGeometry(20, 600, 150, 30)
        self.Aardvark_write.setText('0x0E')
        self.Aardvark_write.setGeometry(170, 600, 50, 30)
        aardvark_write_register_label = QtWidgets.QLabel('Aardvark_write_register', self.left)
        aardvark_write_register_label.setGeometry(250, 600, 150, 30)
        self.Aardvark_write_register.setText('0')
        self.Aardvark_write_register.setGeometry(440, 600, 50, 30)
        aardvark_read_label = QtWidgets.QLabel('Aardvark_read', self.left)
        aardvark_read_label.setGeometry(50, 680, 100, 30)
        self.Aardvark_read.setGeometry(160, 655, 300, 80)
        self.left.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.left.setGeometry(0, 0, 800, 700)

        # Scope setup
        title_label = QtWidgets.QLabel('Keysight Scope Setup', self.mid)
        title_label.setStyleSheet("font-weight:bold; font-size: 18px;")
        title_label.setGeometry(120, 20, 420, 50)
        scope_memory_depth_label = QtWidgets.QLabel('Scope_memory_depth', self.mid)
        scope_memory_depth_label.setGeometry(50, 80, 140, 30)
        self.Scope_memory_depth.setText('10e3')
        self.Scope_memory_depth.setGeometry(280, 80, 100, 30)
        scope_sample_rate_label = QtWidgets.QLabel('Scope_sample_rate', self.mid)
        scope_sample_rate_label.setGeometry(50, 130, 140, 30)
        self.Scope_sample_rate.setText('20e9')
        self.Scope_sample_rate.setGeometry(280, 130, 100, 30)
        scope_time_scale_label = QtWidgets.QLabel('Scope_time_scale', self.mid)
        scope_time_scale_label.setGeometry(50, 180, 140, 30)
        self.Scope_time_scale.setText('10e-9')
        self.Scope_time_scale.setGeometry(280, 180, 100, 30)
        scope_source_label = QtWidgets.QLabel('Scope_source', self.mid)
        scope_source_label.setGeometry(50, 230, 140, 30)
        self.Scope_source.setText('Channel1')
        self.Scope_source.setGeometry(280, 230, 100, 30)
        scope_source_offset_label = QtWidgets.QLabel('Scope_source_offset', self.mid)
        scope_source_offset_label.setGeometry(50, 280, 140, 30)
        self.Scope_source_offset.setText('0')
        self.Scope_source_offset.setGeometry(280, 280, 100, 30)
        scope_source_scale_label = QtWidgets.QLabel('Scope_source_scale', self.mid)
        scope_source_scale_label.setGeometry(50, 330, 140, 30)
        self.Scope_source_scale.setText('0.25')
        self.Scope_source_scale.setGeometry(280, 330, 100, 30)
        scope_source_thre_mode_label = QtWidgets.QLabel('Scope_source_thre_mode', self.mid)
        scope_source_thre_mode_label.setGeometry(50, 380, 140, 30)
        self.Scope_source_thre_mode.setText('PERCent')
        self.Scope_source_thre_mode.setGeometry(280, 380, 100, 30)
        scope_source_thre_high_label = QtWidgets.QLabel('Scope_source_thre_high', self.mid)
        scope_source_thre_high_label.setGeometry(50, 430, 140, 30)
        self.Scope_source_thre_high.setText('80')
        self.Scope_source_thre_high.setGeometry(280, 430, 100, 30)
        scope_source_thre_mid_label = QtWidgets.QLabel('Scope_source_thre_mid', self.mid)
        scope_source_thre_mid_label.setGeometry(50, 480, 140, 30)
        self.Scope_source_thre_mid.setText('50')
        self.Scope_source_thre_mid.setGeometry(280, 480, 100, 30)
        scope_source_thre_low_label = QtWidgets.QLabel('Scope_source_thre_low', self.mid)
        scope_source_thre_low_label.setGeometry(50, 530, 140, 30)
        self.Scope_source_thre_low.setText('20')
        self.Scope_source_thre_low.setGeometry(280, 530, 100, 30)
        scope_trigger_mode_label = QtWidgets.QLabel('Scope_trigger_edge', self.mid)
        scope_trigger_mode_label.setGeometry(50, 580, 140, 30)
        self.Scope_trigger_edge.setText('Rising')
        self.Scope_trigger_edge.setGeometry(280, 580, 100, 30)
        scope_trigger_level_label = QtWidgets.QLabel('Scope_trigger_level', self.mid)
        scope_trigger_level_label.setGeometry(50, 630, 140, 30)
        self.Scope_trigger_level.setText('0')
        self.Scope_trigger_level.setGeometry(280, 630, 100, 30)
        scope_trigger_level_label = QtWidgets.QLabel('Scope_trigger_mode', self.mid)
        scope_trigger_level_label.setGeometry(50, 680, 140, 30)
        self.Scope_trigger_mode.setText('Auto')
        self.Scope_trigger_mode.setGeometry(280, 680, 100, 30)
        scope_run_mode_label = QtWidgets.QLabel('Scope_run_mode', self.mid)
        scope_run_mode_label.setGeometry(50, 730, 140, 30)
        self.Scope_run_mode.setText('Run')
        self.Scope_run_mode.setGeometry(280, 730, 100, 30)
        self.mid.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mid.setGeometry(0, 0, 700, 700)

        # main window
        title_label = QtWidgets.QLabel('Main window', self.right)
        title_label.setStyleSheet("font-weight:bold; font-size: 18px;")
        title_label.setGeometry(150, 20, 420, 150)
        select_path_button = QtWidgets.QPushButton('Select_path', self.right)
        select_path_button.clicked.connect(self.select_path)
        select_path_button.setGeometry(20, 200, 75, 30)
        local_path = os.getcwd()
        self.select_path_line.setText('%s' % local_path)
        self.select_path_line.setGeometry(120, 200, 300, 30)
        open_file_button = QtWidgets.QPushButton('Open_setting_file', self.right)
        open_file_button.clicked.connect(self.open_file)
        open_file_button.setGeometry(20, 340, 150, 30)
        self.open_file_line.setGeometry(180, 340, 230, 30)
        create_file_button = QtWidgets.QPushButton('create_summary_file', self.right)
        create_file_button.clicked.connect(self.summary_file)
        create_file_button.setGeometry(20, 480, 150, 30)
        self.create_summary_file.setText('Max_Min_Frequency_one_band.csv')
        self.create_summary_file.setGeometry(180, 480, 230, 30)
        run_button = QtWidgets.QPushButton('Run', self.right)
        temperature_label = QtWidgets.QLabel('Temperature', self.right)
        temperature_label.setGeometry(20, 620, 75, 30)
        self.temperature.setText('25C')
        self.temperature.setGeometry(120, 620, 75, 30)
        unit_label = QtWidgets.QLabel('Unit', self.right)
        unit_label.setGeometry(250, 620, 75, 30)
        self.unit.setText('1')
        self.unit.setGeometry(330, 620, 75, 30)
        run_button.clicked.connect(self.Run)
        run_button.setGeometry(20, 700, 75, 30)
        self.progress_bar.setGeometry(150, 700, 300, 30)
        self.right.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.right.setGeometry(0, 0, 700, 700)

        splitter1 = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(self.left)
        splitter1.addWidget(self.mid)
        splitter1.addWidget(self.right)
        splitter1.resize(300, 400)
        self.hbox.addWidget(splitter1)
        self.Gui.setLayout(self.hbox)
        self.Gui.setWindowTitle('Max_Min_Frequency_PLL')
        self.Gui.showMaximized()

    def i2c_read(self, start_address, length):
        return list(self.dut_i2c.aa_read_i2c(start_address, length))

    def i2c_write(self, start_address, register_values):
        self.dut_i2c.aa_write_i2c(start_address, register_values)

    def fun_setup(self, channel, duty_cycle, frequency,  vhigh, vlow):
        self.function.duty_cycle(channel, duty_cycle)
        self.function.freq(channel, frequency)
        self.function.vhigh_vlow(channel, vlow, vhigh)

    def fun_frequency(self, channel, frequency):
        self.function.freq(channel, frequency)

    def fun_on_off(self, channel, status):
        self.function.on_off(channel, status)

    def power_setup(self, channel, ran, voltage, current):
        self.power.select_channel(channel)
        self.power.select_range(ran)
        self.power.set_voltage(voltage, current)

    def power_on_off(self, status):
        self.power.on_off(status)

    def scope_setup(self, memory_depth, sample_rate, time_scale, source1, offset, scale, edge, trigger_level,
                    trigger_mode, run_mode):
        self.myscope.measure_clear()
        self.myscope.acquisition(memory_depth, sample_rate, time_scale)
        self.myscope.source_on(source1)
        self.myscope.source_scale_setup(source1, offset, scale)
        self.myscope.trigger_setup(source1, edge, trigger_level, trigger_mode)
        self.myscope.run_mode(run_mode)

    def scope_threshold(self, source1, mode, thre_high, thre_mid, thre_low):
        self.myscope.thresholds_general(mode, source1, thre_high, thre_mid, thre_low)

    def measure(self, source1, frequency, rising_edge):
        self.myscope.measure_clear()
        self.myscope.measure(frequency, source1, rising_edge)
        time.sleep(0.5)
        print (self.myscope.get_result())
        return self.myscope.get_result()[5]

    def select_path(self):
        self.path = str(QtWidgets.QFileDialog.getExistingDirectory(self.right, "Select Directory", 'S:\''))
        reply = QtWidgets.QMessageBox.question(self.right, 'Message',
            'Do you want to select the path?', QtWidgets.QMessageBox.Yes |
            QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.No:
            self.select_path()
        else:
            self.select_path_line.setText(self.path)

    def open_file(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self.right, 'OpenFile')
        reply = QtWidgets.QMessageBox.question(self.right, 'Message',
            'Do you open this file?', QtWidgets.QMessageBox.Yes |
            QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.No:
            self.open_file()
        else:
            self.open_file_line.setText(filename)
            input_content = []
            file_content = open(filename, 'r')
            for line in file_content:
                input_content.append(line)
            for i in range(0, len(input_content)):
                print (input_content[i])

    def summary_file(self):
        os.chdir(self.path)
        create_summary_file = open(self.create_summary_file.text(), "ab")
        writer = csv.writer(create_summary_file, delimiter=",")
        writer.writerow(['Unit', 'Temperature', 'Hi_Lo_control', 'Frequency', 'Max', 'Min'])

    def Run(self, summary_file):
        self.Aardvark_read.clear()
        self.progress_bar.setValue(0)

        # Function Generator setup
        fun_channel = self.Fun_channel.text(); fun_duty_cycle = self.Fun_duty_cycle.text()
        fun_frequency = self.Fun_frequency.text(); fun_vhigh = self.Fun_vhigh.text(); fun_low = self.Fun_vlow.text()
        self.fun_setup(fun_channel, fun_duty_cycle, fun_frequency, fun_vhigh, fun_low)
        self.fun_on_off(1, 'ON')

        # Power supply setup
        power_range = 'LOW'
        power_voltage1 = self.Power_channel1_voltage.text(); power_current_compliance1 = self.Power_channel1_current_compliance.text()
        power_voltage2 = self.Power_channel2_voltage.text(); power_current_compliance2 = self.Power_channel2_current_compliance.text()
        self.power_setup(1, power_range, power_voltage1, power_current_compliance1)
        self.power_setup(2, power_range, power_voltage2, power_current_compliance2)
        self.power_on_off('OFF')
        self.power_on_off('ON')

        # Scope setup
        memory_depth = self.Scope_memory_depth.text(); sample_rate = self.Scope_sample_rate.text(); time_scale = self.Scope_time_scale.text()
        source = self.Scope_source.text(); offset = self.Scope_source_offset.text(); scale = self.Scope_source_scale.text()
        edge = self.Scope_trigger_edge.text(); trigger_level = self.Scope_trigger_level.text(); trigger_mode = self.Scope_trigger_mode.text()
        run_mode = self.Scope_run_mode.text(); thre_mode = self.Scope_source_thre_mode.text()
        thre_high = self.Scope_source_thre_high.text(); thre_mid = self.Scope_source_thre_mid.text(); thre_low = self.Scope_source_thre_low.text()
        self.scope_setup(memory_depth, sample_rate, time_scale, source, offset, scale, edge, trigger_level, trigger_mode, run_mode)
        self.scope_threshold(source, thre_mode, thre_high, thre_mid, thre_low)
        time.sleep(2)

        # Aardvark setup
        aardvark_write_value = list()
        aardvark_write_value.append(int(str(self.Aardvark_write.text()), 16))
        aardvark_write_register = int(str(self.Aardvark_write_register.text()), 16) + 128
        self.i2c_write(aardvark_write_register, aardvark_write_value)
        time.sleep(1)
        aardvark_read_value = self.i2c_read(128, 40)
        row1 = ''
        row2 = ''
        row3 = ''
        row4 = ''
        for i in range(0, 10):
            row1 += str(hex(aardvark_read_value[i])) + ' '
            row2 += str(hex(aardvark_read_value[i + 10])) + ' '
            row3 += str(hex(aardvark_read_value[i + 20])) + ' '
            row4 += str(hex(aardvark_read_value[i + 30])) + ' '
        read_back = """%s
%s
%s
%s
                        """ % (row1, row2, row3, row4)
        self.Aardvark_read.setText(read_back)
        time.sleep(1)
        self.progress_bar.setValue(5)

        # Measurement
        function_frequency = float(fun_frequency)
        target = float(fun_frequency)
        hi_lo_control = str(self.Aardvark_write.text())
        result = [str(self.unit.text()), str(self.temperature.text()), hi_lo_control, str(target)+'MHz']
        difference = 0

        # Get maximum frequency
        while difference < 0.01:
            self.fun_frequency(1, function_frequency)
            time.sleep(0.5)
            fre = float(self.measure('Channel3', 'FREQuency', 'RISing'))/10e5
            self.log.info('Now the input frequency is %s MHz' % function_frequency)
            self.log.info('Now the output frequency is %s MHz' % fre)
            difference = abs(function_frequency - fre)
            self.log.info('The difference between output and input is %s MHz' % difference)
            function_frequency += 0.1
        self.log.info('The maximum frequency is %s MHz.' % (function_frequency-0.2))
        result.append(str(function_frequency-0.2)+'MHz')
        time.sleep(1)
        self.progress_bar.setValue(55)
        difference = 0
        # Get minimum frequency
        while difference < 0.01:
            self.fun_frequency(1, target)
            time.sleep(0.5)
            fre = float(self.measure('Channel3', 'FREQuency', 'RISing'))/10e5
            self.log.info('Now the input frequency is %s MHz' % target)
            self.log.info('Now the output frequency is %s MHz' % fre)
            difference = abs(float(target) - fre)
            self.log.info('The difference between output and input is %s MHz' % difference)
            target -= 0.1
        self.log.info('The minimum frequency is %s MHz.' % (target+0.2))
        result.append(str(target+0.2)+'MHz')
        create_summary_file = open(self.create_summary_file.text(), "ab")
        writer = csv.writer(create_summary_file, delimiter=",")
        writer.writerow(result)
        time.sleep(0.5)
        self.progress_bar.setValue(100)

def main():
    power_gpib = 18
    app = QtWidgets.QApplication(sys.argv)
    max = MaxFrequency(power_gpib, 0x6C)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
