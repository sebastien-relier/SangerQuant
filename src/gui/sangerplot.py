#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 19:13:10 2022

@author: sebastien
"""


# IMPORT PACKAGES
import pyqtgraph as pg
from PyQt6.QtWidgets import QWidget, QMenu
from PyQt6.QtGui import QBrush, QColor, QFont
from PyQt6.QtCore import Qt, QObject, QEvent
import re

from trace_color import Color

## Switch to using white background and black foreground
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')


rgba = {
        "fill": {"T":(255,0,0,50),"C":(50,50,200,50),"A":(0,100,0,50),"G":(0,0,0,50)},
        "line":{"T":(255,0,0),"C":(50,50,200),"A":(0,100,0),"G":(0,0,0), "N":"darkgrey"}
        }

class SangerTraces(pg.PlotWidget):
    
    ''' CREATES PLOT FOR SANGER TRACES AND ADD TO MAIN WINDOW '''
    
    def __init__(self, main):
        
        super().__init__()

        self.main = main
    
        self.mouse_handler = MouseEvent(self) # init mouse Event
    
        self._initialize_figure()
        self._initialize_parameters()
     
        self.subseq = ""
        
        self.quantification_area = QuantificationArea(self)
        self.show_sequence = ShowSequence(self)
        
        # change context menu from right click
        self._override_context_menu()
        
        
    
        
        
    def _initialize_figure(self):
        # create the plot and its mouse click options
        
         # connect the widget to mouse clicking
        self.installEventFilter(self.mouse_handler)
        self.getPlotItem().getViewBox().installEventFilter(self.mouse_handler)
        self.scene().sigMouseClicked.connect(self.mouse_handler.on_click) 
        
    
        self.setMouseEnabled(x = False, y = False)
        self.getPlotItem().hideAxis("left")
        self.getPlotItem().hideAxis("top")
        self.getPlotItem().hideAxis("bottom")
       
    def _initialize_parameters(self):
        
        # -- set parameters for the window of plotting -- #
        self.xmin = -10
        self.xpos = 0
        self.xwindow = 250
        
        self.ymin = 0
        self.percent_max_height = 5 # 1 to 10
        
        # -- set the axis range -- #
        self.setXRange(0, self.xwindow)
        self.setYRange(0, self.percent_max_height * 1000)
        
        # -- hide autorange button -- #
        plot_item = self.getPlotItem()
        plot_item.buttonsHidden = True
        
        # -- set parameters for the look of the lineplot to show the traces -- #
        self.antialias = True
        self.linewidth = 0.5
        
        self.display_sequence = True
        self.show_quality = False

    
    def create_plot(self):
        ''' create the sanger traces plot to the main window '''
        

        # -- set-up anti-aliasing for smooth plot -- #
        pg.setConfigOptions(antialias = self.antialias)
        
        # -- clear any preexisting plot -- #
        self.clear()
    
        # -- select the dataset corresponding to the selected sample on the filelist -- #
        selected_sample = self.main.samples.selected_sample
        traces = self.main.data[selected_sample]["Traces"]
        
        # -- create four line plots, each one represents the traces for T,G,C,A nucleobase -- #
        for nuc in traces.keys():
            
            size = len(traces[nuc])
            
            fill_color = self.main.trace_color.palettes["fill"][nuc]
            line_color = self.main.trace_color.palettes["line"][nuc]
            
            if self.main.trace_color.fill == True:
                self.plot(x = range(size), y= traces[nuc], fillLevel =-0.3 ,brush=fill_color, pen=pg.mkPen(line_color, width=self.linewidth))
            else:
                self.plot(x = range(size), y= traces[nuc], fillLevel =-0.3, pen=pg.mkPen(line_color, width=2))
          
        
        # -- add sequence to chromatograms -- #
        if self.display_sequence != False:
            self.show_sequence.update_text_items()
      
        # -- go to subsequence if any -- #
        if len(self.subseq) > 0:
            self.go_to_subsequence()
        
        # -- show the graphs -- #
        self.main.layout_container.grid.addWidget(self, 1,2, 8, 10)      
        self.setXRange(self.xpos, self.xpos + self.xwindow)

    def _override_context_menu(self):
        
        self.plotItem.ctrlMenu = None
        
        view_box = self.plotItem.getViewBox()
        view_box_menu = view_box.menu

        # Iterate through the actions in the ViewBox menu
        for action in view_box_menu.actions():
            if "Export" in action.text():
                action.setVisible(True)
            else:
                action.setVisible(False)
            

    
    def update_sequence_pos(self):
        
        self.setXRange(self.xpos - (self.xwindow/2), self.xpos + (self.xwindow/2))
        self.show_sequence.update_text_items()
        self.main.scrollbar.setSliderPosition(self.xpos)
    
    def go_to_subsequence(self):
        
        # -- look for position of the subsequence inside the main sequence -- #
        pos = re.findall(self.subseq, self.seq)
        
        # -- set the window of the chromatogram according to the sequence position -- #
        if len(pos) > 0:
        
            pos = self.seq.find(pos[0])
            self.xpos = self.ploc[pos]
            self.setXRange(self.xpos, self.xpos + self.xwindow)
        else: 
           return
       
        # -- adjust the scrollbar position to match the position of the sequence -- #
        self.main.scrollbar.setSliderPosition(self.xpos)
        
    def update_quantification_line(self, position, closest_peak):
        
        # select the peak to quantification based on the selected position
        # -- create the lines to delimit the plot to quantify -- #
        self.quantification_area.peak_pos = position
        self.quantification_area.define_quantification_area()

        # -- arrange data to fit the QTable -- #
       
        res = []
        for nucleotide, value in self.height[closest_peak].items():
            
            res.append([nucleotide, value])

        # -- update the quantifiation table -- #
        self.main.quantification.update_table(data = res)
        self.main.quantification.create_row_label()
        
        
    def create_subsequence_with_N_at_clicked_position(self, peak_pos):
        ''' create new subsequence based on selected peak | selected peak letter is replaced with N to match any nt for quantification '''
        
        if peak_pos < 10:
            r = self.seq[:peak_pos] + "N" + self.seq[peak_pos+1:peak_pos + 10]
        elif peak_pos > len(self.seq) - 10:
            r = self.seq[peak_pos -10: peak_pos] + "N" + self.seq[peak_pos + 1:]
        else:
            r = self.seq[peak_pos - 10: peak_pos] + "N" + self.seq[peak_pos+1:peak_pos + 10]
        
        return r
    
    
    def pass_selected_peak_to_quantification_table(self, subseq):
        ''' change quantification transition table based on surrounding subseq of selected peak'''

        self.main.quantification_transition.queried_sequence.setText(subseq)    # pass subseq to LineEdit to select sequence to analyze
        self.main.quantification_transition.sample_list.selectAll()             # select all sample for analysis

    def pass_selected_peak_to_subsequence_exporter(self, subseq):
        ''' change subsequence visualized bqsed on surrounding sequence of the selected peak '''
        
        self.main.subsequence_exporter.target_sequence.setText(subseq) 
        self.main.subsequence_exporter.sample_list.selectAll() 
        self.main.subsequence_exporter.apply.create_preview_plot()
        
    
class MouseEvent(QObject):
    
    '''
    class to contains all the mouse functions to the sanger plot | 
    left click > peak selection and quantification,
    right click > open context menu to export to svg
    mouse wheel > scroll the plot to visualize
        
    '''
    
    def __init__(self, window):
        
        super().__init__()
        
        self.window = window
        
        
    def eventFilter(self, source, event):
        # Check if the event is a wheel event
        if event.type() == QEvent.Type.Wheel:
            self.handle_wheel(event)
            return True # Tell Qt we handled this event
        
        return super().eventFilter(source, event)
        
        
    def on_click(self, mouseClickEvent):
        ''' link left mouse click to peak selection and quantification '''
        
        if mouseClickEvent.button() == Qt.MouseButton.LeftButton:
            # get raw coordinate of the mouse click
            x_cor = mouseClickEvent.pos()[0]
          
            
            # adjust the raw coordinate based on where we are in the graph and the size of the window
            pos_adjusted = self.window.xpos + ((x_cor / (self.window.width()) * self.window.xwindow))
            
            # find the closest peak to the mouse click coordinate
            closest_peak = min(self.window.ploc, key=lambda x:abs(x-pos_adjusted))
            where = self.window.ploc.index(closest_peak)
            
            self.window.update_quantification_line(where, closest_peak)
            
            # pass selected peak information to quantification and subsequence windows
            subseq = self.window.create_subsequence_with_N_at_clicked_position(where)
            self.window.pass_selected_peak_to_quantification_table(subseq)
            self.window.pass_selected_peak_to_subsequence_exporter(subseq)
        
    
    def handle_wheel(self, event):
        ''' move from the trace using the wheel '''
        
        # -- get the number degrees the wheel was rotated -- #
        degrees = round(event.angleDelta().y() / 8, 0)
        degrees = int(degrees)
        steps = degrees * 5
        
        
        # -- update x-position based on wheel rotation -- #
        self.window.xpos = self.window.main.scrollbar.value() - steps
        
        # -- move scrollbar and move the plot window -- #
        self.window.main.scrollbar.setValue(self.window.main.scrollbar.value() - steps)
        self.window.setXRange(self.window.xpos, self.window.xpos + self.window.xwindow)
        event.accept()
    

        # -- add sequence to chromatograms -- #
        if self.window.display_sequence == False:
            self.window.show_sequence.hide_sequence_from_traces()
        else:
            self.window.show_sequence.show_sequence_from_traces()
    
    
    
class QuantificationArea:
    
    ''' creates the window around peak to quantify '''
    
    def __init__(self, window):
        
        super().__init__()
        
        self.window = window
        self.peak_pos = None
        
        self.line_left = None
    
        # -- create rectangle between lines -- #
        self.fill = pg.QtWidgets.QGraphicsRectItem()
        brush = QBrush(QColor(200, 200, 255, 80))
        
        self.fill.setBrush(brush)  # translucent blue fill
        self.fill.setPen(pg.mkPen(None))  # no outline
    
    def define_quantification_area(self):
        
        self.clear_lines()
            
        # -- create the lines based on position -- #
        self.get_peak_limit()
        self.create_line()
        self.add_line_to_plot()
    
    
    def clear_lines(self):
        
        # -- clear the currently existing lines -- #
        if self.line_left is not None:
            
            self.window.removeItem(self.line_left)
            self.window.removeItem(self.line_right)
            
            self.window.removeItem(self.fill)
            
    def get_peak_limit(self):
        
        # determine the left and right limit of peak to quantif
        self.limit_left = (self.window.ploc[self.peak_pos - 1] + self.window.ploc[self.peak_pos]) / 2
        self.limit_right = (self.window.ploc[self.peak_pos + 1] + self.window.ploc[self.peak_pos]) / 2
      
    def create_line(self):
        
        # -- create the lines surrounding the select peak -- #
        self.line_left = pg.InfiniteLine(self.limit_left)
        self.line_right = pg.InfiniteLine(self.limit_right)
        
        # -- add rectangle to quantify -- #
        x1 = self.line_left.value()
        x2 = self.line_right.value()
        vb = self.window.getViewBox()
        view_range = vb.viewRect()
        
        self.fill.setRect(x1, 0, x2 - x1, 10000)
        self.window.addItem(self.fill)
        
    def add_line_to_plot(self):
        
        self.window.addItem(self.line_left)
        self.window.addItem(self.line_right)
        
        
class ShowSequence(QWidget):
    
    ''' CREATE THE SEQUENCES TO DISPLAY ON THE PYQTGRAPH '''
    
    def __init__(self, trace):
        
        super().__init__()
         
        self.trace = trace
        self.trace.plotItem.vb.sigRangeChanged.connect(self.update_text_items)
        self.text_items = []   
        
    def update_text_items(self):
        
        font = QFont()
        font.setPixelSize(24)
      
        # -- clear label sequence outside the display window -- #
        if self.text_items != []:
            
            for item in self.text_items:
                
                self.trace.removeItem(item)
            
       # -- write the sequence below the trace -- # 
        for x, y in zip(self.trace.ploc, self.trace.seq):
            
            if (self.trace.xpos <= x <= self.trace.xpos + self.trace.xwindow):
                
                nuc = pg.TextItem(text=y, color=self.trace.main.trace_color.palettes["line"][y], anchor=(0.0,0.0))
                nuc.setPos(x - 2, 10)
                nuc.setFont(font)
                
                self.trace.addItem(nuc)
                self.text_items.append(nuc)
                
    def center_text_items(self):
        
        font = QFont()
        font.setPixelSize(24)
      
        # -- clear label sequence outside the display window -- #
        if self.text_items != []:
            
            for item in self.text_items:
                
                self.trace.removeItem(item)
            
       
       # -- write the sequence below the trace -- # 
        for x, y in zip(self.trace.ploc, self.trace.seq):
            
            left = self.trace.xpos - (self.trace.xwindow/2)
            right = self.trace.xpos + (self.trace.xwindow/2)
            
            if (left <= x <= right):
                
                nuc = pg.TextItem(text=y, color=rgba["line"][y], anchor=(0.0,0.0))
                nuc.setPos(x - 2, 10)
                nuc.setFont(font)
                
                self.trace.addItem(nuc)
                self.text_items.append(nuc)

    def show_sequence_from_traces(self):
    
        for item in self.text_items:
            item.setVisible(True)
    

    def hide_sequence_from_traces(self):
    
        for item in self.text_items:
            item.setVisible(False)

    

    

