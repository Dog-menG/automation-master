import pandas as pd
import numpy as np
import os


def append_index(list_name, index):
    for i in range(0, 9):
        list_name.append(index+i)


def process_with_resistor_dataframe(pins_with_resistors, dataframe):
    with_resistor_df = pd.DataFrame()
    for i in range(len(pins_with_resistors)):
        ii_with_resistor = dataframe[dataframe['Pin'].eq(pins_with_resistors[i])]
        with_resistor_df = pd.concat([with_resistor_df, ii_with_resistor])
    return with_resistor_df


def process_without_resistor_dataframe(pins_with_resistors, dataframe):
    for i in range(len(pins_with_resistors)):
        dataframe = dataframe[~dataframe['Pin'].eq(pins_with_resistors[i])]
    return dataframe


def input_leakage(input_leakage_dataframe, status):
    single_ended_ua = input_leakage_dataframe[input_leakage_dataframe['Measured_Unit'] == 'uA']
    single_ended_na = input_leakage_dataframe[input_leakage_dataframe['Measured_Unit'] == 'nA']
    single_ended_pa = input_leakage_dataframe[input_leakage_dataframe['Measured_Unit'] == 'pA']
    if status.lower() == 'high':
        ua_max = single_ended_ua['Measured'].astype('float').max()
        na_max = single_ended_na['Measured'].astype('float').max()
        pa_max = single_ended_pa['Measured'].astype('float').max()
        return np.nanmax([ua_max, na_max/1e3, pa_max/1e6])
    else:
        ua_min = single_ended_ua['Measured'].astype('float').min()
        na_min = single_ended_na['Measured'].astype('float').min()
        pa_min = single_ended_pa['Measured'].astype('float').min()
        return np.nanmin([ua_min, na_min/1e3, pa_min/1e6])


def main(path, name):
    os.chdir(path)
    result = open(name, 'r')
    leakage = []
    for line in result:
        if 'IIL' in line or 'IIH' in line or 'Input_Leakage' in line:
            leakage.append(line.split())
        else:
            continue
    headers = ['Number', 'Site', 'Result', 'Test Name', 'Pin', 'Channel', 'Low', 'Low_Unit',
               'Measured', 'Measured_Unit', 'High', 'High_Unit', 'Force', 'Force_Unit', 'Loc']
    Leakage = pd.DataFrame(leakage, columns=headers)
    measured = Leakage['Measured'].tolist()
    length = len(measured)
    sclk_sda_removed_index = []
    for i in range(0, length-1):
        if '5.56V' == measured[i]:
            append_index(sclk_sda_removed_index, i)
        else:
            continue
    Leakage.drop(sclk_sda_removed_index, inplace=True)
    Leakage['new'] = Leakage['Result'].mask(Leakage['Result'].eq('PASS')).ffill()
    dfs = {keys:values.drop('new', axis=1) for keys, values in Leakage.groupby('new')}
    IIH = dfs['HIGH(IIH)']
    IIL = dfs['LOW(IIL)']
    columns_to_be_removed = ['Number', 'Site', 'Result', 'Channel', 'Low', 'Low_Unit',
                             'High', 'High_Unit', 'Force', 'Force_Unit', 'Loc']
    IIH.drop(IIH.index[0], inplace=True)
    IIL.drop(IIL.index[0], inplace=True)
    IIH.drop(columns_to_be_removed, axis=1, inplace=True)
    IIL.drop(columns_to_be_removed, axis=1, inplace=True)

    # Those below need to be customized
    IIH_with_resistors = ['SMB_A0_TRI', 'SMB_A1_TRI']
    IIL_with_resistors = ['SMB_A0_TRI', 'SMB_A1_TRI', 'PWRGD_PD']

    # select input leakage without pull-up or pull-down resistors
    IIH_without_resistors = process_without_resistor_dataframe(IIH_with_resistors, IIH)
    IIL_without_resistors = process_without_resistor_dataframe(IIL_with_resistors, IIL)

    # select input leakage with pull-up or pull-down resistors
    IIH_with_pull_up_pull_down_resistors = process_with_resistor_dataframe(IIH_with_resistors, IIH)
    IIL_with_pull_up_pull_down_resistors = process_with_resistor_dataframe(IIL_with_resistors, IIL)

    # Calculate the maximum input leakage
    IIH_without_resistors_leakage = input_leakage(IIH_without_resistors, 'high')
    IIL_without_resistors_leakage = input_leakage(IIL_without_resistors, 'low')
    IIH_with_pull_up_pull_down_resistors_leakage = input_leakage(IIH_with_pull_up_pull_down_resistors, 'high')
    IIL_with_pull_up_pull_down_resistors_leakage = input_leakage(IIL_with_pull_up_pull_down_resistors, 'low')

    print IIH_without_resistors_leakage, IIL_without_resistors_leakage
    print IIH_with_pull_up_pull_down_resistors_leakage, IIL_with_pull_up_pull_down_resistors_leakage


if __name__ == '__main__':
    file_path = r'\\corpgroup\ftginfo\9QXLxxxx\9QXL2000ANLGI(AP711T-033)\ATE_datalog'
    file_name = 'data_log.txt'
    main(file_path, file_name)