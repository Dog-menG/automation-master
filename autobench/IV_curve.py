import visa
import time
import sys
import os
import xlsxwriter
from xlsxwriter.utility import xl_col_to_name
import matplotlib.pyplot as plt


def IV_curve():
    KL = visa.ResourceManager().open_resource('GPIB0::24::INSTR')
    KL.timeout = 10000
    start = sys.argv[3]
    stop = sys.argv[4]
    step = sys.argv[5]
    stop = ((int(float(stop)/float(step)))+2)*float(step)
    lst = 'VOLT,CURR'
    KL.write('*RST')
    KL.write(':SOUR:VOLT 0')
    KL.write(':FORM:ELEM %s' % lst)
    KL.write(':SOUR:VOLT:MODE SWE')
    KL.write(':SOUR:SWE:RANG BEST')
    KL.write(':SOUR:SWE:SPAC LIN')
    trigger = (float(stop) - float(start))/(float(step))
    count = int(round(trigger))
    KL.write(':SOUR:VOLT:STAR '+start)
    KL.write(':SOUR:VOLT:STOP '+str(stop))
    KL.write(':SOUR:VOLT:STEP '+step)
    KL.write(':SENS:CURR:PROT 0.1')
    KL.write(':TRIG:COUN '+str(count))
    KL.write('OUTP ON')
    KL.write('*WAI')
    result = str(KL.query('Read?')).split(',')
    KL.write('OUTP OFF')
    voltage = []
    current = []
    for i in range(0, count):
        print 'Voltage: %.3sV,\tCurrent: %.3fmA' % (float(result[2*i]), float(result[2*i+1])*10e2)
        voltage.append(float(result[2*i]))
        current.append(float(result[2*i+1])*10e2)
        time.sleep(0.1)
    print 'It is done.'
    return voltage, current

if __name__ == "__main__":
    number = sys.argv[1]
    temp = sys.argv[2]
    address = sys.argv[6]
    os.chdir(address)
    IV_curve_result = []
    workbook = xlsxwriter.Workbook('IV_curve.xlsx')
    Summary = workbook.add_worksheet('IV_curve_'+temp+'C')
    format = workbook.add_format({'align': 'center', 'valign': 'vcenter'})
    for i in range(0, int(number)):
        IV_curve_result.append(IV_curve())
        plt.plot(IV_curve_result[i][0],IV_curve_result[i][1],linestyle = 'dashed',marker = 'o', color = 'red')
        plt.xlabel('Voltage unit = V', fontsize = 12)
        plt.ylabel('Current unit = mA', fontsize = 12)
        plt.title('IV_curve_'+temp+'C_unit_'+str(i+1), fontsize = 16)
        plt.grid()
        plt.savefig(temp+'C_unit'+str(i+1)+'_IV_curve.png')
        plt.show()
    Summary.set_column('A:Z',13)
    Summary.write('A2','Voltage(V)',format)
    length = len(IV_curve_result[0][0])
    IV_curve_chart = workbook.add_chart({'type': 'scatter','subtype': 'straight_with_markers'})
    for i in range(0,int(number)):
        Summary.write(0,i+1,temp+'C_unit'+str(i+1),format)
        Summary.write(1,i+1,'Current(mA)',format)
        for j in range(0,length):
            Summary.write(j+2,0,IV_curve_result[i][0][j],format)
            Summary.write(j+2,i+1,IV_curve_result[i][1][j],format)
        column = xl_col_to_name(i+1)
        IV_curve_chart.add_series({
            'name': '=IV_curve_'+temp+'C_unit_'+str(i+1),
            'categories': '=IV_curve_'+temp+'C'+'!$A$3:$A$'+str(length+2),
            'values': '=IV_curve_'+temp+'C'+'!$'+column+'$3:$'+column+'$'+str(length+2),
        })
    IV_curve_chart.set_title ({'name': 'IV_curve'})
    IV_curve_chart.set_x_axis({'name': 'Voltage(V)'})
    IV_curve_chart.set_y_axis({'name': 'Current(mA)'})
    IV_curve_chart.set_style(12)
    IV_curve_chart.set_size({'width': 600, 'height': 400})
    Summary.insert_chart(2, int(number)+1, IV_curve_chart, {'x_offset': 0, 'y_offset': 0})
    workbook.close()