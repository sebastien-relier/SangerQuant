#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 18:33:40 2022

@author: sebastien
"""

from PyQt5.QtWidgets import QListWidget, QAbstractItemView


class SampleList(QListWidget):
    
    '''
    This class creates the qlist widget that contain the loaded sample
    * Multi-selection is not allowed
    * Select sample on click and update the sanger traces from QMainWindow
    * resides in the QMainWindow
    '''

    def __init__(self, main):
        
        super().__init__(parent = main)

        self.main = main
        
        # -- add the samples to the ListWidget -- #
        filenames = [x for x in self.main.data.keys()]
        self.addItems(filenames)
        
        # List widget parameters
        self.itemClicked.connect(self.itemClicked_event)
        
    def initialize_plot(self):
        
        # -- extract all samples from data -- #
        self.selected_index = self.currentRow()
        self.selected_sample = list(self.main.data.keys())[self.selected_index]
        
        self.pass_data_to_traceplot(self.selected_sample)
        self.create_plot()
        
    def itemClicked_event(self, item):
    
        self.selected_sample = item.text()
        self.update_plot(self.selected_sample)
        
        
    def update_plot(self, item):
        # helper function
    
        # -- select data to plot -- #
        self.pass_data_to_traceplot(item)
       
        # -- create the new plot corresponding to the selected sample --#
        self.create_plot()
        
        # -- reset the values of quantification table -- #
        self.main.quantification.reset_table_values()
        
    def create_plot(self):
        
        self.main.plot.create_plot()
            
        # -- create the scrollbar to navigate the chromatogram --#
        self.main.scrollbar.initialize_window()
        self.main.layout_container.grid.addWidget(self.main.scrollbar, 0,2,1,10)
        
  
    def pass_data_to_traceplot(self, sample):
      
       # -- update data -- #
       self.main.plot.trace = self.main.data[sample]["Traces"]
       self.main.plot.ploc = self.main.data[sample]["Ploc"]
       self.main.plot.seq = self.main.data[sample]["Seq"]
       self.main.plot.height = self.main.data[sample]["Height"]
       self.main.plot.area = self.main.data[sample]["Area"]
       self.main.plot.phred = self.main.data[sample]["Phred"]
       
       self.main.plot.xmax = len(self.main.plot.trace["G"])
       
  
        
    
       
    
      
            


       
      
        