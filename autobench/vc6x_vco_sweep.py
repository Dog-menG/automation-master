from __future__ import print_function
from sweep_temp_vco import SweepTempVCO
import time
import sys
import logging

sys.path.append('.')


def main(power_on_off, start_temp, stop_temp, stepping, serial=0, tol_temp=0.2):
    vc6x = SweepTempVCO(0x6a)
    logfile = open("log" + str(serial) + '_' + str(start_temp) + "_" + str(stop_temp) + ".txt", 'w+')
    time.sleep(1)
    # vc6x.power_on(False)
# a trick to increase stop_temp by one step
    if (start_temp - stop_temp) % stepping != 0:
        stop_temp += stepping
    for temp in range(start_temp, stop_temp, stepping):
        curr_temp = vc6x.read_temp()
# to decide stop temp by whether temp rises or falls
        if start_temp > stop_temp:
            # if temp + stepping < stop_temp:
            #     temp = stop_temp - stepping
            # else:
            #     pass
            temp = (lambda x: stop_temp - stepping if temp + stepping < stop_temp else temp)(temp)
        elif start_temp < stop_temp:
            # if temp + stepping > stop_temp:
            #     temp = stop_temp - stepping
            # else:
            #     pass
            temp = (lambda x:stop_temp - stepping if temp + stepping > stop_temp else temp)(temp)
        vc6x.set_temp(temp)
        print("RAMP TEMP TO " + str(temp))
        while not((curr_temp < (temp + tol_temp)) and (curr_temp > (temp - tol_temp))):
            curr_temp = vc6x.read_temp()
            print(".", end='')
        if temp == start_temp:
            print("SOAK TIME 1MIN AT STARTING POINT...")
            time.sleep(2)
        if power_on_off in ('y', 'Y'):
            vc6x.power_on(False)
            time.sleep(1)
            idd = vc6x.power_on()
            time.sleep(1)
            if idd < 0.02:
                raise EnvironmentError("IDD TOO SMALL PLEASE CHECK SETUP")
        else:
            idd = vc6x.power_on()
            time.sleep(10)
            if idd < 0.02:
                raise EnvironmentError("IDD TOO SMALL PLEASE CHECK SETUP")
        time.sleep(2)
        frequency1 = vc6x.freq(1,2)[0]
        frequency2 = vc6x.freq(1,2)[1]
        ratio = float('%.6f' % (float(vc6x.freq(1,2)[2])))
        vco_band = list(vc6x.dut_i2c.aa_read_i2c(0x99))[0]
        print('\nLOG: ' + str(time.time()) + '\t' + str(temp) + '\t' + str(frequency1) + '\t' + str(frequency2) + '\t' + str(ratio) + '\t' + str(vco_band))
        logfile.write(str(time.time()) + '\t' + str(temp) + '\t' + str(frequency1) + '\t' + str(frequency2) + '\t' + str(ratio) + '\t' + str(vco_band) + '\n')
    logfile.close()
    vc6x.set_temp(25)
    vc6x.close()

if __name__ == '__main__':
    unitnum = int(raw_input('Please enter the unit number: '))
    power_on_off = str(raw_input('Do you want to recycle power every step?      Y or N ? '))
    print("STARTING TEMP.......... FROM -40C to 105C")
    main(power_on_off, -40, 105, 10, unitnum)
    print("\nDone with first round, starting from 105C.....")
    print("STARTING TEMP.......... FROM 105C to -40C")
    time.sleep(5)
    main(power_on_off, 105, -40, -10, unitnum)
