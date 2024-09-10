#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 19:30:40 2022

@author: sebastien
"""

## LOAD PACKAGES 
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from menu import MenuBar
from toolbar import ToolBar
from sangerplot import SangerTraces, TracesLayout
from filelist import SampleList

import sys


class Main(QMainWindow):

    def __init__(self):
        
        super().__init__()
        
        self.data = {}
        self.samples = SampleList(self)
        
        
        #self.plot_layout = TracesLayout(self)
        self.plot = SangerTraces(self)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        ## CREATE MENUBAR 
        self.menubar = MenuBar(self)
        
        
        ## CREATE TOOLBAR
        self.toolbar = ToolBar(self)
        
        
        ## CREATE DOCK LAYOUT 
        self.dock = QDockWidget(self)
        self.dock.setStyleSheet("margin:0px; padding:0px")
        self.dock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        #self.dock.setLayoutDirection(Qt.RightToLeft)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)


        # create dock2 layout
        self.dock2 = QDockWidget(self)
        self.dock2.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.dock2.setLayoutDirection(Qt.LeftToRight)
        self.addDockWidget(Qt.TopDockWidgetArea, self.dock2)

        
        self.dock3 = QDockWidget(self)
        self.dock3.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.dock3.setLayoutDirection(Qt.LeftToRight)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.dock3)
        
        
        

if __name__=="__main__":

    main = QApplication(sys.argv)
    
    # load and show the main screen
    screen = Main()
    screen.show()
    sys.exit(main.exec_())
