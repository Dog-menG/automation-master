import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import win32com.client as win32

class Signal_Integrity_Summary(object):

    def __init__(self, filename):
        self.filename = filename
        self.dataframe = pd.read_excel(filename, skiprows=1)
        self.dataframe.dropna(how='all', inplace=True)
        self.dataframe.fillna(value=0, inplace=True)

    def slew_rate(self, slew_rate_dataframe, mode):
        slew_rate_outliner_check = slew_rate_dataframe.apply(lambda x: x)
        # print slew_rate_dataframe.ix()
        # max_condition = (slew_rate_outliner_check['Tr Srate(V/ns)mean'] >= 4) | (slew_rate_outliner_check['Tf Srate(V/ns)mean'] >= 4)
        # max_outliner_index = slew_rate_outliner_check.loc[max_condition].index.tolist()
        # min_condition = (slew_rate_outliner_check['Tr Srate(V/ns)mean'] <= 2) | (slew_rate_outliner_check['Tf Srate(V/ns)mean'] <= 2)
        # min_outliner_index = slew_rate_outliner_check.loc[min_condition].index.tolist()
        if mode == 'normal':
            slew_rate_min = float(format(slew_rate_dataframe.apply(lambda x: x).values.min(), '.2f'))
            slew_rate_mean = float(format(slew_rate_dataframe.apply(lambda x: x).values.mean(), '.2f'))
            slew_rate_max = float(format(slew_rate_dataframe.apply(lambda x: x).values.max(), '.2f'))
            slew_rate_summary = [slew_rate_min, slew_rate_mean, slew_rate_max, 'V/ns']
            return slew_rate_summary
        elif mode == 'final':
            typical = slew_rate_dataframe[['25C' in x for x in slew_rate_dataframe.index]]
            slew_rate_min = float(format(slew_rate_dataframe.apply(lambda x: x).values.min(), '.2f'))
            slew_rate_mean = float(format(typical.apply(lambda x: x).values[0][1], '.2f'))
            slew_rate_max = float(format(slew_rate_dataframe.apply(lambda x: x).values.max(), '.2f'))
            slew_rate_summary = [slew_rate_min, slew_rate_mean, slew_rate_max, 'V/ns']
            return slew_rate_summary
        # return slew_rate_summary, max_outliner_index, min_outliner_index

    def skew(self, skew_dataframe, mode1, mode2):
        """
        It is used to calculate skew from the dataframe.
        :param skew_dataframe: Input dataframe, type: pd.DataFrame
        :param mode1: skew mode, out_to_out skew, pll_in_to_out_skew, bp_in_to_out_skew, type: str
        :param mode2: summary mode, temperature summary or final summary, type: str
        :return: Skew summary
        :rtype: list
        """
        if mode1 in 'Out' or mode1 in 'BP':
            if mode2 == 'normal':
                skew_data = skew_dataframe.groupby('CPULabel')['Skew(1-3)mean'].apply(lambda x: max([abs(x.max()), abs(x.min()), x.max() - x.min()]))
                skew_min = float(format(skew_data.min(), '.2f'))
                skew_mean = float(format(skew_data.mean(), '.2f'))
                skew_max = float(format(skew_data.max(), '.2f'))
                if mode1 == 'Out':
                    return [skew_min, skew_mean, skew_max, 'ps']
                else:
                    return [skew_min / 1000, skew_mean / 1000, skew_max / 1000, 'ns']
            elif mode2 == 'final':
                typical = skew_dataframe[['25C' in x for x in skew_dataframe.index]]
                skew_min = float(format(skew_dataframe.apply(lambda x: x).values.min(), '.2f'))
                skew_mean = float(format(typical.apply(lambda x: x).values[0][1], '.2f'))
                skew_max = float(format(skew_dataframe.apply(lambda x: x).values.max(), '.2f'))
                if mode1 == 'Out':
                    return [skew_min, skew_mean, skew_max, 'ps']
                else:
                    return [skew_min, skew_mean, skew_max, 'ns']
        else:
            if mode2 == 'normal':
                skew_data = skew_dataframe.groupby('CPULabel')['Skew(1-3)mean'].apply(lambda x: x)
                skew_min = float(format(skew_data.min(), '.2f'))
                skew_mean = float(format(skew_data.mean(), '.2f'))
                skew_max = float(format(skew_data.max(), '.2f'))
                return [skew_min, skew_mean, skew_max, 'ps']
            elif mode2 == 'final':
                typical = skew_dataframe[['25C' in x for x in skew_dataframe.index]]
                skew_min = float(format(skew_dataframe.apply(lambda x: x).values.min(), '.2f'))
                skew_mean = float(format(typical.apply(lambda x: x).values[0][1], '.2f'))
                skew_max = float(format(skew_dataframe.apply(lambda x: x).values.max(), '.2f'))
                return [skew_min, skew_mean, skew_max, 'ps']


    def duty_cycle(self, duty_cycle_dataframe):
        duty_cycle_min = float(format( duty_cycle_dataframe.apply(lambda x: x).values.min()*100, '.2f'))
        duty_cycle_mean = float(format(duty_cycle_dataframe.apply(lambda x: x).values.mean()*100, '.2f'))
        duty_cycle_max = float(format(duty_cycle_dataframe.apply(lambda x: x).values.max()*100, '.2f'))
        duty_cycle_summary = [duty_cycle_min, duty_cycle_mean, duty_cycle_max, '%']
        return duty_cycle_summary

    def duty_cycle_distortion(self, duty_cycle_distortion_dataframe, index):
        dataframe = duty_cycle_distortion_dataframe.apply(lambda x:x-x.loc[index])
        duty_cycle_distortion_min = float(format(dataframe.values.min() * 100, '.2f'))
        duty_cycle_distortion_mean = float(format(dataframe.values.mean() * 100, '.2f'))
        duty_cycle_distortion_max = float(format(dataframe.values.max() * 100, '.2f'))
        duty_cycle_distortion_summary = [duty_cycle_distortion_min, duty_cycle_distortion_mean, duty_cycle_distortion_max, '%']
        return duty_cycle_distortion_summary


