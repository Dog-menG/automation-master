#!/usr/bin/env python
###########################################################################################
# Test equipment library.
## Supported list of equipment - 
### Tektronix DSA/DPO, Tektronix BERT, Tektronix AWG
###########################################################################################

import sys
import visa
import time
import csv
import smtplib
from decimal import Decimal
from imports import *
visa.logger.disabled = True

#High Speed Intrument Interface
class HSII:
	def __init__(self, ip, terminator=None):
		self.rm = visa.ResourceManager('@py')
		if terminator is None:
			# logger.info("<WARNING>NULL terminator")
			self.scope = self.rm.open_resource(ip)
		else:
			if terminator.lower() == "lf":
				self.scope = self.rm.open_resource(ip)
				self.scope.read_termination = '\n'
				self.scope.write_termination = '\n'
			elif terminator.lower() == "cr":
				self.scope = self.rm.open_resource(ip, read_termination = '\r', write_termination = '\r')
				self.scope.read_termination = '\r'
				self.scope.write_termination = '\r'
				
	def identify(self):
		return str(self.scope.query("*IDN?")).rstrip()

	def disconnect(self):
		self.scope.close()

#Tektronix BERTScope
class BSA(HSII):
	def __init__(self, ip, terminator=None):
		HSII.__init__(self, ip, terminator)
		self.jtol_result_states = {	"0": "Blank",
						"1": "Skipped",
						"2": "InProgress",
						"3": "Passed",
						"4": "NoSync",
						"5": "FAIL_BER",
						"6": "FAIL_CLKERR",
						"7": "FAIL_DATAERR",
						"8": "LIMIT_REACHED"
					  }

	def restore_config(self, cfgfile=None):
		if cfgfile is not None:
			if cfgfile == "Short Channel SV":
				#self.scope.write("RCON \"D:\BitAlyzer\Configurations\Vulcan\Short_Channel\ShortChannel_StressVoltage_nossc_golden.cfg\"")
				self.scope.write("RCON \"D:\BitAlyzer\Configurations\Vulcan\Short_Channel\ShortChannel_StressVoltage_ssc_golden.cfg\"")
			elif cfgfile == "Long Channel SV":
				#self.scope.write("RCON \"D:\BitAlyzer\Configurations\Vulcan\Long_Channel\LongChannel_StressVoltage_nossc_golden.cfg\"")
				self.scope.write("RCON \"D:\BitAlyzer\Configurations\Vulcan\Long_Channel\LongChannel_StressVoltage_ssc_golden.cfg\"")
			elif cfgfile == "Long Channel SJ1":
				self.scope.write("RCON \"D:\BitAlyzer\Configurations\Vulcan\Long_Channel\LongChannel_StressJitter-SJLF1_nossc_golden.cfg\"")
			elif cfgfile == "Long Channel SJ2":
				self.scope.write("RCON \"D:\BitAlyzer\Configurations\Vulcan\Long_Channel\LongChannel_StressJitter-SJLF2_nossc_golden.cfg\"")
			elif cfgfile == "Long Channel SJ3":
				self.scope.write("RCON \"D:\BitAlyzer\Configurations\Vulcan\Long_Channel\LongChannel_StressJitter-SJLF3_nossc_golden.cfg\"")
			elif cfgfile == "Long Channel SJ4":
				self.scope.write("RCON \"D:\BitAlyzer\Configurations\Vulcan\Long_Channel\LongChannel_StressJitter-SJLF4_nossc_golden.cfg\"")
			elif cfgfile == "Long Channel SJ1 SSC":
				self.scope.write("RCON \"D:\BitAlyzer\Configurations\Vulcan\Long_Channel\LongChannel_StressJitter-SJLF1_ssc_golden.cfg\"")
			elif cfgfile == "Long Channel SJ2 SSC":
				self.scope.write("RCON \"D:\BitAlyzer\Configurations\Vulcan\Long_Channel\LongChannel_StressJitter-SJLF2_ssc_golden.cfg\"")
			elif cfgfile == "Long Channel SJ3 SSC":
				self.scope.write("RCON \"D:\BitAlyzer\Configurations\Vulcan\Long_Channel\LongChannel_StressJitter-SJLF3_ssc_golden.cfg\"")
			elif cfgfile == "Long Channel SJ4 SSC":
				self.scope.write("RCON \"D:\BitAlyzer\Configurations\Vulcan\Long_Channel\LongChannel_StressJitter-SJLF4_ssc_golden.cfg\"")
			elif cfgfile == "OIF-CEI JTOL":
				self.scope.write("RCON \"D:\BitAlyzer\Configurations\Vulcan\oif_cei_25g_gen_golden.cfg\"")
			elif cfgfile == "OIF-CEI XTALK":
				self.scope.write("RCON \"D:\BitAlyzer\Configurations\Vulcan\oif_cei_25g_xtalk_golden.cfg\"")
			else:
				logger.info("Unsupported CFG provided")
			time.sleep(25)
		else:
			logger.info("No CFG file provided")

	def dpp_data_ampl(self, value=None):
		if value is not None:
			self.scope.write("DPP:MAXAMPLitude %s" % value)
			if (str(self.scope.query("DPP:MAXAMPLitude?")) == str(value)):
				return True
			else:
				logger.info("<ERROR>Unable to set DPP Amplitude of %s mV" % value)
				return False

		return self.scope.query("DPP:MAXAMPLitude?")

	def dpp_pcie_preset(self, value=None):
		if value is not	None:
			self.scope.write("DPP:PciePREset %s" % value)
			if (str(self.scope.query("DPP:PciePREset?")) == str(value)):
				return True
			else:
				logger.info("<ERROR>Unable to set DPP EQ to %s" % value)
				return False
		return self.scope.query("DPP:PciePREset?")

	def stressedeye(self, component=None, value=None):
		"""
		List of Stressed Eye Components:
		BUJitter:AMPUi, BUJitter:ENABle, BUJitter:FREQuency, BUJitter:TYPE
		EXHFrequency:ENABle
		EXSJitter:AMPUi, EXSJitter:ENABle, EXSJitter:INVErt
		F2Jitter:AMPUi, F2Jitter:AVAilable, F2Jitter:ENABle
		LFRJ:AMPUI, LFRJ:ENABLE
		LFSJ:AMPPS, LFSJ:ENABLE, LFSJ:FREQ
		RJitter:AMPUi, RJitter:ENABle, RJ:TYPE
		SJitter:AMPUi, SJitter:ENABle, SJitter:FREQuency
		SInterference:AMPLitude, SInterference:ENABle, SInterference:FREQuency, SInterference:MODE
		SINEgative:AMPLitude, SINEgative:ENABle, SIPOsitive:AMPLitude, SIPOsitive:ENABle
		"""
		if component is not None:
			if value is not None:
				self.scope.write("GSM:%s %s"%(str(component), str(value)))
				if (str(self.scope.query("GSM:%s?"%str(component))) == str(value)):
					return True
				else:
					logger.info("<ERROR>Unable to set %s to %s"%(str(component), str(value)))
					return False
			else:
				return str(self.scope.query("GSM:%s?"%str(component)))
		else:
			return "UNDEF"
		
	def detector(self, action, value=None):
		if action.lower() == "poll":
			ber 		= self.scope.query("DETector:BER?")
			efber		= self.scope.query("DETector:EFBits?")
			totalbits	= self.scope.query("DETector:BITS?")
			totaltime 	= self.scope.query("DETector:ETIMe?")
			errors 		= self.scope.query("DETector:ERRors?")
			isync           = self.scope.query("DETector:ISYNc?")
			if str(isync) == '0':
				errors = '-1'
			return (ber, efber, totalbits, totaltime, errors)

		elif action.lower() == "autoalign":
			self.scope.write("DETector:RESEtall")
			self.scope.write("DETector:MRESync")
			self.scope.write("DETector:PDC")
			while(int(self.scope.query("RSTate?"))):
				pass	
			self.scope.write("DETector:RESEtall")

	
		elif action.lower() == "sync":	
			self.scope.write("DETector:MRESync")
			self.scope.write("DETector:PDC")
			while(int(self.scope.query("RSTate?"))):
				pass
			time.sleep(10)	
			#status = int(self.scope.query("DETector:DCS?"))
			status = int(self.scope.query("DETector:ISYNc?"))
			return status

		elif action.lower() == "isync":	
			status = self.scope.query("DETector:ISYNc?")
			return status

		elif action.lower() == "run":
			#Save original test time.
			original_runtime = self.scope.query("RDURation?")
			#Set test time.
			self.scope.write("RDURation %s" % value)
			if(str(self.scope.query("RDURation?")) != str(value)):
				logger.info("<ERROR>Unable to set test run of %s seconds" % value)
				return False
			#Reset result, manual resync, autoalign, reset results and run.			
			self.scope.write("DETector:RESEtall")
			self.scope.write("DETector:MRESync")
			self.scope.write("DETector:PDC")
			while(int(self.scope.query("RSTate?"))):
				pass	
			self.scope.write("DETector:RESEtall")
			self.scope.write("RSTate 1")
			while(int(self.scope.query("RSTate?"))):
				pass
			#Set back orginal test time.
			self.scope.write("RDURation %s" % original_runtime)
			time.sleep(5)
			if(str(self.scope.query("RDURation?")) != str(original_runtime)):
				logger.info("<WARNING>Unable to set the original run time of %s seconds" % original_runtime)
			return True
		
		elif action.lower() == "run_nocheck":
			#Set test time.
			self.scope.write("RDURation %s" % value)
			#Manual resync, reset results and run.			
			self.scope.write("DETector:MRESync")	
			self.scope.write("DETector:PDC")
			while(int(self.scope.query("RSTate?"))):
				pass
			self.scope.write("DETector:RESEtall")
			self.scope.write("RSTate 1")
			return True

		elif action.lower() == "stop":
			self.scope.write("RSTate 0")
			if(str(self.scope.query("RSTate?")) == "0"):
				return True
			logger.info("<ERROR>Unable to STOP the ED")
			return False

		elif action.lower() == "resetall":
			self.scope.write("DETector:RESEtall")
			return True

		elif action.lower() == "pattern":
			if value is not None:
				self.scope.write("DETector:PATTern %s" % value)
				if(str(self.scope.query("DETector:PATTern?")) == str(value)):
					return True
				else:
					logger.info("<ERROR>Unable to ED pattern to %s" % value)
					return False
			return self.scope.query("DETector:PATTern?")

		else:
			logger.info("<ERROR>No ED ACTION choosen")
			return False


	def generator(self, action, value=None):
		if action.lower() == "pattern":	
			self.scope.write("GENerator:PATTern " + value)
			time.sleep(3)
			return True

		elif action.lower() == "ssc":
			self.scope.write("GENerator:SSCMOD:ENABle " + value)	
			time.sleep(3)
			return True

		else:
			return False
	
	def clockrecovery(self, action, value=None):
		if action.lower() == "cdrstate":
			lock_state = str(self.scope.query("CRControl:LOCKSTate?"))
			return lock_state
		else:
			return False
			

