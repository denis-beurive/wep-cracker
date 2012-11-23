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

import re
from csvsimple import Csv #@UnresolvedImport
from general.datemanip import str2datetime #@UnresolvedImport

__all__ = ['AirodumpAp']

class AirodumpAp(Csv):
	"Airodump access point interface"
	
	FORMAT = ['bssid', 'first time seen', 'last time seen', 'channel', 'speed', 'privacy', 'cipher', 'authentication', 'power', 'beacons', 'iv', 'lan ip', 'id-length', 'essid', 'key']
	
	# -----------------------------------------------------------------
	# Constructor.
	# ----------------------------------------------------------------- 
	
	def __init__(self, in_values=None):
		super(AirodumpAp, self).__init__(AirodumpAp.FORMAT)
		if not in_values is None:
			for values in in_values:
				self.add(values)
	
	# -----------------------------------------------------------------
	# Public instance's methods.
	# -----------------------------------------------------------------
	
	def add(self, in_values):
		# Strip white spaces.		
		vl = []
		for v in in_values:
			if type(v) is str: v = v.strip()
			vl.append(v)
		
		regexp = re.compile('^\s*<[^>]+>\s*$')
		if regexp.match(in_values[14]): return

		# Add the record.
		vl[1]  = str2datetime(vl[1])
		vl[2]  = str2datetime(vl[2])
		vl[10] = int(vl[10])  # iv
		vl[9]  = int(vl[9])   # beacon
		super(AirodumpAp, self).add(vl)

	# -----------------------------------------------------------------
	# Class' methods
	# -----------------------------------------------------------------

	@staticmethod
	def get(in_record, in_value_name):
		try:
			i = AirodumpAp.index(in_value_name)
			return in_record[i]
		except ValueError:
			raise RuntimeError('Unexpected value name "%s"!' % in_value_name)
		
	@staticmethod
	def index(in_value_name):
		try:
			return AirodumpAp.FORMAT.index(in_value_name)
		except ValueError:
			raise RuntimeError('Unexpected value name "%s"!' % in_value_name)



