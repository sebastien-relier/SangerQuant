#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 30 07:09:54 2025

@author: sebastien
"""

## TO DO LIST
# - STORE THE TRIM PART INTO ANOTHER DICT
# - UNTRIM SEQUENCE


from PyQt5.QtWidgets import QMainWindow, QListWidget, QPushButton, QAbstractItemView
from PyQt5.QtGui import QBrush, QColor, QIcon
from PyQt5.QtCore import Qt
from buttons import CancelButton, HelpButton
import pyqtgraph as pg
from layout import Layout
import copy


class TrimWindow(QMainWindow):
    
    ''' CREATES A WINDOW TO TRIM THE SEQUENCE '''
    
    def __init__(self, main):
        
        super().__init__(None, Qt.WindowStaysOnTopHint)
        
        self.main = main
        
        # -- create widget and layout container -- #
        self.create_widgets()
        self.create_layout()
        
        self.setWindowTitle("SangerQuant - Trim Low Quality Sequence")
        self.setCentralWidget(self.layout)
        self.show()
        
    def create_widgets(self):
        
        # -- create layout to store all the widget -- #
        self.layout = Layout()

        # -- sample list -- #
        self.samples = SampleList(self)
        self.trimplot = TrimPlot(self)
        
        # -- cancel and trim buttons -- #
        self.trimbtn = TrimButton(self)
        self.untrimbtn = UnTrimButton(self)
        self.cancelbtn = CancelButton(self, text="Close")
        self.helpbutton = HelpButton(name = "trim")
        
    def create_layout(self):
        
        # -- create layout -- #
        self.layout.grid.addWidget(self.samples, 0, 0, 8, 1)
        
        self.layout.grid.addWidget(self.cancelbtn, 9,6,1,1)
        self.layout.grid.addWidget(self.untrimbtn, 9,7,1,1)
        self.layout.grid.addWidget(self.trimbtn, 9,8,1,1)
        self.layout.grid.addWidget(self.helpbutton, 9,5,1,1)
        

class TrimPlot(pg.PlotWidget):
    
    ''' CREATE THE LINEPLOT OF PHRED SCORE TO TRIM EXTREMITY '''

    def __init__(self, window):

        super().__init__()
        
        self.window = window
    
        self._set_graphic_parameter()
    
        self.setLabel("left", "Phred Score")
        self.setLabel("bottom", "Position")
    
        self.create_plot()
        
    def create_plot(self):
         
        self.clear()
        phred_max = []
        for sample in self.window.samples.selected_samples:
            
            phred = self.window.main.data[sample]["Phred"]
            phred_max.append(len(phred))
            self.plot(x = range(len(phred)), y= phred,  pen=pg.mkPen("darkgrey", width=1))


        # -- initialize the window range on x-axis -- #
        x_start = 0
        x_end = max(phred_max)
        self.setXRange(x_start, x_end)

        # -- add line to drag -- #
        self.vline1 = TrimLimit(self, 30, "left")
        self.vline2 = TrimLimit(self, max(phred_max) - 30, "right")
        
        self.window.layout.grid.addWidget(self, 0,1,8,8)
        
    def _set_graphic_parameter(self):

       self.setMouseEnabled(x = True, y = False)
     
class TrimLimit:
    
    ''' CREATE INFINITE LINE TO COLOR AREA THAT IS GOING TO BE TRIMMED '''
    
    def __init__(self, graph, pos, direction):
        
        super().__init__()
    
        self.graph = graph
        self.direction = direction
        
        # -- create vline -- #
        self.vline = pg.InfiniteLine(pos=pos, movable=True, bounds=[0, 800], pen=pg.mkPen('r', width=2))

        # -- RectItem to fill the area to the left -- #
        self.fill = pg.QtGui.QGraphicsRectItem()
        self.fill.setBrush(QBrush(QColor(200, 200, 255, 80)))  # translucent blue fill
        self.fill.setPen(pg.mkPen(None))  # no outline
        
        self.graph.addItem(self.fill)
        self.graph.addItem(self.vline)
        
        self.vline.sigPositionChanged.connect(self.update_fill)
        self.graph.getViewBox().sigRangeChanged.connect(lambda *args: self.update_fill)
        
        self.initialize_fill()
        
    def initialize_fill(self):
        
        x = self.vline.value()
        vb = self.graph.getViewBox()
        view_range = vb.viewRect()
        
        if self.direction == "left":
            self.fill.setRect(view_range.left(), 0, x - view_range.left(), 60)
        else:
            self.fill.setRect(x, 0, view_range.right() - x, 60)
        
    # 3. Update function to resize fill when line moves or view changes
    def update_fill(self):
        
        x = self.vline.value()
        vb = self.graph.getViewBox()
        view_range = vb.viewRect()
        
        if self.direction == "left":
            self.fill.setRect(view_range.left(), 0, x - view_range.left(), 60)
        else:
            self.fill.setRect(x, 0, view_range.right() - x, 60)
  
        
  
    
  
    
  
class SampleList(QListWidget):
    
    ''' CREATE A QPUSHBUTTON TO DO THE QUICK TRIM OF THE SEQUENCE '''
    
    def __init__(self, window):
        
        super().__init__()
    
        self.window = window 
        
        # -- create settings -- #
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.itemClicked.connect(self.itemClicked_event)
        
        # -- add filenames to list -- #
        filenames = [x for x in list(self.window.main.data.keys())]
        self.addItems(filenames)
        
        # -- create the plot -- #
        self.selected_samples = [item.text() for item in self.window.main.samples.selectedItems()]
        
    def itemClicked_event(self):
        
        self.selected_samples = [item.text() for item in self.selectedItems()]
        self.window.trimplot.create_plot()


class UnTrimButton(QPushButton):
    
    ''' UNTRIM THE SEQUENCE '''

    def __init__(self, window):
        
        super().__init__()
        
        self.window = window
        self.setText("Untrim")
        self.setIcon(QIcon("://icons/untrim.png"))
        
        self.clicked.connect(self.untrim_sequence)
        
    def untrim_sequence(self):
        
        self.window.main.data = copy.deepcopy(self.window.main.backup)
        self.window.trimplot.create_plot()
        

class TrimButton(QPushButton):
    
    ''' TRIM THE SEQUENCE BASED ON LINE POSITION '''

    
    def __init__(self, window):
        
        super().__init__()
        
        self.window = window
        self.setText("Trim")
        self.setIcon(QIcon("://icons/trim.png"))
        
        self.clicked.connect(self.trim_sequence)
        
    def trim_sequence(self):
        
        # -- get coordinates of vlines -- #
        left, right = self.window.trimplot.vline1.vline.value(), self.window.trimplot.vline2.vline.value()
        left, right = round(left,0), round(right, 0)
        left, right = int(left), int(right)
        
        for sample in self.window.samples.selected_samples:
            
            ploc = self.window.main.data[sample]["Ploc"]
            
            # -- get closest peak to line | cpl = closest peak left | cpr = closest peak right-- #
            cpl, cpr = min(ploc, key=lambda x:abs(x-left)), min(ploc, key=lambda x:abs(x-right))
            
            # -- trim sequence -- #
            self.cut_sequence(sample, cpl, cpr)
            self.cut_traces(sample, cpl, cpr)
            self.cut_phred(sample, cpl, cpr)
            self.cut_peak_quant(sample, cpl, cpr)
            self.cut_ploc(sample, cpl, cpr) 
            
        self.window.trimplot.create_plot()
    
        # -- update vline positions from the trimplot -- #
        self.window.trimplot.vline1.vline.setPos(0)
        self.window.trimplot.vline2.vline.setPos(right - left)
        
        
        # -- update the trimmed sanger traces -- #
        self.window.main.samples.pass_data_to_traceplot(self.window.main.samples.selected_sample)
        self.window.main.plot.create_plot()
        
    def cut_sequence(self, sample, left, right):
        
        self.window.main.data[sample]["Seq"] = self.window.main.data[sample]["Seq"][left:right]
        
    def cut_ploc(self, sample, left, right):
        
        plocs = self.window.main.data[sample]["Ploc"][left:right]
        plocs = [x - plocs[0] for x in plocs]
        
        self.window.main.data[sample]["Ploc"] = plocs 
    
    def cut_phred(self, sample, left, right):
        
        self.window.main.data[sample]["Phred"] = self.window.main.data[sample]["Phred"][left:right]
    
    def cut_traces(self, sample, left, right):
        
        traces = self.window.main.data[sample]["Traces"]
        
        # -- get ploc limit -- #
        start = self.window.main.data[sample]["Ploc"][left]
        end = self.window.main.data[sample]["Ploc"][right]
        
        tmp = {}
        for key in traces:
            
            tmp[key] = traces[key][start:end]
            
        self.window.main.data[sample]["Traces"] = tmp

    def cut_peak_quant(self, sample, left, right):
         
         heights = self.window.main.data[sample]["Height"]
         area = self.window.main.data[sample]["Area"]
         
         # -- get ploc limit -- #
         start = self.window.main.data[sample]["Ploc"][left]
         end = self.window.main.data[sample]["Ploc"][right]
        
         tmp_h, tmp_a = {}, {}
         for key in heights:
             
             if ((key >= start) and (key <= end)):
                 tmp_h[key - start] = heights[key] 
                 tmp_a[key - start] = area[key]
         
     
         self.window.main.data[sample]["Height"] = tmp_h
         self.window.main.data[sample]["Area"] = tmp_a
     

        

    
    
    
        