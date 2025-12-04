#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 20:49:43 2022

@author: sebastien
"""
from Bio.Seq import Seq

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *



class ProteinSequence:
    
    ''' CREATES A WINDOW AND PRINT THREE FRAMES OF PROTEIN SEQUENCES IN FASTA FORMAT '''
    
    def __init__(self, sanger):
        
        super().__init__()
        
        self.sanger = sanger
        
        # CREATE THE WINDOW 
        self.window = QMainWindow()
        self.window.setWindowTitle("Protein sequence")
        self.window.resize(500,800)
        
        ## TRANSLATE DNA SEQUENCE ACCORDING TO THREE FRAMES 
        text_to_add = ""
        for frame in [0,1,2]:
            
            dna = Seq(self.sanger.sequence[frame:])
            translate = str(dna.translate())
            
            text_to_add = text_to_add + "> {} {} \n {} \n \n".format(self.sanger.data, " -frame " + str(frame), translate, self.window)
            
            
        # PROCESS THE SEQUENCE
        text = QPlainTextEdit("{}".format(text_to_add, self.window))
        text.setReadOnly(True)
        
        self.window.setCentralWidget(text)
        self.window.show()