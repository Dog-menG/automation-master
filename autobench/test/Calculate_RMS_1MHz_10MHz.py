import csv
import math
import os
import xlsxwriter

path = r'\\Corpgroup\FTGInfo\9FGLxxx\9FGL0xxx_AP635T\9FGL08x1\AP635T-063_Released\PN\1'
os.chdir(path)
file_names = os.listdir(path)
csv_file = []
Total_jitter = []
for file_name in file_names:
    if file_name.endswith('csv'):
        csv_file.append(file_name)
    else:
        pass
file_number = len(csv_file)
for num in range(0,file_number):
    file = csv.reader(open(csv_file[num],'rb'))
    rows = [row for row in file]
    result = []
    result.append(csv_file[num])
    for float_row in range(1, 724):
        for n in range(0, 2):
            rows[float_row][n] = float(rows[float_row][n])
    integral = 0
    for number in range(517, 645):
        Noise0 = math.pow(10, rows[number][1]/10) * 2
        Noise1 = math.pow(10, rows[number+1][1]/10) * 2
        Power = (rows[number][1]-rows[number+1][1])/(10*(math.log10(rows[number+1][0])-math.log10(rows[number][0])))
        integral += (rows[number][0]*Noise0 - rows[number+1][0]*Noise1)/(Power - 1)
    RMS = math.sqrt((integral))/(2*math.pi*1e+8)
    result.append(RMS * 1e+15)
    Total_jitter.append(result)

workbook = xlsxwriter.Workbook('PN_1MHz_to_10MHz.xlsx')
Summary = workbook.add_worksheet('PN_1MHz_to_10MHz')
format = workbook.add_format({'valign': 'vcenter','align': 'center'})
Summary.set_column('A:A', 84)
Summary.write('A1', 'File_name', format)
Summary.write('B1', 'Unit(fs)', format)
for i in range(0, len(Total_jitter)):
    Summary.write(i+1,0,Total_jitter[i][0],format)
    Summary.write(i+1,1,Total_jitter[i][1],format)
workbook.close()
