#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 16:21:56 2024

@author: sebastien
"""


from ab1Parser import ab1Parser

class ImportAb1:
    
    def __init__(self, filenames):
        
        super().__init__()
        
        ab1 = ab1Parser()
        
        self.dataset = {}
        for f in filenames:
        
            seq = ab1.import_seq(f)
            ploc = ab1.get_ploc(f)
            traces = ab1.get_traces(f)
    
            self.dataset[f] = {"Sequence":seq, "Peak_location":ploc, "Traces":traces} 

        
        
        