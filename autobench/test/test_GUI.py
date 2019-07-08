# import sys
# from PyQt4 import QtGui
#
# test = QtGui.QApplication(sys.argv)
# win = QtGui.QWidget()
# add1 = QtGui.QLineEdit()
# add2 = QtGui.QLineEdit()
# flo = QtGui.QFormLayout()
# vhox = QtGui.QHBoxLayout()
# flo.addRow('adder1', add1)
# flo.addRow('adder2', add2)
# adder1 = QtGui.QLabel('adder1')
# adder2 = QtGui.QLabel('adder2')
# sum = QtGui.QPushButton('sum',win)
# sum.setStyleSheet("background-color: yellow")
# sum.move(100,125)
# def add():
#     para1 = float(add1.text())
#     para2 = float(add2.text())
#     print para1 + para2
# sum.clicked.connect(add)
# win.setGeometry(200,200,500,500)
# win.setWindowTitle('add')
# win.setLayout(flo)
# win.show()
# test.exec_()

# !/usr/bin/python
# -*- coding: utf-8 -*-

# import sys
# from PyQt4 import QtGui, QtCore
#
# # !/usr/bin/python
# # -*- coding: utf-8 -*-
#
#! /usr/bin/env python
# -*- coding: utf-8 -*-
# import sys
# from PyQt4 import QtGui, QtCore
#
#
# class Example(QtGui.QWidget):
#
#     def __init__(self):
#         super(Example, self).__init__()
#
#         self.initUI()
#
#     def initUI(self):
#
#         button = QtGui.QPushButton('Dir', self)
#         button.clicked.connect(self.closeEvent)
#         self.setGeometry(300, 300, 250, 150)
#         self.setWindowTitle('Message box')
#         self.show()
#
#     def closeEvent(self, event):
#
#         file = str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory"))
#         reply = QtGui.QMessageBox.question(self, 'Message',
#             'Do you want to choose the path?', QtGui.QMessageBox.Yes |
#             QtGui.QMessageBox.No, QtGui.QMessageBox.No)
#
#         if reply == QtGui.QMessageBox.No:
#             print 'Please'
#         else:
#             print file
#
# def main():
#
#     app = QtGui.QApplication(sys.argv)
#     ex = Example()
#     sys.exit(app.exec_())
#
#
# if __name__ == '__main__':
#     main()

from Tkinter import *

root = Tk()
root.config(bg="black")

container0 = Frame(root, bg='white', padx=4, pady=4, relief='sunken')
container0.pack()
container0.grid(row=0, column=0, sticky='NESW')

container1 = Frame(root, bg='white', padx=4, pady=4, relief='sunken')
container1.pack()
container1.grid(row=0, column=1, sticky='NESW')

container2 = Frame(root, bg='white', padx=4, pady=4, relief='sunken')
container2.pack()
container2.grid(row=0, column=2, sticky='NESW')

m1_label = Label(container0, text='m1', padx=4, pady=4)
m1_label.grid(row=0, column=0, sticky='NESW')

m2_label = Label(container1, text='m2', padx=4, pady=4)
m2_label.grid(row=0, column=0, sticky='NESW')

m3_label = Label(container2, text='m3', padx=4, pady=4)
m3_label.grid(row=0, column=0, sticky='NESW')

container0.grid_rowconfigure(0, weight=1, pad=10)
container0.grid_columnconfigure(0, weight=1, pad=10)

container1.grid_rowconfigure(0, weight=1, pad=10)
container1.grid_columnconfigure(0, weight=1, pad=10)

container2.grid_rowconfigure(0, weight=1, pad=10)
container2.grid_columnconfigure(0, weight=1, pad=10)

root.grid_rowconfigure(0,weight=1,pad=10)
root.grid_columnconfigure(0,weight=1,pad=10)
root.grid_columnconfigure(1,weight=1,pad=10)
root.grid_columnconfigure(2,weight=1,pad=10)
root.mainloop()
