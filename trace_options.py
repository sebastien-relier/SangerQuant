#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 19:54:43 2024

@author: sebastien
"""
from PyQt5.QtWidgets import QSlider, QSizePolicy
from PyQt5.QtCore import *

class TraceShape(QSlider):
    
    ''' CREATE A QLSIDER TO CONTROL FOR TRACES HEIGHT, WIDTH '''


    def __init__(self, main, connector = "height", orient = Qt.Horizontal, minimum = 1, maximum = 8, interval = 0.1, value=5):
        
        super().__init__()
        
        self.main = main
        
        self.setOrientation(orient)
        self.setMinimum(minimum)
        self.setMaximum(maximum)
        self.setTickInterval(interval)
        self.setValue(value)
        
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    
        if connector == "height":
            self.valueChanged[int].connect(self.change_height)
        elif connector == "width": 
            self.valueChanged[int].connect(self.change_width)
        else:
            pass
    
    def change_height(self):
        
        xpos = self.main.plot.xpos
    
        # -- change the value of the peak height -- #
        self.main.plot.percent_max_height = self.value()
        
        # -- set range to display the graph -- #
        self.main.plot.setYRange(self.main.plot.ymin, (9 - self.main.plot.percent_max_height) * 1000)
        
    def change_width(self):
        
        self.main.plot.xwindow = self.value()
        self.main.plot.setXRange(self.main.plot.xpos, self.main.plot.xpos + self.main.plot.xwindow)
        
        
        pass