#Tektronix Arbitary Waveform Generator
class AWG(HSII):
	def __init__(self, ip, setup_file, channel, terminator=None):
		HSII.__init__(self, ip, terminator)
		self.setup_file = str(setup_file)
		self.channel = str(channel)
		# self.setup()
		
	def setup(self):
		self.scope.write("AWGCONTROL:SRESTORE \"%s\"" %(self.setup_file))
		time.sleep(5)
		self.scope.write("AWGCONTROL:RMODE TRIGGERED")
		time.sleep(2)
		self.scope.write("OUTPUT%s:STATE ON" %(self.channel))
		time.sleep(2)
		self.scope.write("AWGCONTROL:RUN")
		time.sleep(2)
	
	def trigger(self, itr=None):
		if itr is None:
			itr = 1
		else:
			pass
		for x in range(1,(itr+1)):
			logger.info("This is trigger # %s" % str(x))
			self.scope.write("TRIGGER:SEQUENCE:IMMEDIATE")
			time.sleep(2)

#Tektronix Arbitary Function Generator
class AFG(HSII):
	def __init__(self, ip, setup_file, channels, terminator=None):
		HSII.__init__(self, ip, terminator)
		self.setup_file = str(setup_file)
		self.channels = channels
		# self.setup()
		
	def setup(self):
		self.scope.write("*RST")
		time.sleep(3)
		usb_contents = self.scope.query("MMEMory:CATalog?")
		if self.setup_file in usb_contents:
			self.scope.write("MMEMory:LOAD:STATe 0, \"%s\"" %(self.setup_file))
			time.sleep(3)
			self.scope.write("*RCL 0")
			time.sleep(3)
			# self.scope.write('RECALL:SETUp "%s"' % self.setup_file)
			# time.sleep(3)
			for channel in self.channels:
				self.channel(channel, "on")
			time.sleep(2)
		else:
			logger.info("Unable to find %s setup file in the USB drive")

	def channel(self, num, action):
		if action.lower() == "on":
			self.scope.write("OUTPut%s:STATe ON" %str(num))
		elif action.lower() == "off":
			self.scope.write("OUTPut%s:STATe OFF" %str(num))
		else:
			logger.info("Unsupported action=%s on channel=%s"%(str(action.lower()), str(num)))

	def trigger(self, itr=None):
		if itr is None:
			itr = 1
		else:
			pass
		for x in range(1,(itr+1)):
			logger.info("This is trigger # %s" % str(x))
			print ("This is trigger # %s" % str(x))
			self.scope.write("TRIGger:SEQuence:IMMediate")
			time.sleep(1.5)
		
