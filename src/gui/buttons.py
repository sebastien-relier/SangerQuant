#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 29 18:18:11 2025

@author: sebastien
"""

from PyQt5.QtWidgets import QPushButton, QSlider, QSizePolicy, QLabel, QFileDialog, QMessageBox, QLineEdit
from PyQt5.QtGui import QIcon, QRegExpValidator
from PyQt5.QtCore import Qt, QRegExp
import pyqtgraph as pg

class CancelButton(QPushButton):
        
    ''' CREATE THE BUTTON TO CANCEL THE WINDOW '''
    
    def __init__(self, window, text = "Cancel"):
        
        super().__init__()

        self.window = window

        self.setText(text)
        self.setIcon(QIcon(":/icons/cancel.png"))
        self.clicked.connect(self.on_click)
    
    def on_click(self):
        
        self.window.close()
        
class PreviewButton(QPushButton):

    ''' CREATE THE BUTTON TO PREVIEW THE DATA INTO A QTABLEWIDGET '''
    
    def __init__(self, window):
    
        super().__init__()
        
        self.window = window
        
        self.setText("Preview")
        self.setIcon(QIcon(":/icons/view.png"))
        

class ExportButton(QPushButton):
    
    ''' create a QPushButton to graphic from pyqtgraph '''
    
    def __init__(self, plot_area = None):
        
        super().__init__()
        
        self.plot_area = plot_area
        
        self.setIcon(QIcon("://icons/export2.png"))
        self.setText("Export")
        self.clicked.connect(self.export_graphic)
        
    def export_graphic(self):
        
        # QFileDialog
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Save as")
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)
        file_dialog.setNameFilter(".png;;.tiff;;.jpg;;.svg;;")
        
        if file_dialog.exec():
            selected_file = file_dialog.selectedFiles()[0]
            selected_filter = file_dialog.selectedNameFilter()
        
            exporter = pg.exporters.ImageExporter(self.plot_area.getPlotItem())
            exporter.parameters()['width'] = 640
            
            filename = "{}{}".format(selected_file, selected_filter)
            exporter.export(filename)
        
    def export_table(self):
        pass
        

class SettingButton(QPushButton):

    ''' create a QPushButton to open settings for graphic '''

    def __init__(self, setting_window=None):

        super().__init__()

        self.setText("Settings")
        self.setIcon(QIcon("://icons/settings.png"))
        self.setting_window = setting_window
        self.clicked.connect(self.open_window)
        
    def open_window(self):
        
        self.setting_window.show()
        
                
class HelpButton(QPushButton):
    
    ''' CREATE A BUTTON TO GET HELP '''
    
    def __init__(self, name = None):
        
        super().__init__()
        
        # dictionary of help
        self.help = {
    "align_sequence": {
        "title": "How to Align a Sequence",
        "text": 
"""
1. **Paste the reference sequence** in the designated input field.
2. **Left-click** on the Sanger sequence you want to align.
3. (Optional) Open **Settings** to adjust alignment parameters.
"""
    },

    "find_mismatch": {
        "title": "How to Find Mismatches in a Sequence",
        "text": 
"""
1. **Paste the reference sequence** in the bottom-left widget. \n
2. **Left-click** on the sample you want to analyze in the top-left widget.\n
3. Use the **mouse wheel** to zoom in or out of the plot. \n
4. **Left-click** on a bar in the plot to visualize the trace in the Main Window.
"""
    },

    "quantify_mismatch": {
        "title": "How to Quantify Mismatches",
        "text": 
"""
1. **Enter the subsequence** in the input field at the top. \n
2. Replace *G|A|T|C* with *N* at the position you want to quantify. \n
3. **Select one or more samples** from the list to quantify. \n
4. Use the combobox to select the mismatch type to calculate. \n
5. Click *Preview* to visualize the quantification table. \n
6. Click *export* to save the quantification table in .csv format
"""
    },

    "compare_quality": {
        "title": "How to Compare Sequence Quality",
        "text": 
"""
1. *Select* one or more samples from the list for quality comparisons. \n
2. Use combobox to select nucleotide type to compare quality. \n
3. Click *Export* to save the plot in your desired format
"""
    },

    "export_svg": {
        "title": "How to Select a Subsequence for Export",
        "text": 
"""
1. **Enter the subsequence** in the input field at the top.
2. Replace **G|A|T|C** with **N** at the position(s) of interest.
3. **Select one or more samples** from the list to visualize.
4. Use the **spinbox** to choose the number of peaks surrounding the peak of interest.
5. Click **Preview** to plot the subsequences.
6. Click **Export** to save the plot in your desired format.
"""
    },
    "trim": {
        "title": "How to trim sequence",
        "text":
"""
1. *Select* one or more samples from the list for quality comparisons. \n
2. Move the vertical red line to define the area to trim. \n
3. Click *Trim* to trim the selected sequences. \n
4. (Optional) Click *Untrim* to reinitialize the sequences \n
"""}
}

        
        
        self.title = self.help[name]["title"]
        self.text = self.help[name]["text"]
        
        self.setIcon(QIcon("://icons/help.png"))
        self.setText("Help")
        self.clicked.connect(self.display_help)
     
    def display_help(self):
        
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(self.title)
        msg.setText(self.text)
        
        msg.exec()


class LoadButton(QPushButton):
    
    ''' create a button to load the sequence in fasta format '''
    
    def __init__(self, text_container):
        
        super().__init__()
        
        self.setIcon(QIcon("://icons/load.png"))
        
        self.text_container = text_container
        self.clicked.connect(self.load_fasta_file)
    
    
    def load_fasta_file(self):
        pass



    
class CreateLabel(QLabel):
    
    
    ''' Create a QLabel to describe '''
    
    def __init__(self, text = None):
        
        super().__init__()
        
        self.setText(text)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        

class TraceShape(QSlider):
    
    ''' CREATE A QLSIDER TO CONTROL FOR TRACES HEIGHT, WIDTH '''


    def __init__(self, main, connector = "height", orient = Qt.Horizontal, minimum = 1, maximum = 8, interval = 0.1, value=5):
        
        super().__init__()
        
        self.main = main
        
        self.setOrientation(orient)
        self.setMinimum(minimum)
        self.setMaximum(maximum)
        self.setTickInterval(interval)
        self.setValue(value)
        
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    
        if connector == "height":
            self.valueChanged[int].connect(self.change_height)
        elif connector == "width": 
            self.valueChanged[int].connect(self.change_width)
        else:
            pass
    
    def change_height(self):
        
        xpos = self.main.plot.xpos
    
        # -- change the value of the peak height -- #
        self.main.plot.percent_max_height = self.value()
        
        # -- set range to display the graph -- #
        self.main.plot.setYRange(self.main.plot.ymin, (9 - self.main.plot.percent_max_height) * 1000)
        
    def change_width(self):
        
        self.main.plot.xwindow = self.value()
        self.main.plot.setXRange(self.main.plot.xpos, self.main.plot.xpos + self.main.plot.xwindow)
        
        
        pass


class EnterSequence(QLineEdit):
    
    ''' THIS CLASS CREATE THE QLINE EDIT WIDGET TO SELECT THE SEQUENCE TO QUANTIFY '''

    def __init__(self, placeholder = "Enter the sequence"):
        
        super().__init__()
        
        self.create_validator()
        self.setPlaceholderText("Enter the sequence to export (ex : GCATGGCNGTCTT)")
    
        self.textChanged.connect(self.on_change)
        
    def on_change(self):
        
        cursor_pos = self.cursorPosition()    # Save the current cursor position
          
        self.setText(self.text().upper())     # Convert the text to uppercase
              
        self.setCursorPosition(cursor_pos)    # Convert the text to uppercase
        
    def create_validator(self):
        # restricts input to G,A,T,C
        
        regex = QRegExp("[GATCNgatcn(|)*]+")
        validator = QRegExpValidator(regex)
        self.setValidator(validator)

