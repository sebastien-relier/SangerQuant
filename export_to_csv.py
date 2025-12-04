#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 20 21:03:45 2025

@author: sebastien
"""

class ExportToCsv:
    
    ''' export data from to csv file format '''
    
    def __init__(self):
        
        super().__init__()
        
        pass
    
    def export_to_csv(self, separator = ",", headers = ["Samples", "Mismatch(%)"], output_filename = "", data = None):
        
        # -- export list of list to csv -- #
        text_f = separator.join(headers) + "\n"
        with open(output_filename, "w") as f:
            
            for row in data:
                
                text = ""
                
                for col in row:
                    
                    text += str(col)
                    text += separator
                
                text += "\n"
                text_f += text  
                
    
            f.write(text_f)
                
    
        
    
    