#Tektronix High Speed Oscilloscope
class DSA(HSII):
	def __init__(self, ip, terminator=None):
		HSII.__init__(self, ip, terminator)
		self.scope.write("DESE 1")
		self.scope.write("*ESE 1")
		self.scope.write("*SRE 32")
		self.scope.write("HEADER OFF")
		idn = self.identify()
		self.idn = str(idn)

	#DSA70000/DP070000 SERIES SPECIFIC FUNCTIONS	
	def OPCdone(self):
		self.scope.write("*CLS")
		self.scope.write("DSE 1")
		self.scope.write("*ESE 1")
		self.scope.write("*SRE 32")
		self.scope.write("*OPC")
		# consoleprint = 1
		while True:
			logger.info("\tWaiting for remote command on <%s> to complete" %str(self.idn))
			time.sleep(0.2)
			esr = self.scope.query("*ESR?")

			if len(esr) < 1:
				continue
			if esr is not None:
				esr = long(esr)
				if esr == 1 or esr == 33 or esr == 0:
					time.sleep(0.2)
					break

	def frontpanel_control(self, lock):
		if int(lock) == 1:
			self.scope.write("LOCk ALL")
			self.OPCdone()
		elif int(lock) == 0:
			self.scope.write("UNLOCk ALL")
			self.OPCdone()
		else:
			logger.info("Unrecognized value <%s> passed to front panel control function" % str(lock))
	
	def display_onoff(self, ch_math, num, disp):
		ch_math = str(ch_math).upper()
		if ch_math == "CH" or ch_math == "MATH":
			if int(num) > 4 or int(num) < 0:
				logger.info("Invalid %s number <%s> selected" % (ch_math, str(num)))
			else:
				if int(disp) == 1:
					self.scope.write("SELect:%s%s ON" % (ch_math, str(num)))
				elif int(disp) == 0:
					self.scope.write("SELect:%s%s OFF" % (ch_math, str(num)))
				else:
					logger.info("Invalid display action <%s> on %s%s" % (str(disp), ch_math, str(num)))
		else:
			logger.info("Invalid line <%s> selected" % (ch_math))

	def user_label(self, wfm, num, label):
		wfm = str(wfm).upper()
		if (wfm == "CH" or wfm == "MATH"):
			self.scope.write("%s%s LABEL:NAMe \"%s\""%(wfm, str(num), str(label)))
		else:
			logger.info("<user_label> function only supports CH or MATH labeling")
	
	def recall_setup(self, setup_file):
		logger.info("Setup file being used <\"%s\">"%(setup_file))

		if setup_file == "DEFAULT":
			self.scope.write("FACTory")
			time.sleep(5)
			self.OPCdone()
		else:
			self.scope.write("RECALL:SETUp \"%s\""%(setup_file))
			time.sleep(5)
			self.OPCdone()

	def aquisition_state(self, cmd):
		if cmd is None:
			return str(self.scope.query("ACQUIRE:STATE?"))
		else:
			cmd = str(cmd).upper()
			if cmd == "OFF" or cmd == "STOP" or cmd == "ON" or cmd == "RUN":
				self.scope.write("ACQUIRE:STATE %s"%cmd)
				self.OPCdone()
			else:
				logger.info("Unsupported action %s."%cmd)

	def dpojet_command(self, cmd):
		cmd = str(cmd).upper()	
		if (cmd == "RUN" or cmd == "SINGLE" or cmd == "RECALC" or cmd == "CLEAR" or cmd == "STOP"):
			self.scope.write("DPOJET:STATE %s" %str(cmd))
			self.OPCdone()
		else:
			logger.info("Undefined DOPJECT STATE command <%s>"%str(cmd).upper())

	def autoset(self, axis=None):
		"""
		Supported axis:
		HORIzontal | VERTical | BOTH
		"""
		if axis is None:
			logger.info("Axis to be autoset not given")
		else:
			if axis == "HORIzontal" or axis == "VERTical" or axis == "BOTH":
				self.scope.write("DPOJET:SOURCEAutoset %s"%axis)
				time.sleep(5)
				self.OPCdone()
			else:
				logger.info("Unsupported axis %s given.")

	def referencelevel(self, wfm, ch_math):
		wfm = str(wfm).upper()
		ch_math = int(ch_math)
		if (wfm == "CH" or wfm == "MATH"):
			if ch_math < 5 and ch_math > 0:
				self.scope.write("DPOJET:REFLevels:%s%s:AUTOSet 1"%(wfm, str(ch_math)))
				self.OPCdone()
				self.scope.write("DPOJET:REFLevels:AUTOSet EXECute")
				self.OPCdone()
				time.sleep(1.5)
			else:
				logger.info("Unsupported %s%s"%(wfm, str(ch_math)))
		else:
			logger.info("Unsupported CH/MATH=%s"%wfm)
	
	def vertical_scale(self, wfm, ch_math, value=None):
		wfm = str(wfm).upper()
		ch_math = int(ch_math)
		if wfm == "CH":
			if value is None:
				return str(self.scope.query("CH%s:SCAle?"%str(ch_math)))
			else:
				self.scope.write("CH%s:SCAle %s"%(str(ch_math), str(value)))
		elif wfm == "MATH":
			if value is None:
				return str(self.scope.query("MATH%s:VERTical:SCAle?"%str(ch_math)))
			else:
				self.scope.write("MATH%s:VERTical:SCAle %s"%(str(ch_math), str(value)))
		elif wfm == "ZOOM":
			if value is None:
				return str(self.scope.query("ZOOm:MATH%s:VERTical:SCAle?"%str(ch_math)))
			else:
				self.scope.write("ZOOm:MATH%s:VERTical:SCAle %s"%(str(ch_math), str(value)))
		else:
			logger.info("Unsupported CH/MATH=%s"%wfm)

	def caculate_vertical_scale(self, ch_math):
		if int(ch_math) == 1:
			source1 = 'CH1'
			source2 = 'CH2'
		else:
			source1 = 'CH3'
			source2 = 'CH4'
		self.scope.write("MEASUrement:MEAS1:SOUrce1 %s" % source1)
		self.scope.write("MEASUrement:MEAS1:TYPe MAXimum")
		self.scope.write("MEASUrement:MEAS2:SOUrce1 %s" % source1)
		self.scope.write("MEASUrement:MEAS2:TYPe MINImum")
		self.scope.write("MEASUrement:MEAS3:SOUrce1 %s" % source2)
		self.scope.write("MEASUrement:MEAS3:TYPe MAXimum")
		self.scope.write("MEASUrement:MEAS4:SOUrce1 %s" % source2)
		self.scope.write("MEASUrement:MEAS4:TYPe MINImum")
		self.scope.write("MEASUrement:MEAS1:STATE ON")
		self.scope.write("MEASUrement:MEAS2:STATE ON")
		self.scope.write("MEASUrement:MEAS3:STATE ON")
		self.scope.write("MEASUrement:MEAS4:STATE ON")
		time.sleep(3)
		source1_max = float(self.scope.query("MEASUrement:MEAS1:MEAN?"))
		source1_min = float(self.scope.query("MEASUrement:MEAS2:MEAN?"))
		source2_min = float(self.scope.query("MEASUrement:MEAS4:MEAN?"))
		source2_max = float(self.scope.query("MEASUrement:MEAS3:MEAN?"))
		vertical1 = "{:.2e}".format((source1_max - source1_min) / 0.9 / 10)
		vertical2 = "{:.2e}".format((source2_max - source2_min) / 0.9 / 10)
		self.scope.write("MEASUrement:MEAS1:STATE OFF")
		self.scope.write("MEASUrement:MEAS2:STATE OFF")
		self.scope.write("MEASUrement:MEAS3:STATE OFF")
		self.scope.write("MEASUrement:MEAS4:STATE OFF")
		return vertical1, vertical2

	def read_pop(self, slot):
		logger.info("Reading DPOJET measurement population")
		pop = long(self.scope.query("DPOJET:MEAS%s:RESULts:ALLAcqs:POPUlation?"%str(slot)))
		return pop

	def read_measurement(self, field, slot):
		"""
		Fields supported: 	NAME,
					MEAN, STDDev, MAX, MIN, PK2PK, MAXCC, MINCC
		"""
		if field == "NAME":
			return str(self.scope.query("DPOJET:MEAS%s:NAME?"%str(slot))).rstrip().replace("\"","")
		elif (field == "MEAN" or field == "STDDev" or field == "MAX" or field == "MIN" or field == "PK2PK" or field == "MAXCC" or field == "MINCC"):
			return str(self.scope.query("DPOJET:MEAS%s:RESULts:ALLAcqs:%s?"%(str(slot),str(field)))).rstrip().replace("\"","")
		else:
			logger.info("<UNDEF> feild being trying to read, will return UNDEF")
			return "UNDEF"
		
	def report_generator(self, action, value=None):
		"""
		Supported actions:
		EXECute
		REPORTName
		SETupconfig, APPlicationconfig, PASSFailresults, DETailedresults, PLOTimages, AUTOincrement, VIEWreport
		"""
		action = str(action)
		if action == "EXECute":
			self.scope.write("DPOJET:REPORT %s"%action)
			self.OPCdone()
		elif action == "REPORTName":
			if value is None:
				return str(self.scope.query("DPOJET:REPORT:%s?"%action))
			else:
				self.scope.write("DPOJET:REPORT:%s %s"%(action, str("'"+value+"'")))
				self.OPCdone()
				if str(self.scope.query("DPOJET:REPORT:%s?"%action)).rstrip().replace("\"","") == str(value):
					logger.info("<Succesfully set %s = %s"%(action, value))
				else:
					logger.info("<WARNING: Unable to set %s = %s"%(action, value))
			
		elif action == "SETupconfig" or action == "APPlicationconfig" or action == "PASSFailresults" or action == "DETailedresults" or action == "PLOTimages" or action == "AUTOincrement" or action == "VIEWreport":
			if value is None:
				return str(self.scope.query("DPOJET:REPORT:%s?"%action))
			else:
				self.scope.write("DPOJET:REPORT:%s %s"%(action, value))
				self.OPCdone()
				if str(self.scope.query("DPOJET:REPORT:%s?"%action)).rstrip() == str(value):
					logger.info("<Succesfully set %s = %s"%(action, value))
				else:
					logger.info("<WARNING: Unable to set %s = %s"%(action, value))
		else:
			logger.info("<WARNING: Unsupported %s ACTION given"%action)

	def logger(self, action, value=None):
		"""
		Supported actions:
		SNAPshot
		STATistics:STATE, STATistics:FILEname
		MEASurements:STATE, MEASurements:FOLDer
		WORSTcase:STATE, WORSTcase:FOLDer
		
		"""
		action = str(action)
		if action == "SNAPshot":
			if value is None:
				return str(self.scope.query("DPOJET:LOGging:%s?"%action))
			else:
				if value == "STATistics" or value == "MEASurements":
					self.scope.write("DPOJET:LOGging:%s %s"%(action, value))
					self.OPCdone()
					if str(self.scope.query("DPOJET:LOGging:%s?"%action)).rstrip() == str(value):
						logger.info("<Succesfuly set %s = %s"%(action,value))
					else:
						logger.info("<WARNING: Unable to set %s = %s"%(action,value))
				else:
					logger.info("<WARNING: Unsupported %s value for %s"%(str(value), action))
			
		elif action == "STATistics:STATE" or action == "STATistics:FILEname":
			if value is None:
				return str(self.scope.query("DPOJET:LOGging:%s?"%action))
			else:
				self.scope.write("DPOJET:LOGging:%s %s"%(action, value))
				self.OPCdone()
				if str(self.scope.query("DPOJET:LOGging:%s?"%action)).rstrip() == str(value):
					logger.info("<Succesfuly set %s = %s"%(action,value))
				else:
					logger.info("<WARNING: Unable to set %s = %s"%(action,value))

		elif action == "MEASurements:STATE" or action == "MEASurements:FOLDer":
			if value is None:
				return str(self.scope.query("DPOJET:LOGging:%s?"%action))
			else:
				self.scope.write("DPOJET:LOGging:%s %s"%(action, value))
				self.OPCdone()
				if str(self.scope.query("DPOJET:LOGging:%s?"%action)).rsrtip() == str(value):
					logger.info("<Succesfuly set %s = %s"%(action,value))
				else:
					logger.info("<WARNING: Unable to set %s = %s"%(action,value))

		elif action == "WORSTcase:STATE" or action == "WORSTcase:FOLDer":
			if value is None:
				return str(self.scope.query("DPOJET:LOGging:%s?"%action))
			else:
				self.scope.write("DPOJET:LOGging:%s %s"%(action, value))
				self.OPCdone()
				if str(self.scope.query("DPOJET:LOGging:%s?"%action)).rstrip() == str(value):
					logger.info("<Succesfuly set %s = %s"%(action,value))
				else:
					logger.info("<WARNING: Unable to set %s = %s"%(action,value))

		else:
			logger.info("<WARNING: Unsupported %s ACTION"%action)

	#CUSTOM FUNCTIONS
	def dpojet_init(self):
		self.dpojet_command("RUN")
		time.sleep(1)
		self.dpojet_command("STOP")
		self.dpojet_command("CLEAR")

	def dpojet_population(self, preset, max_pop = None):
		# if max_pop is None:
		# 	max_pop = 10
		population = 0
		consoleprint = 1
		# add counter to avoid dead-loop
		counter = 0
		if preset == -3:
			max_pop = 4
		elif -3 < preset < 0:
			max_pop = 2
		elif -1 < preset < 11:
			max_pop = 2
		else:
			max_pop = 2
		while population < max_pop:
			time.sleep(0.1)
			population = self.read_pop(1)
			logger.info("DPOJET has completed only %s measurements, please wait until it completes %s measurements"%(str(population),str(max_pop)))
			counter += 1
			if consoleprint == 1 :
				print("Waiting for DPOJET to complete %s measurements"%str(max_pop))
				consoleprint = 0
			# # stop the program if deadloop happens
			if counter > 3000:
				self.dpojet_command("STOP")
				notify_test_operator('jgou', 'The test fails, please check the setup','4084831216', 'T-MOBILE')
				sys.exit(1)
		self.dpojet_command("STOP")
		# if preset < -2:
		# 	time.sleep(30)
		# elif preset < 0:
		# 	time.sleep(55)
		# else:
		# 	time.sleep(8)
		# self.OPCdone()
		while True:
			result = str(self.scope.query("DPOJET:STATE?").split("\n")[0])
			if result.upper() == 'STOP':
				break
		time.sleep(2)

	def configure_vertscale(self, wfm, ch_math, vertical_source1, vertical_source2):
		if int(ch_math) == 1:
			math_vert = float(vertical_source1) + float(vertical_source2)
			math_vert = str(("%.2E" % math_vert))
			self.vertical_scale(wfm, ch_math, math_vert)
			self.vertical_scale('ZOOM', ch_math, 1)
			self.vertical_scale('CH', 1, vertical_source1)
			self.vertical_scale('CH', 2, vertical_source2)
			print "MATH%s vertical scale is %s" % (ch_math, math_vert)
			read_back = str(self.vertical_scale(wfm, ch_math))
			if float(math_vert) != float(read_back):
				logger.info("Unable to set MATH%s vertical scale to %s" % (str(ch_math), math_vert))
			else:
				logger.info("Succesfully set MATH%s vertical scale to %s" % (str(ch_math), math_vert))
			# force math3,4 to have the same scale as ch1,2
			self.vertical_scale('MATH', 3, vertical_source1)
			self.vertical_scale('ZOOM', 3, 1)
			print "MATH3 vertical scale is %s" % vertical_source1
			self.vertical_scale('MATH', 4, vertical_source2)
			self.vertical_scale('ZOOM', 4, 1)
			print "MATH4 vertical scale is %s" % vertical_source2
			self.display_onoff('MATH', 2, 0)
		elif int(ch_math) == 2:
			math_vert = float(vertical_source1) + float(vertical_source2)
			math_vert = str(("%.2E"%math_vert))
			self.vertical_scale(wfm, ch_math, math_vert)
			self.vertical_scale('ZOOM', ch_math, 1)
			self.vertical_scale('CH', 3, vertical_source1)
			self.vertical_scale('CH', 4, vertical_source2)
			print "MATH%s vertical scale is %s" % (ch_math, math_vert)
			read_back = str(self.vertical_scale(wfm, ch_math))
			if float(math_vert) != float(read_back):
				logger.info("Unable to set MATH%s vertical scale to %s" % (str(ch_math), math_vert))
			else: 
				logger.info("Succesfully set MATH%s vertical scale to %s" % (str(ch_math), math_vert))
			# force math3,4 to have the same scale as ch3,4
			self.vertical_scale('MATH', 3, vertical_source1)
			self.vertical_scale('ZOOM', 3, 1)
			print "MATH3 vertical scale is %s" % vertical_source1
			self.vertical_scale('MATH', 4, vertical_source2)
			self.vertical_scale('ZOOM', 4, 1)
			print "MATH4 vertical scale is %s" % vertical_source2
			self.display_onoff('MATH', 1, 0)
		else:
			logger.info("Unsupported MATH number %s, will just pass" % str(ch_math))
		
	def dpojet_getresults(self, slot):
		#'NAME', 'MEAN', 'STDDev', 'MAX', 'MIN', 'PK2PK', 'POPUlation', 'MAXCC', 'MINCC'
		result_row = []
	
		desc = str(self.read_measurement("NAME",slot))
		mean = str(self.read_measurement("MEAN",slot))
		stddev = str(self.read_measurement("STDDev",slot))
		maxx = str(self.read_measurement("MAX",slot))
		minn = str(self.read_measurement("MIN",slot))
		pktopk = str(self.read_measurement("PK2PK",slot))
		pop = str(self.read_pop(slot))
		maxcc = str(self.read_measurement("MAXCC",slot))
		mincc = str(self.read_measurement("MINCC",slot))

		result_row.extend([desc, mean, stddev, maxx, minn, pktopk, pop, maxcc, mincc])
		return result_row

	def dpojet_resultsanalysis(self, slot, spec, preset, spec_type, analyze=1):
		# 'NAME', 'MEAN', 'STDDev', 'MAX', 'MIN', 'PK2PK', 'POPUlation', 'MAXCC', 'MINCC'
		result_row = []
		applicable = 0

		desc = str(self.read_measurement("NAME", slot))
		mean = str(self.read_measurement("MEAN", slot))
		stddev = str(self.read_measurement("STDDev", slot))
		maxx = str(self.read_measurement("MAX", slot))
		minn = str(self.read_measurement("MIN", slot))
		pktopk = str(self.read_measurement("PK2PK", slot))
		pop = str(self.read_pop(slot))
		maxcc = str(self.read_measurement("MAXCC", slot))
		mincc = str(self.read_measurement("MINCC", slot))
		# vtx-no-eq and ps21 only apply to P4
		if desc in ["PCIEVTXNOEQ1", "PCIEVTXNOEQ2", "PCIEVTXNOEQ3", "PCIEPS21TX1"]:
			if int(preset) == 4:
				applicable = 1
			else:
				applicable = 0
		# vtx-eieos-fs only applies to P10
		elif desc in ["PCIEVTXEIEOS1"]:
			if int(preset) == 10:
				applicable = 1
			else:
				applicable = 0
		elif desc in ['PCIETTXUPWTJ8B10B1', 'PCIETTXUPWDJDD8B10B1']:
			if int(preset) == -3:
				applicable = 0
			else:
				applicable = 1
		else:
			applicable = 1

		if analyze == 1 and applicable == 1:
			if spec_type is "max":
				if float(mean) <= float(spec):
					analysis = "Pass"
				else:
					analysis = "Fail"
			elif spec_type is "min":
				if float(mean) >= float(spec):
					analysis = "Pass"
				else:
					analysis = "Fail"
			else:
				analysis = "Informative"
		else:
			analysis = "Not_Applicable"
		result_row.extend([desc, str(spec), mean, stddev, maxx, minn, pktopk, pop, maxcc, mincc, analysis])
		return result_row
				
	def dpojet_savehtmlreport(self, file_name, user_comment="<PLACEHOLDER>"):
		self.report_generator("VIEWreport","0")
		self.OPCdone()
		self.scope.write("DPOJET:REPORT:COMment '%s'"%str(user_comment))
		self.OPCdone()
		self.report_generator("REPORTName",str(file_name))
		self.OPCdone()
		self.report_generator("EXECute")
		self.OPCdone()
	
	def dpojet_charsetup(self, cfg=None):
		if cfg is None:
			cfg = "DEFAULT"
		else:
			cfg = str(cfg).upper()

		if cfg.endswith('_M1') and "DEEMBEDDED" in cfg:
			# Turn on channel1,2 and math1,3,4
			self.display_onoff("CH",1,1)
			self.display_onoff("CH",2,1)
			self.display_onoff("MATH",1,1)  # Deembedded CH1-CH2
			self.display_onoff("MATH",3,1)  # Deembedded CH1
			self.display_onoff("MATH",4,1)  # Deembedded CH2
			# Turn off channel3,4 and math2
			self.display_onoff("CH",3,0)
			self.display_onoff("CH",4,0)
			self.display_onoff("MATH",2,0)
			if cfg == "PCE4BASE_DEEMBEDDED_GOLDEN_M1":
				self.recall_setup("C:/Users/Tek_Local_Admin/Desktop/Vulcan/Setups/PCE4BASE_DEEMBEDDED_GOLDEN_M1.set")
			elif cfg == "PCE3BASE_DEEMBEDDED_GOLDEN_M1":
				self.recall_setup("C:/Users/Tek_Local_Admin/Desktop/Vulcan/Setups/PCE3BASE_DEEMBEDDED_GOLDEN_M1.set")
			elif cfg == "PCE2BASE_DEEMBEDDED_GOLDEN_M1":
				self.recall_setup("C:/Users/Tek_Local_Admin/Desktop/Vulcan/Setups/PCE2BASE_DEEMBEDDED_GOLDEN_M1.set")
			elif cfg == "PCE1BASE_DEEMBEDDED_GOLDEN_M1":
				self.recall_setup("C:/Users/Tek_Local_Admin/Desktop/Vulcan/Setups/PCE1BASE_DEEMBEDDED_GOLDEN_M1.set")
			elif cfg == "PCE4BASE-RS_DEEMBEDDED_SSC_GOLDEN_M1":
				self.recall_setup("C:/Users/Tek_Local_Admin/Desktop/Vulcan/Setups/PCE4BASE-RS_DEEMBEDDED_SSC_GOLDEN_M1.set")
			elif cfg == "PCE3BASE-RS_DEEMBEDDED_SSC_GOLDEN_M1":
				self.recall_setup("C:/Users/Tek_Local_Admin/Desktop/Vulcan/Setups/PCE3BASE-RS_DEEMBEDDED_SSC_GOLDEN_M1.set")
			elif cfg == "PCE2BASE-RS_DEEMBEDDED_SSC_GOLDEN_M1":
				self.recall_setup("C:/Users/Tek_Local_Admin/Desktop/Vulcan/Setups/PCE2BASE-RS_DEEMBEDDED_SSC_GOLDEN_M1.set")
			elif cfg == "PCE1BASE-RS_DEEMBEDDED_SSC_GOLDEN_M1":
				self.recall_setup("C:/Users/Tek_Local_Admin/Desktop/Vulcan/Setups/PCE1BASE-RS_DEEMBEDDED_SSC_GOLDEN_M1.set")
			elif cfg == "PCE4BASE-VTX_DEEMBEDDED_SSC_GOLDEN_M1":
				self.recall_setup("C:/Users/Tek_Local_Admin/Desktop/Vulcan/Setups/PCE4BASE-VTX_DEEMBEDDED_SSC_GOLDEN_M1.set")
			elif cfg == "PCE3BASE-VTX_DEEMBEDDED_SSC_GOLDEN_M1":
				self.recall_setup("C:/Users/Tek_Local_Admin/Desktop/Vulcan/Setups/PCE3BASE-VTX_DEEMBEDDED_SSC_GOLDEN_M1.set")
			elif cfg == "PCE2BASE-VTX_DEEMBEDDED_SSC_GOLDEN_M1":
				self.recall_setup("C:/Users/Tek_Local_Admin/Desktop/Vulcan/Setups/PCE2BASE-VTX_DEEMBEDDED_SSC_GOLDEN_M1.set")
			elif cfg == "PCE1BASE-VTX_DEEMBEDDED_SSC_GOLDEN_M1":
				self.recall_setup("C:/Users/Tek_Local_Admin/Desktop/Vulcan/Setups/PCE1BASE-VTX_DEEMBEDDED_SSC_GOLDEN_M1.set")
			time.sleep(0.5)
			# self.dpojet_init()

		elif cfg.endswith('_M2') and "DEEMBEDDED" in cfg:
			# Turn on channel3,4 and math2,3,4
			self.display_onoff("CH",3,1)
			self.display_onoff("CH",4,1)
			self.display_onoff("MATH",2,1)  # Deembedded CH3-CH4
			self.display_onoff("MATH",3,1)  # Deembedded CH3
			self.display_onoff("MATH",4,1)  # Deembedded CH4
			# Turn off channel1,2 and math1
			self.display_onoff("CH",1,0)
			self.display_onoff("CH",2,0)
			self.display_onoff("MATH",1,0)
			if cfg == "PCE4BASE_DEEMBEDDED_GOLDEN_M2":
				self.recall_setup("C:/Users/Tek_Local_Admin/Desktop/Vulcan/Setups/PCE4BASE_DEEMBEDDED_GOLDEN_M2.set")
			elif cfg == "PCE3BASE_DEEMBEDDED_GOLDEN_M2":
				self.recall_setup("C:/Users/Tek_Local_Admin/Desktop/Vulcan/Setups/PCE3BASE_DEEMBEDDED_GOLDEN_M2.set")
			elif cfg == "PCE2BASE_DEEMBEDDED_GOLDEN_M2":
				self.recall_setup("C:/Users/Tek_Local_Admin/Desktop/Vulcan/Setups/PCE2BASE_DEEMBEDDED_GOLDEN_M2.set")
			elif cfg == "PCE1BASE_DEEMBEDDED_GOLDEN_M2":
				self.recall_setup("C:/Users/Tek_Local_Admin/Desktop/Vulcan/Setups/PCE1BASE_DEEMBEDDED_GOLDEN_M2.set")
			elif cfg == "PCE4BASE-RS_DEEMBEDDED_SSC_GOLDEN_M2":
				self.recall_setup("C:/Users/Tek_Local_Admin/Desktop/Vulcan/Setups/PCE4BASE-RS_DEEMBEDDED_SSC_GOLDEN_M2.set")
			elif cfg == "PCE3BASE-RS_DEEMBEDDED_SSC_GOLDEN_M2":
				self.recall_setup("C:/Users/Tek_Local_Admin/Desktop/Vulcan/Setups/PCE3BASE-RS_DEEMBEDDED_SSC_GOLDEN_M2.set")
			elif cfg == "PCE2BASE-RS_DEEMBEDDED_SSC_GOLDEN_M2":
				self.recall_setup("C:/Users/Tek_Local_Admin/Desktop/Vulcan/Setups/PCE2BASE-RS_DEEMBEDDED_SSC_GOLDEN_M2.set")
			elif cfg == "PCE1BASE-RS_DEEMBEDDED_SSC_GOLDEN_M2":
				self.recall_setup("C:/Users/Tek_Local_Admin/Desktop/Vulcan/Setups/PCE1BASE-RS_DEEMBEDDED_SSC_GOLDEN_M2.set")
			elif cfg == "PCE4BASE-VTX_DEEMBEDDED_SSC_GOLDEN_M2":
				self.recall_setup("C:/Users/Tek_Local_Admin/Desktop/Vulcan/Setups/PCE4BASE-VTX_DEEMBEDDED_SSC_GOLDEN_M2.set")
			elif cfg == "PCE3BASE-VTX_DEEMBEDDED_SSC_GOLDEN_M2":
				self.recall_setup("C:/Users/Tek_Local_Admin/Desktop/Vulcan/Setups/PCE3BASE-VTX_DEEMBEDDED_SSC_GOLDEN_M2.set")
			elif cfg == "PCE2BASE-VTX_DEEMBEDDED_SSC_GOLDEN_M2":
				self.recall_setup("C:/Users/Tek_Local_Admin/Desktop/Vulcan/Setups/PCE2BASE-VTX_DEEMBEDDED_SSC_GOLDEN_M2.set")
			elif cfg == "PCE1BASE-VTX_DEEMBEDDED_SSC_GOLDEN_M2":
				self.recall_setup("C:/Users/Tek_Local_Admin/Desktop/Vulcan/Setups/PCE1BASE-VTX_DEEMBEDDED_SSC_GOLDEN_M2.set")
			time.sleep(0.5)
			# self.dpojet_init()

		elif cfg == "PCE3BASE_GOLDEN_M1":
			self.display_onoff("CH",1,1)
			self.display_onoff("CH",2,1)
			self.display_onoff("MATH",1,1)  # CH1-CH2

			self.display_onoff("CH",3,0)
			self.display_onoff("CH",4,0)
			self.display_onoff("MATH",2,0)
			self.display_onoff("MATH",3,0)
			self.display_onoff("MATH",4,0)
			self.recall_setup("C:/Users/Tek_Local_Admin/Desktop/Vulcan/Setups/PCE3BASE_GOLDEN_M1.set")
			# self.dpojet_init()

		elif cfg == "PCE3BASE_GOLDEN_M2":
			self.display_onoff("CH",3,1)
			self.display_onoff("CH",4,1)
			self.display_onoff("MATH",2,1)  # CH3-CH4

			self.display_onoff("CH",1,0)
			self.display_onoff("CH",2,0)
			self.display_onoff("MATH",1,0)
			self.display_onoff("MATH",3,0)
			self.display_onoff("MATH",4,0)
			self.recall_setup("C:/Users/Tek_Local_Admin/Desktop/Vulcan/Setups/PCE3BASE_GOLDEN_M2.set")
			# self.dpojet_init()

		elif cfg == "OIF-CEI TX JITTER":
			self.recall_setup("C:/Users/Tek_Local_Admin/Desktop/Setups/Vulcan/tx_jitter_oif-cei-25g_master-0_jan2019.set")
			# self.dpojet_init()
		else:
			self.recall_setup("DEFAULT")	
			logger.info("Undefined CHAR SETUP configuration=<%s>, loading DEFAULT config"%str(cfg).upper())

	def dpojet_launchchar(self, wfm, ch_math):
		self.aquisition_state("RUN")
		time.sleep(2)
		vertical1, vertical2 = self.caculate_vertical_scale(ch_math)
		self.configure_vertscale(wfm, ch_math, vertical1, vertical2)
		time.sleep(2)
		self.referencelevel(wfm, ch_math)
		self.dpojet_command("CLEAR")
		time.sleep(1)
		self.dpojet_command("RUN")

