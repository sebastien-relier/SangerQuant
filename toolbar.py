#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 19:43:13 2022

@author: sebastien
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class ToolBar(QToolBar):
    
    ''' THIS CLASS CREATES THE TOOLBAR OF THE MAIN WINDOW '''
    
    def __init__(self, window):
        
        super().__init__(parent = window)
        
        self.window = window
        
        # CREATE ACTIONS
        save = QAction(QIcon("save.png"), "save",self)
        open_file = QAction("open", self)
        close = QAction(QIcon("exit.png"),"exit",self)
        
        copy = QAction("copy",self)
        
        blast = QAction(QIcon("blast-logo.jpg"),"blast",self)
        
        search_icon = QAction(QIcon("search.png"), "", self)
        search = SearchSequence(window)
       
        # ZOOM-IN
        zoom_in = QAction(QIcon("zoom_in.png"), "zoom", self)
        zoom_out = QAction(QIcon("zoom_out.png"), "zoom",self)
        
        
        # LINK TO FUNCTIONS
        zoom_in.triggered.connect(self.zoom_in_fcn)
        close.triggered.connect(qApp.quit)

        # ADD ACTIONS
        self.addActions([save, close])
        self.addSeparator()
        self.addActions([copy])
        self.addSeparator()
      
        self.addSeparator()
        self.addAction(blast)
        
        self.addAction(search_icon)
        self.addWidget(search)
       
        
        
        window.addToolBar(self)
        
    
    def save(self):
        pass
    
    def open_f(self):
        pass
    
    
    def zoom_in_fcn(self):
        self.window.sanger.limit -= 50
        
        #self.window.sanger.ax.set_lim()
    
    def zoom_out_fcn(self):
        self.window.sanger.limit += 50
        
        
    


class SearchSequence(QLineEdit):
    
    ''' Search the sequence from Trace '''
    
    def __init__(self, main):
    
        super().__init__()
        
        self.main = main
        
        self.setPlaceholderText("Enter the sequence here")
        self.create_validator()
        
        self.textChanged.connect(self.onChange)
    
    def create_validator(self):
        # restricts input to G,A,T,C
        
        regex = QRegExp("[GATC]+")
        validator = QRegExpValidator(regex)
        self.setValidator(validator)

    def onChange(self):
        # actions when the sequence is changed
        
        self.main.plot.subseq = self.text()
        self.main.plot.go_to_subsequence()
        self.control_existence()
        
        
    def control_existence(self):
        # existence of sequence
        
        if (self.text() in self.main.plot.seq):
            self.setStyleSheet("color:black")
        else:
            self.setStyleSheet("color:red")
        
        
    
    
    



