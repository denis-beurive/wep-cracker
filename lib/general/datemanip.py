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

from datetime import datetime

__all__ = ['str2datetime']

def str2datetime(in_str):
    [date, time] = in_str.split(' ')
    [year, month, day] = date.split('-')
    [hour, minute, second] = time.split(':')
    return datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))

