#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 19:17:49 2022

@author: sebastien
"""

from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtWidgets import QWidget, QGridLayout, QRadioButton, QLabel, QLineEdit, QPushButton, QListWidget, QPlainTextEdit, QTextEdit, QSizePolicy, QFileDialog
from PyQt5.QtGui import QRegExpValidator, QIcon, QColor, QTextCursor, QTextCharFormat
from Bio.Seq import Seq
from buttons import CancelButton


class ViewSequence(QWidget):
    
    ''' CREATES A WINDOW AND PRINT THE NUCLEOTIDE SEQUENCE IN FASTA FORMAT '''
    
    def __init__(self, main):
        
        super().__init__(None, Qt.WindowStaysOnTopHint)
        
        self.main = main
        
        # -- WINDOW SETTINGS -- #
        self.setWindowTitle("View Sequences")
        self.resize(800, 600)
       
        # -- create widgets -- # order must be kept
        self.create_textbox()
        self.create_widgets()
        self.selected_frame = self.frame1
        self.create_sample_list()
        
        self.create_layout()
        
    def create_widgets(self):
        
        # -- create labels -- #
        self.sample_label = CreateLabel("Samples")
        self.dna_label = CreateLabel("DNA sequence")
        self.protein_label = CreateLabel("Protein Sequence")
        
        self.matched_sequence = QuerySequence(self)
        self.query_sequence = QuerySequence(self)
        
        # -- creates cancel / export buttons -- #
        self.cancel = CancelButton(self)
        self.export_sequence = ExportButton(self, text = "Export")
        
        # -- create radiobuttons to determine the frame -- #
        self.frame1 = FrameButton(self, orf = 0)
        self.frame1.setChecked(True)
        
        self.frame2 = FrameButton(self, orf = 1)
        self.frame3 = FrameButton(self, orf = 2)
        
    def create_sample_list(self):
        
        # -- add filenames to list -- #
        filenames = [key for key in self.main.data]
        self.samples = SampleList(self, filenames)
        
        self.samples.setCurrentRow(self.main.samples.selected_index)
        self.samples.show_sequence(filenames[self.main.samples.selected_index])

    def create_textbox(self):
        
        self.dna_sequence = SequenceTextBox()
        self.protein_sequence = SequenceTextBox()
        
    def create_layout(self):
        
        # Create the layout
        self.layout = QGridLayout(self)
        self.layout.addWidget(self.sample_label, 0,0, 1, 1)
        self.layout.addWidget(self.samples,1,0,5,1)
        
        self.layout.addWidget(self.dna_label, 0,1, 1, 1)
        self.layout.addWidget(self.dna_sequence, 1,1, 5, 1)
        
        self.layout.addWidget(self.protein_label, 0,2, 1, 1)
        self.layout.addWidget(self.protein_sequence, 1,2,5,3)
        
        # -- frame selection -- #
        self.layout.addWidget(self.frame1, 1,7,1,1)
        self.layout.addWidget(self.frame2, 2,7,1,1)
        self.layout.addWidget(self.frame3, 3,7,1,1)
        
        self.layout.addWidget(self.query_sequence, 7,0,1,2)
        
        # -- button to cancel / export sequences -- #
        self.layout.addWidget(self.cancel, 7,2, 1,1)     
        self.layout.addWidget(self.export_sequence, 7,3,1,1)
        
        self.layout.setRowStretch(1, 1)
        self.setLayout(self.layout)
        
class CreateLabel(QLabel):

    def __init__(self, text):
        
        super().__init__()

        self.setText(text)

        self.setAlignment(Qt.AlignBottom)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

class FrameButton(QRadioButton):
    
    ''' creates radiobutton to change the frame of translation of the sequence '''
    
    def __init__(self, window, orf = 0):
        
        super().__init__()
        
        self.window = window
        self.frame = orf
        
        self.setText("frame {}".format(orf))
        self.clicked.connect(self.translate_dna_sequence)
        
    def translate_dna_sequence(self):
        
        # -- extract dna sequence -- #
        input_seq = self.window.dna_sequence.seq
        coding_dna = Seq(input_seq[self.frame:])
        
        # -- translate protein sequence -- #
        self.window.protein_sequence.add_seq_to_box(str(coding_dna.translate()))
        
        # -- update selected frame -- #
        self.window.selected_frame = self
        
class QuerySequence(QLineEdit):
    
    ''' QLineEdit TO ENTER THE QUERY SEQUENCE TO SEARCH'''
    
    def __init__(self, window):
        
        super().__init__()
        
        self.window = window
        self.setPlaceholderText("Search Query Sequence")
        
        # set validator (allow only GTAC to be entered)
        regex= QRegExp("[A-Za-z*]+")
        validator = QRegExpValidator(regex)
        self.setValidator(validator)

        # connect to function
        self.textChanged.connect(self.on_change)

    def on_change(self):
                
        text = self.text().upper()
        
        # -- color the text of the dna sequence found -- #
        self.window.dna_sequence.change_text_color(self.window.dna_sequence.seq, QColor("black"))
        self.window.dna_sequence.change_text_color(text, QColor("red"))
        
        # -- color the text of the protein sequence found -- #
        self.window.protein_sequence.change_text_color(self.window.protein_sequence.seq, QColor("black"))
        self.window.protein_sequence.change_text_color(text, QColor("green"))
        
        
class ExportButton(QPushButton):
    
    ''' create a QPushButton to export the sequence '''
    
    def __init__(self, window, text = "Export DNA"):
        
        super().__init__()
        
        self.window = window
        self.setText(text)
        self.setIcon(QIcon(":/icons/export2.png"))
        self.clicked.connect(self.export_sequence)

    def export_sequence(self):
        
        # -- filedialog -- #
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Save as")
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)
        file_dialog.setNameFilter(".fasta")

        if file_dialog.exec():
           selected_file = file_dialog.selectedFiles()[0]
           selected_filter = file_dialog.selectedNameFilter()
           
           self.write_output(selected_file + selected_filter)
           
    def write_output(self, filename):
            # -- write dna -- #
           with open(filename, "w") as f:
               f.write(">" + self.window.samples.selected_sample + "\n")
               
               i = 0
               while i < len(self.window.dna_sequence.seq) - 60:
                   seq = self.window.dna_sequence.seq[i:i + 60]
                   f.write(seq + "\n")
                   
                   i += 60
                   
               f.write(self.window.dna_sequence.seq[i: len(self.window.dna_sequence.seq)])
 

class SampleList(QListWidget):
    
    ''' LIST OF SAMPLES TO SELECT '''
    
    def __init__(self, window, filenames):
        
        super().__init__()
        
        self.window = window
        self.addItems(filenames)
        
        # -- connect to click event -- #
        self.itemClicked.connect(self.itemClicked_event)
        
    def itemClicked_event(self, item):
        # change dna sequence and protein sequence based on sample values
        
        # get dna sequence from selected sample from list
        self.selected_sample = item.text()
        self.show_sequence(self.selected_sample)
        
    def show_sequence(self, sample):
        self.seq = self.window.main.data[sample]["Seq"]
       
        # -- change dna sequence -- #
        self.window.dna_sequence.add_seq_to_box(self.seq)
        
        # -- change protein sequence -- #
        self.window.selected_frame.translate_dna_sequence()
           
    
class SequenceTextBox(QTextEdit):
    
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
    
    
    
    
    