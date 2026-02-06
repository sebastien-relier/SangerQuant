#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 12:42:39 2025

@author: sebastien
"""



from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
import re

class SearchSequence(QLineEdit):
    
    ''' Search the sequence from Trace '''
    
    def __init__(self, main):
    
        super().__init__()
        
        self.main = main
        
        self.setPlaceholderText("Search sequence")
        self._create_validator()
        
        self.textChanged.connect(self.onChange)
    
    def _create_validator(self):
        
        # -- allow the input of G,A,T,C only -- #
        
        regex = QRegExp("[GATCNgatcn]+")
        validator = QRegExpValidator(regex)
        self.setValidator(validator)

    def onChange(self):
        
        # -- update the plot to be at the sequence -- #
        
        
        cursor_pos = self.cursorPosition()    # Save the current cursor position
          
        self.setText(self.text().upper())     # Convert the text to uppercase
              
        self.setCursorPosition(cursor_pos)    # Convert the text to uppercase
        
        
        
        self.main.plot.subseq = self.text().replace("N",".")
        self.main.plot.go_to_subsequence()
        self.control_existence()
            
    def control_existence(self):
        
        pos = re.findall(self.main.plot.subseq, self.main.plot.seq)
        
        if len(pos) > 0:
                # -- change color of the text based on the existence of the sequence -- #    
            self.setStyleSheet("color:black")
        else:
            self.setStyleSheet("color:red")