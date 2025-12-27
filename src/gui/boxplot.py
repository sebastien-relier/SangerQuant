#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 21 15:28:37 2025

@author: sebastien
"""


import numpy as np
import pyqtgraph as pg

class Boxplot:
    
    ''' create a boxplot for pyqtgraph from dict '''

    def __init__(self, window):
        
        super().__init__()
        
        self.window = window
        
    def add_whisker(self, data = None):
        
        i = 0
        for key,value in data.items():
            
            # -- extract value for plot -- #
            q1 = np.percentile(value, 25)
            q3 = np.percentile(value, 75)
            median = np.median(value)
            iqr = q3 - q1
            lower_bound = min([x for x in value if x > q1 - 1.5 * iqr])
            upper_bound = max([x for x in value if x < q3 + 1.5 * iqr])
        
            box = pg.QtGui.QGraphicsRectItem(i - 2.5, q1, 5,  iqr)
            box.setPen(pg.mkPen('black', width = 3))
            box.setBrush(pg.mkBrush('lightblue'))
            self.window.addItem(box)
            
    
            # Plot the median line
            median_line = pg.QtGui.QGraphicsLineItem(i - 2.5, median, i +  2.5, median)
            median_line.setPen(pg.mkPen('black', width = 3))
            self.window.addItem(median_line)
            
            # Plot the whiskers
            whisker1 = pg.QtGui.QGraphicsLineItem(i + 0, q1, i + 0, lower_bound)
            whisker1.setPen(pg.mkPen('black', width = 3))
            self.window.addItem(whisker1)
            
            # plot the whiskers
            whisker2 = pg.QtGui.QGraphicsLineItem(i + 0, q3, i + 0, upper_bound)
            whisker2.setPen(pg.mkPen('black', width = 3))
            self.window.addItem(whisker2)
    
    
            # -- create text label -- #
            text_item = pg.TextItem(key)
            text_item.setColor("black")
            text_item.setPos(i, 0)
            text_item.setAngle(90)
            self.window.addItem(text_item)
    
            i+= 10


class ColorMap:
    
    ''' create a colormap on window '''
    
    def __init__(self, window):
        
        super().__init__()
        
        self.window = window
        pass


class BarGraph:
    
    ''' create a bargraph  on window '''
    
    def __init__(self, window):
        
        super().__init__()
        
        self.window = window
    
    def add_bars(self, data = None):
        
        x_values = data[1]
        heights = data[0]
        
        
        bar_graph = pg.BarGraphItem(x=x_values, height=heights, width=0.5, brush='b')

        self.window.addItem(bar_graph)
    

    
    
    
    
    