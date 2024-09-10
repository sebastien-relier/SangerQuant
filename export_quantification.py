#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 05:30:28 2024

@author: sebastien
"""


from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *





class ExportQuantification(QWidget):
    
    ''' THIS CLASS CREATES THE WINDOW TO EXPORT THE QUANTIFICATION '''
    
    def __init__(self, main):
        
        super().__init__()
        
        # Import data
        self.main = main
        
        
        # Init values
        
        
    
        self.create_widgets()
        self.create_layout()
        
    
        self.show()        
    
    def create_widgets(self):
        
        # create list of sample
        self.sample_list = FileList([key for key in self.main.data])
        
        self.basetoquant = FindBaseToQuantify()
        
        # create combobox to choose canonical base
        self.canonical = SelectCanonical() 
        
        # create combobox to choose non-canonical base
        self.noncanonical = SelectNonCanonical()
        
        # create qline edit to enter the sequence to quantify
        self.to_quantify = SequenceToQuantify()
        
        # create calculate button
        
    def create_layout(self):
        
        self.layout = QGridLayout(self)
        
        self.layout.addWidget(self.basetoquant,0,0,1,6)
        
        self.layout.addWidget(self.sample_list, 1,0,6,1)
        self.layout.addWidget(self.canonical, 2,1)
        self.layout.addWidget(self.noncanonical,3,2)
        
        self.setLayout(self.layout)
        

class CalculateButton(QPushButton):
    
    ''' THIS CLASS CREATE THE BUTTON TO CALCULATE THE TRANSITION '''
    
    def __init__(self):
        
        super().__init__()
        
        self.click.connect(self.on_click)
        pass

    def on_click(self):
        
        pass



class FindBaseToQuantify(QLineEdit):
    
    ''' THIS CLASS CREATE THE QLINE EDIT WIDGET TO SELECT THE SEQUENCE TO QUANTIFY '''

    def __init__(self):
        
        super().__init__()
        
        self.create_validator()
        
    def create_validator(self):
        # restricts input to G,A,T,C
        
        regex = QRegExp("[GATCN(|)*]+")
        validator = QRegExpValidator(regex)
        self.setValidator(validator)

class Results(QTableWidget):
    
    ''' THIS CLASS CREATES THE QTABLE WIDGET TO STORE THE RESULTS '''
    
    def __init__(self):
        
        super().__init__()
        
        pass



class FileList(QListWidget):
    
    ''' THIS CLASS CREATES THE QListWidget TO SELECT THE SAMPLES '''
    
    def __init__(self, samples):
        
        super().__init__()

        # add sample names
        self.addItems(samples)
        
        # allow multiple selection
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.itemClicked.connect(self.itemClicked_event)
        
    def itemClicked_event(self):
        pass
    
    
class SelectCanonical(QComboBox):
    
    ''' CREATES A QCOMBOBOX TO SELECT THE CANONICAL BASE TO CALCULATE MISMATCH '''
    
    def __init__(self):
        
        super().__init__()
        
        self.addItems(["G","A","T","C"])
        pass
    
class SelectNonCanonical(QComboBox):
    
    ''' CREATES A QCOMBOBOX TO SELECT THE NON CANONICAL BASE TO CALCULATE MISMATCH '''
    
    def __init__(self):
        
        super().__init__()
        
        self.addItems(["G","A","T","C","All"])
        pass

class SequenceToQuantify(QLineEdit):
    
    ''' CREATES A QLINEEDIT TO SELECT THE SEQUENCE AND THE BASE TO QUANTIFY '''
    
    def __init__(self):
        
        super().__init__()
        

        self.set_validator()
    
    def set_validator(self):
        # restricts input to G,A,T,C
        regex = QRegExp("[GATC]+")
        validator = QRegExpValidator(regex)
        self.setValidator(validator)