#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 27 12:42:39 2025

@author: sebastien
"""

from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
import re

class SearchSequence(QLineEdit):
    
    ''' 
    - Create a QLinEdit below the Sanger Trace:
    - The function of this QLineEdit is to search for a specific sequence within the sanger file
    - If the sequence is found, the plot is automatically updated to show the sequence
    '''
    
    def __init__(self, main):
    
        super().__init__()
        
        self.main = main
        
        self.setPlaceholderText("Search sequence")
        self._create_validator()
        
        self.textChanged.connect(self.onChange)
    
    def _create_validator(self):
        
        # -- allow the input of G,A,T,C only -- #
        
        regex = QRegularExpression("[GATCNgatcn]+")
        validator = QRegularExpressionValidator(regex)
        self.setValidator(validator)

    def onChange(self):
        ''' update text each time a letter is entered '''
        
        cursor_pos = self.cursorPosition()    # Save the current cursor position
          
        self.setText(self.text().upper())     # Convert the text to uppercase
              
        self.setCursorPosition(cursor_pos)    # Convert the text to uppercase
        
        
        
        self.main.plot.subseq = self.text().replace("N",".")
        self.main.plot.go_to_subsequence()
        self.control_existence()
            
    def control_existence(self):
        ''' color the input text in black or red depending on whether the queried sequence is found '''
        
        pos = re.findall(self.main.plot.subseq, self.main.plot.seq)
        
        if len(pos) > 0:
                # -- change color of the text based on the existence of the sequence -- #    
            self.setStyleSheet("color:black")
        else:
            self.setStyleSheet("color:red")