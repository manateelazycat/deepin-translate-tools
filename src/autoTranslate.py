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

import apt
import gtk
import pygtk
import os
import urllib
import urllib2
import threading as td
import json
from jianfan import *
pygtk.require('2.0')

def postGUI(func):
    '''Post GUI code in main thread.'''
    def wrap(*a, **kw):
        gtk.gdk.threads_enter()
        ret = func(*a, **kw)
        gtk.gdk.threads_leave()
        return ret
    return wrap

def textViewGetContent(textView):
    '''Get content of text view.'''
    textBuffer = textView.get_buffer()
    return textBuffer.get_text(textBuffer.get_start_iter(), textBuffer.get_end_iter())

def textViewSetContent(textView, content):
    '''Set content of text view.'''
    textView.get_buffer().set_text(content)

class AutoTranslate:
    '''Auto translate.'''
    DEFAULT_WIDTH = 800
    DEFAULT_HEIGHT = 400
    
    def __init__(self):
        # Init.
        gtk.gdk.threads_init()        
        
        self.cache = apt.Cache()
        self.pkgName = None
        
        # Init window.
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title('深度批量翻译工具') 
        self.window.set_position(gtk.WIN_POS_CENTER_ALWAYS)
        self.window.set_default_size(self.DEFAULT_WIDTH, self.DEFAULT_HEIGHT)
        
        # Init box.
        self.mainBox = gtk.VBox()
        self.window.add(self.mainBox)
        
        # Add choose file button.
        self.fileChooseLabel = gtk.Label("(_O) 选择需要翻译的包")
        self.fileChooseLabel.set_use_underline(True)
        self.fileChooseLabelButton = gtk.Button()
        self.fileChooseLabelButton.add(self.fileChooseLabel)
        self.fileChooseLabelButton.connect("clicked", lambda w: self.showFileChooseDialog())
        self.mainBox.pack_start(self.fileChooseLabelButton, False, False)
        
        # Add translate view.
        self.translatePaned = gtk.HPaned()
        self.mainBox.pack_start(self.translatePaned)        
        self.window.connect("size-allocate", lambda w, e: self.adjustPaned()) # adjust paned position when window change size
        
        self.originalBox = gtk.VBox()
        self.translatePaned.pack1(self.originalBox)
        self.originalName = gtk.Entry()
        self.originalNameFrame = gtk.Frame("软件名称 （英文）")
        self.originalNameFrame.add(self.originalName)
        self.originalBox.pack_start(self.originalNameFrame, False, False)
        
        self.originalShortDesc = gtk.Entry()
        self.originalShortDescFrame = gtk.Frame("简介 （英文)")
        self.originalShortDescFrame.add(self.originalShortDesc)
        self.originalBox.pack_start(self.originalShortDescFrame, False, False)
        
        self.originalLongDesc = gtk.TextView()
        self.originalLongDesc.set_wrap_mode(gtk.WRAP_WORD)
        self.originalLongDescFrame = gtk.Frame("详细介绍 （英文）")
        self.originalLongDescFrame.add(self.originalLongDesc)
        self.originalScrolledView = gtk.ScrolledWindow()
        self.originalScrolledView.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.originalScrolledView.add_with_viewport(self.originalLongDescFrame)
        self.originalBox.pack_start(self.originalScrolledView)

        self.targetBox = gtk.VBox()
        self.translatePaned.pack2(self.targetBox)
        self.targetName = gtk.Entry()
        self.targetNameFrame = gtk.Frame("软件名称 （简体中文)")
        self.targetNameFrame.add(self.targetName)
        self.targetBox.pack_start(self.targetNameFrame, False, False)
        
        self.targetShortDesc = gtk.Entry()
        self.targetShortDescFrame = gtk.Frame("简介 （简体中文)")
        self.targetShortDescFrame.add(self.targetShortDesc)
        self.targetBox.pack_start(self.targetShortDescFrame, False, False)
        
        self.targetLongDesc = gtk.TextView()
        self.targetLongDesc.set_wrap_mode(gtk.WRAP_WORD)
        self.targetLongDescFrame = gtk.Frame("详细介绍 （简体中文)")
        self.targetLongDescFrame.add(self.targetLongDesc)
        self.targetScrolledView = gtk.ScrolledWindow()
        self.targetScrolledView.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.targetScrolledView.add_with_viewport(self.targetLongDescFrame)
        self.targetBox.pack_start(self.targetScrolledView)
        
        # Add action button.
        self.bottomBox = gtk.HBox()
        self.mainBox.pack_start(self.bottomBox, False, False)        
        
        self.notifyLabel = gtk.Label()
        self.notifyLabel.set_selectable(True)
        self.notifyAlign = gtk.Alignment()
        self.notifyAlign.set(0.0, 0.5, 0.0, 0.0)
        self.notifyAlign.add(self.notifyLabel)
        self.bottomBox.pack_start(self.notifyAlign)
        
        self.actionBox = gtk.HBox()
        self.actionAlign = gtk.Alignment()
        self.actionAlign.set(1.0, 0.5, 0.0, 0.0)
        self.actionAlign.add(self.actionBox)
        self.bottomBox.pack_start(self.actionAlign, False, False)
        
        self.moveTranslateButton = gtk.Button("(_M) 移动中文翻译到右边", None, True)
        self.moveTranslateButton.connect("clicked", lambda w: self.moveTranslation())
        self.actionBox.pack_start(self.moveTranslateButton, False, False)
        
        self.googleTranslateButton = gtk.Button("(_T) 参考Google翻译", None, True)
        self.googleTranslateButton.connect("clicked", lambda w: self.getGoogleTranslate())
        self.actionBox.pack_start(self.googleTranslateButton, False, False)
        
        self.finishButton = gtk.Button("(_F) 完成翻译")
        self.finishButton.connect("clicked", lambda w: self.finishTranslate())
        self.actionBox.pack_start(self.finishButton, False, False)
        
        # Show.
        self.window.connect("destroy", self.destroy)
        self.window.show_all()
        
        # Main loop.
        gtk.main()
        
    def showFileChooseDialog(self):
        '''Show file choose dialog.'''
        # Init dialog.
        dialog = gtk.FileChooserDialog(
            '选择需要翻译的包',           
            None,                     
            gtk.FILE_CHOOSER_ACTION_OPEN, 
            (gtk.STOCK_CANCEL,
             gtk.RESPONSE_CANCEL,
             gtk.STOCK_OPEN,
             gtk.RESPONSE_OK)) 
        
        # Set directory.
        dialog.set_current_folder("./todo")
        
        # Run dialog.
        res = dialog.run()

        # Generate docs if response ok.
        if res == gtk.RESPONSE_OK:
            filename = dialog.get_filename()
            self.generateDocs(filename)

        # Destroy dialog.
        dialog.destroy()
        
    def generateDocs(self, filename):
        '''Generate docs.'''
        # Get package name.
        (_, self.pkgName) = os.path.split(filename)
        
        if self.cache.has_key(self.pkgName):
            # Set original information.
            self.originalName.set_text(self.pkgName)
            self.originalShortDesc.set_text(self.cache[self.pkgName].candidate.summary)
            textViewSetContent(self.originalLongDesc, self.cache[self.pkgName].candidate.description)
            
            # Set target information.
            self.targetName.set_text(self.pkgName)
            self.targetShortDesc.set_text("")
            textViewSetContent(self.targetLongDesc, "")
            
            # Clean notify label when init docs.
            self.notifyLabel.set_text("")
            
            # Focus short description entry.
            self.targetShortDesc.grab_focus()
        else:
            # Notify user if haven't package.
            self.notifyLabel.set_text("你的系统没有 %s 这个包， 请选择其他包翻译. :)" % (self.pkgName))
        
    def finishTranslate(self):
        '''Finish translate.'''
        # Remove old file.
        oldFile = "./todo/" + self.pkgName 
        if os.path.exists(oldFile):
            os.remove(oldFile)

        # Get content.
        content = {}
        content["en"] = {"pkgName" : self.originalName.get_text(),
                         "shortDesc" : self.originalShortDesc.get_text(),
                         "longDesc" : textViewGetContent(self.originalLongDesc)}
        content["zh-CN"] = {"pkgName" : self.targetName.get_text(),
                            "shortDesc" : self.targetShortDesc.get_text(),
                            "longDesc" : textViewGetContent(self.targetLongDesc)}
        content["zh-TW"] = {"pkgName" : jtof(self.targetName.get_text()),
                            "shortDesc" : jtof(self.targetShortDesc.get_text()),
                            "longDesc" : jtof(textViewGetContent(self.targetLongDesc))}
        
        # Create new file.
        newFile = open("./finish/" + self.pkgName, 'w')
        newFile.write(str(content))
        newFile.close()
        
        # Notify user when finish translate.
        self.notifyLabel.set_text("完成了%s的翻译， 请点击最上面的按钮翻译下一个包。 :)" % self.pkgName)
        
        print "Finish translate for %s" % (self.pkgName)
        
        # Read dict from file.
        # f = open(‘text.file’,'r’)
        # my_dict = eval(f.read())        
        
    def moveTranslation(self):
        '''Move translation to right side.'''
        # Move translation to right side.
        self.targetName.set_text(self.originalName.get_text())        
        self.targetShortDesc.set_text(self.originalShortDesc.get_text())
        textViewSetContent(self.targetLongDesc, textViewGetContent(self.originalLongDesc))
        
        # Clean translation in left side.
        self.originalShortDesc.set_text("")
        textViewSetContent(self.originalLongDesc, "")
        
        # Show address notify.
        self.notifyLabel.set_text("请从 http://packages.ubuntu.com/en/natty/%s 复制英文文档" % (self.pkgName))
        
    def getGoogleTranslate(self):
        '''Get google translate.'''
        # Get short description.
        getShortDescThread = GetGoogleTranslate(
            self.originalShortDesc.get_text(), 
            self.setShortDesc, 
            self.notifyLabel,
            "抓取%s简介翻译..." % (self.pkgName),
            "抓取%s简介翻译完毕" % (self.pkgName)
            )
        getShortDescThread.start()
        
        # Get long description.
        getLongDescThread = GetGoogleTranslate(
            textViewGetContent(self.originalLongDesc), 
            self.setLongDesc,
            self.notifyLabel,
            "抓取%s详细翻译..." % (self.pkgName),
            "抓取%s详细翻译完毕" % (self.pkgName)
            )
        getLongDescThread.start()
        
    @postGUI
    def setShortDesc(self, desc):
        '''Set short desc.'''
        self.targetShortDesc.set_text(desc)
    
    @postGUI
    def setLongDesc(self, desc):
        '''Set long desc.'''
        textViewSetContent(self.targetLongDesc, desc)
    
    def destroy(self, widget, data=None):
        '''Destroy main window.'''
    	gtk.main_quit()
        
    def adjustPaned(self):
        '''Adjust paned make both side view have same width.'''
        self.translatePaned.set_position(self.window.allocation.width / 2)
        
class GetGoogleTranslate(td.Thread):
    '''Get google translate.'''
	
    def __init__(self, desc, updateCallback, notifyLabel, progressText, finishText):
        '''Init translate thread.'''
        td.Thread.__init__(self)
        self.setDaemon(True) # make thread exit when main program exit 
        self.desc = desc
        self.updateCallback = updateCallback
        self.notifyLabel = notifyLabel
        self.progressText = progressText
        self.finishText = finishText

    def run(self):
        '''Run'''
        try:
            self.notifyLabel.set_text(self.progressText)
            url = "http://ajax.googleapis.com/ajax/services/language/translate?v=1.0&langpair=en|zh-CN&" + urllib.urlencode({"q" : self.desc})
            connection = urllib2.urlopen(url)
            self.notifyLabel.set_text(self.finishText)
            jsonData = json.loads(connection.read())        
            result = (jsonData["responseData"])["translatedText"]
            self.updateCallback(result)
        except Exception, e:
            print "Get google translate failed."
            
if __name__ == "__main__":
    autoTranslate = AutoTranslate()
    
