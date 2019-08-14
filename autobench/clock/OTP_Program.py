from autobench.inst import power, func_gen
from autobench.i2c.aa_i2c import AAReadWrite
from autobench import log
from PyQt5 import QtWidgets, QtCore
import sys
import time
import threading


# noinspection PyArgumentList
class OTP_Program(object):
    """This class is used to burn part of AP711T."""
    def __init__(self, power_gpib1, power_gpib2, i2c_address, func_gen_gpib):
        self.log = log(self.__class__.__name__)
        # self.dut_i2c = AAReadWrite(0, i2c_address, True)
        # self.power1 = power.E3646A(power_gpib1)
        # self.power2 = power.E3631A(power_gpib2)
        # self.fun = func_gen.Agilent81130A(func_gen_gpib)
        self.Gui = QtWidgets.QWidget()
        self.hbox = QtWidgets.QHBoxLayout()
        self.left = QtWidgets.QFrame()
        self.Byte0_to_Byte39 = QtWidgets.QTextEdit(self.left)
        self.B46_OTP_start_address_1 = QtWidgets.QLineEdit(self.left)
        self.B47_OTP_stop_address_1 = QtWidgets.QLineEdit(self.left)
        self.B48_Ram_burn_start_address_1 = QtWidgets.QLineEdit(self.left)
        self.read_back_B0_to_B39 = QtWidgets.QTextEdit(self.left)
        self.first_read_Value_error = QtWidgets.QLineEdit(self.left)
        self.B0_B39_match = QtWidgets.QLineEdit(self.left)
        self.mid = QtWidgets.QFrame()
        self.Byte40_to_Byte45 = QtWidgets.QLineEdit(self.mid)
        self.B46_OTP_start_address_2 = QtWidgets.QLineEdit(self.mid)
        self.B47_OTP_stop_address_2 = QtWidgets.QLineEdit(self.mid)
        self.B48_Ram_burn_start_address_2 = QtWidgets.QLineEdit(self.mid)
        self.second_read_Value_error = QtWidgets.QLineEdit(self.mid)
        self.read_back_B40_to_B45 = QtWidgets.QTextEdit(self.mid)
        self.B40_B45_match = QtWidgets.QTextEdit(self.mid)
        self.right = QtWidgets.QFrame()
        self.Byte58_to_Byte61 = QtWidgets.QLineEdit(self.right)
        self.B46_OTP_start_address_3 = QtWidgets.QLineEdit(self.right)
        self.B47_OTP_stop_address_3 = QtWidgets.QLineEdit(self.right)
        self.B48_Ram_burn_start_address_3 = QtWidgets.QLineEdit(self.right)
        self.third_read_Value_error = QtWidgets.QLineEdit(self.right)
        self.read_back_B58_to_B61 = QtWidgets.QTextEdit(self.right)
        self.B58_B61_match = QtWidgets.QTextEdit(self.right)
        self.ui()

    def ui(self):
        # 1st pass burn and Margin read
        title_label = QtWidgets.QLabel('1st pass burn and Margin read', self.left)
        title_label.setStyleSheet("font-weight:bold; font-size: 18px;")
        title_label.setGeometry(110, 20, 300, 150)
        pass_burn_label = QtWidgets.QLabel('1st pass burn', self.left)
        pass_burn_label.setStyleSheet("font-weight:bold; font-size: 13px;")
        pass_burn_label.setGeometry(185, 90, 300, 100)
        Byte0_to_Byte39_label = QtWidgets.QLabel('Byte0_to_Byte39', self.left)
        Byte0_to_Byte39_label.setGeometry(10, 200, 100, 30)
        Byte0_to_Byte39_value = """0x78 0xFF 0xFF 0x00 0x00 0x01 0xC8 0x08 0xFF 0x00
0x05 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00 0x00
0x04 0x08 0x00 0x00 0x00 0x00 0x00 0x00 0x41 0x61
0xA8 0xC0 0x20 0x00 0xC3 0x00 0x20 0x00 0x99 0x00
                                """
        self.Byte0_to_Byte39.setGeometry(135, 185, 300, 75)
        self.Byte0_to_Byte39.setText(Byte0_to_Byte39_value)
        B46_OTP_start_address_label = QtWidgets.QLabel('B46(OTP_start_address)', self.left)
        B46_OTP_start_address_label.setGeometry(100, 290, 150, 30)
        self.B46_OTP_start_address_1.setText('0x00')
        self.B46_OTP_start_address_1.setGeometry(310, 290, 50, 30)
        B47_OTP_stop_address_label = QtWidgets.QLabel('B47(OTP_stop_address)', self.left)
        B47_OTP_stop_address_label.setGeometry(100, 365, 150, 30)
        self.B47_OTP_stop_address_1.setText('0x27')
        self.B47_OTP_stop_address_1.setGeometry(310, 365, 50, 30)
        B48_Ram_burn_start_address_label = QtWidgets.QLabel('B48(Ram_burn_start_address)', self.left)
        B48_Ram_burn_start_address_label.setGeometry(100, 440, 150, 30)
        self.B48_Ram_burn_start_address_1.setText('0x00')
        self.B48_Ram_burn_start_address_1.setGeometry(310, 440, 50, 30)
        margin_read_label = QtWidgets.QLabel('1st Margin 1 read', self.left)
        margin_read_label.setStyleSheet("font-weight:bold; font-size: 13px;")
        margin_read_label.setGeometry(170, 480, 300, 50)
        read_back_label = QtWidgets.QLabel('Byte0_to_Byte39_readback',self.left)
        read_back_label.setGeometry(10, 555, 150, 30)
        self.read_back_B0_to_B39.setGeometry(160, 535, 300, 75)
        first_read_Value_error_label = QtWidgets.QLabel('First_read_value_error', self.left)
        first_read_Value_error_label.setGeometry(100, 630, 150, 30)
        self.first_read_Value_error.setGeometry(310, 630, 50, 30)
        match_label = QtWidgets.QLabel('Does readback match the value burnt to the part?', self.left)
        match_label.setGeometry(10, 680, 285, 30)
        self.B0_B39_match.setGeometry(310, 680, 100, 30)
        first_burn_margin_read_button = QtWidgets.QPushButton('Run', self.left)
        first_burn_margin_read_button.clicked.connect(self.first_burn_margin_read)
        first_burn_margin_read_button.setGeometry(160, 725, 120, 50)
        self.left.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.left.setGeometry(0, 0, 750, 700)

        # 2nd pass burn and Margin read
        title_label = QtWidgets.QLabel('2nd pass burn and Margin read', self.mid)
        title_label.setStyleSheet("font-weight:bold; font-size: 18px;")
        title_label.setGeometry(110, 20, 300, 150)
        pass_burn_label = QtWidgets.QLabel('2nd pass burn', self.mid)
        pass_burn_label.setStyleSheet("font-weight:bold; font-size: 13px;")
        pass_burn_label.setGeometry(185, 90, 300, 100)
        Byte40_to_Byte45_label = QtWidgets.QLabel('Byte40_to_Byte45', self.mid)
        Byte40_to_Byte45_label.setGeometry(50, 200, 100, 30)
        Byte40_to_Byte45_value = """0x20 0x00 0xC4 0x40 0x20 0x00"""
        self.Byte40_to_Byte45.setGeometry(200, 190, 200, 50)
        self.Byte40_to_Byte45.setText(Byte40_to_Byte45_value)
        B46_OTP_start_address_label = QtWidgets.QLabel('B46(OTP_start_address)', self.mid)
        B46_OTP_start_address_label.setGeometry(100, 290, 150, 30)
        self.B46_OTP_start_address_2.setText('0x28')
        self.B46_OTP_start_address_2.setGeometry(310, 290, 50, 30)
        B47_OTP_stop_address_label = QtWidgets.QLabel('B47(OTP_stop_address)', self.mid)
        B47_OTP_stop_address_label.setGeometry(100, 365, 150, 30)
        self.B47_OTP_stop_address_2.setText('0x2D')
        self.B47_OTP_stop_address_2.setGeometry(310, 365, 50, 30)
        B48_Ram_burn_start_address_label = QtWidgets.QLabel('B48(Ram_burn_start_address)', self.mid)
        B48_Ram_burn_start_address_label.setGeometry(100, 440, 150, 30)
        self.B48_Ram_burn_start_address_2.setText('0x22')
        self.B48_Ram_burn_start_address_2.setGeometry(310, 440, 50, 30)
        margin_read_label = QtWidgets.QLabel('2nd Margin 1 read', self.mid)
        margin_read_label.setStyleSheet("font-weight:bold; font-size: 13px;")
        margin_read_label.setGeometry(170, 480, 300, 50)
        read_back_label = QtWidgets.QLabel('Byte40_to_Byte45_readback', self.mid)
        read_back_label.setGeometry(50, 555, 150, 30)
        self.read_back_B40_to_B45.setGeometry(215, 545, 200, 50)
        second_read_Value_error_label = QtWidgets.QLabel('Second_read_value_error', self.mid)
        second_read_Value_error_label.setGeometry(100, 620, 150, 30)
        self.second_read_Value_error.setGeometry(310, 620, 50, 30)
        match_label = QtWidgets.QLabel('Does readback match the value burnt to the part?', self.mid)
        match_label.setGeometry(25, 680, 285, 30)
        self.B40_B45_match.setGeometry(310, 680, 100, 30)
        first_burn_margin_read_button = QtWidgets.QPushButton('Run', self.mid)
        first_burn_margin_read_button.clicked.connect(self.second_burn_margin_read)
        first_burn_margin_read_button.setGeometry(160, 725, 120, 50)
        self.mid.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.mid.setGeometry(0, 0, 750, 700)

        # 3rd pass burn and Margin read
        title_label = QtWidgets.QLabel('3rd pass burn and Margin read', self.right)
        title_label.setStyleSheet("font-weight:bold; font-size: 18px;")
        title_label.setGeometry(110, 20, 300, 150)
        pass_burn_label = QtWidgets.QLabel('3rd pass burn', self.right)
        pass_burn_label.setStyleSheet("font-weight:bold; font-size: 13px;")
        pass_burn_label.setGeometry(185, 90, 300, 100)
        Byte58_to_Byte61_label = QtWidgets.QLabel('Byte58_to_Byte61', self.right)
        Byte58_to_Byte61_label.setGeometry(50, 200, 100, 30)
        Byte58_to_Byte61_value = """0x00 0x00 0x00 0x90"""
        self.Byte58_to_Byte61.setGeometry(200, 190, 200, 50)
        self.Byte58_to_Byte61.setText(Byte58_to_Byte61_value)
        B46_OTP_start_address_label = QtWidgets.QLabel('B46(OTP_start_address)', self.right)
        B46_OTP_start_address_label.setGeometry(100, 290, 150, 30)
        self.B46_OTP_start_address_3.setText('0x3A')
        self.B46_OTP_start_address_3.setGeometry(310, 290, 50, 30)
        B47_OTP_stop_address_label = QtWidgets.QLabel('B47(OTP_stop_address)', self.right)
        B47_OTP_stop_address_label.setGeometry(100, 365, 150, 30)
        self.B47_OTP_stop_address_3.setText('0x3D')
        self.B47_OTP_stop_address_3.setGeometry(310, 365, 50, 30)
        B48_Ram_burn_start_address_label = QtWidgets.QLabel('B48(Ram_burn_start_address)', self.right)
        B48_Ram_burn_start_address_label.setGeometry(100, 440, 150, 30)
        self.B48_Ram_burn_start_address_3.setText('0x22')
        self.B48_Ram_burn_start_address_3.setGeometry(310, 440, 50, 30)
        margin_read_label = QtWidgets.QLabel('3rd Margin 1 read', self.right)
        margin_read_label.setStyleSheet("font-weight:bold; font-size: 13px;")
        margin_read_label.setGeometry(170, 480, 300, 50)
        read_back_label = QtWidgets.QLabel('Byte58_to_Byte61_readback', self.right)
        read_back_label.setGeometry(50, 555, 150, 30)
        self.read_back_B58_to_B61.setGeometry(215, 545, 200, 50)
        third_read_Value_error_label = QtWidgets.QLabel('Third_read_value_error', self.right)
        third_read_Value_error_label.setGeometry(100, 620, 150, 30)
        self.third_read_Value_error.setGeometry(310, 620, 50, 30)
        match_label = QtWidgets.QLabel('Does readback match the value burnt to the part?', self.right)
        match_label.setGeometry(25, 680, 285, 30)
        self.B58_B61_match.setGeometry(310, 680, 100, 30)
        first_burn_margin_read_button = QtWidgets.QPushButton('Run', self.right)
        first_burn_margin_read_button.clicked.connect(self.third_burn_margin_read)
        first_burn_margin_read_button.setGeometry(160, 725, 120, 50)
        self.right.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.right.setGeometry(0, 0, 750, 700)

        splitter1 = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(self.left)
        splitter1.addWidget(self.mid)
        splitter1.addWidget(self.right)
        splitter1.resize(300, 400)
        self.hbox.addWidget(splitter1)
        self.Gui.setLayout(self.hbox)
        self.Gui.setWindowTitle('OTP Program')
        self.Gui.showMaximized()

    def power1_setup(self, channel, ran, voltage, current):
        self.power1.select_channel(channel)
        self.power1.select_range(ran)
        self.power1.set_voltage(voltage, current)

    def power1_on_off(self, status):
        self.power1.on_off(status)

    # def power2_setup(self, channel, voltage, current):
    #     self.power2.set_voltage(channel, voltage, current)
    #
    # def power2_on_off(self, status):
    #     self.power2.on_off(status)

    def fun_setup(self, channel, frequency, duty_cycle, vlow, vhigh):
        self.fun.freq(channel, frequency)
        self.fun.duty_cycle(channel, duty_cycle)
        self.fun.vhigh_vlow(channel, vlow, vhigh)

    def fun_on_off(self, channel, status):
        self.fun.on_off(channel, status)

    def i2c_read(self, start_address, length):
        return list(self.dut_i2c.aa_read_i2c(start_address, length))

    def i2c_write(self, start_address, resigster_values):
        self.dut_i2c.aa_write_i2c(start_address, resigster_values)

    def first_burn_margin_read(self):
        self.third_read_Value_error.clear()
        self.read_back_B58_to_B61.clear()
        self.B58_B61_match.clear()

        # # E3631 power supply setup
        # power_channel = 1; power_voltage = 3.3; power_current = 0.3
        # self.power2_setup(power_channel, power_voltage, power_current)
        # self.power2_on_off('OFF')
        # self.power2_on_off('ON')

        # E3646 power supply setup
        power_channel1 = 1; power_range1 = 'LOW'; power_voltage1 = 3.3; power_current1 = 0.3
        power_channel2 = 2; power_range2 = 'LOW'; power_voltage2 = 7; power_current2 = 0.3
        self.power1_setup(power_channel1, power_range1, power_voltage1, power_current1)
        self.power1_setup(power_channel2, power_range2, power_voltage2, power_current2)
        self.power1_on_off('OFF')
        self.power1_on_off('ON')

        # 81130A setup
        fun_channel = 1; fun_frequency = 100; fun_duty_cycle = 50; fun_vlow = 0; fun_vhigh = 0.8
        self.fun_setup(fun_channel, fun_frequency, fun_duty_cycle, fun_vlow, fun_vhigh)
        self.fun_on_off(fun_channel, 1)
        time.sleep(1)

        value = self.Byte0_to_Byte39.toPlainText()
        write_value = []*40
        for i in range(0,40):
            hex_express = str(value[5*i:5*i+4])
            hex_int = int(hex_express, 16)
            write_value.append(hex_int)
        self.i2c_write(128, write_value)
        time.sleep(2)
        try:
            burn_result = self.i2c_read(128, 40)
            print (write_value[1:])
            print (burn_result)
            self.first_read_Value_error.setText('No')
            if write_value[1:] == burn_result:
                B46 = int(str(self.B46_OTP_start_address_1.text()), 16)
                B47 = int(str(self.B47_OTP_stop_address_1.text()), 16)
                B48 = int(str(self.B48_Ram_burn_start_address_1.text()), 16)
                burn_registers = [B46, B47, B48]
                self.i2c_write(174, burn_registers)
                time.sleep(0.1)
                # # Burn OTP
                self.i2c_write(173, [0x8C])
                time.sleep(0.5)
                self.i2c_write(173, [0x0C])
                time.sleep(0.5)
                # Margin 1 read
                self.i2c_write(128, [0x00]*40)
                time.sleep(0.5)
                self.i2c_write(177, [0x00])
                time.sleep(0.1)
                self.i2c_write(173, [0x4C])
                time.sleep(0.1)
                self.i2c_write(173, [0x0C])
                time.sleep(1)
                margin_read = self.i2c_read(128, 40)
                row1 = ''
                row2 = ''
                row3 = ''
                row4 = ''
                for i in range(0,10):
                    row1 += str(hex(margin_read[i])) + ' '
                    row2 += str(hex(margin_read[i+10])) + ' '
                    row3 += str(hex(margin_read[i+20])) + ' '
                    row4 += str(hex(margin_read[i+30])) + ' '
                read_back = """%s
%s
%s
%s
                """ % (row1, row2, row3, row4)
                self.read_back_B0_to_B39.setText(read_back)
                if write_value[1:] != margin_read:
                    self.log.warn('The burning is not correct. Please check the setup and do it again.')
                    self.B0_B39_match.setText('It is not matched.')
                else:
                    self.log.info('1st pass burn and margin 1 read are successful, please go on.')
                    self.B0_B39_match.setText('It is matched.')
            else:
                self.log.warn('The burning is not correct. Please check the setup and do it again.')
        except ValueError:
            self.first_read_Value_error.setText('Yes')

    def second_burn_margin_read(self):
        self.read_back_B0_to_B39.clear()
        self.first_read_Value_error.clear()
        self.B0_B39_match.clear()
        value = self.Byte40_to_Byte45.text()
        write_value = [] * 6
        for i in range(0, 6):
            hex_express = str(value[5 * i:5 * i + 4])
            hex_int = int(hex_express, 16)
            write_value.append(hex_int)
        self.i2c_write(162, write_value)
        time.sleep(2)
        try:
            burn_result = self.i2c_read(162, 6)
            self.second_read_Value_error.setText('No')
            if write_value[1:] == burn_result:
                B46 = int(str(self.B46_OTP_start_address_2.text()), 16)
                B47 = int(str(self.B47_OTP_stop_address_2.text()), 16)
                B48 = int(str(self.B48_Ram_burn_start_address_2.text()), 16)
                burn_registers = [B46, B47, B48]
                self.i2c_write(174, burn_registers)
                time.sleep(0.1)
                # Burn OTP
                self.i2c_write(173, [0x8C])
                time.sleep(0.5)
                self.i2c_write(173, [0x0C])
                time.sleep(0.5)
                # Margin 1 read
                self.i2c_write(162, [0x00] * 6)
                time.sleep(0.5)
                self.i2c_write(177, [0x22])
                time.sleep(0.1)
                self.i2c_write(173, [0x4C])
                time.sleep(0.1)
                self.i2c_write(173, [0x0C])
                time.sleep(1)
                margin_read = self.i2c_read(162, 6)
                read_list = []
                for i in range(0,6):
                    read_list.append(hex(margin_read[i])+' ')
                read_str = ''.join(read_list)
                self.read_back_B40_to_B45.setText(read_str)
                if write_value[1:] != margin_read:
                    self.log.warn('The burning is not correct. Please check the setup and do it again.')
                    self.B40_B45_match.setText('It is not matched.')
                else:
                    self.log.info('2nd pass burn and margin 1 read are successful, please go on.')
                    self.B40_B45_match.setText('It is matched.')
            else:
                self.log.warn('The burning is not correct. Please check the setup and do it again.')
        except ValueError:
            self.first_read_Value_error.setText('Yes')

    def third_burn_margin_read(self):
        self.second_read_Value_error.clear()
        self.read_back_B40_to_B45.clear()
        self.B40_B45_match.clear()
        value = self.Byte58_to_Byte61.text()
        write_value = [] * 4
        for i in range(0, 4):
            hex_express = str(value[5 * i:5 * i + 4])
            hex_int = int(hex_express, 16)
            write_value.append(hex_int)
        self.i2c_write(162, write_value)
        time.sleep(2)
        try:
            burn_result = self.i2c_read(162, 4)
            self.third_read_Value_error.setText('No')
            if write_value[1:] == burn_result:
                B46 = int(str(self.B46_OTP_start_address_3.text()), 16)
                B47 = int(str(self.B47_OTP_stop_address_3.text()), 16)
                B48 = int(str(self.B48_Ram_burn_start_address_3.text()), 16)
                burn_registers = [B46, B47, B48]
                self.i2c_write(174, burn_registers)
                time.sleep(0.1)
                # Burn OTP
                self.i2c_write(173, [0x8C])
                time.sleep(0.5)
                self.i2c_write(173, [0x0C])
                time.sleep(0.5)
                # Margin 1 read
                self.i2c_write(162, [0x00] * 4)
                time.sleep(0.5)
                self.i2c_write(177, [0x22])
                time.sleep(0.1)
                self.i2c_write(173, [0x4C])
                time.sleep(0.1)
                self.i2c_write(173, [0x0C])
                time.sleep(1)
                margin_read = self.i2c_read(162, 4)
                read_list = []
                for i in range(0, 4):
                    read_list.append(hex(margin_read[i]) + ' ')
                read_str = ''.join(read_list)
                self.read_back_B58_to_B61.setText(read_str)
                if write_value[1:] != margin_read:
                    self.log.warn('The burning is not correct. Please check the setup and do it again.')
                    self.B58_B61_match.setText('It is not matched.')
                else:
                    self.log.info('3rd pass burn and margin 1 read are successful, please go on.')
                    self.B58_B61_match.setText('It is matched.')
            else:
                self.log.warn('The burning is not correct. Please check the setup and do it again.')
        except ValueError:
            self.first_read_Value_error.setText('Yes')


def main():
    app = QtWidgets.QApplication(sys.argv)
    a = OTP_Program(18, 19, 0x6C, 10)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()