from autobench.inst import power, scope
from autobench.i2c.aa_i2c import AAReadWrite
from autobench import log
from tkinter import *
from PIL import ImageTk, Image
import ttk
import tkFileDialog
import threading
import Queue
import pandas as pd
import time
import os


class LDR(object):
    """This class is used to burn part of AP711T."""

    def __init__(self):
        self.log = log(self.__class__.__name__)
        self.queue = Queue.Queue()
        self.root = Tk()
        self.container0 = Frame(self.root, bg='grey', padx=1, pady=1, bd=2, relief='sunken')
        self.container1 = Frame(self.root, bg='grey', padx=1, pady=1, bd=2, relief='sunken')
        self.container2 = Frame(self.root, bg='grey', padx=1, pady=1, bd=2, relief='sunken')
        self.container3 = Frame(self.root, bg='grey', padx=1, pady=1, bd=2, relief='sunken')
        self.container4 = Frame(self.root, width=600, height=750, bg='grey', padx=1, pady=1, bd=2, relief='sunken')
        # Scope frame
        self.scope_label = Label(self.container0, text='Scope', bg='grey')
        self.memory_depth_label = Label(self.container0, text='Memory_depth', bg='grey')
        self.memory_depth_text = Text(self.container0, height=1, width=8)
        self.sample_rate_label = Label(self.container0, text='Sample_rate', bg='grey')
        self.sample_rate_text = Text(self.container0, height=1, width=8)
        self.time_scale_label = Label(self.container0, text='Time_scale', bg='grey')
        self.time_scale_text = Text(self.container0, height=1, width=8)
        self.scope_source1_label = Label(self.container0, text='Scope_source1', bg='grey')
        self.scope_source1_text = Text(self.container0, height=1, width=8)
        self.scope_source2_label = Label(self.container0, text='Scope_source2', bg='grey')
        self.scope_source2_text = Text(self.container0, height=1, width=8)
        self.trigger_edge_label = Label(self.container0, text='Trigger_edge', bg='grey')
        self.trigger_edge_text = Text(self.container0, height=1, width=8)
        self.trigger_level_label = Label(self.container0, text='Trigger_level', bg='grey')
        self.trigger_level_text = Text(self.container0, height=1, width=8)
        self.trigger_mode_label = Label(self.container0, text='Trigger_mode', bg='grey')
        self.trigger_mode_text = Text(self.container0, height=1, width=8)
        self.trigger_source_label = Label(self.container0, text='Trigger_source', bg='grey')
        self.trigger_source_text = Text(self.container0, height=1, width=8)
        self.threshold_mode_label = Label(self.container0, text='Threshold_mode', bg='grey')
        self.threshold_mode_text = Text(self.container0, height=1, width=8)
        self.threshold_low_label = Label(self.container0, text='Threshold_low',bg='grey')
        self.threshold_low_text = Text(self.container0, height=1, width=8)
        self.threshold_mid_label = Label(self.container0, text='Threshold_mid', bg='grey')
        self.threshold_mid_text = Text(self.container0, height=1, width=8)
        self.threshold_high_label = Label(self.container0, text='Threshold_high', bg='grey')
        self.threshold_high_text = Text(self.container0, height=1, width=8)
        self.scope_ip_address_label = Label(self.container0, text='Scope_IP_Address', bg='grey')
        self.scope_ip_address_text = Text(self.container0, height=1, width=20)
        self.scope_ip_address_text.insert(1.0, 'TCPIP0::157.165.147.57::inst0::INSTR')
        self.scope_ip_address = self.scope_ip_address_text.get(1.0, END).split('\n')[0]
        # Power frame
        self.power_label = Label(self.container1, text='Power_supply', bg='grey')
        self.power_channel_label = Label(self.container1, text='Power_channel', bg='grey')
        self.power_channel_text = Text(self.container1, height=1, width=8)
        self.voltage_channel_label = Label(self.container1, text='Voltage', bg='grey')
        self.voltage_text = Text(self.container1, height=1, width=8)
        self.current_compliance_label = Label(self.container1, text='Current_compliance', bg='grey')
        self.current_compliance_text = Text(self.container1, height=1, width=8)
        self.power_gpib_address_label = Label(self.container1, text='GPIB_Address', bg='grey')
        self.power_gpib_address_text = Text(self.container1, height=1, width=8)
        self.power_gpib_address_text.insert(1.0, 18)
        self.power_gpib = self.power_gpib_address_text.get(1.0, END).split('\n')[0]
        self.power_model_label = Label(self.container1, text='Power_model', bg='grey')
        self.power_model_text = Text(self.container1, height=1, width=8)
        self.power_model_text.insert(1.0, 'E3646')
        self.power_model = self.power_model_text.get(1.0, END).split('\n')[0]
        # Aardvark frame
        self.aardvark = Label(self.container2, text='Aardvark', bg='grey')
        self.aardvark_i2c_address_label = Label(self.container2, text='i2c_address', bg='grey')
        self.aardvark_i2c_Address_text = Text(self.container2, height=1, width=8)
        self.aardvark_i2c_Address_text.insert(1.0, 0x6C)
        self.power_gpib = self.power_gpib_address_text.get(1.0, END).split('\n')[0]
        self.aardvark_write_address_label = Label(self.container2, text='write_address', bg='grey')
        self.aardvark_write_Address_text = Text(self.container2, height=1, width=8)
        self.aardvark_read_address_label = Label(self.container2, text='read_address', bg='grey')
        self.aardvark_read_Address_text = Text(self.container2, height=1, width=8)
        self.aardvark_i2c_write_value_blank1 = Label(self.container2, text="", bg='grey')
        self.aardvark_i2c_write_value_label = Label(self.container2, text="Write_value", bg='grey')
        self.aardvark_i2c_write_value_blank2 = Label(self.container2, text="", bg='grey')
        self.aardvark_i2c_write_value_text = Text(self.container2, height=1, width=8)
        self.aardvark_i2c_read_value_blank1 = Label(self.container2, text="", bg='grey')
        self.aardvark_i2c_read_value_label = Label(self.container2, text="Read_back", bg='grey')
        self.aardvark_i2c_read_value_blank2 = Label(self.container2, text="", bg='grey')
        self.aardvark_i2c_read_value_text = Text(self.container2, height=1, width=8)
        # Main frame
        self.Main = Label(self.container3, text='Main', bg='grey')
        self.temperature_label = Label(self.container3, text='Temperature', bg='grey')
        self.temperature_text = Text(self.container3, height=1, width=8)
        self.unit_number_label = Label(self.container3, text='Unit_number', bg='grey')
        self.unit_number_text = Text(self.container3, height=1, width=8)
        self.output_number_label = Label(self.container3, text='Output_number', bg='grey')
        self.output_number_text = Text(self.container3, height=1, width=8)
        self.open_directory_button = Button(self.container3, text='Load_Directory', bg='grey', command=self.load_file_path)
        self.open_directory_text = Text(self.container3, height=1, width=20)
        self.load_file_button = Button(self.container3, text='Load_File', bg='grey', command=self.openfile)
        self.load_file_text = Text(self.container3, height=1, width=20)
        self.save_path_label = Label(self.container3, text='Save_path', bg='grey')
        self.save_path_text = Text(self.container3, height=1, width=20)
        self.file_name = 'file'
        self.file_ready = 0
        self.directory = ''
        self.run_button = Button(self.container3, text='Run', bg='grey', command=self.spawnthread)
        self.progress_bar = ttk.Progressbar(self.container3, orient=HORIZONTAL, mode='determinate')
        self.width = 1200
        self.height = 750
        # Picture
        path = r'C:\Users\jgou\Documents\GitHub\mmt-autobench\autobench\IDT.png'
        image = Image.open(path)
        picture_width = 600
        picture_height = 750
        image = image.resize((picture_width, picture_height))
        img = ImageTk.PhotoImage(image)
        self.picture = Label(self.container4, image=img)
        self.Ui_init()

    def Ui_init(self):
        # Main widget
        self.root.config(bg="black")
        ws = self.root.winfo_screenwidth()  # width of the screen
        hs = self.root.winfo_screenheight()  # height of the screen
        x = (ws/2) - (self.width/2)
        y = (hs/2) - (self.height/2)
        self.root.geometry('%dx%d+%d+%d' % (1250, 750, x, y))
        # Four Frames
        self.container0.pack()
        self.container0.grid(row=0, column=0, sticky='NESW')
        self.container1.pack()
        self.container1.grid(row=1, column=0, sticky='NESW')
        self.container2.pack()
        self.container2.grid(row=2, column=0, sticky='NESW')
        self.container3.pack()
        self.container3.grid(row=3, column=0, sticky='NESW')
        self.container4.pack()
        self.container4.grid(row=0, rowspan=4, column=1, sticky='NESW')
        for row_number in range(0, 4):
            self.root.grid_rowconfigure(row_number, weight=1, pad=10)
        for column_number in range(0, 2):
            self.root.grid_columnconfigure(column_number, weight=1, pad=10)
        scope_row = 0
        scope_column = 0
        power_row = 0
        power_column = 0
        aardvark_row = 0
        aardvark_column = 0
        main_row = 0
        main_column = 0
        # # Scope Widget label
        self.scope_label.config(font=(None, 20))
        self.scope_label.grid(row=scope_row, column=scope_column+2, columnspan=2, padx=7, pady=1, sticky='WE')
        # Memory_depth label
        self.memory_depth_label.grid(row=scope_row+1, column=scope_column, padx=7, pady=1, sticky='WE')
        # Memory_depth text
        self.memory_depth_text.grid(row=scope_row+1, column=scope_column+1, padx=7, pady=1, sticky='WE')
        self.memory_depth_text.insert(1.0, '40e6')
        # Sample_rate label
        self.sample_rate_label.grid(row=scope_row+1, column=scope_column+2, padx=7, pady=1, sticky='WE')
        # Sample_rate text
        self.sample_rate_text.grid(row=scope_row+1, column=scope_column+3, padx=7, pady=1, sticky='WE')
        self.sample_rate_text.insert(1.0, '20e9')
        # Time_scale label
        self.time_scale_label.grid(row=scope_row+1, column=scope_column+4, padx=7, pady=1, sticky='WE')
        # Time_scale text
        self.time_scale_text.grid(row=scope_row+1, column=scope_column+5, padx=7, pady=1, sticky='WE')
        self.time_scale_text.insert(1.0, '200e-6')
        # scope_source1 label
        self.scope_source1_label.grid(row=scope_row+2, column=scope_column+1, padx=7, pady=1, sticky='WE')
        # scope_source1 text
        self.scope_source1_text.grid(row=scope_row+2, column=scope_column+2, padx=7, pady=1, sticky='WE')
        self.scope_source1_text.insert(1.0, 'CHANnel2')
        # scope_source2 label
        self.scope_source2_label.grid(row=scope_row+2, column=scope_column+3, padx=7, pady=1, sticky='WE')
        # scope_source2 text
        self.scope_source2_text.grid(row=scope_row+2, column=scope_column+4, padx=7, pady=1, sticky='WE')
        self.scope_source2_text.insert(1.0, 'CHANnel3')
        # Trigger_edge label
        self.trigger_edge_label.grid(row=scope_row+3, column=scope_column, padx=7, pady=1, sticky='WE')
        # Trigger_edge text
        self.trigger_edge_text.grid(row=scope_row+3, column=scope_column+1, padx=7, pady=1, sticky='WE')
        self.trigger_edge_text.insert(1.0, 'RISing')
        # Trigger_level label
        self.trigger_level_label.grid(row=scope_row+3, column=scope_column+2, padx=7, pady=1, sticky='WE')
        # Trigger_level text
        self.trigger_level_text.grid(row=scope_row+3, column=scope_column+3, padx=7, pady=1, sticky='WE')
        self.trigger_level_text.insert(1.0, 0)
        # Trigger_mode label
        self.trigger_mode_label.grid(row=scope_row+3, column=scope_column+4, padx=7, pady=1, sticky='WE')
        # Trigger_mode text
        self.trigger_mode_text.grid(row=scope_row+3, column=scope_column+5, padx=7, pady=1, sticky='WE')
        self.trigger_mode_text.insert(1.0, 'TRIGgered')
        # Trigger_source label
        self.trigger_source_label.grid(row=scope_row+4, column=scope_column+1, padx=7, pady=1, sticky='WE')
        # Trigger_source text
        self.trigger_source_text.grid(row=scope_row+4, column=scope_column+2, padx=7, pady=1, sticky='WE')
        self.trigger_source_text.insert(1.0, 'CHANnel2')
        # Thresthod_mode
        self.threshold_mode_label.grid(row=scope_row+4, column=scope_column+3, padx=7, pady=1, sticky='WE')
        # Trigger_mode text
        self.threshold_mode_text.grid(row=scope_row+4, column=scope_column+4, padx=7, pady=1, sticky='WE')
        self.threshold_mode_text.insert(1.0, 'ABSolute')
        # Threshold_low label
        self.threshold_low_label.grid(row=scope_row+5, column=scope_column, padx=7, pady=1, sticky='WE')
        # TThreshold_low text
        self.threshold_low_text.grid(row=scope_row+5, column=scope_column+1, padx=7, pady=1, sticky='WE')
        self.threshold_low_text.insert(1.0, -0.15)
        # Threshold_mid label
        self.threshold_mid_label.grid(row=scope_row+5, column=scope_column+2, padx=7, pady=1, sticky='WE')
        # Threshold_mid text
        self.threshold_mid_text.grid(row=scope_row+5, column=scope_column+3, padx=7, pady=1, sticky='WE')
        self.threshold_mid_text.insert(1.0, 0)
        # Threshold_high label
        self.threshold_high_label.grid(row=scope_row+5, column=scope_column+4, padx=7, pady=1, sticky='WE')
        # Threshold_high text
        self.threshold_high_text.grid(row=scope_row+5, column=scope_column+5, padx=7, pady=1, sticky='WE')
        self.threshold_high_text.insert(1.0, 0.15)
        # Scope_IP_address
        self.scope_ip_address_label.grid(row=scope_row+6, column=scope_column, padx=7, pady=1, sticky='WE')
        # Scope_IP_address text
        self.scope_ip_address_text.grid(row=scope_row+6, column=scope_column+1, columnspan=5, padx=7, pady=1,sticky='WE')
        for row_number in range(0, 7):
            self.container0.grid_rowconfigure(row_number, weight=1, pad=10)
        for column_number in range(0, 6):
            self.container0.grid_columnconfigure(column_number, weight=1, pad=10)
        # Power Widget label
        self.power_label.config(font=(None, 20))
        self.power_label.grid(row=power_row, column=power_column+2, columnspan=2, sticky='WE')
        # Power_channel label
        self.power_channel_label.grid(row=power_row+1, column=power_column, padx=7, pady=1, sticky='WE')
        # Power_channel text
        self.power_channel_text.grid(row=power_row+1, column=power_column+1, padx=7, pady=1, sticky='WE')
        self.power_channel_text.insert(1.0, 1)
        # Power_voltage label
        self.voltage_channel_label.grid(row=power_row+1, column=power_column+2, padx=7, pady=1, sticky='WE')
        # Power_channel text
        self.voltage_text.grid(row=power_row+1, column=power_column+3, padx=7, pady=1,sticky='WE')
        self.voltage_text.insert(1.0, 3.3)
        # Power_current_compliance label
        self.current_compliance_label.grid(row=power_row+1, column=power_column+4, padx=7, pady=1, sticky='WE')
        # Power_channel text
        self.current_compliance_text.grid(row=power_row+1, column=power_column+5, padx=7, pady=1, sticky='WE')
        self.current_compliance_text.insert(1.0, 0.3)
        # Power_model
        self.power_model_label.grid(row=power_row+2, column=power_column+1, padx=7, pady=1, sticky='WE')
        # Power_model text
        self.power_model_text.grid(row=power_row+2, column=power_column+2, padx=7, pady=1, sticky='WE')
        # Power_GPIB_address
        self.power_gpib_address_label.grid(row=power_row+2, column=power_column+3, padx=7, pady=1, sticky='WE')
        # Power_GPIB_address text
        self.power_gpib_address_text.grid(row=power_row+2, column=power_column+4, padx=7, pady=1, sticky='WE')
        for row_number in range(0, 3):
            self.container1.grid_rowconfigure(row_number, weight=1, pad=10)
        for column_number in range(0, 6):
            self.container1.grid_columnconfigure(column_number, weight=1, pad=10)
        # Aardvark Widget label
        self.aardvark.config(font=(None, 20))
        self.aardvark.grid(row=aardvark_row, column=aardvark_column+2, columnspan=2, padx=7, pady=1, sticky='WE')
        # Aardvark_I2C_Address label
        self.aardvark_i2c_address_label.grid(row=aardvark_row+1, column=aardvark_column, padx=7, pady=1, sticky='WE')
        # Aardvark_I2C_Address text
        self.aardvark_i2c_Address_text.grid(row=aardvark_row+1, column=aardvark_column+1, padx=7, pady=1,sticky='WE')
        # Aardvark_I2C_write_start_Address label
        self.aardvark_write_address_label.grid(row=aardvark_row+1, column=aardvark_column+2, padx=7, pady=1, sticky='WE')
        # Aardvark_I2C_Address text
        self.aardvark_write_Address_text.grid(row=aardvark_row+1, column=aardvark_column+3, padx=7, pady=1,sticky='WE')
        self.aardvark_write_Address_text.insert(1.0, 0)
        # Aardvark_I2C_Address label
        self.aardvark_read_address_label.grid(row=aardvark_row+1, column=aardvark_column+4, padx=7, pady=1, sticky='WE')
        self.aardvark_read_Address_text.insert(1.0, 0)
        # Aardvark_I2C_Address text
        self.aardvark_read_Address_text.grid(row=aardvark_row+1, column=aardvark_column+5, padx=7, pady=1,sticky='WE')
        # Aardvark write value label
        self.aardvark_i2c_write_value_blank1.grid(row=aardvark_row+2, column=aardvark_column, padx=7, pady=1,sticky='WE')
        self.aardvark_i2c_write_value_label.grid(row=aardvark_row+3, column=aardvark_column, padx=7, pady=1, sticky='WE')
        self.aardvark_i2c_write_value_blank2.grid(row=aardvark_row+4, column=aardvark_column, padx=7, pady=1,sticky='WE')
        # Aardvark write value text
        self.aardvark_i2c_write_value_text.grid(row=aardvark_row+2, column=aardvark_column+1, columnspan=2, rowspan=3, padx=7, pady=1,sticky='NSWE')
        # Aardvark read value label
        self.aardvark_i2c_read_value_blank1.grid(row=aardvark_row+2, column=aardvark_column+3, padx=7, pady=1,sticky='WE')
        self.aardvark_i2c_read_value_label.grid(row=aardvark_row+3, column=aardvark_column+3, padx=7, pady=1, sticky='WE')
        self.aardvark_i2c_read_value_blank2.grid(row=aardvark_row+4, column=aardvark_column+3, padx=7, pady=1,sticky='WE')
        # Aardvark read value text
        self.aardvark_i2c_read_value_text.grid(row=aardvark_row+2, column=aardvark_column+4, columnspan=2, rowspan=3, padx=7, pady=1,sticky='NSWE')
        for row_number in range(0, 5):
            self.container2.grid_rowconfigure(row_number, weight=1, pad=10)
        for column_number in range(0, 6):
            self.container2.grid_columnconfigure(column_number, weight=1, pad=10)
        # Main Widget label
        self.Main.config(font=(None, 20))
        self.Main.grid(row=main_row, column=main_column+2, columnspan=2, padx=7, pady=1, sticky='WE')
        # Temperature label
        self.temperature_label.grid(row=main_row+1, column=main_column, padx=7, pady=1, sticky='WE')
        # Temperature text
        self.temperature_text.grid(row=main_row+1, column=main_column+1, padx=7, pady=1,sticky='WE')
        self.temperature_text.insert(1.0, 25)
        # Unit_number label
        self.unit_number_label.grid(row=main_row+1, column=main_column+2, padx=7, pady=1, sticky='WE')
        # Unit_number text
        self.unit_number_text.grid(row=main_row+1, column=main_column+3, padx=7, pady=1,sticky='WE')
        self.unit_number_text.insert(1.0, 1)
        # Output_number label
        self.output_number_label.grid(row=main_row+1, column=main_column+4, padx=7, pady=1, sticky='WE')
        # Output_number text
        self.output_number_text.grid(row=main_row+1, column=main_column+5, padx=7, pady=1,sticky='WE')
        self.output_number_text.insert(1.0, 1)
        # Open_directory button
        self.open_directory_button.grid(row=main_row+2, column=main_column, padx=7, pady=1, sticky='WE')
        # File name text
        self.open_directory_text.grid(row=main_row+2, column=main_column+1, rowspan=2, columnspan=5, padx=7, pady=1,sticky='NSWE')
        self.open_directory_text.insert(1.0, 'S:\\')
        # load_file button
        self.load_file_button.grid(row=main_row+3, column=main_column, padx=7, pady=1, sticky='WE')
        # File name text
        self.load_file_text.grid(row=main_row+3, column=main_column+1, rowspan=2, columnspan=5, padx=7, pady=1,sticky='NSWE')
        # save_path label
        self.save_path_label.grid(row=main_row+4, column=main_column, padx=7, pady=1, sticky='WE')
        # save_path text
        self.save_path_text.grid(row=main_row+4, column=main_column+1, columnspan=5, padx=7, pady=1,sticky='WE')
        self.save_path_text.insert(1.0, 'S:\\')
        # Run button
        self.run_button.grid(row=main_row+5, column=main_column, padx=7, pady=1, sticky='WE')
        # Progress bar
        self.progress_bar.grid(row=main_row+5, column=main_column+1,columnspan=5, padx=7, pady=1, sticky='WE')
        for row_number in range(0, 6):
            self.container3.grid_rowconfigure(row_number, weight=1, pad=5)
        for column_number in range(0, 6):
            self.container3.grid_columnconfigure(column_number, weight=1, pad=5)
        self.picture.pack()
        self.root.mainloop()

    def spawnthread(self):
        memory_depth = str(self.memory_depth_text.get(1.0, END)).split('\n')[0]
        sample_rate = self.sample_rate_text.get(1.0, END).split('\n')[0]
        time_scale = self.time_scale_text.get(1.0, END).split('\n')[0]
        source1 = self.scope_source1_text.get(1.0, END).split('\n')[0]
        source2 = self.scope_source2_text.get(1.0, END).split('\n')[0]
        edge = self.trigger_edge_text.get(1.0, END).split('\n')[0]
        scope_ip_address = self.scope_ip_address_text.get(1.0, END).split('\n')[0]
        trigger_level = self.trigger_level_text.get(1.0, END).split('\n')[0]
        trigger_mode = self.trigger_mode_text.get(1.0, END).split('\n')[0]
        thre_mode = self.threshold_mode_text.get(1.0, END).split('\n')[0]
        thre_high = self.threshold_high_text.get(1.0, END).split('\n')[0]
        thre_mid = self.threshold_mid_text.get(1.0, END).split('\n')[0]
        thre_low = self.threshold_low_text.get(1.0, END).split('\n')[0]
        power_gpib = self.power_gpib_address_text.get(1.0, END).split('\n')[0]
        power_model = str(self.power_model_text.get(1.0 ,END).split('\n')[0])
        output = self.output_number_text.get(1.0, END).split('\n')[0]
        unit_number = self.unit_number_text.get(1.0, END).split('\n')[0]
        file_name = self.load_file_text.get(1.0, END).split('\n')[0]
        aardvark_address = int(self.aardvark_i2c_Address_text.get(1.0, END).split('\n')[0])
        scope_setting = [memory_depth, sample_rate, time_scale, source1, source2, edge, trigger_level, trigger_mode,
                         thre_mode, thre_high, thre_mid, thre_low, output, unit_number]
        self.thread = ThreadedClient(self.queue, power_gpib, power_model, aardvark_address, scope_ip_address, file_name,
                                     scope_setting, self.file_ready)
        self.thread.start()
        self.periodiccall()

    def periodiccall(self):
        self.checkqueue()
        if self.thread.is_alive():
            self.root.after(100, self.periodiccall)
        else:
            pass

    def checkqueue(self):
        while self.queue.qsize():
            try:
                package = self.queue.get(0)
                round_number = package[0]
                if round_number == 0:
                    self.progress_bar['value'] = 0
                    self.aardvark_i2c_write_value_text.delete(1.0, END)
                    self.log.info('Initialization is done.')
                else:
                    read_back = package[1]
                    picture = package[2]
                    input_file = pd.read_excel(self.file_name)
                    loop_number = len(input_file.index)
                    # power_supply_frame
                    power_supply = str(input_file.iloc[round_number-1][0]).split(',')
                    channel1 = int(power_supply[0]); voltage1 = float(power_supply[1]); current1 = power_supply[2]
                    self.power_channel_text.delete(1.0, END)
                    self.power_channel_text.insert(1.0, channel1)
                    self.voltage_text.delete(1.0, END)
                    self.voltage_text.insert(1.0, voltage1)
                    self.current_compliance_text.delete(1.0, END)
                    self.current_compliance_text.insert(1.0, current1)
                    # aardvark_frame
                    aardvark = str(input_file.iloc[round_number-1][2]).split(',')
                    register_values = []
                    read_back_result = []
                    start_address = aardvark[0]
                    for n in range(0, len(aardvark[1].split(' '))):
                        register_values.append(int(aardvark[1].split(' ')[n], 16))
                    for i in range(0, len(read_back) - 1):
                        register = hex(read_back[i])[2:].upper()
                        if len(register) == 1:
                            register = '0' + register
                        read_back_result.append(register)
                    self.aardvark_write_Address_text.delete(1.0, END)
                    self.aardvark_write_Address_text.insert(1.0, start_address)
                    self.aardvark_i2c_write_value_text.delete(1.0, END)
                    self.aardvark_i2c_write_value_text.insert(1.0, str(aardvark[1]))
                    self.aardvark_read_Address_text.delete(1.0, END)
                    self.aardvark_read_Address_text.insert(1.0, start_address)
                    self.aardvark_i2c_read_value_text.delete(1.0, END)
                    self.aardvark_i2c_read_value_text.insert(1.0, ' '.join(read_back_result))
                    # main frame
                    temp = str(input_file.iloc[round_number-1][3]); save_path = str(input_file.iloc[round_number-1][4])
                    self.temperature_text.delete(1.0, END)
                    self.temperature_text.insert(1.0, temp)
                    self.save_path_text.delete(1.0, END)
                    self.save_path_text.insert(1.0, save_path)
                    # picture
                    image = Image.open(picture+'.png')
                    image = image.resize((600, 750))
                    img = ImageTk.PhotoImage(image)
                    self.picture.configure(image=img)
                    self.picture.image = img
                    # prograss_bar
                    self.progress_bar['value'] = 100.0 / loop_number * (round_number - 1 + 1)
                    self.log.info('This round is done.')
            except Queue.Empty:
                pass

    def openfile(self):
        self.file_name = tkFileDialog.askopenfilename(initialdir = self.directory)
        self.load_file_text.delete(1.0, END)
        self.load_file_text.insert(1.0, self.file_name)
        self.file_ready = 1

    def load_file_path(self):
        self.directory = tkFileDialog.askdirectory(initialdir = 's:\\')
        self.open_directory_text.delete(1.0, END)
        self.open_directory_text.insert(1.0, self.directory)


