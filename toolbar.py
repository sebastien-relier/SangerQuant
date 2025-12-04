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
     
    
        # -- CREATE THE ACTIONS -- #
        self.save = QAction(QIcon("diskette.png"), "save",self)
        self.open_file = QAction(QIcon("open-folder.png"), "open", self)
        self.exit_action = QAction(QIcon("logout.png"),"exit",self)
        
       
        # create the actions of viewmenu
        self.view_metadata = QAction(QIcon("metadata.png"), "metadata", self)
        self.view_sequence = QAction(QIcon("dna.png"), "sequence", self)
        
       # create the trace menu
        self.fill = QAction(QIcon("peak_fill.png"), "fill", self)
        self.shape = QAction(QIcon("peak_shape.png"), "shape", self)
        
        self.blast = QAction(QIcon("blast-logo.jpg"),"blast",self)
        
        self.search_icon = QAction(QIcon("search.png"), "", self)
        self.search = SearchSequence(window)
       
        # ZOOM-IN
        zoom_in = QAction(QIcon("zoom_in.png"), "zoom", self)
        zoom_out = QAction(QIcon("zoom_out.png"), "zoom",self)
        
        
        # LINK TO FUNCTION
        self.exit_action.triggered.connect(qApp.quit)
        #self.view_sequence.triggered.connect(self.view_sequence)

        # ADD ACTIONS
        self.organize_toolbar()
        
    def organize_toolbar(self):
        
        # actions from file menu
        self.addActions([self.open_file, self.save, self.exit_action])
        self.addSeparator()
    
        # action from view menu    
        self.addAction(self.view_metadata)
        self.addAction(self.view_sequence)
        
        self.addSeparator()
        
        self.addAction(self.fill)
        self.addAction(self.shape)
        
        self.addSeparator()
        
        self.addAction(self.blast)
        
        self.addAction(self.search_icon)
        self.addWidget(self.search)
       
        
        
        self.window.addToolBar(self)
        
    
    def save(self):
        pass
    
    def open_f(self):
        pass
    
    
    def zoom_in_fcn(self):
        self.window.sanger.limit -= 50
        
        #self.window.sanger.ax.set_lim()
    
    def zoom_out_fcn(self):
        self.window.sanger.limit += 50
        
        
    def view_sequence(self):
        pass
    


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
        
        self.main.plot.subseq = self.text()
        self.main.plot.go_to_subsequence()
        self.control_existence()
        
        
    def control_existence(self):
        
        # -- change color of the text based on the existence of the sequence -- #
        
        if (self.text() in self.main.plot.seq):
            self.setStyleSheet("color:black")
            
            
        else:
            self.setStyleSheet("color:red")
        
        
    
    
    



