#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 16:28:27 2024

@author: sebastien
"""


from Bio import SeqIO
from collections import defaultdict


class ImportAb1:
    
    ''' import data from ab1 files '''
    
    def __init__(self, filenames):
        
        super().__init__()
        
        ab1 = ab1Parser()
        
        self.dataset = {}
        for f in filenames:
        
            seq = ab1.import_seq(f)
            ploc = ab1.get_ploc(f)
            traces = ab1.get_traces(f)
    
            self.dataset[f] = {"Sequence":seq, "Peak_location":ploc, "Traces":traces} 




class ab1Parser:

    ''' Import and process ab1 file '''
    
    def __init__(self):
        
        super().__init__()
        pass
        
    def import_seq(self, f):
        
        # import the sequence text result from the ab1 file
                
        handle = open(f, "rb")
        for record in SeqIO.parse(handle, "abi"):
            seq = record.seq

        return str(seq)

    def get_ploc(self,f):
        
        # import the peak location of the chromatograms
        
        record = SeqIO.read(f,"abi")
        return record.annotations["abif_raw"]["PLOC2"]


    def get_traces(self,f):
        
        # import all traces values of the chromatograms
        record = SeqIO.read(f, "abi")
        
        channels = ["DATA9", "DATA10", "DATA11", "DATA12"]
        trace = defaultdict(list)
        for c in channels:
            trace[c] = record.annotations["abif_raw"][c]

        return trace