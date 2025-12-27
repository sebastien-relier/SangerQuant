#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 30 23:09:31 2025

@author: sebastien
"""



from PyQt5.QtWidgets import QWidget, QFileDialog, QListWidget, QComboBox, QGridLayout, QAbstractItemView, QCheckBox, QPushButton,QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import pyqtgraph as pg
import pyqtgraph.exporters
from buttons import CancelButton, ExportButton, HelpButton
from qline import QHSeparationLine
from boxplot import Boxplot



class CompareQuality(QWidget):
    
    ''' Create the window to compare the quality of sanger peaks '''
    
    def __init__(self, data):
        
        super().__init__(None, Qt.WindowStaysOnTopHint)
        
        self.data = data
        
        # -- create window -- #
        self.create_widgets()
        self.create_layout()
        
        # -- create window title -- #
        self.setWindowTitle("SangerQuant - Sequence Quality Comparison")
        self.resize(600,400)
        
        
    def create_widgets(self):
        
        # -- choose samples to display -- #
        self.samples = SampleList(self)
        self.select_all_samples = SelectAll(self)
        
        # -- initialize plot parameters -- #
        self.nucleotide_selection = SelectNucleotide(self)
        
        # -- initialize plotter -- #
        self.plot = QualityPlot(self)
        
        # -- create export / cancel buttons -- #
        self.cancel_button = CancelButton(self)
        self.export_button = ExportButton(self.plot.plot_area) # pass plot area
        self.help_button = HelpButton("compare_quality")
        
    def create_layout(self):
        
        self.layout = QGridLayout()
    
        # -- add list widget of samples to layout -- #
        self.layout.addWidget(self.samples, 1, 0, 7, 2)
        self.layout.addWidget(self.select_all_samples, 8,0,1,2)
        
        self.layout.addWidget(QHSeparationLine(), 9,0,1,4)
        self.layout.addWidget(QLabel("Nucleotide"), 10,0,1,1)
        self.layout.addWidget(self.nucleotide_selection, 10,1,1,1)
        
        # -- add export / cancel buttons -- #
        self.layout.addWidget(self.help_button, 11,9,1,1)
        self.layout.addWidget(self.cancel_button, 11,10,1,1)
        self.layout.addWidget(self.export_button, 11,11,1,1)
        
        # -- add plot to layout -- #
        self.layout.addWidget(self.plot.plot_area, 1,2, 10,10)
        self.setLayout(self.layout)
        
        
class SelectNucleotide(QComboBox):
    
    ''' SELECT THE NUCLEOTIDE G,A,T,C OR ALL FOUR NUCLEOTIDE TO CHECK FOR PHRED SCORE '''
    
    def __init__(self, window):
        
        super().__init__()
        
        self.window = window
        self.addItems(["G","A","T","C", "All"])
        
        self.setCurrentText("All")
        
        # -- initialize nucleotide position to get -- #
        self.currentTextChanged.connect(self.on_combobox_changed)
    
    def on_combobox_changed(self):
    
        self.window.plot.create_plot()
    

class QualityPlot:
    
    ''' create the Phred Score Plot '''

    def __init__(self, window):
        
        super().__init__()
        
        self.window = window
        self.data = self.window.data.copy()
    
        self.initialize_plot_area()
       
        # -- init parameters -- #
        self.nucleotide_choice = "All" 
        self.create_plot()

    def initialize_plot_area(self):
        
        self.plot_area = pg.plot()
        self.plot_area.hideAxis("bottom")
        self.plot_area.setMenuEnabled(False)
    
        # -- hide autorange button -- #
        plot_item = self.plot_area.getPlotItem()
        plot_item.buttonsHidden = True
        
        self.plot_area.setYRange(0,80)
        self.plot_area.setMouseEnabled(x = False, y = False)
        
        self.plot_area.setLabel("left", "Phred Quality Score")

    def create_plot(self):
        
        self.plot_area.clear()
        
        # -- get current nucleotide -- #
        current_nuc = self.window.nucleotide_selection.currentText()
        
        # -- subset data to analyze the nucleotide only -- #
        nuc_pos = self.extract_phred_from_whole_seq(current_nuc)
        
        # -- rearrange data --  #
        res = {}
        for sample in self.window.samples.selected_samples:
            
            phred = self.window.data[sample]["Phred"]
            pos = nuc_pos[sample]
            
            res[sample] = [phred[i] for i in pos]
        
        boxplot = Boxplot(self.plot_area)
        boxplot.add_whisker(data = res)

    def change_graphic_setting(self):

        # -- change graphic frame -- #
        self.window.axes.spines['top'].set_visible(False)
        self.window.axes.spines['right'].set_visible(False)
        self.window.axes.spines['bottom'].set_visible(False)        

        # -- set labels -- #
        self.window.axes.tick_params(axis='both', which='major', labelsize=12)
        self.window.axes.set_ylim(0,70)
        
        # -- rename the y-axis -- #
        self.window.axes.set_ylabel("Quality score (Phred)", fontsize = 18)
                
    def extract_phred_from_whole_seq(self, nuc):
            
        res = {}
        for sample in self.window.samples.selected_samples:
         
            seq = self.window.data[sample]["Seq"]
            
            if nuc != "All":
                nuc_pos = [pos for pos, char in enumerate(seq) if char == nuc]
            else:
                nuc_pos = [pos for pos, char in enumerate(seq)]
                
            res[sample] = nuc_pos
            
        self.nuc_pos = res
        
        return res


class SelectAll(QCheckBox):
    
    ''' Checkbox to select all samples '''
    
    def __init__(self, window):
        
        super().__init__()

        self.window = window
        self.setText("Select all")
        self.setChecked(True)
    
        self.stateChanged.connect(self.manage_sample_selection)    
    
    def manage_sample_selection(self):
        
        if self.isChecked():
            self.window.samples.select_all_samples(True)
        else:
            self.window.samples.select_all_samples(False)
    
        self.window.plot.create_plot()

class SampleList(QListWidget):
    
    ''' Select the samples to compare '''
        
    def __init__(self, window):
        
        super().__init__()
        
        self.window = window
        
        # -- create settings -- #
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.itemClicked.connect(self.itemClicked_event)
        
        # -- add filenames to list -- #
        filenames = [x for x in list(self.window.data.keys())]
        self.addItems(filenames)
        self.select_all_samples(True)
    
    def itemClicked_event(self):
        
        # -- change selected samples -- #
        self.selected_samples = [item.text() for item in self.selectedItems()]
        
        # -- update status of the checkbox that control the selection of all sample -- #
        self.manage_checkbox_status()

        # -- recreate the plots -- #
        self.window.plot.create_plot()
        
    def select_all_samples(self, select):
        
        # -- select all items -- #
        self.selected_samples = []
        for index in range(self.count()):
            
            item = self.item(index)
            item.setSelected(select)
        
            self.selected_samples.append(item.text())
    
    def manage_checkbox_status(self):
        
        if len(self.selected_samples) < self.count():
            self.window.select_all_samples.setChecked(False)
        else:
            self.window.select_all_samples.setChecked(True)





        