def replace_with_zero(excel_file):
    index = excel_file.query('Pin in ["Dif0"]').index.tolist()
    excel_file.loc[index, ['Skew(1-3)min', 'Skew(1-3)mean', 'Skew(1-3)Max']] = 0
    return excel_file

def slew_rate(slew_rate_dataframe, mode):
    slew_rate_outliner_check = slew_rate_dataframe.apply(lambda x: x)
    # print slew_rate_dataframe.ix()
    # max_condition = (slew_rate_outliner_check['Tr Srate(V/ns)mean'] >= 4) | (slew_rate_outliner_check['Tf Srate(V/ns)mean'] >= 4)
    # max_outliner_index = slew_rate_outliner_check.loc[max_condition].index.tolist()
    # min_condition = (slew_rate_outliner_check['Tr Srate(V/ns)mean'] <= 2) | (slew_rate_outliner_check['Tf Srate(V/ns)mean'] <= 2)
    # min_outliner_index = slew_rate_outliner_check.loc[min_condition].index.tolist()
    if mode == 'normal':
        slew_rate_min = float(format(slew_rate_dataframe.apply(lambda x: x).values.min(), '.2f'))
        slew_rate_mean = float(format(slew_rate_dataframe.apply(lambda x: x).values.mean(), '.2f'))
        slew_rate_max = float(format(slew_rate_dataframe.apply(lambda x: x).values.max(), '.2f'))
        slew_rate_summary = [slew_rate_min, slew_rate_mean, slew_rate_max, 'V/ns']
        return slew_rate_summary
    elif mode == 'final':
        typical = slew_rate_dataframe[['25C' in x for x in slew_rate_dataframe.index]]
        slew_rate_min = float(format(slew_rate_dataframe.apply(lambda x: x).values.min(), '.2f'))
        slew_rate_typical = float(format(typical.apply(lambda x: x).values[0][1], '.2f'))
        slew_rate_max = float(format(slew_rate_dataframe.apply(lambda x: x).values.max(), '.2f'))
        slew_rate_summary = [slew_rate_min, slew_rate_typical, slew_rate_max, 'V/ns']
        return slew_rate_summary
    # return slew_rate_summary, max_outliner_index, min_outliner_index


