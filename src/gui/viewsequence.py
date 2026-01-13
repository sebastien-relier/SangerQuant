#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 19:17:49 2022

@author: sebastien
"""


from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtWidgets import QWidget, QGridLayout, QRadioButton, QLabel, QLineEdit, QPushButton, QListWidget, QTextEdit, QSizePolicy, QFileDialog, QListWidgetItem
from PyQt5.QtGui import QRegExpValidator, QIcon, QColor, QTextCursor, QTextCharFormat
from Bio.Seq import Seq
from buttons import CancelButton

class ViewSequence(QWidget):
    '''Creates a window to display and interact with nucleotide sequences in FASTA format.'''

    def __init__(self, main):
        super().__init__(None, Qt.WindowStaysOnTopHint)
        
        self.main = main

        self._setup_window()
        self._create_widgets()
        self._create_layout()

    def _setup_window(self):
        
        self.setWindowTitle("SangerQuant - View Sequences")
        self.resize(800, 600)

    def _create_widgets(self):
        
        self._create_labels()
        self._create_textboxes()
        self._create_buttons()
        self._create_sample_list()
        
        
    def _create_labels(self):
        self.sample_label = CreateLabel("Samples")
        self.dna_label = CreateLabel("DNA sequence")
        self.protein_label = CreateLabel("Protein Sequence")

    def _create_textboxes(self):
        self.dna_sequence = SequenceTextBox()
        self.protein_sequence = SequenceTextBox()

    def _create_buttons(self):
        self.cancel = CancelButton(self)
        self.export_sequence = ExportButton(self)

        self.frame1 = FrameButton(self, orf=0)
        self.frame1.setChecked(True)
        self.frame2 = FrameButton(self, orf=1)
        self.frame3 = FrameButton(self, orf=2)

        self.query_sequence = QuerySequence(self)
        self.selected_frame = self.frame1

    def _create_sample_list(self):
        filenames = list(self.main.data.keys())
        self.samples = SampleList(self, filenames)
        self.samples.setCurrentRow(self.main.samples.selected_index)
        self.samples.show_sequence(filenames[self.main.samples.selected_index])

    def _create_layout(self):
        layout = QGridLayout(self)

        # Labels
        layout.addWidget(self.sample_label, 0, 0, 1, 1)
        layout.addWidget(self.dna_label, 0, 1, 1, 1)
        layout.addWidget(self.protein_label, 0, 2, 1, 1)

        # Textboxes
        layout.addWidget(self.samples, 1, 0, 5, 1)
        layout.addWidget(self.dna_sequence, 1, 1, 5, 1)
        layout.addWidget(self.protein_sequence, 1, 2, 5, 3)

        # Frame selection
        layout.addWidget(self.frame1, 1, 7, 1, 1)
        layout.addWidget(self.frame2, 2, 7, 1, 1)
        layout.addWidget(self.frame3, 3, 7, 1, 1)

        # Query and buttons
        layout.addWidget(self.query_sequence, 7, 0, 1, 2)
        layout.addWidget(self.cancel, 7, 2, 1, 1)
        layout.addWidget(self.export_sequence, 7, 3, 1, 1)

        layout.setRowStretch(1, 1)
        self.setLayout(layout)
        
class CreateLabel(QLabel):
    '''Custom QLabel with bottom alignment and fixed size policy.'''

    def __init__(self, text: str):
        super().__init__()
        self.setText(text)
        self.setAlignment(Qt.AlignBottom)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)

class FrameButton(QRadioButton):
    '''Radio button to select the reading frame for translation.'''

    def __init__(self, window: ViewSequence, orf: int = 0):
        super().__init__()
        self.window = window
        self.frame = orf
        self.setText(f"frame {orf}")
        self.clicked.connect(self.translate_dna_sequence)

    def translate_dna_sequence(self):
        '''Translates the DNA sequence in the selected reading frame.'''
        input_seq = self.window.dna_sequence.seq
        coding_dna = Seq(input_seq[self.frame:])
        self.window.protein_sequence.add_seq_to_box(str(coding_dna.translate()))
        self.window.selected_frame = self
     
        # highlight color of sequence matches
        self.window.dna_sequence.change_text_color(self.window.query_sequence.text(), QColor("red"))
        self.window.protein_sequence.change_text_color(self.window.query_sequence.text(), QColor("red"))
        
class QuerySequence(QLineEdit):
    '''QLineEdit for entering a query sequence to search.'''

    def __init__(self, window: ViewSequence):
        super().__init__()
        self.window = window
        self.setPlaceholderText("Search Sequence")
        regex = QRegExp("[A-Za-z*]+")
        validator = QRegExpValidator(regex)
        self.setValidator(validator)
        self.textChanged.connect(self.on_change)

    def on_change(self):
        '''Highlights the query sequence in the DNA and protein sequences.'''
        text = self.text().upper()
        self.setText(text)

        # Reset colors
        self.window.dna_sequence.change_text_color(self.window.dna_sequence.seq, QColor("black"))
        self.window.protein_sequence.change_text_color(self.window.protein_sequence.seq, QColor("black"))

        # Highlight matches
        self.window.dna_sequence.change_text_color(text, QColor("red"))
        self.window.protein_sequence.change_text_color(text, QColor("red"))
        
        
class ExportButton(QPushButton):
    '''Button to export the current sequence to a FASTA file.'''

    def __init__(self, window: ViewSequence, text: str = "Export DNA"):
        super().__init__()
        self.window = window
        self.setText(text)
        self.setIcon(QIcon(":/icons/export2.png"))
        self.clicked.connect(self.export_sequence)

    def export_sequence(self):
        '''Opens a file dialog to save the sequence in FASTA format.'''
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Save as")
        file_dialog.setAcceptMode(QFileDialog.AcceptSave)
        file_dialog.setViewMode(QFileDialog.Detail)
        file_dialog.setNameFilter("FASTA (*.fasta)")
        if file_dialog.exec_():
            selected_file = file_dialog.selectedFiles()[0]
            self.write_output(selected_file)

    def write_output(self, filename: str):
        '''Writes the sequence to a FASTA file.'''
        with open(filename, "w") as f:
            f.write(f">{self.window.samples.selected_sample}\n")
            seq = self.window.dna_sequence.seq
            for i in range(0, len(seq), 60):
                f.write(seq[i:i + 60] + "\n")
 

class SampleList(QListWidget):
    '''List widget to display and select sample sequences.'''

    def __init__(self, window: ViewSequence, filenames: list):
        super().__init__()
        self.window = window
        self.addItems(filenames)
        self.setCurrentItem(QListWidgetItem(self.window.main.samples.selected_sample))
        self.itemClicked.connect(self.itemClicked_event)

    def itemClicked_event(self, item):
        '''Updates the displayed sequences when a sample is selected.'''
        self.selected_sample = item.text()
        self.show_sequence(self.selected_sample)

    def show_sequence(self, sample: str):
        '''Displays the DNA and protein sequences for the selected sample.'''
        self.seq = self.window.main.data[sample]["Seq"]
        self.window.dna_sequence.add_seq_to_box(self.seq)
        self.window.selected_frame.translate_dna_sequence()



class SequenceTextBox(QTextEdit):
    
    '''CREATE QTextEdit to display DNA sequence'''

    def __init__(self):
        
        super().__init__()
        
        self.seq = ""
        self.cursor = self.textCursor()
        
    def add_seq_to_box(self, seq):
        
        self.seq = seq
        self.setPlainText(self.seq)

    def change_text_color(self, target_string, color):
        
        if not target_string:
            return  # Avoid infinite loop if target_string is empty

        # Find all occurrences of target_string in self.seq
        occ = [i for i in range(len(self.seq)) if self.seq.startswith(target_string, i)]

        cursor = self.textCursor()

        for o in occ:
            cursor.setPosition(o)
            cursor.setPosition(o + len(target_string), QTextCursor.KeepAnchor)

            char_format = QTextCharFormat()
            char_format.setForeground(QColor(color))

            cursor.mergeCharFormat(char_format)

        cursor.clearSelection
    