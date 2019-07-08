# import os
# import time
# # # import numpy as np
# # #
# # # print np.random.randn(1,10)
# # # import re
# # #
# # # a = r'"S:\9ZMLxxxx\25C_3.3_123.csv"'
# # #
# # # b = '"S:\\9ZMLxxxx\\25C_3.3_123.csv"'
# # #
# # # c = r"S:\9ZMLxxxx\25C_3.3_123.csv"
# # #
# # # d = r'"%s"' % c
# # #
# # # print a
# # # print b
# # # print c
# # # print d
# # #
# # # if b == d:
# # #     print 1
# # # else:
# # #     print 2
# # # a = 1
# # # b = 2
# # # c = 3
# # # d = [a, b, c]
# # # print d
# #
# # # a = [32, 0, 196, 64, 32, 0]
# # # b = []
# # # for i in range(0, 6):
# # #     b.append(hex(a[i])+' ')
# # #     print type(hex(a[i]))
# # # print type(b)
# # # print ''.join(b)
# #
# # # a = ['0x00'] * 40
# # # row1 = ''
# # # row2 = ''
# # # row3 = ''
# # # row4 = ''
# # # for i in range(0,10):
# # #     row1 += str(a[i]) + ' '
# # #     row2 += str(a[10+i]) + ' '
# # #     row3 += str(a[20+i]) + ' '
# # #     row4 += str(a[30+i]) + ' '
# # # print row1
# # # print row2
# # # print row3
# # # print row4
# # #
# # # b = """%s
# # # %s
# # # %s
# # # %s
# # #     """ % (row1, row2, row3, row4)
# # #
# # # print b
# #
# # # summary = open("test.csv", "ab")
# # # # writer = csv.writer(summary, delimiter="")
# # # # writer.writerow('The delay to corresponding code')
# # # summary.writelines('The delay to corresponding code\n')
# # # summary.writelines('The delay to corresponding code')
# #
# # #!/usr/bin/python -d
# #
# # # ! /usr/bin/env python
# # # -*- coding: utf-8 -*-
# # # import sys
# # # import os
# # # from PyQt4 import QtGui
# # #
# # # class Window(QtGui.QMainWindow):
# # #
# # #     def __init__(self):
# # #         super(Window, self).__init__()
# # #         os.chdir('E:\\')
# # #         self.setGeometry(50, 50, 500, 300)
# # #         self.setWindowTitle("PyQT tuts!")
# # #         self.setWindowIcon(QtGui.QIcon('spring_breakers_png_by_flawlessduck-d5xdmmp.png'))
# # #         self.show()
# # #
# # # app = QtGui.QApplication(sys.argv)
# # # GUI = Window()
# # # sys.exit(app.exec_())
# # #
# # # from threading import Thread, current_thread
# # #
# # # import threading
# # # a = 10
# # # b = 20
# # # print a+b
# # # print threading.current_thread().name
# # #
# # # c = 40
# # # d = 50
# # # print c+d
# # # print threading.current_thread().name
# # #
# # #
# # # import os
# # # print os.getpid()
# # #
# # # from PyQt4.QtGui import *
# # # from PyQt4.QtCore import *
# # # from PyQt4 import QtGui, QtCore
# # # import sys
# # #
# # #
# # # def main():
# # #     app = QApplication(sys.argv)
# # #     gui = QWidget()
# # #     table = QTableWidget(gui)
# # #     tableItem = QTableWidgetItem()
# # #
# # #     # initiate table
# # #     table.setWindowTitle("QTableWidget Example @pythonspot.com")
# # #     table.resize(400, 250)
# # #     gui.setGeometry(400,400,400,400)
# # #     table.setRowCount(4)
# # #     table.setColumnCount(2)
# # #     # rowPosition = table.rowCount()
# # #     # table.insertRow(rowPosition)    table.setHorizontalHeaderLabels(['a','b'])
# # #     a = 'dgfgfd'
# # #     # set data
# # #     table.setItem(0, 0, QTableWidgetItem("row"))
# # #     table.setItem(0, 1, QTableWidgetItem(a))
# # #     table.setItem(1, 0, QTableWidgetItem("Item (2,1)"))
# # #     table.setItem(1, 1, QTableWidgetItem("Item (2,2)"))
# # #     table.setItem(2, 0, QTableWidgetItem("Item (3,1)"))
# # #     table.setItem(2, 1, QTableWidgetItem("Item (3,2)"))
# # #     table.setItem(3, 0, QTableWidgetItem("Item (4,1)"))
# # #     table.setItem(3, 1, QTableWidgetItem("Item (4,2)"))
# # #
# # #     # show table
# # #     gui.show()
# # #     return app.exec_()
# # #
# # #
# # # if __name__ == '__main__':
# # #     main()
# # import sys
# # from PyQt4.QtCore import *
# # from PyQt4.QtGui import *
# #
# #
# # def window():
# #     app = QApplication(sys.argv)
# #     win = QWidget()
# #
# #     l1 = QLabel("Name")
# #     nm = QLineEdit()
# #
# #     l2 = QLabel("Address")
# #     add1 = QLineEdit()
# #     add2 = QLineEdit()
# #     fbox = QFormLayout()
# #     fbox.addRow(l1, nm)
# #     vbox = QVBoxLayout()
# #
# #     vbox.addWidget(add1)
# #     vbox.addWidget(add2)
# #     fbox.addRow(l2, vbox)
# #     hbox = QHBoxLayout()
# #
# #     r1 = QRadioButton("Male")
# #     r2 = QRadioButton("Female")
# #     hbox.addWidget(r1)
# #     hbox.addWidget(r2)
# #     hbox.addStretch()
# #     fbox.addRow(QLabel("sex"), hbox)
# #     fbox.addRow(QPushButton("Submit"), QPushButton("Cancel"))
# #     win.setLayout(fbox)
# #
# #     win.setWindowTitle("PyQt")
# #     win.show()
# #     sys.exit(app.exec_())
# #
# #
# # if __name__ == '__main__':
# #     window()
# #
# # from math import pi, sin
# # import struct, sys
# # from PyQt4.QtCore import QBuffer, QByteArray, QIODevice, Qt
# # from PyQt4.QtGui import QApplication, QFormLayout, QLineEdit, QHBoxLayout, QPushButton, QSlider, QVBoxLayout, QWidget
# # from PyQt4.QtMultimedia import QAudio, QAudioDeviceInfo, QAudioFormat, QAudioOutput
# #
# #
# # class Window(QWidget):
# #
# #     def __init__(self, parent=None):
# #
# #         QWidget.__init__(self, parent)
# #
# #         format = QAudioFormat()
# #         format.setChannels(1)
# #         format.setFrequency(22050)
# #         format.setSampleSize(16)
# #         format.setCodec("audio/pcm")
# #         format.setByteOrder(QAudioFormat.LittleEndian)
# #         format.setSampleType(QAudioFormat.SignedInt)
# #         self.output = QAudioOutput(format, self)
# #         self.frequency = 440
# #         self.volume = 0
# #         self.buffer = QBuffer()
# #         self.data = QByteArray()
# #         self.deviceLineEdit = QLineEdit()
# #         self.deviceLineEdit.setReadOnly(True)
# #         self.deviceLineEdit.setText(QAudioDeviceInfo.defaultOutputDevice().deviceName())
# #         self.pitchSlider = QSlider(Qt.Horizontal)
# #         self.pitchSlider.setMaximum(100)
# #         self.volumeSlider = QSlider(Qt.Horizontal)
# #         self.volumeSlider.setMaximum(32767)
# #         self.volumeSlider.setPageStep(1024)
# #         self.playButton = QPushButton(self.tr("&Play"))
# #         self.pitchSlider.valueChanged.connect(self.changeFrequency)
# #         self.volumeSlider.valueChanged.connect(self.changeVolume)
# #         self.playButton.clicked.connect(self.play)
# #         formLayout = QFormLayout()
# #         formLayout.addRow(self.tr("Device:"), self.deviceLineEdit)
# #         formLayout.addRow(self.tr("P&itch:"), self.pitchSlider)
# #         formLayout.addRow(self.tr("&Volume:"), self.volumeSlider)
# #         buttonLayout = QVBoxLayout()
# #         buttonLayout.addWidget(self.playButton)
# #         buttonLayout.addStretch()
# #         horizontalLayout = QHBoxLayout(self)
# #         horizontalLayout.addLayout(formLayout)
# #         horizontalLayout.addLayout(buttonLayout)
# #
# #     def changeFrequency(self, value):
# #         self.frequency = 440 + (value * 2)
# #
# #     def play(self):
# #         if self.output.state() == QAudio.ActiveState:
# #             self.output.stop()
# #         if self.buffer.isOpen():
# #             self.buffer.close()
# #         self.createData()
# #         self.buffer.setData(self.data)
# #         self.buffer.open(QIODevice.ReadOnly)
# #         self.buffer.seek(0)
# #         self.output.start(self.buffer)
# #     def changeVolume(self, value):
# #         self.volume = value
# #
# #     def createData(self):
# #         self.data.clear()
# #         for i in xrange(2 * 22050):
# #             t = i / 22050.0
# #             value = int(self.volume * sin(2 * pi * self.frequency * t))
# #             self.data.append(struct.pack("<h", value))
# #
# #
# # if __name__ == "__main__":
# #     app = QApplication(sys.argv)
# #     window = Window()
# #     window.show()
# #     sys.exit(app.exec_())
#
# # !/usr/bin/env python
#
#
# #############################################################################
# ##
# ## Copyright (C) 2010 Hans-Peter Jansen <hpj@urpla.net>.
# ## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
# ## All rights reserved.
# ##
# ## This file is part of the examples of PyQt.
# ##
# ## $QT_BEGIN_LICENSE:BSD$
# ## You may use this file under the terms of the BSD license as follows:
# ##
# ## "Redistribution and use in source and binary forms, with or without
# ## modification, are permitted provided that the following conditions are
# ## met:
# ##   * Redistributions of source code must retain the above copyright
# ##     notice, this list of conditions and the following disclaimer.
# ##   * Redistributions in binary form must reproduce the above copyright
# ##     notice, this list of conditions and the following disclaimer in
# ##     the documentation and/or other materials provided with the
# ##     distribution.
# ##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
# ##     the names of its contributors may be used to endorse or promote
# ##     products derived from this software without specific prior written
# ##     permission.
# ##
# ## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# ## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# ## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# ## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# ## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# ## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# ## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# ## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# ## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# ## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# ## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
# ## $QT_END_LICENSE$
# ##
# #############################################################################
#
#
# # This is only needed for Python v2 but is harmless for Python v3.
# # -*- coding: utf-8 -*-
#
# # Form implementation generated from reading ui file 'form.ui'
# #
# # Created: Wed Dec 16 18:18:01 2009
# #      by: PyQt4 UI code generator 4.7-snapshot-20091216
# #
# # WARNING! All changes made in this file will be lost!
#
# from numpy import pi, zeros, ones, array, mean, sqrt, log, exp, cos, cumsum, convolve, arange, cov, transpose, shape, hanning, argsort, std , concatenate
# import pandas as pd
#
#
# def makegrids(fre):
#     return 2 * pi * 1j * fre
#
#
# def main():
#     pn = pd.read_csv('25C_3.3V_Wenzel_tran(6.0V)_9ZML1252F_AP711T_HiBW_12k_20M_Unit5_222.690f.csv')
#     row_conut = len(pn.index)
#     gen1_filter = []
#     gen2_LoBW_filter = []
#     gen2_HiBW_filter = []
#     gen3_2M_4M_filter = []
#     gen3_2M_5M_filter = []
#     gen4_2M_4M_filter = []
#     gen4_2M_5M_filter = []
#     gen2_sris_filter = []
#     gen3_sris_filter = []
#
#     # Gen1 Spread off setting
#     f3db1_gen1 = 22e6; zeta1_gen1 = 0.54; f3db2_gen1 = 1.5e6; zeta2_gen1 = 0.54; f3db3_gen1 = 1.5e6
#     fx1_gen1 = 200e6; fx2_gen1 = 200e6; delay1_gen1 = 0e-9; delay2_gen1 = 10e-9
#     sscgRemoveFlag_gen1 = False; responseType_gen1 = 'COMMONCLOCKED'
#
#     # Gen2 LoBW& HiBW Spread off setting
#     f3db1_gen2 = 16e6; zeta1_gen2 = 0.54; f3db2_gen2 = 5e6; zeta2_gen2 = 1.16; f3db3_gen2 = 1.0e6
#     fx1_gen2 = 2000e6; fx2_gen2 = 2000e6; delay1_gen2 = 0e-9; delay2_gen2 = 12e-9
#     sscgRemoveFlag_gen2 = True; responseType_gen2 = 'COMMONCLOCKED'
#
#     # Gen3,4_2M_4M Spread off setting
#     f3db1_gen3_2M_4M = 2.000e6; zeta1_gen3_2M_4M = 0.73; f3db2_gen3_2M_4M = 4.00e6; zeta2_gen3_2M_4M = 0.73
#     f3db3_gen3_2M_4M = 1.0e7; fx1_gen3_2M_4M = 2.0e15; fx2_gen3_2M_4M = 2.e15; delay1_gen3_2M_4M = 1.2e-8
#     delay2_gen3_2M_4M = 0e-8; sscgRemoveFlag_gen3_2M_4M = True; responseType_gen3_2M_4M = 'COMMONCLOCKED'
#
#     # Gen3,4_2M_5M Spread off setting
#     f3db1_gen3_2M_5M = 2.000e6; zeta1_gen3_2M_5M = 1.16; f3db2_gen3_2M_5M = 5.00e6; zeta2_gen3_2M_5M = 1.16
#     f3db3_gen3_2M_5M = 1.0e7; fx1_gen3_2M_5M = 2.0e15; fx2_gen3_2M_5M = 2.e15; delay1_gen3_2M_5M = 1.2e-8
#     delay2_gen3_2M_5M = 0e-8; sscgRemoveFlag_gen3_2M_5M = True; responseType_gen3_2M_5M = 'COMMONCLOCKED'
#
#     # Gen2_SRIS setting
#     f3db1_gen2_sris = 16e6; zeta1_gen2_sris = 0.54; f3db2_gen2_sris = 0; zeta2_gen2_sris = 0; f3db3_gen2_sris = 4.8586e6
#     fx1_gen2_sris = 2.0e11; fx2_gen2_sris = 2.0e11; delay1_gen2_sris = 0e-8; delay2_gen2_sris = 1.2e-8
#     sscgRemoveFlag_gen2_sris = False; responseType_gen2_sris = 'SRIS_GEN2'
#
#     # Gen3_SRIS setting
#     f3db1_gen3_sris = 4e6; zeta1_gen3_sris = 0.73; f3db2_gen3_sris = 0; zeta2_gen3_sris = 0; f3db3_gen3_sris = 1.0e7
#     fx1_gen3_sris = 2.0e11; fx2_gen3_sris = 2.0e11; delay1_gen3_sris = 0e-8; delay2_gen3_sris = 1.2e-8
#     sscgRemoveFlag_gen3_sris = False; responseType_gen3_sris = 'SRIS_GEN3'
#
#     # Gen1 calculation
#     for i in range(0, row_conut):
#         PCIe_1 = EC_analysis('Gen1 E.C.', f3db1_gen1, zeta1_gen1, f3db2_gen1, zeta2_gen1, f3db3_gen1, fx1_gen1, fx2_gen1,
#                              delay1_gen1, delay2_gen1, sscgRemoveFlag_gen1, responseType_gen1,
#                              pn['Offset Frequency (Hz)'][i])
#         PCIe1_real = PCIe_1.calcFilterResponse().real
#         PCIe1_imag = PCIe_1.calcFilterResponse().imag
#         gen1_filter.append(20 * log(sqrt(PCIe1_real * PCIe1_real + PCIe1_imag * PCIe1_imag)))
#
#     # Gen2_LoBW_HiBW calculation
#         PCIe_2 = EC_analysis('Gen2', f3db1_gen2, zeta1_gen2, f3db2_gen2, zeta2_gen2, f3db3_gen2, fx1_gen2, fx2_gen2,
#                              delay1_gen2, delay2_gen2, sscgRemoveFlag_gen2, responseType_gen2,
#                              pn['Offset Frequency (Hz)'][i])
#         PCIe2_real = PCIe_2.calcFilterResponse().real
#         PCIe2_imag = PCIe_2.calcFilterResponse().imag
#         gen2_LoBW_filter.append(20 * log(sqrt(PCIe2_real*PCIe2_real+ PCIe2_imag * PCIe2_imag)))
#         gen2_HiBW_filter.append(20 * log(sqrt(PCIe2_real * PCIe2_real + PCIe2_imag * PCIe2_imag)))
#
#     # Gen3_Gen4_2M_4M calculation
#     for i in range(0, row_conut):
#         PCIe_3_4_2M_4M = EC_analysis('Gen3_Gen4_2M_4M', f3db1_gen3_2M_4M, zeta1_gen3_2M_4M, f3db2_gen3_2M_4M,
#                                      zeta2_gen3_2M_4M, f3db3_gen3_2M_4M, fx1_gen3_2M_4M, fx2_gen3_2M_4M,
#                                      delay1_gen3_2M_4M, delay2_gen3_2M_4M, sscgRemoveFlag_gen3_2M_4M,
#                                      responseType_gen3_2M_4M, pn['Offset Frequency (Hz)'][i])
#         PCIe2_3_4_2M_4M_real = PCIe_3_4_2M_4M.calcFilterResponse().real
#         PCIe2_3_4_2M_4M_imag = PCIe_3_4_2M_4M.calcFilterResponse().imag
#         gen3_2M_4M_filter.append(20 * log(sqrt(PCIe2_3_4_2M_4M_real * PCIe2_3_4_2M_4M_real + PCIe2_3_4_2M_4M_imag * PCIe2_3_4_2M_4M_imag)))
#         gen4_2M_4M_filter.append(20 * log(sqrt(PCIe2_3_4_2M_4M_real * PCIe2_3_4_2M_4M_real + PCIe2_3_4_2M_4M_imag * PCIe2_3_4_2M_4M_imag)))
#
#     # Gen3_Gen4_2M_5M calculation
#     for i in range(0, row_conut):
#         PCIe_3_4_2M_5M = EC_analysis('Gen3_Gen4_2M_5M', f3db1_gen3_2M_5M, zeta1_gen3_2M_5M, f3db2_gen3_2M_5M,
#                                      zeta2_gen3_2M_5M, f3db3_gen3_2M_5M, fx1_gen3_2M_5M, fx2_gen3_2M_5M,
#                                      delay1_gen3_2M_5M, delay2_gen3_2M_5M, sscgRemoveFlag_gen3_2M_5M,
#                                      responseType_gen3_2M_5M, pn['Offset Frequency (Hz)'][i])
#         PCIe2_3_4_2M_5M_real = PCIe_3_4_2M_5M.calcFilterResponse().real
#         PCIe2_3_4_2M_5M_imag = PCIe_3_4_2M_5M.calcFilterResponse().imag
#         gen3_2M_5M_filter.append(20 * log(sqrt(PCIe2_3_4_2M_5M_real * PCIe2_3_4_2M_5M_real + PCIe2_3_4_2M_5M_imag * PCIe2_3_4_2M_5M_imag)))
#         gen4_2M_5M_filter.append(20 * log(sqrt(PCIe2_3_4_2M_5M_real * PCIe2_3_4_2M_5M_real + PCIe2_3_4_2M_5M_imag * PCIe2_3_4_2M_5M_imag)))
#
#     # Gen2_SRIS calculation
#         PCIe_2_sris = EC_analysis('Gen2_SRIS', f3db1_gen2_sris, zeta1_gen2_sris, f3db2_gen2_sris, zeta2_gen2_sris,
#                                   f3db3_gen2_sris, fx1_gen2_sris, fx2_gen2_sris, delay1_gen2_sris, delay2_gen2_sris,
#                                   sscgRemoveFlag_gen2_sris, responseType_gen2_sris, pn['Offset Frequency (Hz)'][i])
#         PCIe2_sris_real = PCIe_2_sris.calcFilterResponse().real
#         PCIe2_sris_imag = PCIe_2_sris.calcFilterResponse().imag
#         gen2_sris_filter.append(20 * log(sqrt( PCIe2_sris_real * PCIe2_sris_real+ PCIe2_sris_imag * PCIe2_sris_imag)))
#
#     # Gen3_SRIS calculation
#         PCIe_3_sris = EC_analysis('Gen3_SRIS', f3db1_gen3_sris, zeta1_gen3_sris, f3db2_gen3_sris, zeta2_gen3_sris,
#                                   f3db3_gen3_sris, fx1_gen3_sris, fx2_gen3_sris, delay1_gen3_sris, delay2_gen3_sris,
#                                   sscgRemoveFlag_gen3_sris, responseType_gen3_sris, pn['Offset Frequency (Hz)'][i])
#         PCIe3_sris_real = PCIe_3_sris.calcFilterResponse().real
#         PCIe3_sris_imag = PCIe_3_sris.calcFilterResponse().imag
#         gen3_sris_filter.append(20 * log(sqrt( PCIe3_sris_real * PCIe3_sris_real+ PCIe3_sris_imag * PCIe3_sris_imag)))
#
#     pn['Gen1_Filter'] = gen1_filter
#     pn['Gen2_LoBW_filter'] = gen2_LoBW_filter
#     pn['Gen2_HiBW_filter'] = gen2_HiBW_filter
#     pn['Gen3_2M_4M_filter'] = gen3_2M_4M_filter
#     pn['Gen4_2M_4M_filter'] = gen4_2M_4M_filter
#     pn['Gen3_2M_5M_filter'] = gen3_2M_5M_filter
#     pn['Gen4_2M_5M_filter'] = gen4_2M_5M_filter
#     pn['Gen2_SRIS_filter'] = gen2_sris_filter
#     pn['Gen3_SRIS_filter'] = gen3_sris_filter
#     print pn
#     pn.to_csv('test.csv')
#
#
# class EC_analysis:
#     def __init__(self,name,f3db1,zeta1,f3db2,zeta2,f3db3,fx1,fx2,delay1,delay2,sscgRemoveFlag,responseType,frequency):
#         self.name = name
#         self.f3db1 = f3db1
#         self.zeta1 = zeta1
#         self.f3db2 = f3db2
#         self.zeta2 = zeta2
#         self.f3db3 = f3db3
#         self.fx1 = fx1
#         self.fx2 = fx2
#         self.delay1 = delay1
#         self.delay2 = delay2
#         self.wn1 = (2*pi*self.f3db1 /((1.0 + 2.0*self.zeta1**2.0 + ((1.0 + 2.0*self.zeta1**2.0)**2.0+1.0)**0.5)**0.5))
#         self.wn2 = (2*pi*self.f3db2 /((1.0 + 2.0*self.zeta2**2.0 + ((1.0 + 2.0*self.zeta2**2.0)**2.0+1.0)**0.5)**0.5))
#         self.w3 = (2*pi*self.f3db3)
#         self.wx1 = (2*pi*self.fx1)
#         self.wx2 = (2*pi*self.fx2)
#         self.frequency = frequency
#         self.sscgRemoveFlag = sscgRemoveFlag
#         self.responseType = responseType
#
#     def H_commonClocked(self,s):
#         H1 = ((2*s*self.zeta1*self.wn1 + self.wn1**2)/(s**2 + 2*s*self.zeta1*self.wn1 + self.wn1**2))*(1.0 / (1 + s/self.wx1))*(exp(-self.delay1*s))
#         H2 = ((2*s*self.zeta2*self.wn2 + self.wn2**2)/(s**2 + 2*s*self.zeta2*self.wn2 + self.wn2**2))*(1.0 / (1 + s/self.wx2))*(exp(-self.delay2*s))
#         H3 = (s/(s+self.w3))
#         return (H1-H2)*H3
#
#     def H_dataClocked(self,s):
#         H1 = ((2*s*self.zeta1*self.wn1 + self.wn1**2)/(s**2 + 2*s*self.zeta1*self.wn1 + self.wn1**2))*(1.0 / (1 + s/self.wx1))*(exp(-self.delay1*s))
#         H2 = ((2*s*self.zeta2*self.wn2 + self.wn2**2)/(s**2 + 2*s*self.zeta2*self.wn2 + self.wn2**2))*(1.0 / (1 + s/self.wx2))*(exp(-self.delay2*s))
#         return H1*(1-H2)
#
#     def H_SRIS(self,s): ## 20150610 add hpf pole @ 400 kHz
#         H1 = ((2*s*self.zeta1*self.wn1 + (self.wn1)**2)/(s**2 + 2*s*self.zeta1*self.wn1 + (self.wn1)**2))
#         H2 = s/(s+2*pi*400e3) ## 20150610 add hpf pole @ 400 kHz
#         H3 = (s**2/(s**2+s*2*pi*10**7+2.2*(2*pi)**2*10**12))*((s**2 + 2*s*2*pi*10**7+(2*pi*10**7)**2)/(s**2 + (2*s*2*pi*(10**7)/sqrt(2))+(2*pi*10**7)**2))
#         return H1*H2*H3 ## 20150610 add hpf pole @ 400 kHz
#
#     def H_SRIS_GEN2(self,s):
#         H1 = ((2*s*self.zeta1*self.wn1 + self.wn1**2)/(s**2 + 2*s*self.zeta1*self.wn1 + self.wn1**2))
#         H3 = ((s**2)/(s**2 + sqrt(2)*s*self.w3+ self.w3**2))
#         return H1*H3
#
#     def calcFilterResponse(self):
#         fre = makegrids(self.frequency)
#         if (self.responseType == 'COMMONCLOCKED'):
#             self.filterResponse = self.H_commonClocked(fre)
#         if (self.responseType == 'DATACLOCKED'):
#             self.filterResponse = self.H_dataClocked(fre)
#         if (self.responseType == 'SRIS_GEN3'):
#             self.filterResponse = self.H_SRIS(fre)
#         if (self.responseType == 'SRIS_GEN2'):
#             self.filterResponse = self.H_SRIS_GEN2(fre)
#         return self.filterResponse
#
# if __name__ == '__main__':
#     main()

