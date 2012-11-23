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

import os
import re
import subprocess

def ps():
	lines = subprocess.check_output(['ps', 'awxv'], shell=False, universal_newlines=True).split(os.linesep)
	# lines.pop(0)
	regexp = re.compile('^\s*([^\s]+)\s+([^\s]+)\s+([^\s]+)\s+([^\s]+)\s+([^\s]+)\s+([^\s]+)\s+([^\s]+)\s+([^\s]+)\s+([^\s]+)\s+(.+)$')
	pids = []
	for line in lines:
		match = regexp.match(line)
		if match:
			pid = {}
			pid['PID']     = match.group(1)
			pid['TTY']     = match.group(2)
			pid['STAT']    = match.group(3)
			pid['TIME']    = match.group(4)
			pid['MAJFL']   = match.group(5)
			pid['TRS']     = match.group(6)
			pid['DRS']     = match.group(7)
			pid['RSS']     = match.group(8)
			pid['MEM']     = match.group(9)
			pid['COMMAND'] = match.group(10)
			pids.append(pid)
	return pids



