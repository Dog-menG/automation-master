from autobench.inst import scope
import visa, time

# a = visa.ResourceManager().open_resource(visa.ResourceManager().list_resources()[0])
# a.timeout = 100000
b = visa.ResourceManager().list_resources()
print b
# c = b.open_resource('GPIB0::7::INSTR')
# for i in range(100,121,1):
#     c.write(':FREQuency1 %sMHz' % i)
#     time.sleep(5)
# a.timeout = 60000
# a.write(':BLANk CHANnel1')
# a.write(':BLANk CHANnel2')
# a.write(':BLANk CHANnel3')
# a.write(':BLANk CHANnel4')
# a.write(':VIEW CHANnel2')
# a.write(':VIEW CHANnel3')
# a.write(':MEASure:VPP Channel2')
# print a.ask(':MEASure:RESults?').split(',')
# a.write(':MEASure:FREQuency CHANnel1,Rising')
# print a.ask(':MEASure:RESults?').split(',')
# a.write(':AUToscale')
# a.write('*WAI')
# a.write(':MEAsure:VPP CHANnel3')
# a.write(':MEASure:STATistics MEAN')
# amplitude = a.query(':MEASure:RESults?')[4]
# a.write(':CHANnel3:RANGe %s' % amplitude)
# print "{0:.5f}".format(float(amplitude))
# print a.query('*IDN?')
# a.write(':CHANnel2:OFFset 0')
# print a.query(':CHANnel2:DISPlay:RANGe?')

# a.write(':AUToscale:VERTical CHANnel2 ')

# a.write(':FUNCtion1:MTRend MEAS1')
# b = r"\\Corpgroup\FTGInfo\9FGLxxx\9FGL6241_eSSD\9FGL6241Q3LTGI_AP635T-065-070_Xtal\input_file\LDR"
# b = r"S:\9FGLxxx\9FGL6241_eSSD\9FGL6241Q3LTGI_AP635T-065-070_Xtal\LDR\Dif_in_-0p5SS_PLL_spoff\1"
# print a.query(':FUNC1?')
# a.write(':DISK:SAVE:WAVeform FUNCtion1,"%s" ,TXT,OFF' % b)
# a.write('FUNCtion1:Display off')
# a.write(":MEASURE:PERIOD CHANNEL1, RISING")
# a.write(":FUNCTION1:MTREND MEAS1")
# a.write(":FUNCTION1:DISPLAY ON")
# a.write(':MEASure:VPP CHAnnel2')
# print a.ask(':MEASure:RESults?')
# print a.query(':MEASure:RESults?')
# a.write(':CDISplay')
# a.write(':DISK:SAVE:WAVeform FUNCtion2,"%s" ,TXT,OFF' % b)