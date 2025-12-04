#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 29 18:18:11 2025

@author: sebastien
"""

from PyQt5.QtWidgets import QPushButton, QSlider, QSizePolicy, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *


class CancelButton(QPushButton):
        
    ''' CREATE THE BUTTON TO CANCEL THE WINDOW '''
    
    def __init__(self, window, text = "Cancel"):
        
        super().__init__()

        self.window = window

        self.setText(text)
        self.setIcon(QIcon(":/icons/cancel.png"))
        self.clicked.connect(self.on_click)
    
    def on_click(self):
        
        self.window.close()
        
        
class PreviewButton(QPushButton):

    ''' CREATE THE BUTTON TO PREVIEW THE DATA INTO A QTABLEWIDGET '''
    
    def __init__(self, window):
    
        super().__init__()
        
        self.window = window
        
        self.setText("Preview")
        self.setIcon(QIcon(":/icons/view.png"))
        
        
        
        

class HelpButton(QPushButton):
    
    ''' CREATE A BUTTON TO GET HELP '''
    
    def __init__(self, image):
        
        super().__init__()
        
        self.image = image
        
        self.setText("Help")
        self.setIcon(QIcon("help_icon.png"))
        self.clicked.connect(self.display_help)
        
    def display_help(self):
        
        pass


class CreateLabel(QLabel):
    
    
    ''' Create a QLabel to describe '''
    
    def __init__(self, text = None):
        
        super().__init__()
        
        self.setText(text)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        





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




