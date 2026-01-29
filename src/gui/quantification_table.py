#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 16:58:41 2025

@author: sebastien
"""


## LOAD PACKAGES 

from PyQt5.QtGui import QFont, QBrush, QColor
from PyQt5.QtWidgets import QTableWidget, QPushButton, QMenu, QAction, QAbstractItemView, QHeaderView, QApplication, QTableWidgetItem,  QAbstractScrollArea
from PyQt5.QtCore import *

## CREATE TABLE TO STORE VALUES OF G A T C
class PeakQuant(QTableWidget):
    
    ''' CREATE QTABLEWIDGET TO STORE THE QUANTIFICATION '''
    
    
    def __init__(self, main, rowlabel = {}, header = ["Nucleotide", "Height"], nrow = 4, ncol = 2):
        
        super().__init__()
        
        self.main = main
        self.header = header
        self.rowlabel = rowlabel
        
        
        # -- set number of rows and columns -- #
        self.setRowCount(nrow)
        self.setColumnCount(ncol)
        
        # -- cancel editable feature of the qtablewidget -- #
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setHorizontalHeaderLabels(header)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        
        
        
        # -- set the right click menu to copy to clipboard -- #
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)
        
    
    def create_row_label(self):
        # create the GATC labels on the quantification table
        
        # -- create a font -- #
        font = QFont()
        font.setBold(True)
        
        # -- add row label to the QTable if required -- #
        i = 0
        for key,value in self.rowlabel.items():
            
            tmp = QTableWidgetItem(key)   
            tmp.setForeground(QBrush(QColor(value)))
            tmp.setFont(font)
            
            self.setItem(i,0, tmp)
            
            i += 1
     
    def update_table(self, data = None):
        
        '''
        this method update the table from input data
        you can change ncol to fit required number of columns
        
        data structure must be list of list:
            [[sample_name, value1, value2], [sample_name2, value1, value2]]
        
        '''
        
        # set the number of row and the number columns based on the number of samples
        self.setRowCount(len(data))
        self.setColumnCount(len(data[0]))

       
        # add value per for each row then columns
        i = 0
        for row in data:
            
            j = 0
            for k in row:
                
                tmp = QTableWidgetItem(str(k))
                self.setItem(i, j, tmp)
            
                j += 1
            
            i += 1
    
    def reset_table_values(self):
        
        row, col = self.rowCount(), self.columnCount()
        
        for r in range(row):
            for c in range(col):
               
                self.setItem(r,c, None)
        
    
    def rename_headers(self, new_header):
        
        
        self.setColumnCount(len(new_header))
        
        self.header = new_header
        self.setHorizontalHeaderLabels(new_header)
    
    
    
    
    def showContextMenu(self, pos):
        
       # -- create a context menu -- #
       contextMenu = QMenu(self)

       # Add a "Copy" action to the menu
       copyAction = QAction("Copy", self)
       copyAction.triggered.connect(self.copySelection)
       contextMenu.addAction(copyAction)

       # Show the context menu at the requested position
       contextMenu.exec_(self.viewport().mapToGlobal(pos))

    def copySelection(self):
       # Get the selected items
       selected = self.selectedItems()

       if not selected:
           return

       # Sort the selected items by row and column
       selected.sort(key=lambda x: (x.row(), x.column()))

       # Create a string with the selected items
       text = ""
       prev_row = selected[0].row()
       
       # -- add header to text -- #
       for h in self.header:
           
           text += h + "\t"
       
       text += "\n"
       
       # -- add cell content to text -- #
       for item in selected:
          
           
           if item.row() != prev_row:
               text += "\n"
               prev_row = item.row()
           text += item.text() + "\t"

       # Remove the trailing tab character
       text = text.rstrip("\t")
       
       # Copy the text to the clipboard
       clipboard = QApplication.clipboard()
       clipboard.setText(text)
    
    
                
                
                