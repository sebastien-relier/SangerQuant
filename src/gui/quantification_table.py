#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 17 16:58:41 2025

@author: sebastien
"""


## LOAD PACKAGES 

from PyQt6.QtGui import QFont, QBrush, QColor, QAction
from PyQt6.QtWidgets import QTableWidget, QPushButton, QComboBox, QCheckBox, QMenu,  QAbstractItemView, QHeaderView, QApplication, QTableWidgetItem,  QAbstractScrollArea
from PyQt6.QtCore import Qt

## CREATE TABLE TO STORE VALUES OF G A T C
class PeakQuant(QTableWidget):
    
    ''' CREATE QTABLEWIDGET TO STORE THE QUANTIFICATION '''
    
    
    def __init__(self, main, rowlabel = {}, header = ["Nucleotide", "Height"], nrow = 4, ncol = 2):
        
        super().__init__()
        
        self.main = main
        self.header = header
        self.rowlabel = rowlabel
        
        
        ## options
        self.show_ratio = ShowRatio(self)       # checkbox to determine if values displayed are raw or ratio
        self.nuc_reference = Reference(self)    # qcomboboc to determine the nucleotide of reference
        
        
        # -- set number of rows and columns -- #
        self.setRowCount(nrow)
        self.setColumnCount(ncol)
        
        # -- cancel editable feature of the qtablewidget -- #
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.setHorizontalHeaderLabels(header)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        
        # -- set the right click menu to copy to clipboard -- #
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
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
     
    
    
    def _transform_value(self, data = None):
        ''' convert raw data into ratio or not based on the selected options '''
        
        # CALCULATE RATIO TO REFERENCE IF QCHECKBOX IS CHECKED
        if self.show_ratio.isChecked() is True:
    
            # calculate sum of overlapping peak, G,A,T,C
            somme = [self.data[key] for key in self.data]
            somme = sum(somme)
                            
            # calculate the ratio
            res = []
            for key in self.data:
                
                value = self.data[key]
                ratio = value / somme * 100
                ratio = round(ratio, 2)
                
                tmp = [key, ratio]
                res.append(tmp)
            
            return res
        
        else:
            
            res = []
            for key in self.data:
                value = self.data[key]
            
                tmp = [key, value]
                res.append(tmp)
            
            return res
    
    def update_table(self):
        
        '''
        this method update the table from input data
        you can change ncol to fit required number of columns
        
        data structure must be list of list:
            [[sample_name, value1, value2], [sample_name2, value1, value2]]
        
        '''
        
        data = self._transform_value(self.data)
        
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
            
    
    def update_table_for_transition(self, data = None):
        
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
        ''' functon to show the context when right clicking on the table | allow to copy value into clipboard '''
         
        # -- create a context menu -- #
        contextMenu = QMenu(self)
        
        # Add a "Copy" action to the menu
        copyAction = QAction("Copy", self)
        copyAction.triggered.connect(self.copySelection)
        contextMenu.addAction(copyAction)
        
        # Show the context menu at the requested position
        contextMenu.exec(self.viewport().mapToGlobal(pos))

    def copySelection(self):
        ''' function to copy values from context menu into clipboard '''
         
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
 
    
class ShowRatio(QCheckBox):
    
    ''' Determine settings for PeakQuantification '''

    def __init__(self, window):
        
        super().__init__()
        
        self.window = window
        self.setText("Percentage ? | Reference:")
        
        self.stateChanged.connect(self._on_click)
        
    def _on_click(self):
        ''' activate | inactivate QComboBox of reference based on checkbox status'''
        
        self.window.update_table()
        self.window.create_row_label()
        
        
        if self.isChecked() is True:
            self.window.nuc_reference.setEnabled(False)
            self.window.rename_headers(["Nucleotide", "Height (%)"])
        else:
            self.window.nuc_reference.setEnabled(False)
            self.window.rename_headers(["Nucleotide", "Height"])
            

class Reference(QComboBox):
    
    ''' DETERMINE THE NUCLEOTIDE OF REFERENCE TO CALCULATE THE RATIO '''
    
    def __init__(self, window):
        
        super().__init__()

        self.window = window 
        self.setEnabled(False)
        
        items = ["All", "G", "A", "T", "C"]
        self.addItems(items)
        



                
                