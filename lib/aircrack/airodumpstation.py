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

from csvsimple import Csv #@UnresolvedImport
from general.datemanip import str2datetime #@UnresolvedImport

__all__ = ['AirodumpStation']

class AirodumpStation(Csv):
	"Airodump station interface"
	
	FORMAT = ['station mac', 'first time seen', 'last time seen', 'power', 'packets', 'bssid', 'probed essids']
	
	# -----------------------------------------------------------------
	# Constructor.
	# -----------------------------------------------------------------
	
	def __init__(self, in_values=None):
		super(AirodumpStation, self).__init__(AirodumpStation.FORMAT)
		if not in_values is None:
			for values in in_values:
				self.add(values)
	
	# -----------------------------------------------------------------
	# Public instance's methods.
	# -----------------------------------------------------------------
	
	def add(self, in_values):
		if len(in_values) != 7: return
		# Strip white spaces.		
		vl = []
		for v in in_values:
			if type(v) is str: v = v.strip()
			vl.append(v)
		
		# Add the record.
		vl[1] = str2datetime(vl[1])
		vl[2] = str2datetime(vl[2])
		super(AirodumpStation, self).add(vl)

	# -----------------------------------------------------------------
	# Class' methods
	# -----------------------------------------------------------------

	@staticmethod
	def get(in_record, in_value_name):
		try:
			i = AirodumpStation.FORMAT.index(in_value_name)
			return in_record[i]
		except ValueError:
			raise RuntimeError('Unexpected value name "%s"!' % in_value_name)

	@staticmethod
	def index(in_value_name):
		try:
			return AirodumpStation.FORMAT.index(in_value_name)
		except ValueError:
			raise RuntimeError('Unexpected value name "%s"!' % in_value_name)
		
		
		
		
