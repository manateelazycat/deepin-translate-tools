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

import gtk
import pygtk
import os
pygtk.require('2.0')

class AutoClassify:
    '''Auto classify.'''
    DEFAULT_WIDTH = 800
    DEFAULT_HEIGHT = 400
	
    def __init__(self):
        '''Init auto classify.'''
        gtk.gdk.threads_init()        
        
        # Init un-classify list.
        unclassifyFile = open("./unclassify_pkgs.txt", "r")
        unclassifyList = eval(unclassifyFile.read())
        unclassifyFile.close()
        
        # Init classify list.
        classifyList = []
        classifyCategory = ["互联网", "影音", "游戏", "图形图像", "实用工具", "行业软件", "编程开发", "硬件驱动", "Windows软件", "其他"]
        
        # Init window.
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('深度批量归类工具') 
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_default_size(self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT)
        
        # Create main box.
        self.mainBox = gtk.VBox()
        self.window.add(self.mainBox)
        
        # Create action box.
        self.actionBox = gtk.HBox()
        self.mainBox.pack_start(self.actionBox, False, False)
        
        self.fileChooseLabel = gtk.Label("(_O) 选择软件包")
        self.fileChooseLabel.set_use_underline(True)
        self.fileChooseLabelButton = gtk.Button()
        self.fileChooseLabelButton.add(self.fileChooseLabel)
        self.actionBox.pack_start(self.fileChooseLabelButton)
        
        self.classifyBox = gtk.ComboBox()
        self.actionBox.pack_start(self.classifyBox)
        
        self.finishButton = gtk.Button("(_F) 完成分类")
        self.actionBox.pack_start(self.finishButton)
        
        # Create info box.
        self.infoNameFrame = gtk.Frame("名字")
        self.mainBox.pack_start(self.infoNameFrame, False, False)
        
        self.infoCategoryFrame = gtk.Frame("系统分类")
        self.mainBox.pack_start(self.infoCategoryFrame, False, False)
        
        self.infoShortDescFrame = gtk.Frame("简介")
        self.mainBox.pack_start(self.infoShortDescFrame, False, False)
        
        self.infoLongDescFrame = gtk.Frame("详细介绍")
        self.mainBox.pack_start(self.infoLongDescFrame)
        
        # Show.
        self.window.connect("destroy", self.destroy)
        self.window.show_all()
        
        # Main loop.
        gtk.main()
        
    def destroy(self, widget, data=None):
        '''Destroy main window.'''
    	gtk.main_quit()
        
if __name__ == "__main__":
    autoClassify = AutoClassify()
    