def skew(skew_dataframe, mode1, mode2):
    if mode1 in 'Out' or mode1 in 'BP':
        if mode2 == 'normal':
            skew_data = skew_dataframe.groupby('CPULabel')['Skew(1-3)mean'].apply(lambda x : max([abs(x.max()),abs(x.min()),x.max()-x.min()]))
            skew_min = float(format(skew_data.min(), '.2f'))
            skew_mean = float(format(skew_data.mean(), '.2f'))
            skew_max = float(format(skew_data.max(), '.2f'))
            if mode1 == 'Out':
                return [skew_min, skew_mean, skew_max, 'ps']
            else:
                return [skew_min/1000, skew_mean/1000, skew_max/1000, 'ns']
        elif mode2 == 'final':
            typical = skew_dataframe[['25C' in x for x in skew_dataframe.index]]
            skew_min = float(format(skew_dataframe.apply(lambda x: x).values.min(), '.2f'))
            skew_mean = float(format(typical.apply(lambda x: x).values[0][1], '.2f'))
            skew_max = float(format(skew_dataframe.apply(lambda x: x).values.max(), '.2f'))
            if mode1 == 'Out':
                return [skew_min, skew_mean, skew_max, 'ps']
            else:
                return [skew_min, skew_mean, skew_max, 'ns']
    else:
        if mode2 == 'normal':
            skew_data = skew_dataframe.groupby('CPULabel')['Skew(1-3)mean'].apply(lambda x : x)
            skew_min = float(format(skew_data.min(), '.2f'))
            skew_mean = float(format(skew_data.mean(), '.2f'))
            skew_max = float(format(skew_data.max(), '.2f'))
            return [skew_min, skew_mean, skew_max, 'ps']
        elif mode2 == 'final':
            typical = skew_dataframe[['25C' in x for x in skew_dataframe.index]]
            skew_min = float(format(skew_dataframe.apply(lambda x: x).values.min(), '.2f'))
            skew_mean = float(format(typical.apply(lambda x: x).values[0][1], '.2f'))
            skew_max = float(format(skew_dataframe.apply(lambda x: x).values.max(), '.2f'))
            return [skew_min, skew_mean, skew_max, 'ps']


def duty_cycle(duty_cycle_dataframe, mode):
    if mode == 'normal':
        duty_cycle_min = float(format(duty_cycle_dataframe.apply(lambda x: x).values.min()*100, '.2f'))
        duty_cycle_mean = float(format(duty_cycle_dataframe.apply(lambda x: x).values.mean()*100, '.2f'))
        duty_cycle_max = float(format(duty_cycle_dataframe.apply(lambda x: x).values.max()*100, '.2f'))
        return [duty_cycle_min, duty_cycle_mean, duty_cycle_max, '%']
    elif mode == 'final':
        typical = duty_cycle_dataframe[['25C' in x for x in duty_cycle_dataframe.index]]
        duty_cycle_min = float(format(duty_cycle_dataframe.apply(lambda x: x).values.min(), '.2f'))
        duty_cycle_typical = float(format(typical.apply(lambda x: x).values[0][1], '.2f'))
        duty_cycle_max = float(format(duty_cycle_dataframe.apply(lambda x: x).values.max(), '.2f'))
        return [duty_cycle_min, duty_cycle_typical, duty_cycle_max, '%']


def duty_cycle_distortion(duty_cycle_distortion_dataframe, index):
    index_length = len(index)
    if index_length == 1:
        duty_cycle_distortion_dataframe = duty_cycle_distortion_dataframe.groupby('CPULabel')['DCycle']
        dataframe = duty_cycle_distortion_dataframe.apply(lambda x:x-x.loc[index[0]]).drop(index[0])
        duty_cycle_distortion_min = float(format(dataframe.values.min() * 100, '.2f'))
        duty_cycle_distortion_mean = float(format(dataframe.values.mean() * 100, '.2f'))
        duty_cycle_distortion_max = float(format(dataframe.values.max() * 100, '.2f'))
        return [duty_cycle_distortion_min, duty_cycle_distortion_mean, duty_cycle_distortion_max, '%']
    elif index_length == 2:
        clock1_dataframe_index = duty_cycle_distortion_dataframe.index.tolist()
        clock2_dataframe_index = duty_cycle_distortion_dataframe.index.tolist()
        clock1_dataframe_index.remove(index[0])
        clock2_dataframe_index.remove(index[1])
        clock1_dataframe = duty_cycle_distortion_dataframe.ix[clock1_dataframe_index]
        clock2_dataframe = duty_cycle_distortion_dataframe.ix[clock2_dataframe_index]
        clock1_dataframe = clock1_dataframe.groupby('CPULabel')['DCycle'].apply(lambda x: x - x.loc[index[1]]).drop([index[1]])
        clock2_dataframe = clock2_dataframe.groupby('CPULabel')['DCycle'].apply(lambda x: x - x.loc[index[0]]).drop([index[0]])
        duty_cycle_distortion_min1 = float(format(clock1_dataframe.values.min() * 100, '.2f'))
        duty_cycle_distortion_mean1 = float(format(clock1_dataframe.values.mean() * 100, '.2f'))
        duty_cycle_distortion_max1 = float(format(clock1_dataframe.values.max() * 100, '.2f'))
        duty_cycle_distortion_min2 = float(format(clock2_dataframe.values.min() * 100, '.2f'))
        duty_cycle_distortion_mean2 = float(format(clock2_dataframe.values.mean() * 100, '.2f'))
        duty_cycle_distortion_max2 = float(format(clock2_dataframe.values.max() * 100, '.2f'))
        duty_cycle_distortion_min = min(duty_cycle_distortion_min1, duty_cycle_distortion_min2)
        duty_cycle_distortion_mean = np.mean([duty_cycle_distortion_mean1, duty_cycle_distortion_mean2])
        duty_cycle_distortion_max = max(duty_cycle_distortion_max1, duty_cycle_distortion_max2)
        return [duty_cycle_distortion_min, duty_cycle_distortion_mean, duty_cycle_distortion_max, '%']


