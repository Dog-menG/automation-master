import pyvisa


def open_res(type, addr):
    if type == 'GPIB':
        return pyvisa.ResourceManager().open_resource('GPIB0::%s::INSTR' % addr)