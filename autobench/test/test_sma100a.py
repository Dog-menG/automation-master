from autobench.inst import SMA100A

test = SMA100A.SMA100A(28)
test.rf_frequency('100MHz')
test.rf_output_level('300mV')
test.rf_out_state(1)