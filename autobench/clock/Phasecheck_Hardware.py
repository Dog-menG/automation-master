from autobench.inst.scope import Keysight
from autobench.inst.func_gen import Agilent81130A
from autobench.inst.power import E3646A
from autobench import log
from autobench.email_txt_msg import Email_Txt_Msg
import time


class MultiplePowerUp(object):

    def __init__(self, i2c_add=0x6C):
        self.log = log(self.__class__.__name__)
        self.fun = Agilent81130A()
        self.scope = Keysight()
        self.mail = Email_Txt_Msg()
        self.power2 = E3646A(19)

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
        self.scope.source_on(output_channel)
        self.scope.source_setup(input_channel, 0, 0.25)
        self.scope.source_setup(output_channel, 0, 0.25)
        self.scope.thresholds_general('PERCent', input_channel, 80, 50, 20)
        self.scope.thresholds_general('PERCent', output_channel, 80, 50, 20)
        self.scope.trigger_setup(output_channel, 'Positive', 0, 'AUTO')
        self.scope.run_mode('RUN')

    def power_setup(self):
        self.power2 = E3646A(19)
        self.power2.select_channel(1)
        self.power2.set_voltage(3.3, 0.5)

    def scope_measure(self):
        self.scope.measure_delta_time('Channel3', 'Channel1')
        return self.scope.get_result()[4]

    def power_on_off(self, source, status):
        self.power2.on_off(status)

    def measure(self):
        state = 'normal'
        self.power_on_off(2, True)
        time.sleep(2)
        propagation = float(self.scope_measure()) * 10e11
        self.log.info('The propogation delay of PLL mode is %f ps.' % propagation)
        while state is 'normal':
            if abs(propagation) > 500:
                self.log.info('The propagation delay of PLL mode is %f ps.' % propagation)
                self.log.info('The I2O shift still exits!')
                state = 'abnormal'
            else:
                self.power_on_off(2, False)
                self.power_on_off(2, True)
                time.sleep(2)
                propagation = float(self.scope_measure()) * 10e11
                self.log.info('The propagation delay of PLL mode is %f ps.' % propagation)


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

