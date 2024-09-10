#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 07:09:46 2024

@author: sebastien
"""

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class ExportSVG(QWidget):
    
    ''' THIS CLASS CREATES THE WINDOW TO EXPORT THE SVG '''
    
    def __init__(self, main):
        
        super().__init__()
        
        self.main = main
    
        self.create_widgets()
        self.create_layout()    
        
    def create_widgets(self):
        
        self.sequence = SequenceToExport()
        self.apply = ApplyButton(self.main, self.sequence)
        self.export = ExportButton()
        self.cancel = CancelButton(self)
        self.canvas = Canvas()

    def create_layout(self):
        
        self.grid = QGridLayout()
        self.grid.addWidget(self.sequence, 0,0,1,0)
        self.grid.addWidget(self.canvas, 1,0,6,6)
        self.grid.addWidget(self.cancel,7,3)
        self.grid.addWidget(self.apply, 7,4)
        self.grid.addWidget(self.export,7,5)
        
        self.setLayout(self.grid)
        
class SequenceToExport(QLineEdit):
    
    ''' THIS CLASS CREATE THE QLINE EDIT WIDGET TO SELECT THE SEQUENCE TO QUANTIFY '''

    def __init__(self):
        
        super().__init__()
        
        self.create_validator()
        
    def create_validator(self):
        # restricts input to G,A,T,C
        
        regex = QRegExp("[GATCN(|)*]+")
        validator = QRegExpValidator(regex)
        self.setValidator(validator)
        
        
class ApplyButton(QPushButton):
    
    ''' THIS CLASS CREATE THE FIGURE TO APPLY THE SEQUENCE SEARCH AND PREVIEW THE GRAPH '''

    def __init__(self, main, sequence):
        
        super().__init__()
        
        self.setText("Apply")
        
        self.main = main
        self.sequence = sequence
        self.clicked.connect(self.create_preview_plot)
    
    

    def get_plot_limits(self, subseq, full_sequence):
    
        match = re.search(subseq, full_sequence)
    
    
        left = int(match.span()[0])
        right = int(match.span()[1])
        limits = [ploc[left - 1 - int(args.window)], ploc[right + 1 + int(args.window)]]
        return limits

    
    
    
    def create_preview_plot(self):
        
        subseq = self.sequence.text()
        
        for key in self.main.data:
            
            sequence = self.main.data[key]["Seq"]
            ploc = self.main.data[key]["Ploc"]
            traces = self.main.data[key]["Traces"]
            
            # start pos of subset
            startpos = sequence.find(subseq)
            endpos = startpos + len(sequence)
            
            for base in traces.keys():
                
                tmp = traces[base]
                
                plt.plot(tmp[startpos:endpos])
            
            plt.show()

            
        
            
    
class ExportButton(QPushButton):
    
    ''' THIS CLASS CREATE THE EXPORT BUTTON TO EXPORT THE SUBSET SEQUENCE IN SVG FORMAT '''
    
    def __init__(self):
        
        super().__init__()
        self.setText("Export")
        pass
    
    
class CancelButton(QPushButton):
    
    ''' THIS CLASS CREATE THE CANCEL BUTTON TO CANCEL THE EXPORT OF GRAPH TO SVG FILE FORMAT '''
    
    def __init__(self, window):
        
        super().__init__()
        self.setText("Cancel")
        
        self.window = window
        
        self.clicked.connect(self.close_window)
        
    def close_window(self):
        
        self.window.close()
        

        
class Canvas(FigureCanvas):
    
    ''' THIS CLASS CREATE THE FIGURE CANVAS TO EMBEDD THE PLOT PREVIEW BEFORE EXPORTING '''
    
    def __init__(self):
        
        super().__init__()
        
        pass
