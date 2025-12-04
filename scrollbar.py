#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 22:29:29 2025

@author: sebastien
"""

# -- import package -- #
from PyQt5.QtWidgets import QScrollBar
from PyQt5.QtCore import Qt



# -- create the scrollbar class -- #
class ScrollBar(QScrollBar):
    
    ''' CREATE THE SCROLLBAR TO SLIDE THE CHROMATOGRAM GRAPHS '''
    
    def __init__(self, main):
        
        super().__init__()
    
        self.main = main
    
        ## CREATE THE SCROLLBAR
        self.setOrientation(Qt.Horizontal)
        self.sliderMoved.connect(self.slider)
        self.setMouseTracking(True)
        
    def initialize_window(self):
        
        self.setMinimum(0)
        self.setMaximum(self.main.plot.xmax - self.main.plot.xwindow) # to replace 11700

    def slider(self):
        
        self.main.plot.xpos = self.value()
        
        if self.value() >=  self.main.plot.xmax - self.main.plot.xwindow:
            return
        else:

            self.main.plot.setXRange(self.main.plot.xpos, self.main.plot.xpos + self.main.plot.xwindow)
    
        # -- add sequence to the chromatogram -- #
        if self.main.plot.display_sequence == False:
            self.main.plot.show_sequence.hide_sequence_from_traces()
        else:
            self.main.plot.show_sequence.show_sequence_from_traces()
    
    
        
        
        