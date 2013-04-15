# Copyright (C) 2013 ~ 2014 rapidhere
#
# Author:     rapidhere@gmail.com
# Maintainer: rapidhere@gmail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
rpbtman Exceptions

  All the Errors and Warnings are the subtype of EXC_rpbtman
    -- All the Errors are subtype of rpbtman_Error
    -- All the Warnings are subtype of rpbtman_Warning
"""
import urllib2

class EXC_rpbtman(Exception):
    def __init__(self,info):
        Exception.__init__(self)
        self.info = info

    def FormatStr(self): return self.info

class rpbtman_Error(EXC_rpbtman):
    def __init__(self,ename,info):
        EXC_rpbtman.__init__(self,"Error : %s \n    %s" % (ename,info))

class rpbtman_Warning(EXC_rpbtman):
    def __init__(self,wname,info):
        EXC_rpbtman.__init__(self,"Warning : %s \n    %s" % (wname,info))