class tekexpress(object):
	"""
	TekExpress PCIE package classte
	"""
	def __init__(self, ip, port = 5000):
		self.rm = visa.ResourceManager('@py')
		self.ip = ip
		self.port = port
		self.socket_address = ip + "::" + str(port) + "::SOCKET"
		self.scope = self.rm.open_resource(self.socket_address)
		self.scope.read_termination = '\n'
		self.scope.write_termination = '\r\n'

	def acquire_mode(self, mode, query = 0):
		"""
		Set or query the acquire mode as live or pre-recorded.
		:param mode: LIVE or PRE-RECORDED
		:param query: 0: set the state, 1: query the state
		:return: acquire_mode
		"""
		if query == 0:
			self.scope.write('TEKEXP:ACQUIRE_MODE %s' % mode)
		else:
			return str(self.scope.query('TEKEXP:ACQUIRE_MODE?'))

	def dut_id(self, dut_id):
		"""
		Set the value of the parameter of DUTID
		:param dut_id: dut_id
		:return: None
		"""
		self.scope.write('TEKEXP:VALUE DUTID,"%s"' % dut_id)

	def generate(self, parameter, value):
		"""
		Set the parameter of type General
		:param parameter: parameter
		:param value: value
		:return: None
		"""
		self.scope.write('TEKEXP:VALUE GENERAL,"%s","%s"' % (parameter, value))

	def identify(self):
		"""
		Query the active TekExpress application name running on the oscilloscope.
		:return: active TekExpress application name running ot the oscilloscope
		"""
		return self.scope.query('TEKEXP:*IDN?')

	def instrument(self, instrument_type, instrument):
		"""
		Set the value for the selected instrument type.
		:param instrument_type: Alternate Real Time Scope or Real Time Scope
		:param instrument: Instrument name
		:return: None
		"""
		self.scope.write('TEKEXP:INSTRUMENT "%s",%s' % (instrument_type, instrument))

	def list(self, type, instrument = 'Real Time Scope'):
		"""
		Query the list of available device, test, version or instrument.
		:param type: device or test or version or instrument
		:param instrument: "Real Time Scope"
		:return: List of device or test or version or instrument
		"""
		if type.upper() == 'DEVICE':
			return self.scope.query('TEKEXP:LIST? DEVICE')
		elif type.upper() == 'SUITE':
			return self.scope.query('TEKEXP:LIST? SUITE')
		elif type.upper == 'VERSION':
			return self.scope.query('TEKEXP:LIST? TEST')
		else:
			return self.scope.query('TEKEXP:LIST? INSTRUMENT,"%s"' % instrument)

	def mode(self, mode):
		"""
		Set the execution mode as compliance or user defined.
		:param mode: COMPLIANCE or USER-DEFINED.
		:return: None
		"""
		self.scope.write('TEKEXP:MODE %s' % mode)

	def report_generate(self):
		"""
		Generate the report for the current session.
		:return: None.
		"""
		self.scope.write('TEKEXP:REPORT GENERATE')

	def result(self, test_name):
		"""
		Query the result available in report summary/details table.
		:param: test_name
		:return: None
		"""
		self.scoep.query('TEKEXP:RESULT? "%s"' % test_name)

	def setup_operation(self, operation, setup_file = None):
		"""
		Set the value of the current setup.
		:param operation: DEFAULT or OPEN or SAVE
		:param setup_file: setup file name
		:return: None
		"""
		if setup_file is None:
			if operation.upper() == 'DEFAULT':
				self.scope.write('TEKEXP:SETUP DEFAULT')
			elif operation.upper() == 'SAVE':
				self.scope.write('TEKEXP:SETUP SAVE')
			else:
				pass
		else:
			if operation.upper() == 'OPEN':
				self.scope.write('TEKEXP:SETUP OPEN,"%s"' % setup_file)
			elif operation.upper() == 'SAVE':
				self.scope.write('TEKEXP:SETUP SAVE,"%s"' % setup_file)
			else:
				pass

	def select(self, type, name = None, status = 'TRUE', query = 0):
		"""
		Select or query the device, suite, verison, test
		:param type: DEVICE or SUITE or VERSION
		:param name: DeviceName or SuiteName or VersionName or TestName
		:param status: selection status, TRUE or FALSE
		:param query: 0: set the state, 1: query the state
		:return: name of selected device, suite, verison, or test
		"""
		if query == 0:
			if type.upper() == 'DEVICE':
				self.scope.write('TEKEXP:SELECT DEVICE,"%s:,%s' % (name, status))
			elif type.upper() == 'SUITE':
				self.scope.write('TEKEXP:SELECT SUITE,"%s",%s' % (name, status))
			elif type.upper() == 'VERSION':
				self.scope.write('TEKEXP:SELCET VERSION, "%s",%s' % (name, status))
			else:
				if name.upper() == 'ALL' or name.upper() == 'REQUIRED':
					self.scope.write('TEKEXP:SELECT TEST,%s,%s' % (name, status))
				else:
					self.scope.write('TEKEXP:SELECT TEST,"%s",%s' % (name, status))
		else:
			self.scope.query('TEKEXP:SELECT? %s' % type)

	def state(self, state, query = 0):
		"""
		Set or query the state of the execution state of the application.
		:param state: RUN or STOP or PAUSE or RESUME
		:param query: 0: set the state, 1: query the state
		:return: execution state of the application
		"""
		if query == 0:
			self.scope.write('TEKEXP:STATE %s' % state)
		else:
			return self.scope.query('TEKEXP:STATE?')

	def wait(self):
		"""
		Query the execution status of the last executed command and add some delays correspondingly
		"""
		status = str(self.scope.query('TEKEXP:*OPC?'))
		while status == '0':
			status = str(self.scope.query('TEKEXP:*OPC?'))
		time.sleep(1)


