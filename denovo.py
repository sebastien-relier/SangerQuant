#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 23:27:38 2025

@author: sebastien
"""

# TO DO LIST
# - Create the graph area for the barplot
# - Create the 


# PACKAGES
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Bio.Align import MultipleSeqAlignment
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import pyqtgraph as pg


from buttons import CancelButton
from qline import QHSeparationLine, QVSeparationLine

class Denovo(QWidget):
    
    ''' THIS CLASS PERFORM DE NOVO IDENTIFICATION OF TRANSITION '''
    
    def __init__(self, main):
        
        super().__init__()
        
        self.main = main
        
        self.create_window()
        self.create_widgets()
        self.create_grid_layout()        
        
        
    def create_window(self):
        
        self.setWindowTitle("De novo identification of mismatch")
        self.setFixedSize(800,600)
        
        self.show()
        
    def create_widgets(self):
        
        # -- create qfilelist to sample -- # 
        self.samples = FileList(self)
        self.reference = Reference()
        
        
        # -- create QLabel -- #
        self.label_sample = QLabel("Select the sample")
        self.label_input =QLabel("Enter the input sequence")
        self.label_method = QLabel("Calculation method : ")
        self.label_thresold = QLabel("Mismatch Thresold : ")
        
        
        self.upload = UploadFasta(self)
        
        
        self.height = MethodCalc("Height")
        self.area = MethodCalc("Area")
        self.filter = FilterThresold()
        
        
        # -- create a button -- #
        self.export_button = ExportButton(self)
        self.preview_button = PreviewButton(self)
        self.cancel_button = CancelButton(self)
        
        
        self.mismatch_plot = MisMatchPlotter(self)
        
        #-- create canvas --#
        self.fig, self.axes = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        
    def create_grid_layout(self):
        
        self.grid = QGridLayout()
        
        # -- list widget to select samples to analyze -- #
        self.grid.addWidget(self.label_sample, 0,0)
        self.grid.addWidget(self.samples, 1, 0, 1, 4)
        
        self.grid.addWidget(QHSeparationLine(), 6, 0,1,4)
        
        
        
        
        # -- Add box to enter the sequence of reference -- #
        self.grid.addWidget(self.label_input,0,5,1,1)
        self.grid.addWidget(self.reference, 1,5,1,4)
        self.grid.addWidget(self.upload, 0,6,1,1)
        
         
        self.grid.addWidget(self.mismatch_plot, 1, 9, 3, 10)
         
         
         # -- Add options for the plots -- #
         
        self.grid.addWidget(self.label_method, 2,0)
        self.grid.addWidget(self.height, 2,1, 1, 1)
        self.grid.addWidget(self.area,2,2,1, 1)
        
        
        
        self.grid.addWidget(self.label_thresold, 3,0,1,1)
        self.grid.addWidget(self.filter, 3, 1,1,2)
        
        
        self.grid.addWidget(self.preview_button, 5,6)
        self.grid.addWidget(self.cancel_button, 5,6)
        
        self.setLayout(self.grid)
        
        
class FileList(QListWidget):
    
    ''' THIS CLASS CREATES THE QListWidget TO SELECT THE SAMPLES '''
    
    def __init__(self, window):
        
        super().__init__()

        # add sample names
        self.window = window
        self.addItems([key for key in self.window.main.data])
        
        # allow multiple selection
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.itemClicked.connect(self.itemClicked_event)
        
    def itemClicked_event(self):
        
        self.selected_samples = [item.text() for item in self.selectedItems()]
        
        self.window.mismatch_plot.create_barplot()
    
    

class Reference(QPlainTextEdit):
    
    ''' creates a QLineEdit to enter reference sequence '''

    def __init__(self):
        
        super().__init__()

        self.text_content = ""
        self.textChanged.connect(self.on_change)

    def on_change(self):
        
        self.text_content = self.toPlainText()
        
        
        

    
class MethodCalc(QRadioButton):
    
    ''' SELECT PEAK HEIGHT OR PEAK AREA FOR DE NOVO DISCOVERY OF CT TRANSITION '''

    def __init__(self, name):
        
        super().__init__()
        
        self.setText(name)
        
        pass


class FilterThresold(QDoubleSpinBox):
    
    ''' DETERMINE OF THRESOLD TO DISPLAY THE BAR '''


    def __init__(self):

        super().__init__()
        
        self.setRange(0,1)

        self.setValue(0.2)
        self.setSingleStep(0.1)
        pass        
    


class MisMatchPlotter(pg.PlotWidget):
    
    
    ''' arrange data and create the plot to represent mismatch per sequence '''
    
    def __init__(self, window):
        
        super().__init__()

        self.window = window
        
        


    def create_barplot(self):
        
        sample = self.window.samples.selected_samples[0]
    
        data = self.window.main.data[sample]["Height"]
        
        for key in data:
                
            print(data[key])
        
        
        
        pass






class PreviewButton(QPushButton):
    
    ''' create a QpushButton to display the graphic on the canvas '''
    
    def __init__(self, window):
        
        super().__init__()

        self.setText("Preview")
        self.setIcon(QIcon("view.png"))
        
        self.window = window 
        
        self.clicked.connect(self.create_preview_plot)
     
     
    def create_preview_plot(self):
        
        # get data and selected sample
        data = self.window.main.data.copy()
        selected_samples = self.window.samples.selected_samples
        
        
        # -- get sequence of reference -- #
        refseq = self.window.reference.text_content
        
        
        # -- create alignment with Biopython -- #
        for sample in selected_samples:
            
            sequence = data[sample]["Seq"]
            
            
            
            
            
        print(align)
            
            
            
            
            # align target sequence with reference sequence (refseq)
            
            
            
            
            
            
            
        # -- get sequence -- #
        
        
        
        # add canvas to grid
        self.window.grid.addWidget(self.window.canvas, 1, 10, 5, 6)
        self.window.grid.addWidget
        
        pass

    def control_sequence(self, reference, target):
        
        print(refseq, target)
    
             
         

class ExportButton(QPushButton):
    
    ''' THIS CLASS CREATE THE EXPORT BUTTON TO EXPORT THE SUBSET SEQUENCE IN SVG FORMAT '''
    
    def __init__(self, window):
        
        super().__init__()
        self.setText("Export")
        self.setIcon(QIcon("export.png"))
        
        self.window = window
        
        self.clicked.connect(self.export_svg)
        
    def export_svg(self):
        pass

    

class UploadFasta(QPushButton):
    
    ''' creates a QPushButton to load the fasta sequence '''

    def __init__(self, window):
        
        super().__init__()

        self.window = window
        self.clicked.connect(self.open_file_dialog)

    def open_file_dialog(self):
        
        filename, _ = QFileDialog.getOpenFileName(self,"Open File","", "All Files (*);;Fasta files (*.fa *.fasta *.fai)")
    
        f = open(filename)
        
        self.pass_sequence_to_textbox(f)
        
    def extract_sequence(self, input_file):
        
        # create sequence
        seq = [l for l in input_file.readlines() if not l.startswith('>')]
        seq = seq[0].strip("\n")
        
        self.window.reference.text_content = seq
        
    def pass_sequence_to_textbox(self, input_file):
        
        self.window.reference.setPlainText(input_file.read())
        pass
        
        


        