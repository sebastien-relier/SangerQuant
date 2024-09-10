#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 13:08:15 2022

@author: sebastien
"""
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPainter, QIcon


import os


from viewsequence import ViewSequence
from ab1Parser import ab1Parser
from mismatch import Mismatch
from trace_options import TraceParameters
from export_quantification import ExportQuantification
from export_svg import ExportSVG


class FileMenu(QMainWindow):
    
    ''' CREATE THE FILEMENU OF THE APP AND ITS ASSOCIATED FUNCTIONS '''
    
    def __init__(self, menubar, main):
        
        super().__init__()
        
        self.menubar = menubar
        self.main = main
        
        # create filemenu actions
        openAction = QAction("Open", self.menubar)
        saveAction = QAction(QIcon("save.png"),"Save", self.menubar)
        exitAction = QAction(QIcon("exit.png"),"Exit",self.menubar)
        exportsvgAction = QAction("&Export svg", self.menubar)
        exportquantAction = QAction("&Export quantification", self.menubar)
    
    
        # linked menu to actions
        openAction.triggered.connect(self.open_ab1_file)
        exportsvgAction.triggered.connect(self.export_svg)
        #saveAction.triggered.connect(self.save_f)
        exitAction.triggered.connect(qApp.quit)
        
        # create the filemenu
        filemenu = self.menubar.addMenu("File")
        filemenu.addActions([openAction, saveAction, exportsvgAction, exportquantAction, exitAction])
        
    
    
    def open_ab1_file(self):
        
        # open ab1 file and parse data to store into dict
        filenames = QFileDialog.getOpenFileNames(filter = "*.ab1*")
        
        if filenames[0] == "":
            return
        
        self.parse_ab1_file(filenames)
        
    def export_svg(self):
        
        self.exportsvg = ExportSVG(self.main)
        self.exportsvg.show()
        
    
    def parse_ab1_file(self, filenames):
        
        # parse ab1 data
        parser = ab1Parser()
        data = {}
        for f in filenames[0]:
            
            name = os.path.basename(f)
            tmp = {"Ploc":parser.get_ploc(f), "Seq":parser.import_seq(f), "Traces":parser.get_traces(f), "Quant":parser.get_peak_heights(f)}
        
            self.main.data[name] = tmp 
            
            print(self.main.data[name]["Quant"])
            
        # add files to list
        self.main.samples.add_sample()
        self.main.samples.display_list()
    
        

class EditMenu(QMainWindow):
    
    ''' CREATE THE EDIT MENU OF THE APP '''
    
    def __init__(self, menubar, main):
        
        super().__init__()
        
        self.menubar = menubar
        

        editmenu = self.menubar.addMenu("Edit")

class ViewMenu(QMainWindow):
    
    ''' CREATE THE VIEW MENU OF THE APP '''
    
    def __init__(self, menubar, main):
        
        super().__init__()
    
        self.menubar = menubar
        self.main = main
        
        
        # create actions
        dnaseqAction = QAction("dna sequence", self.menubar)
        
        # connect menu
        dnaseqAction.triggered.connect(self.display_dna)
        
        # add menu 
        view = self.menubar.addMenu("View")
        view.addActions([dnaseqAction])
    
    def display_dna(self):
        
        self.viewseq = ViewSequence(self.main.data)
        self.viewseq.show()
    
   
    
    
    
    
class TracesMenu(QMainWindow):
    
    ''' CREATE THE TRACE MENU OF THE APP '''
    
    def __init__(self, menubar, main):
        
        super().__init__()
        
        self.menubar = menubar
        self.main = main
        
        # create actions
        alignAction = QAction("align traces", self.menubar)
        fillAction = QAction("Fill sanger", self.menubar)
        peakshapeAction = QAction("Set peak heights and widths", self.menubar)
        
        fillAction.triggered.connect(self.fill_peak)
        peakshapeAction.triggered.connect(self.change_peak_shape)
        
        tracesmenu = self.menubar.addMenu("Traces")
        tracesmenu.addActions([fillAction, peakshapeAction])


    def fill_peak(self):
        
        if self.main.plot.fill == True:
            self.main.plot.fill = False
        else:    
            self.main.plot.fill = True
            
        self.main.plot.create_plot()
        
    def change_peak_shape(self):
        
        self.parameters = TraceParameters(self.main)
        self.parameters.show()
        pass
        

class AnalysisMenu(QMainWindow):
    
    ''' CREATE THE VIEW MENU OF THE APP '''
    
    def __init__(self, menubar, main):
        
        super().__init__()
        
        self.menubar = menubar
        self.main = main

        quant = QAction("peak heights", self.menubar)
        
        quant.triggered.connect(self.quantify_peak)
        quantification = self.menubar.addMenu("Quantification")
        quantification.addActions([quant])
    
    def quantify_peak(self):
        
        self.mm = ExportQuantification(self.main)
        self.mm.show()
        










class MenuBar(QMainWindow):
    
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
        #slf.filemenu.openfile.triggered.connect(self.open_ab1_file)
        
        
        
        
        #EditMenu(self.menubar, self.main)
       
        
        
        
        
        '''
        ## CREATE ACTIONS
        viewsequence = QAction("Sequence", self.menubar)
        viewprotein = QAction("Protein sequence", self.menubar)
        
        
        viewsequence.triggered.connect(self.show_seq)
        viewprotein.triggered.connect(self.show_protein_seq)
        
        '''
        
        # CREATE MENUS
    
        

        '''
        self.editMenu = self.menubar.addMenu("Edit")
        
        
        # CREATE VIEW MENU
        self.viewMenu = self.menubar.addMenu("View")
        self.viewMenu.addActions([viewsequence, viewprotein])
        
        
        
        
        
        
        
        
        
        
        
        
        # CREATE ANALYSIS MENU
        self.analysisMenu = self.menubar.addMenu("Analysis")
        
        
        
        
        
        
        
        # CREATE HELP MENU
        self.helpMenu = self.menubar.addMenu("Help")
    
    
    
    
    def open_f(self):
        
        # THIS FUNCTION OPEN AND DECODE AB1 FILE
        
        filenames = QFileDialog.getOpenFileNames(filter = "*.ab1*")
        
        if filenames[0] == "":
            return
        
        ## CREATE FILE LIST
        self.list = FileList(self.window, filenames)
        self.list.show()
    
        self.window.dock.setWidget(self.list)
    
        ## CREATE PLOT AREAS
        self.window.sanger.data = filenames[0][0].split("/")[-1]
        self.window.sanger.current_path = filenames[0][0]
        
        self.window.sanger.read_ab1_file(self.window.sanger.current_path)
        self.window.sanger.create_canvas()
        self.window.sanger.create_plot()
    
    
    def save_f(self):
        pass
    
    
    def show_seq(self):
        seq = ViewSequence(self.window.sanger)
        seq.show()
        
    def show_protein_seq(self):
        seq = ProteinSequence(self.window.sanger)
        seq.show()
        
    '''