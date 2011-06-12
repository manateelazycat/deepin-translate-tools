#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Author:     Andy Stewart <lazycat.manatee@gmail.com>
# Maintainer: Andy Stewart <lazycat.manatee@gmail.com>
#
# Copyright (C) 2011 Andy Stewart, all rights reserved.
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

import sys
import apt
import os

def fillContent():
    '''Fill packages' content.'''
    # Init cache.
    cache = apt.Cache()
    
    # Get directory.
    directory = sys.argv[1]
    
    # Fill content.
    [(root, dirs, files)] = os.walk(directory)
    for pkgName in files:
        pkgFile = open(directory + pkgName, "w")
        pkgContent = {"en" : {"pkgName"    : pkgName,
                              "shortDesc"  : cache[pkgName].candidate.summary,
                              "longDesc"   : cache[pkgName].candidate.description}}
        pkgFile.write(str(pkgContent))
        pkgFile.close()

if __name__ == "__main__":
    fillContent()
    
