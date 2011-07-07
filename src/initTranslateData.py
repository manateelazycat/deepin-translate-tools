#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 Deepin, Inc.
#               2011 Yong Wang
#
# Author:     Yong Wang <lazycat.manatee@gmail.com>
# Maintainer: Yong Wang <lazycat.manatee@gmail.com>
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

def initTranslateData():
    '''Init translate data.'''
    # Get pkg list.
    pkgList = sys.argv[1]
    
    # Get generate directory.
    genDir = sys.argv[2]
    
    # Generate files.
    for line in open(pkgList).readlines():
        pkgName = line.rstrip("\n")
        print "Create todo file: ", pkgName
        open(genDir + pkgName, 'w').close()
        
if __name__ == "__main__":
    initTranslateData()
    
