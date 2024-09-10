#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 28 19:54:43 2024

@author: sebastien
"""
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class TraceParameters(QWidget):
    
    ''' Create a window to set traces options '''
    
    def __init__(self, main):
        
        super().__init__()
        
        self.main = main
        
        # set window dimensions
        self.setFixedHeight(100)
        self.setFixedWidth(200)
        
        # initialize slider
        self.height_slider = PeakHeight(self.main)
        self.width_slider = PeakWidth(self.main)
        
        self.create_layout()
        
    def create_layout(self):
        
        self.grid = QGridLayout(self)
        
        self.grid.addWidget(QLabel("Peak Height : "), 0,0)
        self.grid.addWidget(self.height_slider, 0,1)
        
        self.grid.addWidget(QLabel("Peak Width : "), 1,0)
        self.grid.addWidget(self.width_slider, 1,1)        
        
        self.setLayout(self.grid)
        
        
    def display_window(self):
        
        self.show()
        
        
class PeakHeight(QSlider):
    
    ''' CREATE A QSLIDER TO CONTROL FOR TRACES HEIGHT '''
    
    def __init__(self, main):
        
        super().__init__()
        
        self.main = main
        self.valueChanged[int].connect(self.changeValue)
        
        self.setOrientation(Qt.Horizontal)
        self.setMinimum(1)
        self.setMaximum(10)
        self.setTickInterval(0.1)

    def changeValue(self):
        
        # change maximum value of y-axis (hidden on graph) to set the peak Height
        self.main.plot.percent_max_height = self.value()
        self.main.plot.setYRange(0, self.main.plot.percent_max_height * 1000)
        


class PeakWidth(QSlider):

    ''' CREATE A QSLIDER TO CONTROL PEAK WIDTH '''
    
    def __init__(self, main):
        
        super().__init__()
        
        self.main = main
        self.valueChanged[int].connect(self.changeValue)
        
        self.setOrientation(Qt.Horizontal)
        
        self.setMinimum(100)
        self.setMaximum(750)
        self.setTickInterval(10)
        
    def changeValue(self):
        
        self.main.plot.xwindow = self.value()
        self.main.plot.setXRange(self.main.plot.xpos, self.main.plot.xpos + self.main.plot.xwindow)