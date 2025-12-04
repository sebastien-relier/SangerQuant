#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 20 17:00:51 2025

@author: sebastien
"""



from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Bio import pairwise2
from Bio.Seq import Seq


import pyqtgraph as pg
import re
import regex





class ConcatenateWindow(QWidget):
    
    ''' Concatenate several sequences to form a new one '''
    
    def __init__(self, main):
        
        super().__init__()
        
        self.main = main        
        
        
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):
        
        self.sample_list = SampleList(self.main.data) 
        self.concatenate_button = ConcatenateButton(self)
        
        self.seed_seq = SeedSequence()
    
    
        # -- create QPushButton -- #
        self.execute = ConcatenateButton(self)
    
    def create_layout(self):
        
        self.grid = QGridLayout()
        self.grid.addWidget(self.sample_list, 0,0,1,2)
        self.grid.addWidget(self.seed_seq, 1,0)
        self.grid.addWidget(self.concatenate_button, 2,0)
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
    
    
    
class ConcatenatePlot(pg.PlotWidget):
    
    ''' THIS CLASS CREATE THE PSEUDO-ALIGNMENT PLOT TO CONCATENATE SEQUENCES '''
    
    def __init__(self, window):
        
        super().__init__()
        
        self.window = window
        
        
    def create_plot(self):

        for sample in self.window.samples.selected_samples:
            
            pass
        
    
        pass
    

class SeedSequence(QLineEdit):
    
    ''' enter the seed seauence to perform concatenation '''
    
    def __init__(self):
        
        super().__init__()

        pass
    
    
class AddSeedSequence(QPushButton):
    
    ''' QPushButton to add the seed sequence to concatenate from '''

    def __init__(self, window):
        
        super().__init__()
        
        self.clicked.connect(self.add_see_sequence)
        
    def add_seed_sequence(self):
        
        pass






class ConcatenateButton(QPushButton):
    
    ''' THIS CLASS CONCATENATE SEVERAL SEQUENCES INTO ONE '''

    def __init__(self, window):
        
        super().__init__()
        
        self.window = window
        
        self.setText("Concatenate")
        self.clicked.connect(self.concatenate)
        
        
    def concatenate(self):
        
        # -- extract samples -- #
        selected_samples = [item.text() for item in self.window.sample_list.selectedItems()]
        seqs = [self.window.main.data[s]["Seq"] for s in selected_samples]
    
    
        t = 0
        for i in seqs:
            
            subset = ""
            for j in seqs[t:]:
                
                if i == j:
                    continue
                
                r = self.longest_common_substring(i, j)
                    
                pos_i, pos_j =  i.find(r), j.find(r)
                
                if pos_i < pos_j:
                    subset = i[0:pos_i] + j[0:]
                    
                elif pos_i > pos_j:
                    subset = j[0:pos_j] + i[0:]
                    
                else:
                    pass
                
                
                
                t += 0 
        print(subset)
    
    def longest_common_substring(self, s1, s2):
        
        m = [[0] * (1 + len(s2)) for _ in range(1 + len(s1))]
        longest, x_longest = 0, 0
    
        for x in range(1, 1 + len(s1)):
            
            for y in range(1, 1 + len(s2)):
                
                if s1[x - 1] == s2[y - 1]:
                    m[x][y] = m[x - 1][y - 1] + 1
                    
                    if m[x][y] > longest:
                        longest = m[x][y]
                        x_longest = x
                else:
                    m[x][y] = 0
    
        return s1[x_longest - longest: x_longest]
        
        

    def merge_sequence(self, overlap_seq):
        
        for key in overlap_seq:
 
            position = overlap_seq[key]["Position"]
            target = overlap_seq[key]["Target"]
            
            tmp_seq = self.window.main.data[key]["Seq"]
            
            tmp_seq2 = self.window.main.data[target]["Seq"]
            
            c = tmp_seq[:position] + tmp_seq2

    
                        
        
        
        
        
        
    