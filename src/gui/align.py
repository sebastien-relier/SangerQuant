#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 13 12:42:07 2025

@author: sebastien
"""


from Bio import Align


class Aligner:
    
    ''' create alignment between two sequence '''
    
    def __init__(self):
        
        super().__init__()
        
        self.param_init = {"match_score": 1, "mismatch_score": -1, "open_gap_score":-10, "extend_gap_score":-0.5}
        self.param = {"match_score": 1, "mismatch_score": -1, "open_gap_score":-10, "extend_gap_score":-0.5}
        
        # initialize aligner
        self.aligner = Align.PairwiseAligner()
        self.aligner.mode = "local"
        
        self.get_score()
        
    def get_score(self):
        
        self.aligner.match_score = self.param["match_score"]
        self.aligner.mismatch_score = self.param["mismatch_score"]
        self.aligner.open_gap_score = self.param["open_gap_score"]
        self.aligner.extend_gap_score = self.param["extend_gap_score"]
        
    def align_sequence(self, seq1, refseq):
        
        alignments = self.aligner.align(seq1, refseq)
        for alignment in alignments:

            return alignment
            break
          
        