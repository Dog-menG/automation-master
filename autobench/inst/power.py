from autobench.inst.gpib import GPIB


class E3631A(GPIB):
    # A class that defines and controls E3631A through GPIB
    powername = 'E3631A'

    def __init__(self, gpib_addr):
        super(E3631A, self).__init__(gpib_addr, self.powername)

    def on_off(self, status):
        if status == 'ON':
            self.write("OUTPUT:STATe ON")
        else:
            self.write("OUTPUT:STATe OFF")

    def set_voltage(self, channel, voltage, current=0.8):
        if channel == 1:
            self.write('APPL P6V, %s, %s' % (voltage, current))
        elif channel == 2:
            self.write('APPL P25V, %s, %s' % (voltage, current))
        elif channel == 3:
            self.write('APPL N25V, %s, %s' % (voltage, current))
        else:
            self.logger('The input is invalid.')

    def read_current(self):
        return float(self.query('MEASure:CURRent:DC?'))

    def read_voltage(self):
        return float(self.query('MEASure:VOLTage:DC?'))

    def reset(self):
        self.write('*RST')

    def clear(self):
        self.write('*CLS')

    def save_state(self, save_number):
        try:
            self.write('*SAV %s' % save_number)
        except not(save_number == 1 or save_number == 2 or save_number == 3):
            self.logger('Save_number is invaild.', lvl=2)
            pass

    def recall_state(self, recall_number):
        try:
            self.write('*RCL %s' % recall_number)
        except not(recall_number == 1 or recall_number == 2 or recall_number == 3):
            self.logger('The input is invaild.', lvl=2)
            pass


class E3632_3_4A(E3631A):
    """Used for Agilent E3632/33/34A"""

    def __init__(self, gpib_addr):
        self.powername = "E3632A"
        super(E3632_3_4A, self).__init__(gpib_addr)

    def set_voltage(self, voltage, current=0.8):
        self.write('APPL %s, %s' % (voltage, current))

    def incre_decre(self, step, direction):
        self.write('VOLT:STEP %s' % step)
        self.write('VOLT %s' % direction)

    def select_range(self, power_range):
        self.write('VOLTage:RANGe %s' % power_range)


class E3646A(E3632_3_4A):
    def __init__(self, gpib_addr):
        self.powername = "E3634A"
        super(E3632_3_4A, self).__init__(gpib_addr)

    def select_channel(self, channel):
        self.write('INST:SEL OUT%s' % channel)