def notify_test_operator(usr, msg, number, carrier):
	#Sends a text message.
	if (number.isdigit()):
		ip_texter = smtplib.SMTP('maili.marvell.com')
		message = str(msg)
		carrier = str(carrier)
		source = usr + "@marvell.com"
		if carrier == "SPRINT":
			ip_texter.sendmail(source, number + "@messaging.sprintpcs.com", message)
		elif carrier == "AT&T":
			ip_texter.sendmail(source, number + "@txt.att.net", message)
		elif carrier == "VERISON":
			ip_texter.sendmail(source, number + "@vtext.com", message)
		elif carrier == "T-MOBILE":
			ip_texter.sendmail(source, number + "@tmomail.net", message)
		else:
			pass
		ip_texter.quit()
############################################################################################
if __name__ == "__main__":
	print "~~~ Welcome to the TEKTRONIX test equipment library ~~~"
	print "\tSupports the following test equipment--"
	print "\t(1)BERTSCOPE BSA series"
	print "\t(2)AWG7000 series"
	print "\t(3)DSA70000/DPO70000 series"
	print "\t(4)AFG3000 series"
	
	"""	
	AFGIP = "TCPIP0::10.110.162.235::INSTR"
	AFGSCOPE = AFG(AFGIP, "PCIE_PING.TFS", 1)
	AFGID = str(AFGSCOPE.identify())
	print "IDN = %s at IP = %s" % (AFGID, AFGIP)
	AFGSCOPE.trigger(3)
	"""	

	"""
	char_result = "results.csv"
	char_header = ['PHY', 'LANE', 'PRESET', 'NAME', 'MEAN', 'STDDev', 'MAX', 'MIN', 'PK2PK', 'POPUlation', 'MAXCC', 'MINCC']
	handle = open(char_result,'w')
	publish = csv.writer(handle)
	publish.writerow(char_header)
	
	char_cfg = "PCIE3BASESPEC_M1"
	DSASCOPE = DSA("TCPIP0::10.7.30.70::INSTR")
	print("DSA ID = %s"%str(DSASCOPE.idn))
	DSASCOPE.dpojet_charsetup(char_cfg)
	DSASCOPE.dpojet_launchchar("MATH",1)
	DSASCOPE.dpojet_population(5)
	handle = open(char_result,'a')
	publish = csv.writer(handle)
	
	for phy in range(0,1):
		for lane in range(3,4):
			for preset in range(0,11):
				for s in range(1,9):
					result = []
					result.extend([phy, lane, preset])
					value = DSASCOPE.dpojet_getresults(s)
					result.extend(value)
					publish.writerow(result)
				DSASCOPE.dpojet_savehtmlreport(r"C:\Users\Tek_Local_Admin\Desktop\Vulcan\Reports\Preset%s_PHY%s_LANE%s.mht"%(str(preset),str(phy),str(lane)))
	"""

	"""	
	AWGIP = "TCPIP0::10.7.30.72::INSTR"
	AWGSCOPE = AWG(AWGIP, "C:\PCIE_Patterns\PCIE_Toggle_Sequence.awg", 2)
	#AWGID = str(AWGSCOPE.identify())
	#print "BERT ID = %s at IP = %s" % (AWGID, AWGIP)
	AWGSCOPE.trigger(3)
	"""

	"""
	BERTIP = "TCPIP0::10.7.31.237::23::SOCKET"
	BERT = BSA(BERTIP,"lf")
	BERTID = BERT.identify()
	print "BERT ID = %s at IP = %s" % (BERTID, BERTIP)
	vdpp_cal = BERT.dpp_data_ampl()
	print "DPP data amplitude = %s" % vdpp_cal
	vdpp = 850
	if (BERT.dpp_data_ampl(vdpp) == True):
		print "DPP data amplitude = %s succesfull" % vdpp
	else:
		print "DPP data amplitude not succesfully set!!"
	dpp_preset = BERT.dpp_pcie_preset()
	print "DPP PCIE PRESET = %s" % dpp_preset
	preset = "P5"
	if (BERT.dpp_pcie_preset(preset) == True):
		print "DPP PCIE Preset = %s scucesfull" % preset
	else:
		print "DPP PCIE Preset not succesfully set!!"
	ber, ef_ber, total_bits, total_time, error = BERT.detector("poll")
	print "Before stop/reset, ERROR=%s" % error
	BERT.detector("stop")
	BERT.detector("resetall")
	ber, ef_ber, total_bits, total_time, error = BERT.detector("poll")
	print "After reset, ERROR=%s" % error
	BERT.detector("run",30)
	ber, ef_ber, total_bits, total_time, error = BERT.detector("poll")
	print "After BER test, ERROR=%s BER=%s" % (error, ef_ber)
	BERT.disconnect()
	"""
