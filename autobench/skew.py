from inst.scope import Keysight
from inst.func_gen import Agilent81130A
from inst.power import E3631A, E3646A
from autobench import log
from i2c.aa_i2c import AAReadWrite
from email_txt_msg import Email_Txt_Msg
import time


class MultiplePowerUp(object):

    def __init__(self, i2c_add=0x6C):
        self.log = log(self.__class__.__name__)
        self.fun = Agilent81130A()
        self.scope = Keysight()
        self.mail = Email_Txt_Msg()
        self.power1 = E3631A(18)
        self.power2 = E3646A(19)
        self.dut_i2c = AAReadWrite(0, i2c_add, True)

    def i2c_write(self, byte, value):
        self.dut_i2c.aa_write_i2c(byte, value)

    def fun_setup(self):
        self.fun.on_off(1, 'ON')
        self.fun.freq(1, 100)
        self.fun.duty_cycle(1, 50)
        self.fun.vhigh_vlow(1, 0, 0.8)

    def scope_setup(self, input_channel, output_channel):
        self.scope.measure_clear()
        self.scope.acquisition(10e3, 10e9, 10e-9)
        self.scope.source_on(input_channel)
        self.scope.source_on(output_channel)
        self.scope.source_setup(input_channel, 0, 0.25)
        self.scope.source_setup(output_channel, 0, 0.25)
        self.scope.thresholds_general('PERCent', input_channel, 80, 50, 20)
        self.scope.thresholds_general('PERCent', output_channel, 80, 50, 20)
        self.scope.trigger_setup(output_channel, 'Positive', 0, 'AUTO')
        self.scope.run_mode('RUN')

    def power_setup(self):
        self.power1 = E3631A(18)
        self.power1.set_voltage(2, 3.3, 0.6)
        self.power2 = E3646A(19)
        self.power2.select_channel(1)
        self.power2.set_voltage(3.3, 0.5)

    def scope_measure(self):
        self.scope.measure_delta_time('Channel3', 'Channel1', 'RISing', 4, 'MIDDle', 'RISing', 4, 'MIDDle')
        return self.scope.get_result()[4]

    def power_on_off(self, source, status):
        if source == 1:
            self.power1.on_off(status)
        elif source == 2:
            self.power2.on_off(status)
        else:
            self.log.info('Source number is invalid')

    def measure(self):
        state = 'normal'
        result = False
        count = 0
        self.power_on_off(2, True)
        self.i2c_write(139, [0xC0])
        time.sleep(0.5)
        propogation = float(self.scope_measure()) * 10e11
        self.log.info('The propogation delay of PLL mode is %f ps' % propogation)
        while state is 'normal':
            if abs(propogation) > 500:
                self.i2c_write(139, [0xC0])
                state = 'abnormal'
            else:
                self.power_on_off(2, False)
                self.power_on_off(2, True)
                time.sleep(0.1)
                self.i2c_write(139, [0xC0])
                time.sleep(0.5)
                propogation = float(self.scope_measure()) * 10e11
                self.log.info('The propogation delay of PLL mode is %f ps' % propogation)
        self.i2c_write(172, [0x84])
        self.i2c_write(172, [0x80])
        while result is False:
            self.log.info('This is the %d cycle' % count)
            propogation = float(self.scope_measure()) * 10e11
            self.log.info('The propogation delay of PLL mode is %f ps' % propogation)
            if abs(propogation) > 500:
                result = True
                self.log.info('There is one more step for output divider.')
            else:
                result = False
                self.i2c_write(172, [0x84])
                self.i2c_write(172, [0x80])
                time.sleep(0.5)
                self.log.info('Output divider works well.')
                count += 1

    def send_mail(self, source, destination, subject, text):
        self.mail.send_msg(source, destination, subject, text)


def main():
    test = MultiplePowerUp()
    test.fun_setup()
    test.scope_setup('Channel1', 'Channel3')
    test.power_setup()
    test.measure()
    # test.send_mail('jun.gou@idt.com', '4084831216@vtext.com', 'The test is done.', 'The test is done. Please take care.')

if __name__ == "__main__":
    main()