class ThreadedClient(threading.Thread):

    def __init__(self, queue, power_gpib, power_model, i2c_address, scope_ip_address, file_name, scope_setting, file_ready):
        threading.Thread.__init__(self)
        self.log = log(self.__class__.__name__)
        self.queue = queue
        self.power_model = power_model
        if self.power_model == 'E3646':
            self.power_3646 = power.E3646A(power_gpib)
        elif self.power_model == 'E3631':
            self.power_3631 = power.E3631A(power_gpib)
        self.scope = scope.Keysight(scope_ip_address)
        self.dut_i2c = AAReadWrite(0, i2c_address, True)
        self.dut_i2c.length = 1
        self.input_file = file_name
        self.memory_depth = scope_setting[0]
        self.sample_rate = scope_setting[1]
        self.time_scale = scope_setting[2]
        self.source1 = scope_setting[3]
        self.source2 = scope_setting[4]
        self.edge = scope_setting[5]
        self.trigger_level = scope_setting[6]
        self.trigger_mode = scope_setting[7]
        self.thre_mode = scope_setting[8]
        self.thre_high = scope_setting[9]
        self.thre_mid = scope_setting[10]
        self.thre_low = scope_setting[11]
        self.output = scope_setting[12]
        self.unit_number = scope_setting[13]
        self.measurement = 'PERiod'
        self.function_number = 2
        self.measurement_number = 1
        self.trend_status = 'ON'
        self.run_mode = 'RUN'
        self.all_edge_status = 'ON'
        self.file_ready = file_ready
        self.file_name = ''
        self.save_path = ''
        self.slew_rate_results = []

    def i2c_read(self, start_address, length):
        return list(self.dut_i2c.aa_read_i2c(start_address, length))

    def i2c_write(self, start_address, resigster_values):
        self.dut_i2c.aa_write_i2c(start_address, resigster_values)

    def i2c_close(self):
        self.dut_i2c.close()

    def power_on_off(self, power_model, status):
        if power_model == 'E3646':
            self.power_3646.on_off(status)
        elif power_model == 'E3631':
            self.power_3631.on_off(status)

    def power_setup(self, power_model, channel, voltage, current):
        if power_model == 'E3646':
            self.power_3646.select_channel(channel)
            self.power_3646.set_voltage(voltage, current)
        elif power_model == 'E3631':
            self.power_3631.set_voltage(channel, voltage, current)

    def scope_display_clear(self):
        self.scope.clear_dispay()
        self.scope.wait()

    def scope_slew_rate_measure(self, source):
        self.scope.thresholds_general_absolute(source, 0.01, 0, -0.01)
        time.sleep(1)
        self.scope_measure('SLEWrate', source)
        self.scope_measure('Period', source)
        self.scope_measure_vertical('VTOP', source)
        self.scope.measure_vertical('VBASe', source)
        result = self.scope.get_result()
        self.scope.clear_dispay()
        time.sleep(1)
        return result

    def scope_run_mode(self, run_mode):
        self.scope.run_mode(run_mode)
        self.scope.wait()

    def scope_vertical_full_swing(self, source):
        if 'FUNCtion' in source:
            self.scope.function_vertical_mode(source, 'AUTO')
            self.scope.function_vertical_mode(source, 'MANual')
        else:
            pass
        self.scope.auto_scale_vertical(source)
        self.scope_wait()
        self.scope_measure_vertical('VPP', source)
        vertical = self.scope.get_result()[5]
        self.scope_wait()
        self.scope_measure_vertical('VMAX', source)
        vtop = self.scope.get_result()[5]
        self.scope_wait()
        self.scope_measure_vertical('VMIN', source)
        vbase = self.scope.get_result()[5]
        self.scope_wait()
        offset = (float(vtop) + float(vbase)) / 2
        self.scope.source_range_setup(source, vertical, offset)
        self.scope.measure_clear()

    def scope_trend_measure(self, function_number, measurement_number, function_status):
        self.scope.source_on_off('FUNCtion'+str(function_number), function_status)
        self.scope.function_measure_trend(function_number, measurement_number)

    def scope_measure(self, measurement, source):
        self.scope.measure(measurement, source, direction='RISing')

    def scope_measure_vertical(self, measurement, source):
        self.scope.measure_vertical(measurement, source)

    def scope_save_picture(self, file_name):
        self.scope.screen_save(file_name)
        self.scope.measure_clear()
        self.scope_wait()

    def scope_save_waveform(self, source, file_name, file_type, header):
        self.scope.waveform_save(source, file_name, file_type, header)

    def scope_wait(self):
        status = self.scope.require_status().strip()
        while status != '1':
            status = str(self.scope.require_status().strip())

    def scope_setup(self, source1, source2, edge, trigger_level, trigger_mode, run_mode, status, file_path_name):
        self.scope.acquisition(20e3, 20e9, 10e-9)
        self.scope.trigger_setup(source1, 'POSitive', 0.1, 'AUTO')
        self.scope.source_on(source1)
        self.scope.source_on(source2)
        self.scope.run_mode('RUN')
        self.scope.measure_clear()
        self.scope.function_double('FUNCtion1', 'SUBTract', source1, source2)
        self.scope.source_on_off('FUNCtion1', 'ON')
        self.scope_vertical_full_swing('FUNCtion1')
        time.sleep(0.1)
        self.scope.source_on_off(source1, 'OFF')
        self.scope.source_on_off(source2, 'OFF')
        results = self.scope_slew_rate_measure('FUNCtion1')
        self.scope_save_picture(file_path_name)
        self.scope.trigger_setup(source1, edge, trigger_level, trigger_mode)
        self.scope_run_mode(run_mode)
        self.scope.measure_all_edges(status)
        return results

    def run(self):
        if self.file_ready:
            input_file = pd.read_excel(self.input_file)
            loop_number = len(input_file.index)
            for x in range(0, loop_number+1):
                if x == 0:
                    self.queue.put([x, x])
                    time.sleep(1)
                else:
                    power_supply = str(input_file.iloc[x-1][0]).split(',')
                    channel1 = int(power_supply[0]); voltage1 = float(power_supply[1]); current1 = power_supply[2]

                    Aardvark = str(input_file.iloc[x-1][2]).split(',')
                    register_values = []
                    start_address = Aardvark[0]
                    for n in range(0, len(Aardvark[1].split(' '))):
                        register_values.append(int(Aardvark[1].split(' ')[n], 16))

                    temp = str(input_file.iloc[x-1][3]); save_path = str(input_file.iloc[x-1][4])
                    part = str(input_file.iloc[x-1][5]); Label = str(input_file.iloc[x-1][6])

                    path_file_name = r"%s\%smV_%sC_%s_Unit%s_output%s_%s" %(save_path, int(voltage1 * 1000),temp, part,
                                                                            self.unit_number, self.output, Label)

                    slew_rate_file_name = r"%s\%smV_%sC_%s_Unit%s_%s" %(save_path, int(voltage1 * 1000),temp, part,
                                                                            self.unit_number, Label)
                    self.file_name = slew_rate_file_name + '_slew_rate.csv'

                    # power supply setup
                    self.power_on_off(self.power_model, 'OFF')
                    self.power_setup(self.power_model, channel1, voltage1, current1)
                    self.power_on_off(self.power_model, 'ON')
                    time.sleep(0.5)

                    # Aardvark write and read
                    self.i2c_write(start_address, register_values)
                    read_start_address = int(start_address, 16)
                    read_back = self.i2c_read(read_start_address, len(register_values))

                    # scope setup and save picture
                    results = self.scope_setup(self.source1, self.source2, self.edge,self.trigger_level,
                                               self.trigger_mode, self.run_mode, self.all_edge_status, path_file_name)
                    results.append(part + '_Unit' + self.unit_number + '_Output' + self.output + '_' + Label)
                    self.slew_rate_results.append(results[24:])
                    # LDR measure
                    self.scope_display_clear()
                    if str(self.thre_mode).upper() == 'ABSOLUTE':
                        self.scope.thresholds_general_absolute('FUNCtion1', self.thre_high, self.thre_mid, self.thre_low)
                    elif str(self.thre_mode).upper() == 'PERCENT':
                        self.scope.thresholds_general_percent('FUNCtion1', self.thre_high, self.thre_mid, self.thre_low)
                    else:
                        self.scope.thresholds_general_absolute('FUNCtion1', self.thre_high, self.thre_mid, self.thre_low)
                    self.scope_measure(self.measurement, 'FUNCtion1')
                    self.scope_wait()
                    self.scope_trend_measure(self.function_number, self.measurement_number, self.trend_status)
                    self.scope_wait()
                    self.scope_display_clear()
                    time.sleep(2)
                    self.scope.acquisition(self.memory_depth, self.sample_rate, self.time_scale, 'ON')
                    self.scope_wait()
                    time.sleep(5)
                    # To get better result
                    self.scope_run_mode('stop')
                    time.sleep(2)
                    self.scope_display_clear()
                    time.sleep(2)
                    self.scope_run_mode('single')

                    # Waveform save
                    waveform_name = r"%s\%smV_%sC_%s_Unit%s_output%s_%s" % (save_path, int(voltage1 * 1000), temp, part,
                                                                            self.unit_number, self.output, Label)
                    waveform_source = 'FUNCtion2'
                    file_type = 'TXT'
                    Header_status = 'OFF'
                    self.scope_save_waveform(waveform_source, waveform_name, file_type, Header_status)
                    self.scope_wait()
                    return_package = [x, read_back, path_file_name]
                    self.queue.put(return_package)
                    time.sleep(1)
            self.i2c_close()
            # summarize data
            columns = ['label', 'current', 'result_state', 'Min V/ns', 'Max V/ns', 'Mean V/ns', 'STD', 'Numbers', 'part']
            drop_columns = ['label', 'current', 'result_state', 'STD', 'Numbers']
            slew_rate = pd.DataFrame(self.slew_rate_results, columns=columns)
            slew_rate.drop(drop_columns, axis=1, inplace=True)
            slew_rate = slew_rate[['part'] + slew_rate.columns[:-1].tolist()]
            slew_rate['Min V/ns'] = slew_rate['Min V/ns'].astype('float')/10e8
            slew_rate['Max V/ns'] = slew_rate['Max V/ns'].astype('float')/10e8
            slew_rate['Mean V/ns'] = slew_rate['Mean V/ns'].astype('float')/10e8
            slew_rate = slew_rate.round({'Min V/ns': 2, 'Max V/ns': 2, 'Mean V/ns': 2})
            slew_rate.to_csv(self.file_name, mode='a', index=False)
        else:
            pass


def main():
    LDR()


if __name__ == "__main__":
    main()