def final_duty_cycle_distortion(final_duty_cycle_distortion_dataframe):
    typical = final_duty_cycle_distortion_dataframe[['25C' in x for x in final_duty_cycle_distortion_dataframe.index]]
    final_duty_cycle_distortion_min = float(format(final_duty_cycle_distortion_dataframe.apply(lambda x: x).values.min(), '.2f'))
    final_duty_cycle_distortion_typical = float(format(typical.apply(lambda x: x).values[0][1], '.2f'))
    final_duty_cycle_distortion_max = float(format(final_duty_cycle_distortion_dataframe.apply(lambda x: x).values.max(), '.2f'))
    return [final_duty_cycle_distortion_min, final_duty_cycle_distortion_typical, final_duty_cycle_distortion_max, '%']


def skew_variation(skew_variation_dataframe, mode):
    if mode == 'PLL':
        variation_25C = skew_variation_dataframe.loc['25C_PLL_In_To_Out_Skew']['Mean']
        variation_85C = skew_variation_dataframe.loc['85C_PLL_In_To_Out_Skew']['Mean']
        variation_minus_40C = skew_variation_dataframe.loc['-40C_PLL_In_To_Out_Skew']['Mean']
        variation_min = variation_25C - variation_85C
        variation_mean = 0
        variation_max = variation_25C - variation_minus_40C
        return [variation_min, variation_mean, variation_max, 'ps']
    elif mode == 'BP':
        variation_25C = skew_variation_dataframe.loc['25C_BP_In_To_Out_Skew']['Mean']
        variation_85C = skew_variation_dataframe.loc['85C_BP_In_To_Out_Skew']['Mean']
        variation_minus_40C = skew_variation_dataframe.loc['-40C_BP_In_To_Out_Skew']['Mean']
        variation_min = variation_25C - variation_85C
        variation_mean = 0
        variation_max = variation_25C - variation_minus_40C
        return [variation_min * 1000, variation_mean * 1000, variation_max * 1000, 'ps']


