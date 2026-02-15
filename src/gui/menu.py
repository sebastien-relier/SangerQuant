#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 13:08:15 2022

@author: sebastien
"""

from PyQt5.QtWidgets import QAction, QMainWindow, qApp, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

import copy
import os
from viewsequence import ViewSequence
from export_quantification import ExportQuantification
from export_svg import ExportSVG
from compare_quality import CompareQuality
from mismatch_whole_seq import QuantifyWholeSeq
from alignment import AlignmentWindow
from trace_color import ColorWindow

from ab1Parser import ab1Parser

from search_sequence import SearchSequence
from filelist import SampleList
from buttons import TraceShape
from scrollbar import ScrollBar
from sangerplot import SangerTraces
from quantification_table import PeakQuant
from export_raw_values import Exporter
from reverse_complement import ReverseComplement
from trim_sequence import TrimWindow


#################################################
# FILE MENU: import / export datasets
################################################# 

class FileMenu:
    
    ''' CREATE THE FILEMENU OF THE APP AND ITS ASSOCIATED FUNCTIONS '''
    
    def __init__(self, menubar, main):
        
        super().__init__()
        
        self.menubar = menubar
        self.main = main
        
        # -- create filemenu actions -- #
        openAction = QAction(QIcon("://icons/document.png"), "&Import", self.menubar)
        self.exportAction = QAction(QIcon("://icons/export_raw.png"),"&Export data", self.menubar)
        self.exportAction.setObjectName("exportaction")
        
        exitAction = QAction(QIcon(":/icons/exit2.png"), "&Exit",self.menubar)

        # -- linked menu to actions -- #
        openAction.triggered.connect(self.open_ab1_file)
        self.exportAction.triggered.connect(self.export_raw_data)
        exitAction.triggered.connect(qApp.quit)
        
        # -- create the filemenu -- #
        self.filemenu = self.menubar.addMenu("&File")
        self.filemenu.addActions([openAction, self.exportAction, exitAction])
        

    def open_ab1_file(self):
        ''' use QFileDialog and custom .ab1 parser to load ab1 data into the app '''
        # open ab1 file and parse data to store into dict
        
        # Create the QFileDialog
        self.file_dialog = QFileDialog(parent=self.main)
        self.file_dialog.setWindowFlags(Qt.WindowStaysOnTopHint)
        
        filenames = self.file_dialog.getOpenFileNames(filter = "*.ab1*")
        
        if filenames[0] == []:
            return
        else:
            # -- import datasets -- #
            self._parse_ab1_file(filenames)
            
            # -- create main window widget -- #
            self._create_main_window_widgets()
            
            # -- initialize the plot of the sanger trace of the first sample -- #
            self.main.samples.setCurrentRow(0)
            self.main.samples.initialize_plot()
        
            # -- indicate that the data have been loaded -- #
            self.main.load_status = "YES"
            
            # -- change the style sheet of the menubar -- #
            self.main.menubar.activate_actions(True)
            
    def _parse_ab1_file(self, filenames):
        
        ''' parse .ab1 file to extract sequence, traces, quality etc ... '''
        
        for f in filenames[0]:
            
            # check if file has already been open; and don't open the file if so #
            if f.split("/")[-1] in list(self.main.data.keys()):
                continue
            
            # -- parse the ab1 file to extract the data -- #
            parser = ab1Parser(f)
            name = os.path.basename(f)
            tmp = {"Ploc":parser.get_ploc(), 
                   "Seq":parser.import_seq(f), 
                   "Traces":parser.get_traces(), 
                   "Height":parser.get_peak_heights(), 
                   "Area": parser.get_peak_area(), 
                   "Phred":parser.get_phred_score(),
                   "MedianPhred": parser.get_median_phred_score(),
                   "Width": parser.get_peak_width()
                   }
        
            self.main.data[name] = tmp 
            
        # create a back-up of the data
        self.main.backup = copy.deepcopy(self.main.data)
        
    def _create_main_window_widgets(self):
        
        ''' create the new widgets upon loading data (i.e: graphic canvas, sample list '''
 
        # -- create the QTable to store the quantification on QMainWindow -- #
        self.main.quantification = PeakQuant(self, rowlabel={"G":"black","A":"green","T":"red","C":"blue"})
        self.main.quantification.create_row_label()
        self.main.layout_container.grid.addWidget(self.main.quantification, 8,0,2,2)
    
    
        # -- create the SampleList -- #
        self.main.samples = SampleList(self.main)
        self.main.layout_container.grid.addWidget(self.main.samples, 0,0,8,2)
       
    
        # -- create the scrollbar to move on the graph -- #
        self.main.scrollbar = ScrollBar(self.main)
        self.main.layout_container.grid.addWidget(self.main.scrollbar, 0,2,1,10)
        
        # -- create the searchbar to seek out sequences -- #
        self.main.search = SearchSequence(self.main)
        self.main.layout_container.grid.addWidget(self.main.search, 9,2,1,8)
        
        
        # -- create QSlider to change width of the traces
        self.trace_width = TraceShape(self.main, minimum=100, maximum=750, interval=50, value=450, connector="width")
        self.main.layout_container.grid.addWidget(self.trace_width, 9,11,1,1)  
        
        
        # -- create QSlider to change Height of the traces -- #
        self.trace_height = TraceShape(self.main, minimum=1, maximum=8, interval=1, value=5, connector="height")
        self.main.layout_container.grid.addWidget(self.trace_height, 9,10,1,1)
        
        
        # -- create the plot layout to add the chromatogram -- #
        self.main.plot = SangerTraces(self.main)
        self.main.layout_container.grid.addWidget(self.main.plot, 1,2, 8, 10)
       

    def export_raw_data(self):
        
        ''' open window to export raw data of sanger traces '''

        self.exporter = Exporter(self.main, self.main.data)
        self.exporter.show()
        
        
#################################################
# EDIT MENU: edit the traces
#################################################          
    
class EditMenu:
    
    ''' CREATE THE EDIT MENU OF THE APP '''
    
    def __init__(self, menubar, main):
        
        super().__init__()
        
        self.menubar = menubar
        self.main = main
        
        self.editmenu = self.menubar.addMenu("&Edit")
        
        # -- create actions -- #
        self.trimAction = QAction(QIcon("://icons/trim.png"), "&Trim", self.menubar)
        self.reverseAction = QAction("&Reverse complement", self.menubar)
        self.reverseAction.setCheckable(True)
        self.reverseAction.setChecked(False)

        # -- connect actions -- #
        self.reverseAction.triggered.connect(self.show_reverse_complement)
        self.trimAction.triggered.connect(self.trim_sequence)

        # -- add Actions to the menubar -- #
        self.editmenu.addAction(self.trimAction)
        self.editmenu.addAction(self.reverseAction)
        
    
    def show_reverse_complement(self):
        ''' display reverse complement of the sequences '''
        
        reverse_comp = ReverseComplement(self.main)
        reverse_comp.get_reverse_complement()
            
        self.main.samples.pass_data_to_traceplot(self.main.samples.selected_sample)
        self.main.plot.create_plot()
    
    def trim_sequence(self):
        ''' open the window to trim the sequence '''

        # -- this function allows to trim the sequence of bad quality score phred -- #
        # trim 5' or 3' extremity of the sequence of bad quality
        trim_seq = TrimWindow(self.main)
    
    
#################################################
# VIEW Menu: display important informations about the datasets
#################################################   
class ViewMenu:
    
    ''' create the view menu to show sequence, quality '''
    
    def __init__(self, menubar, main):
        
        super().__init__()
    
        self.menubar = menubar
        self.main = main
        
        # -- create actions -- #
        self.dnaseqAction = QAction(QIcon("://icons/view_seq.png"), "&Sequences", self.menubar)
        self.qualityAction = QAction("&Quality", self.menubar)
        
        # -- connect actions -- #
        self.dnaseqAction.triggered.connect(self.display_dna)
        self.qualityAction.triggered.connect(self.compare_quality)
        
        # -- add actons to menu  -- #
        self.menu = self.menubar.addMenu("&View")
        self.menu.addAction(self.dnaseqAction)
        self.menu.addAction(self.qualityAction)
        
    
    def display_dna(self):
        ''' open window to display DNA sequence and perform sequence operations '''
        
        self.viewseq = ViewSequence(self.main)
        self.viewseq.show()
    
    def compare_quality(self):
        ''' open window to comparer overall sequence quality between samples '''
        
        self.quality_control = CompareQuality(self.main.data)
        self.quality_control.show()
   
#################################################
# TRACES MENU: modify aspect of the trace
#################################################
   
class TracesMenu:
    
    ''' create the menu to change the look of the traces '''
    
    def __init__(self, menubar, main):
        
        super().__init__()
        
        self.menubar = menubar
        self.main = main
        
        # -- create actions to fill the area under peak of sanger traces -- #
        self.fillAction = QAction("&Fill", self.menubar)
        self.fillAction.setCheckable(True)
        self.fillAction.setChecked(True)
        
        # -- create actions to display the sequence below the sanger traces -- #
        self.seqAction = QAction("&Show sequence", self.menubar)
        self.seqAction.setCheckable(True)
        self.seqAction.setChecked(True)
        
        
        self.quickcolorAction = QAction("&Colorblind mode", self.menubar)
        self.quickcolorAction.setCheckable(True)
        self.quickcolorAction.setChecked(False)
        
        self.morecolorAction = QAction("&More colors", self.menubar)
        
        
        # -- connect the actions to their functions -- #
        self.fillAction.triggered.connect(self.fill_peak)
        self.seqAction.triggered.connect(self.show_sequence)
        self.quickcolorAction.triggered.connect(self._set_to_colorblind_mode)
        self.morecolorAction.triggered.connect(self._show_more_color_options)
        
        # -- add the actions to the trace menus under specific order -- #
        self.menu = self.menubar.addMenu("&Traces")
        self.menu.addAction(self.seqAction)
        self.menu.addAction(self.fillAction)
        self.menu.addAction(self.quickcolorAction)
        #self.menu.addSeparator()
        #self.menu.addAction(self.morecolorAction) # will be a new feature for next release
        

    def fill_peak(self):
        ''' enable or disable color fill or the area under chromatograms '''
        
        # -- fill the chromatograms or not -- #
        if self.main.plot.fill == True:
            self.main.plot.fill = False
            self.fillAction.setChecked(False)
        else:    
            self.main.plot.fill = True
            self.fillAction.setChecked(True)
            
        self.main.plot.create_plot()
        
    def show_sequence(self):
        ''' show / hide sequence below the trace plot '''
        
        status = self.main.plot.display_sequence
        
        if status == True:
            self.main.plot.display_sequence = False
            self.main.plot.show_sequence.hide_sequence_from_traces()
        else:
            self.main.plot.display_sequence = True
            self.main.plot.show_sequence.show_sequence_from_traces()
        
        
    def _set_to_colorblind_mode(self):
        ''' activate / deactivate colorblind mode of the trace '''
        
        
        if  self.main.plot.colormode == "colorblind":
            self.main.plot.color_palette = self.main.plot.color.palettes["regular"]
            self.main.plot.colormode = "regular"
        else:
            self.main.plot.color_palette = self.main.plot.color.palettes["colorblind"]
            self.main.plot.colormode = "colorblind"
        
        self.main.plot.create_plot()
        
    def  _show_more_color_options(self):
        ''' display more color options '''
    
        self.color_options = ColorWindow()
        self.color_options.show()
   
        ## this part is not finished, may be released in another update
        
   
#################################################
# ANALYSIS MENU
#################################################
class AnalysisMenu:
    
    ''' create the menu to choose your analysis to perform '''
    
    def __init__(self, menubar, main):
        
        super().__init__()
        
        self.menubar = menubar
        self.main = main

        self.alignAction = QAction("&Align sequences", self.menubar)
        self.mismatchAction = QAction("&Find mismatches", self.menubar)
        self.quantAction = QAction(QIcon("://icons/batch_quantification.png"), "&Quantify mismatch", self.menubar)
        self.exportsubseqAction = QAction(QIcon("://icons/batch_svg_export.png"), "&Export sequence subsets", self.menubar)
        
        self.alignAction.triggered.connect(self.show_alignment_window)
        self.quantAction.triggered.connect(self.quantify_peak)
        self.exportsubseqAction.triggered.connect(self.export_svg)
        self.mismatchAction.triggered.connect(self.show_mismatches_across_seq)
        
        ## Add action to the menu
        self.menu = self.menubar.addMenu("&Analyses")
        self.menu.addAction(self.alignAction)
        self.menu.addSeparator()
        self.menu.addAction(self.mismatchAction)
        self.menu.addAction(self.quantAction)
        self.menu.addAction(self.exportsubseqAction)
    
    def quantify_peak(self):
        
        self.mm = ExportQuantification(self.main)
        self.mm.show()
        
    def export_svg(self):
        
        self.export_svg = ExportSVG(self.main)
        self.export_svg.show()
    
    def show_mismatches_across_seq(self):
        
        self.m = QuantifyWholeSeq(self.main)
        self.m.show()
    
    def show_alignment_window(self):
        
        self.w = AlignmentWindow(self.main)
        self.w.show()
  
#################################################
# HELPMENU
#################################################


class HelpMenu():
    
    ''' CREATE THE HELP MENU TO SEND TO DOCUMENTATION '''
    
    def __init__(self, menubar):
        
        super().__init__()

        # create actions on menubar
        self.menubar = menubar
        self.menubar.addMenu("&Help")
   
        
   
#################################################
# MENUBAR
#################################################

class MenuBar(QMainWindow):
    
    ''' create the menubar of the application '''
    
    def __init__(self, main):
        
        super().__init__()
        
        self.main = main
        self.menubar = self.main.menuBar()
        
        # 
        self.filemenu = FileMenu(self.menubar, self.main)
        self.editmenu = EditMenu(self.menubar, self.main)
        self.viewmenu = ViewMenu(self.menubar, self.main)
        self.tracemenu = TracesMenu(self.menubar, self.main)
        self.analysismenu = AnalysisMenu(self.menubar, self.main)
        self.helpmenu = HelpMenu(self.menubar)
        
        self.activate_actions(False)
        
    def activate_actions(self, status):
        ''' activate the actions of after loading the data '''
        
        # from the filemenu
        self.filemenu.exportAction.setEnabled(status)
        
        # from the edit menu
        self.editmenu.reverseAction.setEnabled(status)
        self.editmenu.trimAction.setEnabled(status)
        
        # from the view menu
        self.viewmenu.dnaseqAction.setEnabled(status)
        self.viewmenu.qualityAction.setEnabled(status)
        
        # from the tracemenu
        self.tracemenu.seqAction.setEnabled(status)
        self.tracemenu.fillAction.setEnabled(status)
        self.tracemenu.quickcolorAction.setEnabled(status)
        
        # from the analysismenu
        self.analysismenu.quantAction.setEnabled(status)
        self.analysismenu.exportsubseqAction.setEnabled(status)
        self.analysismenu.alignAction.setEnabled(status)
        self.analysismenu.mismatchAction.setEnabled(status)
        