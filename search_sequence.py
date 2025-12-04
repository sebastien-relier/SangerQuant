#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 12:42:39 2025

@author: sebastien
"""



from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator

class SearchSequence(QLineEdit):
    
    ''' Search the sequence from Trace '''
    
    def __init__(self, main):
    
        super().__init__()
        
        self.main = main
        
        self.setPlaceholderText("Enter the sequence here")
        self.create_validator()
        
        self.textChanged.connect(self.onChange)
    
    def create_validator(self):
        
        # -- allow the input of G,A,T,C only -- #
        
        regex = QRegExp("[GATCgatc]+")
        validator = QRegExpValidator(regex)
        self.setValidator(validator)

    def onChange(self):
        
        # -- update the plot to be at the sequence -- #
        self.setText(self.text().upper())
        self.main.plot.subseq = self.text()
        self.main.plot.go_to_subsequence()
        self.control_existence()
        
        
    def control_existence(self):
        
        # -- change color of the text based on the existence of the sequence -- #
        if (self.text() in self.main.plot.seq):
            self.setStyleSheet("color:black")
        else:
            self.setStyleSheet("color:red")