import re
import os


def decimate(trend_path):
    period = []
    period_buffer = ""
    with open(trend_path, 'r') as data:
        dlog_data = data.read().splitlines()
    for lines in dlog_data:
        period_raw = lines
        if period_raw == period_buffer:
            continue
        else:
            period.append(period_raw)
            period_buffer = period_raw
            # print(period)

    file_edited = open("deci_trend_path.txt", "w+")
    file_edited.writelines(list("%s\n" % item for item in period))

    # print(period, file=file_edited)


def main():
    decimate("RefCurve_2017-02-02_1_161432.Wfm.csv")

if __name__ == '__main__':
    main()
