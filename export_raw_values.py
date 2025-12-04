#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  7 03:40:15 2025

@author: sebastien
"""


## IMPORT PACKAGES
from PyQt5.QtWidgets import QWidget, QRadioButton, QGridLayout, QListWidget,  QPushButton, QAbstractItemView, QLineEdit, QLabel, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from buttons import CancelButton
from quantification_table import PeakQuant
from export_to_csv import ExportToCsv
from qline import QHSeparationLine


class Exporter(QWidget):
    
    ''' create window to export the raw values '''
    
    def __init__(self, data):
        
        super().__init__(None, Qt.WindowStaysOnTopHint)

        self.data = data
        self.setWindowTitle("TraceQ - Export Raw Data")
        
        self.create_widgets()
        self.create_layout()        
        
    def create_widgets(self):
        
        self.cancel = CancelButton(self)
        self.export = ExportButton(self)
        self.samples = SampleList(self, items = [key for key in self.data])
        
        self.folderpath = ExportPath(self)
        self.selectpath = ChoosePath(self.folderpath)
        
        # -- select the file extension to be exported -- #
        self.extension = ExportPath(self)
        self.extension.setText("_peak.csv")
        
        # -- create QCheckBoxes to select the data to export -- #
        self.select_chromatogram = ExportDataType(self, data_type = "chromatogram", text = "Trace Channels")
        self.select_peak_infos = ExportDataType(self, data_type = "peak_height", text="Peak Infos", checked = True)
        
        self.preview_table = PeakQuant(self, header= ["Base","Phred",  "G","A","T","C"], nrow = 20, ncol=6)
        
    def create_layout(self):
        
        self.grid = QGridLayout()
        
        self.grid.addWidget(self.samples, 0,0,1,4)
        self.grid.addWidget(QHSeparationLine(), 1,0,1,4)
        
        # -- data options -- #
        self.grid.addWidget(QLabel("Select Data To Export"), 2,0,1,1)
        self.grid.addWidget(self.select_chromatogram, 3,0,1,1)
        self.grid.addWidget(self.select_peak_infos, 3,1,1,1)
        
        # -- export options -- #
        self.grid.addWidget(QLabel("Manage Export "), 5,0,1,1)
        self.grid.addWidget(QLabel("Export path : "), 6,0,1,1)
        self.grid.addWidget(self.folderpath, 6,1,1,1)
        self.grid.addWidget(self.selectpath, 6,2,1,1)
        
        self.grid.addWidget(QHSeparationLine(), 4,0,1,4)
        
        self.grid.addWidget(QLabel("File extension : "), 7,0,1,1)
        self.grid.addWidget(self.extension, 7,1,1,1)
        
        self.grid.addWidget(self.preview_table, 0,4,10,10)
        self.grid.addWidget(self.cancel, 11,12)
        self.grid.addWidget(self.export,11,13)
        
        self.grid.setColumnStretch(10, 1)
        self.setLayout(self.grid)



class ExportButton(QPushButton):

    ''' create a QPushButton to export the table '''
    
    def __init__(self, window):
        
        super().__init__()
    
        self.setText("Export")
        self.setIcon(QIcon(":/icons/export2.png"))
        self.window = window
        self.clicked.connect(self.export_table)

    def export_table(self):
        
        exporter = ExportToCsv()
        for item in self.window.samples.selectedItems():
            
            txt = item.text()
            txt = txt.replace(".ab1", self.window.export_extension)
            
            exporter.export_to_csv(headers = self.window.preview_table.header, output_filename=txt, data = self.window.processed_results)


class ExportPath(QLineEdit):
    
    ''' print the export path '''

    def __init__(self, window):
        
        super().__init__()
        
        self.window = window
        

    def update_value(self):
        
        if self.window.select_chromatogram.isChecked():
            self.setText("_trace.csv")
        else:
            self.setText("_peak.csv")


class ChoosePath(QPushButton):
    
    ''' open QFileDialog to select for export path '''
    
    def __init__(self, folderpath):
        
        super().__init__()
        
        self.folderpath = folderpath
        self.clicked.connect(self.open_filedialog)
        self.setText("...")
        
        
    def open_filedialog(self):
        
        directory = QFileDialog.getExistingDirectory()
        
        self.folderpath.setText(directory)
    
    
class ExportDataType(QRadioButton):
    
    ''' create a QCheckBox to export data depending on their type '''

    def __init__(self, window, data_type = "Raw", text = None, checked = False): 
    
        super().__init__()
        
        self.setText(text)
        self.setChecked(checked)

        self.window = window
    
        self.clicked.connect(self.on_click)
    
    def on_click(self):
        
        self.window.samples.update_table()
        self.window.extension.update_value()


class SampleList(QListWidget):
    
    ''' create a QListWidget to select the sample to export the raw data from '''
    
    def __init__(self, window, items = None):
        
        super().__init__()
        
        self.window = window  
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
    
        
        self.addItems(items)
        self.clicked.connect(self.update_table)
        
    def update_table(self):
        
        # -- get current selection of data -- #
        item = self.currentItem().text()
        data = self.window.data[item]
        
        if self.window.select_chromatogram.isChecked():
            self.show_traces(data)
        else:
            self.show_peak_height(data)
        
        
    def show_peak_height(self, data):
        
        res = []
        for s,p,h, in zip(data["Seq"], data["Phred"], data["Height"]):
            
            tmp = data["Height"][h]
            res.append([s,p, tmp["G"], tmp["A"], tmp["T"], tmp["C"]])

        self.window.preview_table.rename_headers(["BaseCalled","Phred",  "G","A","T","C"])
        self.window.preview_table.reset_table_values()
        self.window.preview_table.update_table(res)            
            
        self.window.export_extension = "_height.csv"
        self.window.processed_results = res
        
    def show_traces(self, data):
        
        res = []
        trace = data["Traces"]
        
        for g,a,t,c in zip(trace["G"], trace["A"], trace["T"], trace["C"]):
            res.append([g,a,t,c])
            
        self.window.preview_table.rename_headers(["G","A","T","C"])
        self.window.preview_table.reset_table_values()
        self.window.preview_table.update_table(res)
            
        self.window.export_extension = "_trace.csv"
        self.window.processed_results = res
        
        
    
    
    



