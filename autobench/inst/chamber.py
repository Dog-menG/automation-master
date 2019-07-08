import visa
import time


class Chamber(object):
    """MMT Temp Chamber GPIB Control"""

    def __init__(self, gpib_addr):
        """
        Initiate Chamber GPIB interface
        :param gpib_addr: GPIB address, no need for the full resource name, only GPIB int
        :rtype None
        """
        self.chamber = visa.ResourceManager().open_resource('GPIB0::%s::INSTR' % gpib_addr)

    def set_temp(self, tar_temp):
        self.chamber.write('TEMP, S' + str(tar_temp))
        time.sleep(0.05)

    def read_temp(self):
        self.chamber.query("TEMP?")
        time.sleep(0.05)
        temp = self.chamber.query("TEMP?")
        time.sleep(0.5)
        return float(temp.split(',')[0])

    def chanmber_operating_mode(self, operating_mode):
        """
        This command is used to switch the chamber to the specified operating mode.
        :param operating_mode: the operating mode: 'OFF': turn control power off, type: str
                                                    'STANDBY': set the chamber on standby, type: str
                                                    'CONSTANT': set the constant mode, type: str
                                                    "RUN program N0.": run a program, type: str
        :return: None
        :rtype: None
        """
        self.chamber.write("MODE, %s" % operating_mode)

    def erase_program(self, program_number):
        """
        This command is used to delete specified program
        :param program_number: the program number to be deleted, type :int
        :return: None
        :rtype: None
        """
        self.chamber.write("PRGM ERASE, PGM: %s" % program_number)

    def query_current_program(self):
        """
        This command is used to request the chamber to return the setup of current remote program.
        :return: 'start temp, target temp, exposure time, REF code'
        :rtype: str
        """
        return self.chamber.query("RUN PRGM?")

    def query_operating_mode(self):
        """
        This command is used to request the chamber to return the operating mode.
        :return: operating mode of the chamber
        :type: str
        """
        return self.chamber.query("MODE?")

    def query_written_program(self, program_number):
        """
        This command is used to request the chamber to return the setup of the specified program.
        :param program_number: the program number to be returned, type: int
        :return: "Number of steps, number of cycles, end mode"
        :rtype: str
        """
        return self.chamber.query("PRGM DATA?, PGM: %s" % program_number)

    def query_step(self, program_number, step_number):
        """
        This command is used to request the chamber to return the setup of the specified step of specified program.
        :param program_number: the program number to be returned, type: int
        :param step_number: the step number to be returned, type: int
        :return: "step NO., target temp, temperature control setting, exposure time setting, guaranteed soak control"
        :rtype: str
        """
        return self.chamber.query("PRGM DATA?, PGM: %s, STEP%s" % (program_number, step_number))

    def query_temp(self):
        """
        This command is used to request the chamber temperature parameter.
        :return: 'Monitored temp, target temp, absolute high temp limit, absolute low temp limit'
        :rtype: str
        """
        return self.chamber.query("TEMP?")

    def setup_program(self, start_temp, target_temp, exposure_time):
        """
        This command is used to set up a program to be run from the remote. The program is started automatically when
        the setup is complete.
        :param start_temp: start_temperature, type: one precision digit float
        :param target_temp: target_temperature, type: one precison digit float
        :param exposure_time: exposure or during time, type: str
        :return: None
        :rtype: None
        """
        # self.chamber.write("RUN PRGM, TEMP%s GOTEMP%s TIME%s" % (start_temp, target_temp, exposure_time))
        self.chamber.write("RUN PRGM, TEMP%s TRAMP ON TIME%s" % (start_temp, exposure_time))

    def write_program_counter(self, program_number, start_repeated_number, stop_repeated_number, repeated_number):
        """
        This command is used to set the repeat counter.
        :param program_number: the program number, type:int
        :param start_repeated_number: the number of repeat cycle start step, type: int
        :param stop_repeated_number: the number of repeat cycle end step, type: int
        :param repeated_number: the number of repeat cycle, type: int
        :return: None
        :rtype: None
        """
        self.chamber.write("PRGM DATA WRITE, PGM: %s, COUNT,(%s, %s, %s)"
                   % (program_number, start_repeated_number, stop_repeated_number, repeated_number))

    def write_program_end_mode(self, program_number, end_mode):
        """
        This command is used to set end mode.
        :param program_number: the program number, type: int
        :param end_mode: end mode, 'OFF': shut off control power at program end, type: str
                                    'HOLD': hold the last step at program end, type: str
                                    'CONSTANT': run the constant mode at program end, type: str
        :return: None
        :rtype: Mome
        """
        self.chamber.write("PRGM DATA WRITE, PGM: %s, END, %s" % (program_number, end_mode))

    def write_program_humidity(self, program_number, step_number, target_humi, exposure_time):
        """
        This command is used to set temperature program
        :param program_number: the program number, type: int
        :param step_number: the step number, type: int
        :param target_humi: the target temperature, type: float
        :param exposure_time: the exposure time, type: str
        :return: None
        :rtype: None
        """
        self.chamber.write("PRGM DATA WRITE, PGM: %s, STEP%s, HUMI%s, TIME %s"
                   % (program_number, step_number, target_humi, exposure_time))

    def write_program_temperature(self, program_number, step_number, target_temp, exposure_time):
        """
        This command is used to set temperature program
        :param program_number: the program number, type: int
        :param step_number: the step number, type: int
        :param target_temp: the target temperature, type: float
        :param exposure_time: the exposure time, type: str
        :return: None
        :rtype: None
        """
        self.chamber.write("PRGM DATA WRITE, PGM: %s, STEP%s, TEMP%s, TRAMP ON, TIME %s"
                   % (program_number, step_number, target_temp, exposure_time))

    def write_program(self, program_numer, step_number, target_temp, exposure_time, end_mode):
        """
        This command is used to set up program.
        :param program_number: the program number, type: int
        :param step_number: the step number, type: int
        :param target_temp: the target temperature, type: float
        :param exposure_time: the exposure time, type: str
        :param end_mode: end mode, 'OFF': shut off control power at program end, type: str
                                    'HOLD': hold the last step at program end, type: str
                                    'CONSTANT': run the constant mode at program end, type: str
        :return: None
        :rtype: Mome
        """
        self.chamber.write("PRGM DATA WRITE, PGM: %s, EDIT START" % program_numer)
        self.write_program_temperature(program_numer, step_number, target_temp, exposure_time)
        self.write_program_end_mode(program_numer, end_mode)
        self.chamber.write("PRGM DATA WRITE, PGM: %s, EDIT END" % program_numer)

    def overwrite_program(self, program_numer, step_number, target_temp, exposure_time, end_mode):
        """
        This command is used to edit program.
        :param program_number: the program number, type: int
        :param step_number: the step number, type: int
        :param target_temp: the target temperature, type: float
        :param exposure_time: the exposure time, type: str
        :param end_mode: end mode, 'OFF': shut off control power at program end, type: str
                                    'HOLD': hold the last step at program end, type: str
                                    'CONSTANT': run the constant mode at program end, type: str
        :return: None
        :rtype: Mome
        """
        self.chamber.write("PRGM DATA WRITE, PGM: %s, OVER WRITE START" % program_numer)
        self.write_program_temperature(program_numer, step_number, target_temp, exposure_time)
        self.write_program_end_mode(program_numer, end_mode)
        self.chamber.write("PRGM DATA WRITE, PGM: %s, OVER WRITE END" % program_numer)
