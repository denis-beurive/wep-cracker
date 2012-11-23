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
import subprocess

PWD = os.path.dirname(os.path.realpath(__file__))
PWD = "%s/waves" % PWD

def beep_ok():
	command = ['speaker-test', '-t', 'wav', '-w', 'ok.wav', '-W', PWD, '-r', '44100', '-l', '1']
	subprocess.check_output(command, shell=False, universal_newlines=True)

def beep_error():
	command = ['speaker-test', '-t', 'wav', '-w', 'error.wav', '-W', PWD, '-r', '44100', '-l', '1']
	subprocess.check_output(command, shell=False, universal_newlines=True)

def beep_go():
	command = ['speaker-test', '-t', 'wav', '-w', 'go.wav', '-W', PWD, '-r', '44100', '-l', '1']
	subprocess.check_output(command, shell=False, universal_newlines=True)

def beep_success():
	command = ['speaker-test', '-t', 'wav', '-w', 'success.wav', '-W', PWD, '-r', '22050', '-l', '1']
	subprocess.check_output(command, shell=False, universal_newlines=True)

# beep_success()
# beep_ok()
# beep_go()
# beep_error()