def multiple_dfs(df_list, sheets, file_name, spaces):
    slew_rate_min = 2; slew_rate_max = 4
    out_to_out_max = 50
    in_to_out_bp_min = 1.6; in_to_out_bp_max = 3.5
    in_to_out_pll_min = -100; in_to_out_pll_max = 100
    duty_cycle_min = 45; duty_cycle_max = 55
    duty_cycle_distortion_min = -1; duty_cycle_distortion_max = 1
    writer = pd.ExcelWriter(file_name,engine='xlsxwriter')
    row = 0
    length = len(df_list)
    for i in range(0, length):
        if i != length - 1:
            df_list[i].to_excel(writer,sheet_name=sheets,startrow=row , startcol=0)
            row = row + len(df_list[i].index) + spaces + 1
        else:
            df_list[i].to_excel(writer,sheet_name=sheets,startrow=0 , startcol=6)
    # for dataframe in df_list:
    #     dataframe.to_excel(writer,sheet_name=sheets,startrow=row , startcol=0)
    #     row = row + len(dataframe.index) + spaces + 1
    workbook = writer.book
    sheet_format = workbook.add_format({'align': 'center', 'valign': 'center'})
    conditional_format = workbook.add_format({'align': 'center', 'valign': 'center', 'font_color': 'red'})
    worksheet = writer.sheets[sheets]
    worksheet.set_column('A:A', 32, sheet_format)
    worksheet.set_column('B:Z', None, sheet_format)
    worksheet.set_column('G:G', 32, sheet_format)
    # slew rate conditional format
    worksheet.conditional_format('B2:D2', {'type': 'cell', 'criteria': 'not between', 'maximum': slew_rate_max, 'minimum': slew_rate_min, 'format': conditional_format})
    worksheet.conditional_format('B10:D10', {'type': 'cell', 'criteria': 'not between', 'maximum': slew_rate_max, 'minimum': slew_rate_min, 'format': conditional_format})
    worksheet.conditional_format('B18:D18', {'type': 'cell', 'criteria': 'not between', 'maximum': slew_rate_max, 'minimum': slew_rate_min, 'format': conditional_format})
    # Out to Out skew conditional format
    worksheet.conditional_format('B3:D3', {'type': 'cell', 'criteria': '>', 'value': out_to_out_max, 'format': conditional_format})
    worksheet.conditional_format('B11:D11', {'type': 'cell', 'criteria': '>', 'value': out_to_out_max, 'format': conditional_format})
    worksheet.conditional_format('B19:D19', {'type': 'cell', 'criteria': '>', 'value': out_to_out_max, 'format': conditional_format})
    # In to out skew BP mode conditional format
    worksheet.conditional_format('B4:D4', {'type': 'cell', 'criteria': 'not between', 'maximum': in_to_out_bp_max, 'minimum': in_to_out_bp_min, 'format': conditional_format})
    worksheet.conditional_format('B12:D12', {'type': 'cell', 'criteria': 'not between', 'maximum': in_to_out_bp_max, 'minimum': in_to_out_bp_min, 'format': conditional_format})
    worksheet.conditional_format('B20:D20', {'type': 'cell', 'criteria': 'not between', 'maximum': in_to_out_bp_max, 'minimum': in_to_out_bp_min, 'format': conditional_format})
    # In to out skew PLL mode conditional format
    worksheet.conditional_format('B5:D5', {'type': 'cell', 'criteria': 'not between', 'maximum': in_to_out_pll_max, 'minimum': in_to_out_pll_min, 'format': conditional_format})
    worksheet.conditional_format('B13:D13', {'type': 'cell', 'criteria': 'not between', 'maximum': in_to_out_pll_max, 'minimum': in_to_out_pll_min, 'format': conditional_format})
    worksheet.conditional_format('B21:D21', {'type': 'cell', 'criteria': 'not between', 'maximum': in_to_out_pll_max, 'minimum': in_to_out_pll_min, 'format': conditional_format})
    # Duty_cycle conditional format
    worksheet.conditional_format('B6:D6', {'type': 'cell', 'criteria': 'not between', 'maximum': duty_cycle_max, 'minimum': duty_cycle_min, 'format': conditional_format})
    worksheet.conditional_format('B14:D14', {'type': 'cell', 'criteria': 'not between', 'maximum': duty_cycle_max, 'minimum': duty_cycle_min, 'format': conditional_format})
    worksheet.conditional_format('B22:D22', {'type': 'cell', 'criteria': 'not between', 'maximum': duty_cycle_max, 'minimum': duty_cycle_min, 'format': conditional_format})
    # In to out skew PLL mode conditional format
    worksheet.conditional_format('B7:D7', {'type': 'cell', 'criteria': 'not between', 'maximum': duty_cycle_distortion_max, 'minimum': duty_cycle_distortion_min, 'format': conditional_format})
    worksheet.conditional_format('B15:D15', {'type': 'cell', 'criteria': 'not between', 'maximum': duty_cycle_distortion_max, 'minimum': duty_cycle_distortion_min, 'format': conditional_format})
    worksheet.conditional_format('B23:D23', {'type': 'cell', 'criteria': 'not between', 'maximum': duty_cycle_distortion_max, 'minimum': duty_cycle_distortion_min, 'format': conditional_format})
    writer.save()


def xls_to_xlsx(path):
    excel = win32.gencache.EnsureDispatch('Excel.Application')
    book = excel.Workbooks.Open(r'C:\Users\dogod\Documents\test\3.465V_-40C.xls')
    book.SaveAs(r'C:\Users\dogod\Documents\test\3.465V_-40C.xlsx', FileFormat = 51)
    book.Close()
    excel.Quit()

