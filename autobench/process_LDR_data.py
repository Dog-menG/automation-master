from autobench import log
from xlsxwriter.utility import xl_rowcol_to_cell
import os
import re
import time
import xlsxwriter
import pandas as pd


class combine_csv(object):

    def __init__(self):
        """
        This function is used to initialize the instance.
        """
        self.log = log(self.__class__.__name__)
        self.csv_files = []
        self.slew_rate_file = []

    def timestamp(self, s):
        now = time.clock()
        self.log.info('time:' + '%5.2f' % now + s)

    def list_csv(self, path, suffix=".csv"):
        file_names = os.listdir(path)
        txt = re.compile('txt')
        slew_rate = re.compile('slew_rate')
        for file_name in file_names:
            if file_name.endswith(suffix) and re.search(txt, file_name):
                self.csv_files.append(file_name)
            elif re.search(slew_rate, file_name):
                self.slew_rate_file = file_name
            else:
                pass
        return self.csv_files, self.slew_rate_file

    def combine_csv(self, csv_list, path):
        os.chdir(path)
        temp = path.split('\\')[-1]
        excel_name = ''.join((temp, '_LDR.xlsx'))
        workbook = xlsxwriter.Workbook(excel_name)
        summary = workbook.add_worksheet('LDR_data')
        data_format = workbook.add_format({'valign': 'vcenter'})
        number = len(csv_list)
        summary.write('A1', 'LDR_data')
        self.timestamp(" time begins")
        for i in range(0, number):
            ldr_data = open(csv_list[i], 'r')
            data = ldr_data.readline().split(',')
            summary.write('A2', data[0])
            summary.write(1, i+1, data[1])
            for row in range(0, 57):
                float_data = ldr_data.readline().split(',')
                summary.write(row+2, 0, float_data[0], data_format)
                summary.write(row+2, i+1, float(float_data[1]), data_format)
        self.timestamp(" time ends")
        workbook.close()


class merge_files(object):
    def __init__(self, path):
        """
        This function is used to initialize the instance.
        """
        self.log = log(self.__class__.__name__)
        self.path = path
        self.voltage_temp = path.split('\\')[-1]

    def add_formula_to_excel(self, worksheet, row_number, col_number, header, header_format, sheet_format):
        header_col = 0
        new_col = 0
        if 'PCIe Gen 2 WORST RMS loBand (ps) Spec = 3 ps' in header:
            header_col = 3
            new_col = col_number + 1
        elif 'PCIe Gen 2 WORST RMS hiBand (ps) Spec = 3.1 ps' in header:
            header_col = 4
            new_col = col_number + 2
        elif 'Gen2 SRIS : RMS   (ps) Spec = 3 ps' in header:
            header_col = 5
            new_col = col_number + 3
        elif 'PCIe Gen 3 WORST RMS(ps) Spec = 1 ps' in header:
            header_col = 6
            new_col = col_number + 4
        elif 'Gen3 SRIS : RMS   (Int) Spec = 0.7 ps' in header:
            header_col = 7
            new_col = col_number + 5
        worksheet.write(0, new_col, header, header_format)
        for i in range(0, row_number):
            cell_location = xl_rowcol_to_cell(i+1, new_col)
            output_range = xl_rowcol_to_cell(i+1, header_col)
            input_range = xl_rowcol_to_cell(row_number, header_col)
            slew_rate_wenzel = xl_rowcol_to_cell(row_number, 8)
            slew_rate_output = xl_rowcol_to_cell(i+1, 8)
            formula = "=IF((%s)^2>=((%s/%s)*%s)^2, SQRT((%s)^2-((%s/%s)*%s)^2),0)" % (output_range, slew_rate_wenzel,
                                                                                      slew_rate_output, input_range,
                                                                                      output_range, slew_rate_wenzel,
                                                                                      slew_rate_output, input_range)
            worksheet.write_formula(cell_location, formula, sheet_format)

    def merged_ldr_slew_rate_to_dataframe(self):
        os.chdir(self.path)
        LDR = pd.read_excel(self.voltage_temp + '_LDR.xlsx', skiprows=1)
        LDR = LDR.transpose()
        columns = ['Cycle-to-Cycle Jitter  (ps)', 'Gen1 E.C. : pk-pk (ps) Spec = 86 ps',
                   'PCIe Gen 2 WORST RMS loBand (ps) Spec = 3 ps', 'PCIe Gen 2 WORST RMS hiBand (ps) Spec = 3.1 ps',
                   'Gen2 SRIS : RMS   (ps) Spec = 3 ps', 'PCIe Gen 3 WORST RMS(ps) Spec = 1 ps',
                   'Gen3 SRIS : RMS   (Int) Spec = 0.7 ps']
        LDR = LDR.rename(columns=LDR.iloc[0])
        LDR = LDR.drop(LDR.index[0])
        LDR = LDR[columns]
        LDR_index = LDR.index.tolist()
        slew_rate_file = ''
        slew_rate = re.compile('slew_rate')
        files_names = os.listdir(self.path)
        for file_name in files_names:
            if re.search(slew_rate, file_name):
                slew_rate_file = file_name
            else:
                pass
        slew_rate_df = pd.read_csv(slew_rate_file, header=None)
        slew_rate_df.drop_duplicates(inplace=True)
        slew_rate_df = slew_rate_df.rename(columns=slew_rate_df.iloc[0])
        slew_rate_df = slew_rate_df.drop(slew_rate_df.index[0])
        slew_rate_df = slew_rate_df.set_index('part')
        slew_rate_df_index = slew_rate_df.index.tolist()
        sorted_slew_rate_df_index = []
        while len(slew_rate_df_index):
            for i in range(len(LDR_index)):
                if slew_rate_df_index[0] in LDR_index[i]:
                    sorted_slew_rate_df_index.append(slew_rate_df_index[0])
                    del slew_rate_df_index[0]
                else:
                    pass
        sorted_slew_rate_df = slew_rate_df.reindex(index=sorted_slew_rate_df_index)
        mean_slew_rate = sorted_slew_rate_df['Mean V/ns'].tolist()
        mean_slew_rate = [float(i) for i in mean_slew_rate]
        LDR['Mean V/ns'] = mean_slew_rate
        return LDR

    def merged_dataframe_to_excel(self, dataframe):
        writer = pd.ExcelWriter(self.voltage_temp + '_LDR.xlsx')
        dataframe.to_excel(writer, self.voltage_temp + '_LDR')
        workbook = writer.book
        # Add a header format.
        header_format = workbook.add_format({'bold': True, 'text_wrap': True, 'align': 'center', 'valign': 'vcenter'})
        index_format = workbook.add_format({'bold': True, 'text_wrap': True, 'align': 'center', 'valign': 'vcenter'})
        sheet_format = workbook.add_format({'align': 'center', 'valign': 'vcenter', 'text_wrap': True, 'num_format': '0.000'})
        worksheet = writer.sheets[self.voltage_temp + '_LDR']
        # worksheet.set_row(0, 30)
        worksheet.set_column('A:A', 40, sheet_format)
        worksheet.set_column('B:I', 7, sheet_format)
        for col_num, value in enumerate(dataframe.columns.values):
            worksheet.write(0, col_num + 1, value, header_format)
        for row_num, value in enumerate(dataframe.index.values):
            worksheet.write(row_num + 1, 0, value, index_format)
        # Get the range to use for the sum formula
        cols = len(dataframe.columns.values)
        rows = len(dataframe.index.values)
        # PCIE_GEN2 LoBW
        self.add_formula_to_excel(worksheet, rows, cols, 'PCIe Gen 2 WORST RMS loBand (ps) Spec = 3 ps calibrated',
                                  header_format, sheet_format)
        # PCIE_GEN2 High
        self.add_formula_to_excel(worksheet, rows, cols, 'PCIe Gen 2 WORST RMS hiBand (ps) Spec = 3.1 ps calibrated',
                                  header_format, sheet_format)
        # PCIE GEN2 SRIS
        self.add_formula_to_excel(worksheet, rows, cols, 'Gen2 SRIS : RMS   (ps) Spec = 3 ps calibrated',
                                  header_format, sheet_format)
        # PCIE GEN3
        self.add_formula_to_excel(worksheet, rows, cols, 'PCIe Gen 3 WORST RMS(ps) Spec = 1 ps calibrated',
                                  header_format, sheet_format)
        # PCIE GEN3 SRIS
        self.add_formula_to_excel(worksheet, rows, cols, 'Gen3 SRIS : RMS   (Int) Spec = 0.7 ps calibrated',
                                  header_format, sheet_format)
        writer.save()


