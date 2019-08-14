from autobench.inst.scope import Keysight
from autobench.inst.func_gen import Agilent81130A
from autobench.inst.power import E3631A, E3646A
from autobench import log
import time


class MultiplePowerUp(object):

    def __init__(self):
        self.log = log(self.__class__.__name__)
        self.fun = Agilent81130A()
        self.scope = Keysight()
        self.power1 = E3631A(18)
        self.power2 = E3646A(19)

    def fun_setup(self):
        self.fun.on_off(1, 'ON')
        self.fun.freq(1, 100)
        self.fun.duty_cycle(1, 50)
        self.fun.vhigh_vlow(1, 0, 0.8)

    def scope_setup(self, channel=2):
        self.scope.measure_clear()
        self.scope.acquisition(10e3, 20e9, 10e-9)
        self.scope.source_on('channel' + str(channel))
        self.scope.source_scale_setup('channel' + str(channel), 0, 0.25)
        self.scope.thresholds_general_percent('Channel' + str(channel), 80, 50, 20)
        self.scope.trigger_setup('Channel' + str(channel), 'Positive', 0, 'AUTO')
        self.scope.run_mode('RUN')

    def power_setup(self):
        self.power1 = E3631A(18)
        self.power1.set_voltage(2, 3.3, 0.6)
        self.power2 = E3646A(19)
        self.power2.select_channel(1)
        self.power2.set_voltage(3.3, 0.1)

    def scope_measure(self):
        self.scope.measure('Channel2', 'Frequency')
        return self.scope.get_result()[2]

    def power_on_off(self, source, status):
        if source == 1:
            self.power1.on_off(status)
        elif source == 2:
            self.power2.on_off(status)
        else:
            self.log.info('Source number is invalid')

    def measure(self):
        result = False
        count = 0
        while result is False:
            self.log.info('This is the %d cycle' % count)
            self.power_on_off(1, True)
            self.power_on_off(2, False)
            self.power_on_off(2, True)
            time.sleep(0.5)
            frequency = float(self.scope_measure())/1e6
            self.log.info('The output frequency is %f MHz' % frequency)
            dif = frequency - 100
            self.log.info('The difference between output frequency and 100MHz is %f MHz' % dif)
            if dif < 1 and dif > -1:
                result = False
                count += 1
                self.log.info('It is locked.')
                self.power_on_off(2, 'OFF')
            else:
                result = True
                self.log.info('It is unlocked.')


def main():
    test = MultiplePowerUp()
    test.fun_setup()
    test.scope_setup()
    test.power_setup()
    test.measure()

if __name__ == "__main__":
    main()

