#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 19:13:10 2022

@author: sebastien
"""


# IMPORT PACKAGES
import pyqtgraph as pg
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtWidgets import QGridLayout, QWidget, QScrollBar, QSlider, QLabel
from PyQt5.QtGui import *


## Switch to using white background and black foreground
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


rgba = {
        "red":(255,0,0,50),
        "blue":(50,50,200,50),
        "green":(0,255,0,50),
        "black":(0,0,0,50)
        }


class TracesLayout(QWidget):
    
    ''' CREATE THE QGRIDLAYOUT TO EMBEDD PYQTGRAPH INTO IT '''
    
    def __init__(self, main):
        
        super().__init__()
        
        self.main = main
        self.main.setCentralWidget(self)
        
        self.scroll = ScrollBar(main)
        
        
    def create_layout(self, trace):
        
        self.layout = QGridLayout()
        
        self.layout.addWidget(self.scroll, 0,0)
        self.layout.addWidget(traces,1,0)
        
        self.main.dock2.setWidget(self.scroll)
        self.layout.setLayout(self.layout)
        

 


class SangerTraces(pg.PlotWidget):
    
    ''' CREATES PLOT FOR SANGER TRACES AND ADD TO MAIN WINDOW '''
    
    def __init__(self, main):
        
        super().__init__()
    
        ## Init values
        self.trace = ""
        self.ploc = ""
        self.seq = ""
        self.quant = ""
        
        # init subsequence
        self.subseq = ""
        
        # Init the plot
        self.initialize_figure()
        
        ## Parameters for the plot look and shape
        self.initialize_figure_parameters()
        self.initialize_figure_look_options()
        
        ## Init the window that display quantification values
        self.quant_window = QuantificationWindow()
        
        
        self.main = main
        self.main.setCentralWidget(self)
    
    def initialize_figure(self):
        # create the plot and its mouse click options
        
         # connect the widget to mouse clicking
        self.scene().sigMouseClicked.connect(self.mouse_clicked) 
    
        self.setMouseEnabled(x = False, y = False)
        self.getPlotItem().hideAxis("left")
        self.getPlotItem().hideAxis("top")
        self.getPlotItem().showAxis("bottom")
    
   
    def initialize_figure_parameters(self):
        # create figure parameter such yaxis height and xaxis width
        
        # Parameters of window width (determine the number of peak to display)
        self.xmin = 0
        self.xpos = 0
        self.xwindow = 250
        
        self.ymin = 0
        self.percent_max_height = 5 # 1 to 10
        
        self.line_left = 0
        self.line_right = 0
        
        self.setXRange(0, self.xwindow)
        self.setYRange(0, self.percent_max_height * 1000)
        
        
    def initialize_figure_look_options(self):
        
        self.fill = True
        self.antialias = True
        
        self.linewidth = 5
    
    def create_plot(self):
        
        # this functions create the plot from sanger traces
        
        # set-up anti-aliasing
        pg.setConfigOptions(antialias = self.antialias)
        
        
        # clear pre-existing plot (if any)
        self.clear()
    
        # create line plot with colors corresponding to T,A,G,C
        for nuc, color in zip(list(self.trace.keys()), ["black","green","red","blue"]):
            
            size = len(self.trace[nuc])
            
            if self.fill == True:
                self.plot(x = range(size), y= self.trace[nuc], fillLevel =-0.3 ,brush=rgba[color], pen=pg.mkPen(color, width=5))
            else:
                self.plot(x = range(size), y= self.trace[nuc], fillLevel =-0.3, pen=pg.mkPen(color, width=5))
                
        
        axis = self.getAxis("bottom")
        
        self.go_to_subsequence()
        
        # set x
        self.show()
        
        
    def go_to_subsequence(self):
        # go to subsequence indicated in QLineEdit of toolbar
        
        pos = self.seq.find(self.subseq)
        
        if pos > -1:
        
            self.xpos = self.ploc[pos]
            
            mapped_point = self.plotItem.mapToView(QPointF(self.xpos, 0))
            x_coord = mapped_point.x()
            
            self.setXRange(self.xpos, self.xpos + self.xwindow)
        else: 
            
           pass
        

    def mouse_clicked(self, mouseClickEvent):
        
        # clear pre selected peak
        if self.line_left != 0 :
            
            self.removeItem(self.line_left)
            self.removeItem(self.line_right)
        
        # move the sanger traces using left mouse click
        x_cor, y_cor = mouseClickEvent.pos()[0], mouseClickEvent.pos()[1]
        
        
        # get position based on mouse click on the window
        pos_adjusted = self.xpos + ((x_cor / (self.width()) * self.xwindow))
        
        
        closest_peak = min(self.ploc, key=lambda x:abs(x-pos_adjusted))
        where = self.ploc.index(closest_peak)
        
        limit_left = (self.ploc[where - 1] + self.ploc[where]) / 2
        limit_right = (self.ploc[where + 1] + self.ploc[where]) / 2

        self.line_left = pg.InfiniteLine(limit_left)
        self.line_right = pg.InfiniteLine(limit_right)
        
        self.addItem(self.line_left)
        self.addItem(self.line_right)
        
        
        # update the values in the window
        self.quant_window.quant = self.quant[closest_peak]
        self.quant_window.update_values()
        
        
        
        
        
class QuantificationWindow(QWidget):
    
    ''' CREATE A WINDOW TO DISPLAY THE QUANTIFICATION OF PEAK '''
    
    def __init__(self):
        
        super().__init__()
        
        # Init grid 
        self.create_label()
        self.create_layout()
        
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        
        
    

    def create_layout(self):
        
        self.layout = QGridLayout()
        
        self.layout.addWidget(self.G, 0,0)
        self.layout.addWidget(self.g_values,0,1)
        
        
        self.layout.addWidget(self.T,1,0)
        self.layout.addWidget(self.t_values,1,1)
        
        self.layout.addWidget(self.C, 2,0)
        self.layout.addWidget(self.c_values,2,1)
        
        self.layout.addWidget(self.A,3,0)
        self.layout.addWidget(self.a_values,3,1)
        
        self.setLayout(self.layout)
    
    def create_label(self):
        
        self.G = QLabel("G", self)
        self.G.setStyleSheet("color:black;font-weight:bold")
        
        self.T = QLabel("T", self)
        self.T.setStyleSheet("color:red;font-weight:bold")
        
        self.C = QLabel("C", self)
        self.C.setStyleSheet("color:blue;font-weight:bold")
        
        self.A = QLabel("A", self)
        self.A.setStyleSheet("color:green;font-weight:bold")


        self.g_values = QLabel("0", self)
        self.t_values = QLabel("0", self)
        self.c_values = QLabel("0", self)
        self.a_values = QLabel("0", self)
        
    def update_values(self):
        
        self.g_values.setText(str(self.quant["DATA9"]))
        self.t_values.setText(str(self.quant["DATA11"]))
        self.c_values.setText(str(self.quant["DATA12"]))
        self.a_values.setText(str(self.quant["DATA10"]))
        
        self.show()
    def show_window(self):
        self.show()
        
    def hide_window(self):
        self.hide()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.offset is not None:
            self.move(self.pos() + event.pos() - self.offset)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.offset = None
