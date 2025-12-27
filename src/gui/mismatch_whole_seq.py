#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 13 06:59:32 2025

@author: sebastien
"""


from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QListWidget, QAbstractItemView, QGridLayout, QPlainTextEdit, QLabel
from PyQt5.QtCore import Qt
from qline import QHSeparationLine, QVSeparationLine
from buttons import CancelButton, ExportButton, SettingButton, CreateLabel, HelpButton
from align import Aligner
from boxplot import BarGraph
import pyqtgraph as pg


# -- IMPORT CLASS -- #
class QuantifyWholeSeq(QWidget):

    ''' THIS CLASS CREATES THE WINDOW TO EXPORT THE QUANTIFICATION '''

    def __init__(self, main):

        super().__init__(None, Qt.WindowStaysOnTopHint)

        self.setWindowTitle("SangerQuant - Find mismatches within a sequence")
        
        # Import data
        self.main = main

        # Init values
        self._create_widgets()
        self._create_layout()

        self.show()

    def _create_widgets(self):

        # create list of sample
        self.sample_list = FileList(self, [key for key in self.main.data])
        self.reference_seq = ReferenceSeq(self)
        
        self.aligner = Aligner()
        self.mismatch_plotter = MismatchCalculator(self)
        
        # create plot related widgets
        self.plot = PlotArea(self) 
        self.plot_setting = PlotSetting(self)
        self.settingbutton = SettingButton(setting_window=self.plot_setting)
        
        
        self.cancelbutton = CancelButton(self)
        self.exportbutton = ExportButton(self.plot.plot_area)
        self.helpbutton = HelpButton(name="find_mismatch")    
        
    def _create_layout(self):

        self.layout = QGridLayout(self)

        # add the sample list
        self.layout.addWidget(CreateLabel(text="Select samples:"), 0,0,1,1)
        self.layout.addWidget(self.sample_list, 1, 0, 4, 4)
        self.layout.addWidget(QHSeparationLine(),5,0,1,4)
        
        self.layout.addWidget(CreateLabel(text="Reference:"), 6,0,1,1)
        self.layout.addWidget(self.reference_seq, 7,0,5,4)

        # -- add the button to execute the functions -- #
        #self.layout.addWidget(self.settingbutton, 11,5)
        self.layout.addWidget(self.helpbutton, 13,6)
        self.layout.addWidget(self.cancelbutton, 13, 7)
        self.layout.addWidget(self.exportbutton, 13, 8)
        
        
        self.layout.addWidget(self.plot.plot_area, 0,5, 12,7)
        self.layout.setColumnStretch(5, 5)
        
        # add buttons
        self.setLayout(self.layout)
        
class FileList(QListWidget):

    ''' SELECT THE SAMPLES TO ANALYZE '''

    def __init__(self, window, samples):

        super().__init__()

        self.window = window
    
        # add sample names
        self.addItems(samples)
        
        # allow multiple selection
        self.itemClicked.connect(self._itemClicked_event)

        self.selected_samples = samples
         
    def _itemClicked_event(self):
        
        # create new plot of mismatches
        self.selected_samples = [item.text() for item in self.selectedItems()]
        self.window.mismatch_plotter.create_plot()
        
        # update trace to match the selected samples
        self.window.main.samples.setCurrentRow(self.currentRow()) # display selected sample on list of the MainWindow
        self.window.main.samples.selected_sample = self.selected_samples[0] # need to update the selected sample to update the plot
        self.window.main.samples.update_plot(self.selected_samples[0])
        
    
        s = self.window.main.data[self.selected_samples[0]]["Seq"]
        self.window.plot.plot_area.setLimits(xMin=-5, xMax=len(s), yMin=0, yMax=100)
        
    
    
class ReferenceSeq(QPlainTextEdit):
    
    ''' ENTER THE REFERENCE SEQUENCE '''
    
    def __init__(self, window):
        
        super().__init__()
        
        self.window = window
        self.setPlaceholderText("Paste the reference sequence here")
    
    def keyPressEvent(self, event):
        # Get the character from the event
        key = event.text().upper()
        # Allow only A, T, C, G, and basic editing keys (backspace, delete, arrows, etc.)
        if key in ["A", "T", "C", "G"] or event.key() in [
            Qt.Key_Backspace,
            Qt.Key_Delete,
            Qt.Key_Left,
            Qt.Key_Right,
            Qt.Key_Up,
            Qt.Key_Down,
            Qt.Key_Home,
            Qt.Key_End,
        ]:
            super().keyPressEvent(event)
        else:
            event.ignore()
        
class MismatchCalculator:
    
    ''' calculate the mismatch rate at every nucleotide, based on the reference sequence '''
    
    def __init__(self, window):
        
        super().__init__()
    
        self.window = window
    
    def _extract_informations(self, sample):
        
        # return information for processing
        
        seq = self.window.main.data[sample]["Seq"]
        refseq = self.window.reference_seq.toPlainText()
        
        ref_split = refseq.split("\n")
        ref_split = [x for x in ref_split if (">" in x) == False]
        
        refseq = "".join(ref_split)
        
        
        return seq, refseq

    def _subset_sequence(self, alignment, seq, i):
       
       start, end = alignment.coordinates[i][0], alignment.coordinates[i][1]
       seq = seq[start: end]
       return seq
            
    def _calculate_mismatch(self, s, seq, refseq, alignment):
        # need alignment to get coordinates, refseq to get reference base, and s to get samples
        
        # extract peak height
        peak_heights = self.window.main.data[s]["Height"]
        
        # determine sequence alignment coordinate from local alignment
        seq_start = alignment.coordinates[0][0] 
        seq_end = alignment.coordinates[0][1]
        
        # determine reference sequence alignment coordinates
        refseq_start= alignment.coordinates[1][0]
        refseq_end = alignment.coordinates[1][1]
    
        # subset aligned part of the reference and sequence test
        subset = [peak_heights[x] for x in list(peak_heights.keys())[seq_start:seq_end]]
        refseq = refseq[refseq_start:refseq_end]
        
        # calculate mismatch at each position of the aligned sequence, using the reference seq as a reference of the base
        mm = []
        for x,y in zip(subset, refseq):
            
            total = list(x.values())
            total = sum(total)
            
            mismatch = ((total - x[y]) / total) * 100
            mismatch = round(mismatch, 2)
                   
            mm.append(mismatch)
        
        pos = [i for i in range(seq_start, seq_end)]
        return [mm, pos]
            
    def create_plot(self):
        
        self.window.plot.plot_area.clear()
        
        # align sequences with the sequence of reference
        for s in self.window.sample_list.selected_samples:
            
            seq, refseq = self._extract_informations(s)
        
            # extract coordinates of alignment
            alignment = self.window.aligner.align_sequence(seq,refseq)
            
            self.window.calculated_mismatch = self._calculate_mismatch(s, seq, refseq, alignment)
            
            # create the bar plot
            self.barplot = BarGraph(self.window.plot.plot_area)
            self.barplot.add_bars(data = self.window.calculated_mismatch)
            
class PlotArea:
    
    ''' create the plot area to contain the graph '''
    
    def __init__(self, window):
        
        super().__init__()
        
        self.window = window
    
        self._initialize_plot_area()
        self.plot_area.scene().sigMouseClicked.connect(self.on_mouse_click)
        
    def _initialize_plot_area(self):
        
        self.plot_area = pg.plot()
        self.plot_area.setMenuEnabled(False)
    
        # -- hide autorange button -- #
        plot_item = self.plot_area.getPlotItem()
        plot_item.buttonsHidden = True
        
        self.plot_area.setXRange(0,600)
        self.plot_area.setYRange(0,100)
        self.plot_area.setMouseEnabled(x = True, y = False)
        self.plot_area.setLabel("left", "Mismatch Rate (%)")
        self.plot_area.setLabel("bottom", "Peak position")
        
    
    def on_mouse_click(self, mouseClickEvent):
    
        # Get the position of the click in scene coordinates
        scene_pos = mouseClickEvent.scenePos()
        
        # -- plot area
        plot_item = self.plot_area.getPlotItem()
        
        # Convert the scene coordinates to the ViewBox's local (plot) coordinates
        if plot_item.vb.sceneBoundingRect().contains(scene_pos):
            mouse_point = plot_item.vb.mapSceneToView(scene_pos)
            x = mouse_point.x()
            x = round(x, 0)
            x= int(x)
            
        # -- update trace plot to select the desired peak -- #
        s = self.window.sample_list.selected_samples[0] # get select sample
        ploc = self.window.main.data[s]["Ploc"][x] # look for peak position
        
        # update the trace to show from main window
        self.window.main.plot.xpos = ploc
        self.window.main.plot.update_sequence_pos()
    
        # update the quantification line and the sequence to display
        self.window.main.plot.update_quantification_line(x,ploc) # pass
        self.window.main.plot.show_sequence.center_text_items()
    

class PlotSetting(QWidget):
    
    ''' open settings for the plot '''
    
    def __init__(self, window):
        
        super().__init__()
        
        self.window = window
        
        self._create_widgets()
        self._create_layout()
        
    def _create_widgets(self):
    
        self.title = QLineEdit(self)
        
        self.xaxis = QLineEdit(self)
        self.yaxis = QLineEdit(self)
        
        #self.xfont_size = QSpinBox(self)
        #self.yfont_size = QSpinBox(self)
        pass
    
    def _create_layout(self):
        
        grid = QGridLayout(self)
        
        grid.addWidget(CreateLabel(text="Title:"), 0,0,1,1)
        grid.addWidget(self.title, 0,1,1,6)
        
        grid.addWidget(QHSeparationLine(),1,0,1,7)
        
        grid.addWidget(CreateLabel(text="x-axis"), 2,1,1,1)
        grid.addWidget(CreateLabel(text="Label:"), 3,0,1,1)
        grid.addWidget(self.xaxis, 3,1,1,2)
        
        
        grid.addWidget(CreateLabel(text="y-axis"), 2,5,1,1)
        grid.addWidget(CreateLabel(text="Label:"), 3,4,1,1)
        grid.addWidget(self.yaxis, 3,5,1,1)
        
        grid.addWidget(QVSeparationLine(),1,3,4,1)
        
        
        self.setLayout(grid)
        
        pass
    
    
