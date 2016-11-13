from mooltipass_hid_device import *
from mooltipass_defines import *
from os.path import isfile, join
from array import array
from time import sleep
from os import listdir
import platform
import usb.core
import usb.util
import os.path
import random
import struct
import string
import pickle
import copy
import time
import sys
import os

		
# Get a packet to send for a given command and payload
def mpmMassProdInitGetPacketForCommand(cmd, len, data):
	# data to send
	arraytosend = array('B')

	# if command copy it otherwise copy the data
	if cmd != 0:
		arraytosend.append(len)
		arraytosend.append(cmd)

	# add the data
	if data is not None:
		arraytosend.extend(data)
		
	return arraytosend

def mooltipassMiniMassProdInit(mooltipass_device):		
	# Check for update bundle
	if not os.path.isfile("updatefile.img"):
		print "Couldn't find data file!"
		return

	# Loop
	try:
		temp_bool = 0
		while temp_bool == 0:
			# Operation success state
			success_status = True
			
			# Get serial number
			mooltipass_device.getInternalDevice().sendHidPacket([0, CMD_GET_MINI_SERIAL])
			serial_number = mooltipass_device.getInternalDevice().receiveHidPacketWithTimeout()
			if serial_number != None:
				serial_number = serial_number[DATA_INDEX+0]*16777216 + serial_number[DATA_INDEX+1]*65536 + serial_number[DATA_INDEX+2]*256 + serial_number[DATA_INDEX+3]*1
				sys.stdout.write("MPM-"+str(serial_number)+" found... ")
				sys.stdout.flush()
			else:
				success_status = False

			# Send our bundle
			if success_status == True:
				sys.stdout.write('Uploading graphics... ')
				sys.stdout.flush()
				
				# Upload bundle, password is not used in that context
				success_status = mooltipass_device.uploadBundle("00000000000000000000000000000000", "updatefile.img", False)
				
				# For the mini version this procedure doesn't check the last return packet because in normal mode the device reboots
				if success_status == True:
					if mooltipass_device.getInternalDevice().receiveHidPacketWithTimeout()[DATA_INDEX] == 0x01:
						success_status = True
					else:
						success_status = False
						print "last packet fail!!!"
						print "likely causes: problem with external flash"
				else:
					success_status = False
					print "fail!!!"
					print "likely causes: problem with external flash"

			# Inform the Mooltipass that the bundle is sent so it can start functional test
			if success_status == True:
				magic_key = array('B')
				magic_key.append(0)
				magic_key.append(187)
				mooltipass_device.getInternalDevice().sendHidPacket(mpmMassProdInitGetPacketForCommand(CMD_SET_MOOLTIPASS_PARM, 2, magic_key))
				if mooltipass_device.getInternalDevice().receiveHidPacket()[DATA_INDEX] == 0x01:
					success_status = True
					print ""
				else:
					success_status = False
					print "fail!!!"
					print "likely causes: none"

			# Wait for the mooltipass to inform the script that the test was successfull
			if success_status == True:
				temp_bool2 = False
				sys.stdout.write('Please follow the instructions on the mooltipass screen...')
				sys.stdout.flush()
				while temp_bool2 != True:
					test_result = mooltipass_device.getInternalDevice().receiveHidPacketWithTimeout()
					if test_result == None:
						sys.stdout.write('.')
						sys.stdout.flush()
					else:
						if test_result[CMD_INDEX] == CMD_FUNCTIONAL_TEST_RES and test_result[DATA_INDEX] == 0:
							success_status = True
							print " ok!"
						else:
							success_status = False
							print " fail!!!"
							print "Please look at the screen to know the cause"
						temp_bool2 = True

			if success_status == True:
				# Here we should print the label...
				
				# Let the user know it is done
				print "Setting up Mooltipass MPM-"+str(serial_number).zfill(4)+" DONE"
			else:
				print ""
				print "|!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!|"
				print "|---------------------------------------------------------|"
				print "|---------------------------------------------------------|"
				print "| Setting up Mooltipass MPM-"+str(serial_number).zfill(4)+" FAILED                  |"
				print "|                                                         |"                     
				print "|           PLEASE PUT AWAY THIS MOOLTIPASS!!!!           |"                     
				print "|---------------------------------------------------------|"
				print "|---------------------------------------------------------|"
				print "|!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!|"

			# Disconnect this device
			print "\r\nPlease disconnect this Mooltipass"

			# Wait for no answer to ping
			temp_bool2 = 0
			while temp_bool2 == 0:
				try :
					# Send ping packet
					mooltipass_device.pingMooltipass()
				except usb.core.USBError as e:
					#print e
					temp_bool2 = 1
				time.sleep(.5)

			# Connect another device
			print "Connect other Mooltipass"

			# Wait for findHidDevice to return something
			temp_bool2 = False;
			while temp_bool2 == False:
				temp_bool2 = mooltipass_device.connect(False)
				time.sleep(.5)

			# Delay
			time.sleep(1)

			# New Mooltipass detected
			print "New Mooltipass detected"
			print ""
	except KeyboardInterrupt:
		print "File written, everything ok"