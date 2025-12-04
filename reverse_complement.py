#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 27 21:18:58 2025

@author: sebastien
"""




from Bio import Seq

complement = {
    "G":"C",
    "C":"G",
    "A":"T",
    "T":"A",
    }



class ReverseComplement():
    
    ''' Reverse complement all the data '''
    
    def __init__(self, main):
        
        super().__init__()
        
        self.main = main
        
        
    def get_reverse_complement(self):
        # helper function to reverse complement all the data
        
        for key in self.main.data:
            
            self.change_sequence(key)
            self.change_traces(key)
            self.change_heights_and_area(key)
            self.change_ploc(key)
    
    
        
    
    def revert_dict(self, var):
    
        res = {}        
        for key in var:
            
            new_loc = self.length_of_values - key
            
            tmp = var[key]
            
            tmp["G"], tmp["C"] = tmp["C"], tmp["G"]
            tmp["A"], tmp["T"] = tmp["T"], tmp["A"]
            
            res[new_loc]= tmp
            
        return res
    
    def change_sequence(self, sample):
        # reverse complement the sequence
        
        sequence = list(self.main.data[sample]["Seq"])
        
        sequence = [s.replace(s, complement[s]) if s in list(complement.keys()) else s for s in sequence]
        sequence = sequence[::-1]
        sequence = str("".join(sequence))
        
        self.main.data[sample]["Seq"] = sequence
    
        
    
    def change_traces(self, sample):
        
        # -- changes traces -- #
    
        traces = self.main.data[sample]["Traces"]
        
        tmp = {}
        for k in list(traces.keys()):
            
            # reverse traces
            val = list(traces[k])
            val.reverse()
            
            # add trace to new dict for complement base
            tmp[complement[k]] = val
            
        
        self.main.data[sample]["Traces"] = tmp
        

    def change_heights_and_area(self, sample):
        
        trace = self.main.data[sample]["Traces"]["G"]
        self.length_of_values = len(trace)
        
    
        # -- get height value -- #
        height = self.main.data[sample]["Height"]
        height = dict(list(height.items())[::-1])
        height = self.revert_dict(height)
        
        # -- get area value -- #
        area = self.main.data[sample]["Area"]
        area = dict(list(area.items())[::-1])
        area = self.revert_dict(area)
       
    
        # -- change the values -- #
        self.main.data[sample]["Height"] = height    
        self.main.data[sample]["Area"] = area
        
    def change_ploc(self, sample):
        
        # -- extract peak traces length -- #
        ploc = self.main.data[sample]["Ploc"]
        trace = self.main.data[sample]["Traces"]["G"]
        
        # -- revert the peak location -- #
        ploc = list(ploc)[::-1]
        ploc = [len(trace) - p for p in ploc]
       
        self.main.data[sample]["Ploc"] = ploc
        
        
        