# import numpy as np
# import pandas as pd
# import os
# import matplotlib.pyplot as plt
#
# os.chdir(r'C:\Users\jgou\Desktop\kaggle')
# game = pd.read_csv(r'Video_Games_Sales_as_at_22_Dec_2016.csv')
# platform = game['Platform'].unique()
# Wii = game[game['Platform'].eq('Wii')].dropna()
# Wii_score = Wii['User_Score']
# print Wii[Wii['User_Score'] == Wii_score.max()]
# print Wii[Wii['User_Score'] == Wii_score.min()]
# plt.hist(Wii_score, 5)
# plt.show()
#

# class Solution(object):
#     def numJewelsInStones(self, J, S):
#         """
#         :type J: str
#         :type S: str
#         :rtype: int
#         """
#         stones = 0
#         for stone in J:
#             if stone in S:
#                 stones += S.count(stone)
#                 S.replace(stone, '')
#         return stones
#
#
# a = Solution()
# print a.numJewelsInStones('aAbB', 'agfdagasbagaABBFAF')


# class Solution(object):
#     def twoSum(self, nums, target):
#         """
#         :type nums: List[int]
#         :type target: int
#         :rtype: List[int]
#         """
#         d = {}
#         for i in range(len(nums)):
#             if target - nums[i] in d.keys():
#                 return [d[target-nums[i]], i]
#             else:
#                 d[nums[i]] = i
#                 print d
#
# a = Solution()
#
# print a.twoSum([1,2,3,0,7,8,9,3], 6)


