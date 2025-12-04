#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 07:09:46 2024

@author: sebastien
"""


from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QGridLayout, QListWidget, QLineEdit, QSpinBox, QAbstractItemView, QFileDialog, QRadioButton, QMessageBox
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QIcon, QRegExpValidator

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import re
import math
from buttons import CancelButton, CreateLabel
from qline import QHSeparationLine


class ExportSVG(QWidget):
    
    ''' THIS CLASS CREATES THE WINDOW TO EXPORT THE SVG '''
    
    def __init__(self, main):
        
        super().__init__(None, Qt.WindowStaysOnTopHint)
        
        self.main = main
    
        self.setWindowTitle("TraceQ - Batch Export of Selected Subsequences")
        self.resize(600,400)
        
        self.create_widgets()
        self.creata_canvas()
        self.create_layout()    
        
        self.traceplotter = TracePlotter(self)
        
    def create_widgets(self):
        
        # -- create widgets -- #
        self.sample_list = SampleList(self.main.data)
        self.target_sequence = SequenceToExport()
        self.apply = ApplyButton(self)  # enter self and data
        self.export = ExportButton(self)
        self.cancel = CancelButton(self)
        
        # -- create RadioButton to select file format -- #
        self.png = SelectFileFormat(".png")
        self.svg = SelectFileFormat(".svg")
        self.svg.setChecked(True)
        self.jpg = SelectFileFormat(".jpg")
        self.tiff = SelectFileFormat(".tiff")
        
        # -- create option'''s to shortens or extend the sequence window -- #
        self.extend_selection = QLabel("Extra Peak : ", self)
        self.number_of_peak = TraceExtraLength(self)
    
        self.alert = Alert()
    
    def creata_canvas(self):
        # create canvas to store the plot
        
        self.fig, self.axes = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        
        self.axes.spines['top'].set_visible(False)
        self.axes.spines['right'].set_visible(False)
        self.axes.spines['bottom'].set_visible(False)
        self.axes.spines['left'].set_visible(False)
        
        self.axes.get_xaxis().set_ticks([])
        self.axes.get_yaxis().set_ticks([])
        
    def create_layout(self):
        
        # -- create grid layout -- #
        self.grid = QGridLayout()
        self.grid.addWidget(self.target_sequence, 0,0,1,12)
        self.grid.addWidget(self.sample_list, 1,0,9,4)
        
        self.grid.addWidget(QHSeparationLine(),10,0,1,4)
      
        # -- add widgets to set the options of the graphic -- #
        self.grid.addWidget(CreateLabel(text = "Traces options"), 11,0,1,4)
        self.grid.addWidget(CreateLabel(text = "Peak Number"), 12,0,1,1)
        self.grid.addWidget(self.number_of_peak, 12,1,1,3)
       
        self.grid.addWidget(self.cancel,13,9)
        self.grid.addWidget(self.apply,13,10)
        self.grid.addWidget(self.export,13,11)
        
        self.grid.addWidget(self.canvas, 1,4,12,8)
        self.setLayout(self.grid)


class SampleList(QListWidget):
    
    ''' THIS CLASS CREATES A QLISTWIDGET OF THE FILES TO ANALYZE '''
    
    def __init__(self, data):
        
        super().__init__()

        self.data = data
        
        # List widget parameters
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.add_sample()
        
  
    def add_sample(self):
        
        # this function add new filenames to the list
        
        filenames = [x for x in self.data.keys()]
        self.addItems(filenames)
    

class SequenceToExport(QLineEdit):
    
    ''' THIS CLASS CREATE THE QLINE EDIT WIDGET TO SELECT THE SEQUENCE TO QUANTIFY '''

    def __init__(self):
        
        super().__init__()
        
        self.create_validator()
        self.setPlaceholderText("Enter the sequence to export (ex : GCATGGCNGTCTT)")
        
    def create_validator(self):
        # restricts input to G,A,T,C
        
        regex = QRegExp("[GATCN(|)*]+")
        validator = QRegExpValidator(regex)
        self.setValidator(validator)
        


class TracePlotter:
    
    ''' creates the plot to export '''

    def __init__(self, window):
        
        super().__init__()
        
        self.window = window
        self.colors = {"G":"black", "T":"red", "A":"green","C":"blue"}
        
    def arrange_data(self):
        
        # -- extract samples to plot -- #
        samples = self.window.sample_list.selectedItems()
        
        # -- extract subsequence to plot -- #
        query_seq = self.window.target_sequence.text().replace("N",".")
        
        i = 0
        self.arranged_data = {}
        for s in samples:
        
            # -- extract sample names -- #
            item = s.text()
            
            # -- extract sample infos -- #
            seq = self.window.main.data[item]["Seq"]
            ploc = self.window.main.data[item]["Ploc"]
            traces = self.window.main.data[item]["Traces"]
            
            # -- get start and end position of the trace to export -- #
            limits, subseq = self.get_plot_limits(query_seq, seq, ploc)
         
            start, end = limits[0], limits[1]
            
            self.arranged_data[i] = {"Name":item,  "SubSequence":subseq, "Trace": traces, "Start":start, "End":end}
        
            i += 1
            
            
    def create_plot(self):
    
        # control that the input sequence meets the requirement (ie > 10 nt long, with a N for the target base)
        ctl = self.window.alert.control_input_sequence_requirement(sequence = self.window.target_sequence.text())
        if ctl == "FAILED":
            return
    
        # control for the sequence existence
       
    
        # -- arrange the data to create the plot -- #
        self.arrange_data()
        
    
        # -- subset the data -- #
        number_of_samples = len(self.arranged_data.keys())
        
        # determine number of row and columns to plot
        row, cols = self.get_smallest_grid(number_of_samples)
        self.window.fig, self.window.axes = plt.subplots(row, cols)
        
        
        # -- adapt the title fontsize based on size -- #
        fs = round(80 / number_of_samples,0)
        
        
        # -- create the plots -- #
        for i in range(number_of_samples):
            
            subset = self.arranged_data[i]
            
            trace, subseq, start, end = subset["Trace"], subset["SubSequence"], subset["Start"], subset["End"]
        
            if row == 1 and cols == 1:
                axes = self.window.axes
            
                for nuc, in trace.keys():
                    axes.plot(trace[nuc][start:end], color= self.colors[nuc])
                    axes.axis('off')
                    axes.set_title(subset["Name"], fontsize = fs)
            
            else:
                
                # -- flatten the ax for easier iteration
                axes = self.window.axes.flatten()
        
                for nuc in trace.keys():
                    axes[i].plot(trace[nuc][start:end], color = self.colors[nuc])
                    axes[i].axis('off')
                    axes[i].set_title(subset["Name"], fontsize = fs)
            
        # remove extra plot when number of samples cannot fit in a square
        modulo = (row * cols)%number_of_samples
        
        if modulo > 0 :
            
            plot_to_del = number_of_samples - modulo + 1
            
            for ax in axes[plot_to_del:]:
            
                ax.remove()
        
        
   
    def control_sequence_existence(self):
        
        samples = self.window.sample_list.selectedItems()
        for s in samples:
            
            item = s.text()
            
            subseq = self.window.target_sequence.text().replace("N",".")
            seq = self.window.main.data[item]["Seq"]
            
            
        
        
        
    def preview_plot(self):
            
        self.canvas = FigureCanvas(self.window.fig)
        self.canvas.draw()
        self.window.grid.addWidget(self.canvas, 1,4,12,8)         
        
    def get_smallest_grid(self, n):
        # design the grid shape for the preview
        
        # Calculate the square root of n
        sqrt_n = math.sqrt(n)
    
        # Find the smallest integer m such that m * (m + 1) >= n
        m = math.floor(sqrt_n)
    
        # Check if m * m is enough to hold n graphs
        if m * m >= n:
            rows = m
            cols = m
        else:
            # Otherwise, use m rows and ceil(n / m) columns
            rows = m
            cols = math.ceil(n / m)
    
        return rows, cols
    
    def get_plot_limits(self, subseq, full_sequence, ploc):
    
        m = re.search(subseq, full_sequence)
        target_pos = subseq.find(".")
        ploc = list(ploc)
        
        if m is not None:
            # -- calculate the pos of the peak to quantify -- #
            left = int(m.span()[0]) + target_pos
            right = int(m.span()[1]) - target_pos + 1
        
            limits = [ploc[left - 1 - self.window.number_of_peak.value()], ploc[right + self.window.number_of_peak.value()]]

            return limits, m[0]
        else:
            
            self.window.alert.sequence_not_found(samples)

class TraceExtraLength(QSpinBox):
    
    ''' create QSpinBox to increase the spanning sequence surrounding the trace '''
    
    def __init__(self, window):
        
        super().__init__()
        
        self.window = window
        self.setValue(2)
        
        self.setMinimum(0)
        self.setMaximum(10)
        

class SelectFileFormat(QRadioButton):
    
    '''  QRadioButton to select the file format of export between png, jpg, tiff and svg '''

    def __init__(self, text):
        
        super().__init__()
    
        self.setText(text)


class ApplyButton(QPushButton):
    
    ''' THIS CLASS CREATES THE FIGURE TO APPLY THE SEQUENCE SEARCH AND PREVIEW THE GRAPH '''

    def __init__(self, window):
        
        super().__init__()
        
        self.window = window 
        
        self.setText("Preview")
        self.setIcon(QIcon(":/icons/preview.png"))
        self.clicked.connect(self.create_preview_plot)
    
    def create_preview_plot(self):
        
        self.window.traceplotter.create_plot()
        self.window.traceplotter.preview_plot()
       
        
class ExportButton(QPushButton):
    
    ''' THIS CLASS CREATE THE EXPORT BUTTON TO EXPORT THE SUBSET SEQUENCE IN SVG FORMAT '''
    
    def __init__(self, window):
        
        super().__init__()
        self.setText("Export")
        self.setIcon(QIcon(":/icons/export2.png"))
        
        self.window = window
        self.clicked.connect(self.export_svg)
    
    def export_svg(self):
        
        # -- create the plot -- #
        self.window.traceplotter.create_plot()
        self.window.traceplotter.preview_plot()
        
        # -- filedialog -- #
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Save as")
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)
        file_dialog.setNameFilter(".png;;.tiff;;.jpg;;.svg;;")

        if file_dialog.exec():
           selected_file = file_dialog.selectedFiles()[0]
           selected_filter = file_dialog.selectedNameFilter()
           
           plt.savefig(selected_file + selected_filter)
           
           

class Alert(QWidget):
    
    ''' create a class to show alerts when problem are arising '''
    
    def __init__(self):
        
        super().__init__(None, Qt.WindowStaysOnTopHint)
        
        # add sample whithout any sequence matching to be display in QPlainTextEdit
        self.sample_not_found = []
    
        self.msg = QMessageBox()
        self.wrong_sequence = self.create_alert(icon = QMessageBox.Critical, title = "Error ! Wrong input sequence", text = """The input sequence is missing critical informations:\n - Sequence must contain a letter N at a given position\n- Sequence can't be shorter than 10 nucleotides\n\n Example: GCATGGCNGTTCTT""")
     
        
    def display_window(self, title):
        
        self.setWindowTitle(title)
        self.show()
    
    
    def control_input_sequence_requirement(self, sequence):
         
        # -- check for sequence -- #
        if sequence.find("N") == -1:
            self.wrong_sequence.show()
            return "FAILED"
        elif len(sequence) < 10:
            
            return "FAILED"
        else:
           pass
        
    def create_alert(self, icon = None, title= None, text = None):
        
        self.msg.setIcon(icon)
        self.msg.setWindowTitle(title)
        self.msg.setText(text)
        return self.msg
    
    def sequence_not_found(self, samples):
        pass


          