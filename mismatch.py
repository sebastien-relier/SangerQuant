#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 17 18:33:34 2024

@author: sebastien
"""

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *



class Mismatch(QWidget):
    
    ''' create a window to calculate mismatch '''
    
    def __init__(self, main):
        
        super().__init__() 
        
        
        # create window
        self.setWindowTitle("Quantify peaks of sanger traces")
        self.resize(800, 600)
        
        
        self.main = main
        
        
        
        
        
        self.samples = SamplesList(self.main)
        
        self.target = SelectSequence()
        
        self.create_layout()
    
    def create_layout(self):
        
        self.layout = QGridLayout(self)
        
        self.layout.addWidget(QLabel("Samples"), 0,0)
        self.layout.addWidget(self.target, 1,0)
        self.layout.addWidget(self.samples, 2,0)
        
        self.layout.setRowStretch(1,1)
        self.setLayout(self.layout)
        
        

class Calculate(QPushButton):
    
    ''' Create the button to calculate transition '''
    
    def __init__(self):
        
        super().__init__()
        
        self.click.connect(self.calculate_mismatch_rate)
        
    def calculate_mismatch_rate(self):
        
        pass
    
class Transition(QComboBox):
    
    ''' Create a Combobox box to calculate transition '''
    
    def __init__(self):
        
        super().__init__()
    
        pass


class SelectSequence(QLineEdit):
    
    ''' Create a QLineEdit to enter the sequence '''
    
    def __init__(self):
        
        super().__init__()
        
        # set validator (allow only GTAC to be entered)
        regex= QRegExp("[GTAC*.]+")
        validator = QRegExpValidator(regex)
        self.setValidator(validator)

    def get_target_sequence(self):
        
        return self.text




class SamplesList(QListWidget):
    
    ''' Create a list to contain samples '''

    def __init__(self, main):
        
        super().__init__()
        
        # List widget parameters
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        
        
        self.main = main
        
        
        # fill list with filenames
        filenames = [key for key in self.main.data]
        self.addItems(filenames)
        
        # connect to functions
        self.itemClicked.connect(self.itemClicked_event)
        
    def itemClicked_event(self):
        
        items = [x.text() for x in self.selectedItems()]
        
        print(items)
        
        
        
        pass