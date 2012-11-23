
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
import re
import os

def get():
	# Execute commande and get the result.
	command = ['iwconfig']
	lines   = subprocess.check_output(command, shell=False,  stderr=subprocess.STDOUT, universal_newlines=True).split(os.linesep)
	# Parse the outout.
	iws      = {'essid':[], 'monitor':[]}
	wireless = re.compile('^([a-zA-Z0-9_]+)\s+IEEE\s+802\.11.+\s+ESSID:.+$')
	monitor  = re.compile('^([a-zA-Z0-9_]+)\s+IEEE\s+802\.11.+\s+Mode:Monitor.+$')
	for line in lines:
		match = wireless.search(line)
		if match: iws['essid'].append(match.group(1))
		match = monitor.search(line)
		if match: iws['monitor'].append(match.group(1))
	return iws
	
def stop(in_interface_name):
	command = ['ifconfig', in_interface_name, 'down']
	lines = subprocess.check_output(command, shell=False, universal_newlines=True).split(os.linesep)
	
def changeMac(in_interface_name):
	# Execute commande and get the result.
	command = ['macchanger', '-A', in_interface_name]
	lines   = subprocess.check_output(command, shell=False, universal_newlines=True).split(os.linesep)
	# Execute commande and get the result.
	oldmac  = re.compile('^Current\s+MAC\s*:\s+([^\s]+)\s')
	newmac  = re.compile('^Faked\s+MAC\s*:\s+([^\s]+)\s')
	# Parse the output.
	match = oldmac.search(lines[0])
	if not match:
		raise RuntimeError("Could not change MAC! Output does not contain the old MAC!")
	old_mac = match.group(1)
	match = newmac.search(lines[1])
	if not match:
		raise RuntimeError("Could not change MAC! Output does not contain the new MAC!")
	new_mac = match.group(1)
	return {'old': old_mac, 'new': new_mac}


	