# class Solution(object):
#     def twoSum(self, nums, target):
#         """
#         :type nums: List[int]
#         :type target: int
#         :rtype: List[int]
#         """
#         d = []
#         for i in range(len(nums)):
#             if target - nums[i] in d:
#                 return [d.index(target-nums[i]), i]
#             else:
#                 d.append(nums[i])
#
# a = Solution()
#
# print a.twoSum([1,2,4,0,7,8,9,3], 20)


# class Solution(object):
#     def repeatedNTimes(self, A):
#         """
#         :type A: List[int]
#         :rtype: int
#         """
#         if A[0] == A[1] or A[0] == A[len(A)-1]:
#             return A[0]
#         elif A[len(A)/2] == A[len(A)/2+1] or A[len(A)/2] == A[len(A)/2-1]:
#             return A[len(A)/2]
#         else:
#             for i in range(0, len(A)/2):
#                 if A[i] == A[i+len(A)/2]:
#                     return A[i]
#
# a = Solution()
#
# print (a.repeatedNTimes([2,1,2,3,4,2]))

# class Solution(object):
#     def sortArrayByParity(self, A):
#         i, j = 0, len(A) - 1
#         while i < j:
#             if A[i] % 2 > A[j] % 2:
#                 A[i], A[j] = A[j], A[i]
#
#             if A[i] % 2 == 0: i += 1
#             if A[j] % 2 == 1: j -= 1
#
#         return A
# a = Solution()
# print (a.sortArrayByParity([3, 4, 2, 1]))

# class Solution(object):
#     def sortedSquares(self, A):
#         """
#         :type A: List[int]
#         :rtype: List[int]
#         """
#         return list(map(lambda x: x*x, A))
#
# a = Solution()
# print (a.sortedSquares([-4, -1, 0, 3, 10]))
#
# import autobench.Velo
#
# print (autobench.Velo.time())

# class Solution(object):
#     def judgeCircle(self, moves):
#         """
#         :type moves: str
#         :rtype: bool
#         """
#         if moves.count('U') == moves.count('D') and moves.count('L') == moves.count('R'):
#             return True
#         else:
#             return False
#
# a = Solution()
# print (a.judgeCircle('RLUD'))

a = '123415'
print (a.rfind('7'))