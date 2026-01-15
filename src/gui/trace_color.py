#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 18:00:48 2026

@author: sebastien
"""


from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QPushButton


class Color:
    
    ''' SET THE COLOR OF THE TRACE '''
    
    def __init__(self):
        
        super().__init__()
        
        self.palettes = {
            "regular":{
                    "fill":
                        {
                        "T":(255,0,0,50),
                        "C":(50,50,200,50),
                        "A":(0,100,0,50),
                        "G":(0,0,0,50)
                        },
                    "line":
                        {"T":(255,0,0),
                         "C":(50,50,200),
                         "A":(0,100,0),
                         "G":(0,0,0), 
                         "N":"darkgrey"
                         }
                    },
                "colorblind":{
                    "fill":
                        {
                        "T":(213,94,0,70),
                        "C":(0,114,178, 70),
                        "A":(0,158,115, 70),
                        "G":(204,121,167, 70)
                        },
                    "line":
                        {"T":(213,94,0),
                         "C":(0,114,178),
                         "A":(0,158,115),
                         "G":(204,121,167), 
                         "N":"darkgrey"
                         }
                    }
                }
    



class ColorWindow(QWidget):
    
    ''' CREATE A WINDOW TO SELECT THE COLOR TO DISPLAY '''

    def __init__(self):
        
        super().__init__()
        
        
        self._create_layout()
        
        
    def _create_layout(self):
        
        
        grid = QGridLayout()
        grid.addWidget(QLabel("T:"), 0,0)
        grid.addWidget(QLabel("C:"), 1,0)
        grid.addWidget(QLabel("A:"), 2,0)
        grid.addWidget(QLabel("G:"), 3,0)        
        
        grid.addWidget(QPushButton(self, color="red"), 1,0)
        
        self.setLayout(grid)
        
        pass
        






