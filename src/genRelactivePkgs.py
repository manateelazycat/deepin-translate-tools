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

import os
import apt_pkg
import apt

def genRelactivePkgs(whitelistDir):
    '''Generate relactive packages.'''
    apt_pkg.init()
    cache = apt.Cache()
    
    for (dirpath, dirname, files) in os.walk(whitelistDir):
        for pkgFile in files:
            content = ""
            for line in open(whitelistDir + "/" + pkgFile).readlines():
                pkgName = line.rstrip("\n")
                content += pkgName + "\n"
                dependencies = cache[pkgName].candidate.dependencies
                for d in dependencies:
                    for bd in d.or_dependencies:
                        content += bd.name + "\n"
                content += "\n"
                
            filepath = "./relactiveWhitelist/" + pkgFile
            pFile = open(filepath, "w")            
            pFile.write(content)
            pFile.close()
                
if __name__ == "__main__":
    genRelactivePkgs("./whitelist")
