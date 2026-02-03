#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 14 09:24:47 2025

@author: sebastien
"""

from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox, QLineEdit, QListWidget, QMessageBox, QAbstractItemView, QGridLayout, QFileDialog, QTextEdit, QLabel, QRadioButton, QSpinBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from qline import QHSeparationLine
from buttons import CancelButton, CreateLabel, SettingButton, HelpButton, LoadButton
from mismatch_whole_seq import ReferenceSeq
from align import Aligner



# -- IMPORT CLASS -- #
class AlignmentWindow(QWidget):

    ''' THIS CLASS CREATES THE WINDOW TO EXPORT THE QUANTIFICATION '''

    def __init__(self, main):

        super().__init__(None, Qt.WindowStaysOnTopHint)

        self.setWindowTitle("SangerQuant - Sequence alignment with a reference")
        self.resize(1200,850)
        
        # Import data
        self.main = main
        self.alignment = MakeAlignment(self)
        self.aligner = Aligner()
        
        # Init values
        self.create_widgets()
        self.create_layout()

    def create_widgets(self):

        # create widgets
        self.sample_list = FileList(self, [key for key in self.main.data])
        self.reference_seq = ReferenceSeq(self)
        self.store_alignment = StoreAlignment(self)
        
        # create buttons
        self.cancelbutton = CancelButton(self)
        self.exportbutton = ExportButton(self)
        self.helpbutton = HelpButton(name="align_sequence")
        
        # create setting window
        self.alignment_settings = AlignmentSettings(self)
        self.settingbutton = SettingButton(self.alignment_settings)
        
    def create_layout(self):

        self.layout = QGridLayout(self)

        # add the sample list
        self.layout.addWidget(CreateLabel(text="Select samples:"),0,0,1,1)
        self.layout.addWidget(self.sample_list, 1, 0, 4, 4)
        self.layout.addWidget(QHSeparationLine(),5,0,1,4)
        self.layout.addWidget(CreateLabel(text="Reference sequence:"),6,0,1,1)
        self.layout.addWidget(self.reference_seq,7,0,5,4)
        
        
        
        self.layout.addWidget(self.store_alignment,1,5,11,5)
        
        # -- add buttons -- #
        self.layout.addWidget(self.helpbutton, 12,6,1,1)
        self.layout.addWidget(self.settingbutton, 12, 7,1,1)
        self.layout.addWidget(self.cancelbutton, 12,8,1,1)
        self.layout.addWidget(self.exportbutton,12,9,1,1)
        
        self.layout.setColumnStretch(5,1)
        self.setLayout(self.layout)
        
        
class FileList(QListWidget):

    ''' SELECT THE SAMPLES TO ANALYZE '''

    def __init__(self, window, samples):

        super().__init__()

        self.window = window
    
        # add sample names
        self.addItems(samples)
        
        # allow multiple selection
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.itemClicked.connect(self.itemClicked_event)

        self.selected_samples = samples
         
    def itemClicked_event(self):
        
        self.selected_samples = [item.text() for item in self.selectedItems()]
        self.window.alignment.align_sequences()
  
        
  
class StoreAlignment(QTextEdit):
    
    ''' This class store the alignment results in QPlainTextEdit '''
    
    def __init__(self, window):
        
        super().__init__()
        
        self.window = window
        self.setAlignment(Qt.AlignCenter)
        self.setReadOnly(True)
        
        # init font
        font = QFont()
        font.setFamily("Monospace") # monospace font allow for alignment between the lines of alignment
        self.setFont(font)

    def add_alignment(self, txt):
        
        self.text = txt
        self.setPlainText(txt)
        
        
        
class MakeAlignment:
    
    ''' This class store the alignment results in QPlainTextEdit '''
    
    def __init__(self, window):
        
        super().__init__()
        
        self.window = window
    
    def _extract_informations(self, sample):
        
        '''
        method to extract the sanger sequence and the reference sequence from the Widgets
        '''
        
        # return information for processin
        seq = self.window.main.data[sample]["Seq"]
        refseq = self.window.reference_seq.toPlainText()
        refseq = refseq.replace("\n", "")
        
        return seq, refseq
       
    def align_sequences(self):
        
        ''' 
        method to perform pairwise alignment between the reference and the sample sequences
        '''
        
        # align sequences with the sequence of reference
        for s in self.window.sample_list.selected_samples:
            
            seq, refseq = self._extract_informations(s) # extract target and reference sequence to align to
            self.alignment = self.window.aligner.align_sequence(seq,refseq) # make alignment
            
            target_start, target_end = self.alignment.coordinates[0][0], self.alignment.coordinates[0][-1] # get coordinate of alignment from target sequence
            ref_start, ref_end = self.alignment.coordinates[1][0], self.alignment.coordinates[1][-1] # get coordinate of alignment from reference sequence
            
            subset_seq = seq[target_start:target_end]  # subset target sequence
            subset_ref = refseq[ref_start:ref_end] # subset refenrece sequence
            
            match = ["|" if x == y else "." for x,y in zip(list(subset_seq),list(subset_ref))]
            match= "".join(match)
           
            self._create_alignment_text(subset_seq, subset_ref, match)
                     
    def _create_alignment_text(self, aligned_seq, aligned_ref, match_symbol):
        
        ''' 
        method to pcreate the alignment text that will be display after alignments
        '''
        
        res = "\n\n"
        
        j = self.alignment.coordinates[1][0]
        s = self.alignment.coordinates[0][0]
        for i in range(0, len(aligned_seq), 60):
            
            sp_tar, sp_ref = self._create_spacer(s, j)
            
            spacer = "".join([" " for x in range (8)])
            middle_spacer = "".join([" " for x in range (len(spacer + "    target " + sp_tar + str(s) + "-" ))])
            
            res = res + spacer + "    target " + sp_tar + str(s) + "-" + aligned_seq[i:i + 60] + "-" + str(s + 60) +"\n"
            res = res + middle_spacer + match_symbol[i:i + 60] + "\n"
            res = res + spacer + " reference " + sp_ref + str(j) + "-" + aligned_ref[i:i + 60] + "-" + str(j + 60) + "\n\n"
        
            j += 60
            s += 60
            
            self._create_spacer(s, j)
            self.window.store_alignment.add_alignment(res)
            
            
    def _create_spacer(self, s, j):
        
        n_space_tar = 5 - len(str(s))
        n_space_ref = 5 - len(str(j))
        
        spacer_tar = "".join([" " for x in range (n_space_tar)])
        spacer_ref = "".join([" " for x in range (n_space_ref)])
        
        
        return spacer_tar, spacer_ref
        
 

                      
class ExportButton(QPushButton):
    
    '''Button to export the current sequence to a FASTA file'''

    def __init__(self, window: AlignmentWindow, text: str = "Export"):
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
        file_dialog.setNameFilter("TEXT (*.txt")
        
        if file_dialog.exec_():
            selected_file = file_dialog.selectedFiles()[0]
            self.write_output(selected_file)

    def write_output(self, filename: str):
        
        '''Writes the sequence to a FASTA file.'''
        
        with open(filename, "w") as f:
            
            f.write(f">{self.window.samples.selected_sample}\n")
            f.write(self.window.store_alignment.text)
    
    

class AlignmentSettings(QWidget):
    
    ''' CREATE A WINDOW TO CHANGE THE ALIGNMENT SETTING:
        - change match-score
        - mismatch-score
        - open-gap-score
        - extend-gap-score
    '''
    
    def __init__(self, window):
        
        super().__init__(None, Qt.WindowStaysOnTopHint)
        
        # create window
        self.window = window
        self.setWindowTitle("Alignment Settings")
        
        self._create_widgets()
        self._set_spinbox_values()
        self._create_layout()
        
    def _create_widgets(self):
        
        # select type of alignment
        self.local_align = SetAlignmentType(self.window, text="Local")
        self.global_align = SetAlignmentType(self.window, text="Global")
        self.local_align.setChecked(True)
        
        # select alignment parameters and penalties
        self.match_score = SetAlignmentScore(self.window, text="match_score", value= 2, minimum = 0, maximum=10)
        self.mismatch_score = SetAlignmentScore(self.window, text= "mismatch_score", value= -1, minimum=-10, maximum=0)
        self.open_gap_score = SetAlignmentScore(self.window,text="open_gap_score", value = -10, minimum=-10, maximum=0)
        self.extend_gap_score = SetAlignmentScore(self.window, text ="extend_gap_score", value = -1, minimum=-10, maximum=0)
        
        # pushbutton
        self.apply_button = ApplyButton(self.window)
        self.cancel_button = CancelButton(self)
    
    def _create_layout(self):
    
        grid = QGridLayout(self)
        grid.addWidget(QLabel("Alignment: "), 0,0,1,1)
        grid.addWidget(self.global_align, 0,1,1,1)
        grid.addWidget(self.local_align, 0,2,1,1)
        
        grid.addWidget(QHSeparationLine(),1,0,1,3) # separation line
        
        # score parameters
        grid.addWidget(QLabel("Penalty scores"), 2,0,1,1)
        grid.addWidget(QLabel("Match: "),3,0,1,1)
        grid.addWidget(self.match_score, 3,1,1,2)
        grid.addWidget(QLabel("Mismatch: "),4,0,1,1)
        grid.addWidget(self.mismatch_score, 4,1,1,2)
        grid.addWidget(QLabel("Open gap: "),5,0,1,1)
        grid.addWidget(self.open_gap_score, 5,1,1,2)
        grid.addWidget(QLabel("Extend gap: "),6,0,1,1)
        grid.addWidget(self.extend_gap_score, 6,1,1,2)
    
        grid.addWidget(QHSeparationLine(),7,0,1,3) # separation line
        
        grid.addWidget(self.cancel_button, 8,1,1,1)
        grid.addWidget(self.apply_button, 8,2,1,1)
        
        self.setLayout(grid)
        
    def _set_spinbox_values(self):
        
        '''
        method to init the parameters of aligments
        '''
        
        self.match_score.setValue(2)
        self.mismatch_score.setValue(-1)
        self.open_gap_score.setValue(-10)
        self.extend_gap_score.setValue(-1)
        
class SetAlignmentType(QRadioButton):
    
    ''' choose type of alignment '''
    
    def __init__(self, window: AlignmentWindow, text="Local"):
        
        super().__init__()
        
        self.window = window
        
        self.setText(text)
        self.value = text
        
                                                                
class SetAlignmentScore(QSpinBox):

    ''' set score for alignment '''    

    def __init__(self, window: AlignmentWindow, text="match_score", value=2, minimum=0, maximum=10):
            
        super().__init__()
        
        self.window = window
        
        self.text = text
        self.setText = self.text
        self.setValue(value)
        
        self.setRange(minimum, maximum)
        self.valueChanged.connect(self.set_new_scores)
    
    def set_new_scores(self):
        
        current_value = self.value()
      
        self.window.aligner.param[self.text] = current_value
        self.window.aligner.get_score()
        
        
        
class ApplyButton(QPushButton):
    
    ''' 
    CREATE A QPUSHBUTTON TO APPLY NEW SETTING FROM THE ALIGNEMENT SETTING WINDOW
    '''
    
    def __init__(self, window:AlignmentWindow):
        
        super().__init__()
        
        self.window = window
        self.setText("Apply")
        
        self.clicked.connect(self.apply_settings)
            
    def apply_settings(self):
        
        if self.window.alignment_settings.local_align.isChecked():
            self.window.aligner.aligner.mode = self.window.alignment_settings.local_align.value.lower()
        else:
            self.window.aligner.aligner.mode = self.window.alignment_settings.global_align.value.lower()
        
        self.window.alignment.align_sequences()
        self.window.alignment_settings.close()

    
