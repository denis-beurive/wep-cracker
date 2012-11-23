# -*- coding: utf-8 -*-

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


def cleanEnvironment():
	command = ['airmon-ng', 'check', 'kill']
	lines   = subprocess.check_output(command, shell=False,  stderr=subprocess.STDOUT, universal_newlines=True).split(os.linesep)

def stopInterface(in_interface_name):
	command   = ['airmon-ng', 'stop', in_interface_name]
	lines     = subprocess.check_output(command, shell=False,  stderr=subprocess.STDOUT, universal_newlines=True).split(os.linesep)
	

def startInterface(in_interface_name):
	command   = ['airmon-ng', 'start', in_interface_name]
	lines     = subprocess.check_output(command, shell=False,  stderr=subprocess.STDOUT, universal_newlines=True).split(os.linesep)
	mon       = re.compile('^\s+\(\s*monitor\s+mode\s+enabled\s+on\s+([a-zA-Z0-9_]+)\)\s*$')
	interface = None
	for line in lines:
		match = mon.search(line)
		if match:
			interface = match.group(1)
			break
	if interface is None:
		print("ERROR")
		raise RuntimeError("Could not enable monitor mode for %s" % in_interface_name)
	return interface
		
