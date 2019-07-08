import visa
phase_noise = visa.ResourceManager().open_resource('GPIB0::17::INSTR')
phase_noise.timeout = 50000
name1 = '"C:\\Users\\jgou\\Desktop\\test\\1.png"'
name2 = '"C:\\Users\\jgou\\Desktop\\test\\1.csv"'
phase_noise.write(":MMEMory:STORe:IMAGe %s" % name1)
phase_noise.write(":MMEMory:PN:TRACe:STORe %s" % name2)
phase_noise.write(':SENSe:PN:FBANd BAND2')
phase_noise.write(':SENSe:PN:IFGain 50')
phase_noise.write(':CALCulate:PN:TRACe:MARKer8:STATe ON')
phase_noise.write('DISPlay:MESSage:CLEar')
phase_noise.write(':TRIGger:SOPC ON')
phase_noise.write(':TRIGger:AVERage ON')
phase_noise.write(':INITiate:PN:IMMediate')
phase_noise.write(':INITiate:PN:CONTinuous OFF')
phase_noise.write(':SENSe:PN:AVERage:STATe ON')
phase_noise.write(':SENSe:PN:AVERage:COUNt 16')
phase_noise.write(':SENSe:PN:CORRelation:COUNt 2')
phase_noise.write(':INITiate:PN:CONTinuous ON')
status = str(phase_noise.query('*OPC?')).strip()
if status == '+1':
    phase_noise.write(':INITiate:PN:CONTinuous OFF')
else:
    print 'it is wrong.'
print str(phase_noise.query(':CALCulate:PN:TRACe:FUNCtion:INTegral:DATA?')).split(',')[4]
