#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 16:28:27 2024

@author: sebastien
"""


from Bio import SeqIO
from collections import defaultdict
import numpy as np

class ab1Parser:

    ''' Import and process ab1 file '''
    
    def __init__(self, f):
        
        super().__init__()
        
        self.channels = {
            "DATA9":"G", 
            "DATA10":"A", 
            "DATA11":"T", 
            "DATA12":"C",
                         }
        
        self.record = SeqIO.read(f, "abi")        
        self.ploc = list(self.record.annotations["abif_raw"]["PLOC2"])
    
        
        self.init_trace()
    
    def init_trace(self):
        
        self.trace = defaultdict(list)
        
        for key in self.channels:
            
            nuc = self.channels[key]
            
            self.trace[nuc] = self.record.annotations["abif_raw"][key][0:self.ploc[-1] + 50]
            
    def import_seq(self, f):
        
        # import the sequence text result from the ab1 file
                
        handle = open(f, "rb")
        for record in SeqIO.parse(handle, "abi"):
            seq = record.seq

        return str(seq)

    def get_ploc(self):
    
        return self.ploc

    def get_traces(self):
    
        return self.trace
    
    
    def get_phred_score(self):
        
        phred = self.record.annotations["abif_raw"]["PCON1"]
        return list(phred)
    
    def get_median_phred_score(self):
        
        phred = self.record.annotations["abif_raw"]["PCON1"]
        return np.median(list(phred))
    

    def get_peak_heights(self):

        res = {}
        for pos in self.ploc:
        
            tmp = {}
            for nuc in self.trace:
                
                # get peak height of each nucleotide
                values = self.trace[nuc]
                tmp[nuc] = values[pos]
                
                # get peak area of each nucleotide
            
            res[pos] = tmp
                
        return res
        
    
    def get_peak_area(self):
        
        res = {}
        for pos in self.ploc:
            
            tmp =  {}
            
            # extract peak area for every peak location
            index = self.ploc.index(pos)
            
            
            if index < 0:
                left = self.ploc[0]
                right = (self.ploc[index + 1] + self.ploc[index]) / 2
            elif index == len(self.ploc) - 1:
                left =  (self.ploc[index - 1] + self.ploc[index]) / 2
                right = self.ploc[-1]
            else:
                left =  (self.ploc[index - 1] + self.ploc[index]) / 2
                right = (self.ploc[index + 1] + self.ploc[index]) / 2
            
            
            for nuc in self.trace:
                
                values = self.trace[nuc]
                subset = values[int(left):int(right)]
                
                area = np.trapezoid(subset, dx=1)
       
                tmp[nuc] = area
            
            
            res[pos] = tmp
            
        return res
    
    
    



    def get_peak_width(self):
        
        widths = []
        for pos in self.ploc:
            
            # extract peak area for every peak location
            index = self.ploc.index(pos)
        
            if index < 0:
                left = self.ploc[0]
                right = (self.ploc[index + 1] + self.ploc[index]) / 2
            elif index == len(self.ploc) - 1:
                left =  (self.ploc[index - 1] + self.ploc[index]) / 2
                right = self.ploc[-1]
            else:
                left =  (self.ploc[index - 1] + self.ploc[index]) / 2
                right = (self.ploc[index + 1] + self.ploc[index]) / 2


            widths.append([left,right]) 

            
        return widths
        
    