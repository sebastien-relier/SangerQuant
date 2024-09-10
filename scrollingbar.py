#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 17:11:24 2022

@author: sebastien
"""

# LOAD THE PYTHON MODULES 
import sys 

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class ScrollBar(QScrollbar):
    
    def __init__(self, main):
        
        super().__init__()
    
    
        self.main = main
    
    
        ## CREATE THE SCROLLBAR
        self.setOrientation(Qt.Horizontal)
        self.sliderMoved.connect(self.slider)
    
        self.scrollbar.setMinimum(self.sanger.xmin)
        self.scrollbar.setMaximum(self.sanger.xmax)
        
    def slider(self):
        
        if self.scrollbar.value() >= self.sanger.xmax - self.sanger.limit:
            return
        else:

            self.sanger.figure.setXRange(self.scrollbar.value(), self.scrollbar.value() + self.sanger.limit)
            