def main(file_path):
    # combine csv files
    combine_csv_files = combine_csv()
    csv_files, slew_rate_file = combine_csv_files.list_csv(file_path)
    combine_csv_files.combine_csv(csv_files, file_path)
    time.sleep(1)
    # merge slew rate and LDR files
    merge_ldr_slew_rate_files = merge_files(file_path)
    merged_dataframe = merge_ldr_slew_rate_files.merged_ldr_slew_rate_to_dataframe()
    merge_ldr_slew_rate_files.merged_dataframe_to_excel(merged_dataframe)


if __name__ == "__main__":
        path = r'C:\Users\jgou\Desktop\test'
        # check 3.3V_25C directory exists or not
        path_3p3V_25C = ''.join((path, r'\3.3V_25C'))
        if os.path.exists(path_3p3V_25C):
            main(path_3p3V_25C)
        else:
            print ('Path: %s does not exist!' % path_3p3V_25C)
        exist_3p3V_25C_flag = 1
        # check 2.97V_85C directory exists or not
        path_2p97V_85C = ''.join((path, r'\2.97V_85C'))
        if os.path.exists(path_2p97V_85C):
            main(path_2p97V_85C)
        else:
            print ('Path: %s does not exist!' % path_2p97V_85C)
        exist_2p97V_85C_flag = 1
        # check 3.135V_85C directory exists or not
        path_3p135V_85C = ''.join((path, r'\3.135V_85C'))
        if os.path.exists(path_3p135V_85C):
            main(path_3p135V_85C)
        else:
            print ('Path: %s does not exist!' % path_3p135V_85C)
        exist_3p135V_85C_flag = 1
        # check 3.465V_-40C directory exists or not
        path_3p465V_minus40C = ''.join((path, r'\3.465V_-40C'))
        if os.path.exists(path_3p465V_minus40C):
            main(path_3p465V_minus40C)
        else:
            print ('Path: %s does not exist!' % path_3p465V_minus40C)
        exist_3p465V_minus40C_flag = 1
        # check 3.63V_-40C directory exists or not
        path_3p63V_minus40C = ''.join((path, r'\3.63V_-40C'))
        if os.path.exists(path_3p63V_minus40C):
            main(path_3p63V_minus40C)
        else:
            print ('Path: %s does not exist!' % path_3p63V_minus40C)
        exist_3p63V_minus40C_flag = 1