def main():
    path = r'C:\Users\jgou\Desktop\test'
    os.chdir(path)
    files = os.listdir(path)
    summary_25C = pd.DataFrame()
    summary_85C = pd.DataFrame()
    summary_minus_40C = pd.DataFrame()
    for filename in files:
        excel = pd.read_excel(filename, skiprows=1)
        excel = replace_with_zero(excel)
        excel.fillna(value=0, inplace=True)
        excel.drop_duplicates(keep=False, inplace=True)
        duty_cycle_distortion_dataframe = excel.copy()
        general = excel[excel['Pin'].str.contains('Clkin') == False]
        general = general[general.CPULabel.str.endswith('Fast')]
        clk = excel[excel['Pin'].str.contains('Clkin')]

        # slew rate calculation
        slew_rate_dataframe = general.groupby('CPULabel')['Tr Srate(V/ns)mean', 'Tf Srate(V/ns)mean']
        slew_rate_temperature = slew_rate(slew_rate_dataframe, 'normal')
        # for index in slew_rate(slew_rate_dataframe)[1]:
        #     print excel.ix[index, ['Pin', 'CPULabel']]

        # out_to_out skew calculation
        out_to_out_skew_temperature = skew(general, 'Out', 'normal')

        if '25C' in filename[:-5]:
            summary_25C = pd.DataFrame(list(zip(slew_rate_temperature, out_to_out_skew_temperature)),
                                       columns=['25C_Slew_Rate', '25C_Out_To_Out_Skew'],
                                       index=['Min', 'Mean', 'Max', 'Unit']).transpose()
        elif '85C' in filename[:-5]:
            summary_85C = pd.DataFrame(list(zip(slew_rate_temperature, out_to_out_skew_temperature)),
                                       columns=['85C_Slew_Rate', '85C_Out_To_Out_Skew'],
                                       index=['Min', 'Mean', 'Max', 'Unit']).transpose()
        elif '-40C' in filename[:-5]:
            summary_minus_40C = pd.DataFrame(list(zip(slew_rate_temperature, out_to_out_skew_temperature)),
                                             columns=['-40C_Slew_Rate', '-40C_Out_To_Out_Skew'],
                                             index=['Min', 'Mean', 'Max', 'Unit']).transpose()
    summary = pd.concat([summary_25C, summary_85C, summary_minus_40C])
    del summary['Unit']
    # final slew rate
    final_slew_rate_dataframe = summary[['Slew_Rate' in x for x in summary.index]]
    final_slew_rate = slew_rate(final_slew_rate_dataframe, 'final')
    # final out_to_out_skew
    final_out_to_out_dataframe = summary[['Out_To_Out_Skew' in x for x in summary.index]]
    final_out_to_out_skew = skew(final_out_to_out_dataframe, 'Out', 'final')
    # final summary
    final_summary = pd.DataFrame(list(zip(final_slew_rate, final_out_to_out_skew)),
                               columns=['Slew_Rate', 'Out_To_Out_Skew'],
                               index=['Min', 'Typical', 'Max', 'Unit']).transpose()
    # list of dataframes
    dfs = [summary_25C, summary_85C, summary_minus_40C, final_summary]
    # run function
    multiple_dfs(dfs, 'test', 'test.xlsx', 1)


if __name__ == '__main__':
    main()
# xls_to_xlsx(r'C:\Users\dogod\Documents\test\3.465V_-40C.xls')
# import pandas as pd
# df0 = pd.read_csv('Dif0.csv', skiprows = 20, names = ['Frequency','100MHz_Dif0','102MHz_Dif0'])
# df1 = pd.read_csv('Dif1.csv', skiprows = 20, names = ['Frequency','100MHz_Dif1','102MHz_Dif1'])
# df = pd.merge(df0, df1, how = 'outer')
# # df = df.set_index('Frequency')
# column = df.shape[1]
# # print df.values.max(), df.values.mean(), df.values.min()
# # print df.ix[df.idxmax()]
# # print df.ix[df.idxmin()]
# # a = df[(df['Frequency'] == 99999999.9999985) | (df['Frequency'] == 101999999.999998)]
# a = df[(abs((df['Frequency'] - 1.000000e+08)) <= 0.000002) | (abs((df['Frequency'] - 1.020000e+08)) <= 0.000002)]
# # a = df.loc[99999999.9999985]
# b = df.drop((abs((df['Frequency'] - 1.000000e+08)) <= 0.000002) | (abs((df['Frequency'] - 1.020000e+08)) <= 0.000002))
# df = pd.concat([a, b])
# df = df.set_index(['Frequency'])
# print a
# print df