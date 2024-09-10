#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 18:33:40 2022

@author: sebastien
"""

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt


class ViewSequenceList(QListWidget):
    
    def __init__(self, data):
        
        super().__init__()

        # get filenames from data dict
        filenames = [x for x in list(data.keys())]
        
        self.addItems(filenames)
        
        self.itemClicked.connect(self.itemClick_event)


    def itemClick_event(self):
        pass

    

class SampleList(QListWidget):
    
    ''' THIS CLASS CREATES A QLISTWIDGET OF THE FILES TO ANALYZE '''
    
    def __init__(self, main):
        
        super().__init__(parent = main)

        self.main = main
        
        # List widget parameters
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)


        self.itemClicked.connect(self.itemClicked_event)
        
        
    def itemClicked_event(self, item):
    
        # get all samples
        sample = item.text()
        
        # update data
        self.main.plot.trace = self.main.data[sample]["Traces"]
        self.main.plot.ploc = self.main.data[sample]["Ploc"]
        self.main.plot.seq = self.main.data[sample]["Seq"]
        self.main.plot.quant = self.main.data[sample]["Quant"]
        
        self.main.plot.xmax = len(self.main.plot.trace["DATA9"])
        
    
        self.p1 = self.main.plot.create_plot()
            
        self.scroll = ScrollBar(self.main)
        self.main.dock2.setWidget(self.scroll)
        
  
    def add_sample(self):
        
        # this function add new filenames to the list
        
        filenames = [x for x in self.main.data.keys()]
        self.addItems(filenames)
    
    
    def display_list(self):
        
        # this function displays the list on dock of the main window
        
        self.show()
        self.main.dock.setWidget(self)
        
        

class FileList(QListWidget):
    
    ''' THIS CLASS CREATES A QLISTWIDGET OF THE FILES TO ANALYZE '''
    
    def __init__(self, window, filenames):
        
        super().__init__(parent = window)
        
        self.window = window
        
        self.filepaths = filenames[0]
        
        self.filenames = [f.split("/")[-1] for f in filenames[0]]
        
        self.addItems(self.filenames)
        
        self.itemClicked.connect(self.itemClicked_event)
        return 
    
    
    
    def itemClicked_event(self, item):
    
        # when clicked on item list, plot new graphs and set title of current item
        self.window.sanger.data = item.text()
        
    
        # PLOT NEW GRAPHS 
        path = self.filepaths[self.currentRow()]
        
        self.window.sanger.read_ab1_file(path)
        self.window.sanger.create_plot()
        
        
        
        
class ScrollBar(QScrollBar):
    
    ''' CREATE THE SCROLLBAR TO SLIDE THE CHROMATOGRAM GRAPHS '''
    
    def __init__(self, sanger):
        
        super().__init__()
    
        self.sanger = sanger
    
        ## CREATE THE SCROLLBAR
        self.setOrientation(Qt.Horizontal)
        self.sliderMoved.connect(self.slider)
    
        
        self.setMinimum(0)
        self.setMaximum(self.sanger.plot.xmax - self.sanger.plot.xwindow)
        
    def slider(self):
        
        self.sanger.plot.xpos = self.value()
        
        
        if self.value() >=  self.sanger.plot.xmax - self.sanger.plot.xwindow:
            return
        else:

            self.sanger.plot.setXRange(self.sanger.plot.xpos, self.sanger.plot.xpos + self.sanger.plot.xwindow)
            
            



       
      
        