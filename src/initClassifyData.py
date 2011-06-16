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

def initClassifyData():
    '''Init classify data.'''
    # Init.
    cache = apt.Cache()
    classifyList = []
    
    # Get pkg list.
    pkgList = sys.argv[1]
    
    # Get generate directory.
    genDir = sys.argv[2]
    
    # Generate files.
    for line in open(pkgList).readlines():
        pkgName = line.rstrip("\n")
        if cache.has_key(pkgName) and cache[pkgName].candidate != None:
            # Get package section
            pkg = cache[pkgName]
            pkgSection = pkg.candidate.section
            splitResult = pkgSection.split('/')
            if len (splitResult) == 2:
                # Remove repository prefix, such as, pick pkg from `universal/pkg`
                section = splitResult[1]
            else:
                section = pkgSection
            
            # Classify package.
            classifyList.append((pkgName, section))
        else:
            print "Haven't package %s" % (pkgName)
            
    # Generate classify data.
    dataFile = open(genDir + "unclassify_pkgs.txt", "w")
    dataFile.write(str(classifyList))
    dataFile.close()
        
if __name__ == "__main__":
    initClassifyData()
    
