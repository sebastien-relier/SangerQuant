#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 19:17:49 2022

@author: sebastien
"""

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from filelist import ViewSequenceList
from Bio.Seq import Seq

class ViewSequence(QWidget):
    
    ''' CREATES A WINDOW AND PRINT THE NUCLEOTIDE SEQUENCE IN FASTA FORMAT '''
    
    def __init__(self, data):
        
        super().__init__()
        
        self.data = data
        
        
        # CREATE THE WINDOW
        self.setWindowTitle("Display Sequence from Sanger Traces")
        self.resize(800, 600)
        
        
        self.search = SeqFinder()
        self.search.textChanged.connect(self.onChange)
        
        self.close = QPushButton("Close", self)
        
        
        
        # create labels of lists and sequences
        self.create_sample_list()
        self.create_textbox()
        self.create_layout()
        
    def create_sample_list(self):
        
        # get list of filenames
        filenames = [key for key in self.data]
        
        self.samples = QListWidget()
        self.samples.addItems(filenames)
        
        self.samples.itemClicked.connect(self.itemClicked_event)
    
    def create_textbox(self):
        
        self.ds = DnaTextBox()
        self.ps = ProteinTextBox()
        
        self.found = QTextEdit("", self)
        
        
    def create_layout(self):
        
        # Create the layout
        self.layout = QGridLayout(self)
        self.layout.addWidget(QLabel("Samples"), 0,0)
        self.layout.addWidget(self.samples,1,0,5,1)
        
        self.layout.addWidget(QLabel("DNA Sequence"),0,1)
        self.layout.addWidget(self.ds, 1,1, 5, 1)
        
        self.layout.addWidget(QLabel("Protein Sequence"),0,2)
        self.layout.addWidget(self.ps, 1,2,5,1)
        self.layout.addWidget(self.found, 6,0,1,5)
        self.layout.addWidget(self.search, 7,0,1,3)
        self.layout.addWidget(self.close, 7,3, 1,2)        
        
        self.layout.setRowStretch(1, 1)
        self.setLayout(self.layout)
        
        
    def itemClicked_event(self, item):
        # change dna sequence and protein sequence based on sample values
        
       
        # get dna sequence from selected sample from list
        sample = item.text()
        self.seq = self.data[sample]["Seq"]
        
        # change dna sequence
        self.ds.add_seq_to_box(self.seq)
        
        # change protein sequence
        self.ps.translate_dna(self.seq)
        self.ps.add_seq_to_box()
        
        # get the current search sequence
        search = self.search.text()
        self.ds.change_text_color(search, QColor("blue"))

    def onChange(self, text):
   
        # connect from QLineEdit to search sequence
        self.search_in_all_sample(text)
        
        # color the text from the sequence match
        self.ds.add_seq_to_box(self.seq)
        self.ds.change_text_color(text, QColor("red"))
        
    def search_in_all_sample(self, text):
        
        # Match the sequence to search across samples and write in which sample it is found
        filenames = [key for key in self.data]
        
        # search for all sequences
        res = []
        for f in filenames:
            
            s = self.data[f]["Seq"]
            
            if s.find(text) == -1:
                continue
            else:
                res.append(f)
            
        # change text 
        if res == []:
            self.found.setPlainText("Sequence not found in any of the samples")
        elif len(res) == len(filenames):
            self.found.setPlainText("Sequence found in all samples")
        else:
            to_write = ["- " + r + "\n" for r in res]
            self.found.setPlainText("Sequence found in the following sample : {}".format(to_write))


class SeqFinder(QLineEdit):
    
    ''' Create QLineEdit and search for sequence'''
    
    def __init__(self):
        
        super().__init__()
        
        # set validator (allow only GTAC to be entered)
        regex= QRegExp("[GTAC]+")
        validator = QRegExpValidator(regex)
        self.setValidator(validator)

    






    
    
    
class ProteinTextBox(QPlainTextEdit):
    
    ''' CREATE QplainTextEdit to display protein sequence'''
    
    def __init__(self):
        
        super().__init__()
        #self.dnaseq = dna_sequence
        
        self.seq = ""
    
    def translate_dna(self, seq):
    
        txt = ""
        for i in range(3):
            coding_dna = Seq(seq[i:])
            txt = txt + "Frame {} \n  {} \n\n".format(i, str(coding_dna.translate()))
            
        self.seq = txt
        

    
    def add_seq_to_box(self):
        self.setPlainText(self.seq)
        pass
    
    
class DnaTextBox(QTextEdit):
    
    ''' CREATE QPlainTextEdit to display DNA sequence '''
    
    def __init__(self):
        
        super().__init__()
        
        self.seq = ""
        self.cursor = self.textCursor()
        
    def add_seq_to_box(self, seq):
        
        self.seq = seq
        self.setPlainText(self.seq)
    
    def change_text_color(self, target_string, color):
        

        ## find all occurences between target string and seq
        occ = [i for i in range(len(self.seq)) if self.seq.startswith(target_string, i)]
        
        
        # Get the current QTextCursor from QTextEdit
        self.cursor = self.textCursor()
        
        for o in occ:
            
            # Move the cursor to the beginning of the QTextEdit
            self.cursor.setPosition(o)
            self.cursor.setPosition(o + len(target_string), QTextCursor.KeepAnchor)
        
            # Create a QTextCharFormat instance
            char_format = QTextCharFormat()
    
            # Set the text color
            char_format.setForeground(color)
            
            self.cursor.mergeCharFormat(char_format)
        
        
     
    
    
        self.cursor.clearSelection()
    
    
    
    
    