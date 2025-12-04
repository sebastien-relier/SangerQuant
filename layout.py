#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 23:32:02 2025

@author: sebastien
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

class Layout(QWidget):
    
    ''' creates a QWidget to be set as a central widget of QMainWindow class in order to embed a grid inside '''
    
    def __init__(self):
        
        super().__init__()
        
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        
        