#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 05:30:28 2024

@author: sebastien
"""


# -- IMPORT PACKAGES -- #
from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QComboBox, QLineEdit, QListWidget, QMessageBox, QAbstractItemView, QGridLayout, QFileDialog
from PyQt5.QtGui import QRegExpValidator, QIcon
from buttons import CancelButton, HelpButton, CreateLabel
from quantification_table import PeakQuant
from export_to_csv import ExportToCsv
from qline import QHSeparationLine
import re


# -- IMPORT CLASS -- #
class ExportQuantification(QWidget):

    ''' THIS CLASS CREATES THE WINDOW TO EXPORT THE QUANTIFICATION '''

    def __init__(self, main):

        super().__init__(None, Qt.WindowStaysOnTopHint)

        self.setWindowTitle("TraceQ - Batch Quantification of Mismatch")
        
        # Import data
        self.main = main

        # Init values
        self.create_widgets()
        self.create_layout()

        self.show()

    def create_widgets(self):

        # create list of sample
        self.sample_list = FileList(self, [key for key in self.main.data])

        self.queried_sequence = QueriedSequence()

        # -- create the widgets to select the transition -- #
        self.canonical = SelectBase(self, basedefault = "C")
        self.noncanonical = SelectBase(self, basedefault = "T")
        self.transition = ShowTransition(self)

        # -- create calculate button -- #
        self.calc = Calculator(self)

       
        # -- create buttons to execute the functions or close the window -- #
        self.cancelbutton = CancelButton(self)
        self.previewbutton = PreviewButton(self.calc)
        self.exportbutton = ExportButton(self)
        self.helpbutton = HelpButton("test")

         # -- create table to store results -- #
        self.results = PeakQuant(self, header = ["Samples", "Mismatch"], nrow = 10, ncol = 2)
        
    def create_layout(self):

        self.layout = QGridLayout(self)

        # add the QLineEdit to select the target sequence
        self.layout.addWidget(self.queried_sequence, 0, 0, 1, 10)

        # add the sample list
        self.layout.addWidget(self.sample_list, 1, 0, 4, 3)
        self.layout.addWidget(QHSeparationLine(),5,0,1,4)
        self.layout.addWidget(CreateLabel(text="Select Mismatch to Quantify"), 6,0,1,4)

        # create the widgets to select the transition
        self.layout.addWidget(self.canonical, 7, 0)
        self.layout.addWidget(self.noncanonical, 7, 1)
        self.layout.addWidget(self.transition, 7, 2, 1, 1)


        # -- add the button to execute the functions -- #
        #self.layout.addWidget(self.helpbutton, 7,4)
        self.layout.addWidget(self.cancelbutton, 8, 6)
        self.layout.addWidget(self.previewbutton, 8, 7)
        self.layout.addWidget(self.exportbutton, 8, 8)
        
        # -- add the table to the layout -- #
        self.layout.addWidget(self.results, 1, 4, 7, 6)

        self.layout.setColumnStretch(4, 1)
        self.setLayout(self.layout)




class PreviewButton(QPushButton):

    ''' CREATE THE BUTTON TO PREVIEW THE DATA INTO A QTABLEWIDGET '''

    def __init__(self, calculator):

        super().__init__()

        self.calculator = calculator

        self.setText("Preview")
        self.setIcon(QIcon(":/icons/preview.png"))
        self.clicked.connect(self.on_click)

    def on_click(self):

        self.calculator.on_click()
        self.calculator.update_table()



class ExportButton(QPushButton):

    ''' CREATE THE BUTTON TO EXPORT THE DATA INTO CSV FILE FORMAT '''

    def __init__(self, window):

        super().__init__()

        self.window = window

        self.setText("Export")
        self.setIcon(QIcon(":/icons/export2.png"))
        self.clicked.connect(self.on_click)

    def on_click(self):

        self.window.calc.on_click()
        self.window.calc.update_table()
        self.export_data_to_csv()

        
    def export_data_to_csv(self):
        
        export = ExportToCsv()
        
        file_dialog = QFileDialog(self)
        file_dialog.setWindowTitle("Save File")
        file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        file_dialog.setViewMode(QFileDialog.ViewMode.Detail)
        
        if file_dialog.exec():           
            selected_file = file_dialog.selectedFiles()[0]
            print("Selected File for Saving:", selected_file)

            export.export_to_csv(output_filename=selected_file, headers = self.window.results.header, data=self.window.calc.res)   
        


class Calculator:

    ''' CALCULATES TRANSITION AND WRITE RESULTS IN A QTABLEWIDGET '''

    def __init__(self, window):

        super().__init__()

        self.window = window
        
        # -- get the transition to quantify -- #
        self.reference_nucleoside = self.window.canonical.currentText()
        self.nucleoside_to_quantify = self.window.noncanonical.currentText()
        self.transition = self.reference_nucleoside + ":" + self.nucleoside_to_quantify

        # -- get the samples to analyze -- #
        self.samples = self.window.sample_list.selected_samples

       

        # initialize the message boxes
        self.msg = MessageBoxes()

    def on_click(self):

        # -- extract the values of reference base and target to quantify -- #
        self.get_reference_and_target_base()


        # -- pipeline to quantify transition from large sets of samples -- #
        self.res = []
        for sample in self.samples:

            pos_of_target = self.get_position_of_nucleoside_to_quantify(sample)

            if pos_of_target is not None:
            
                peak_values = self.extract_peak_values_at_target_position(sample, pos_of_target)
            
                target_value = self.calculate_target_value(peak_values)
                
                reference_value = self.calculate_reference_value(peak_values)
        
                transition_value = self.calculate_transition(target_value, reference_value)

                self.res.append([sample, transition_value])
            else:
                self.res.append([sample, None])
            
    
    def get_reference_and_target_base(self):
        # extract the nucleoside of reference and the target from ComboBox to calculate desired transition (ex : C:T), 
        
        self.nucleoside_to_quantify = self.window.noncanonical.currentText()
        self.reference_nucleoside = self.window.canonical.currentText()
        
    
    def get_position_of_nucleoside_to_quantify(self, sample):
        # Get the position of nucleoside to quantify from the sequence
        
        queried_sequence = self.window.queried_sequence.text()    
        queried_sequence = queried_sequence.replace("N",".")
        
        # get position of the nucleoside to quantify within the sanger sequence
        pos = self.find_sequence(queried_sequence, self.window.main.data[sample]["Seq"])
        
        if pos is not None:
            pos = pos + queried_sequence.find(".")
            return pos
        else:
            return None

        

    def extract_peak_values_at_target_position(self, sample, pos):

        #  -- the area under peak or peak height --  #
        index = list(self.window.main.data[sample]["Height"].keys())[pos]
        peak = self.window.main.data[sample]["Height"][index]

        # convert to 1 if value is 0
        for key in peak:
        
            if peak[key] == 0:
                peak[key] = 1
            else:
                continue

        return peak

    def calculate_target_value(self, peak):

       value_of_target = peak[self.nucleoside_to_quantify]
       return value_of_target

    def calculate_reference_value(self, peak):

        value_of_reference = peak[self.reference_nucleoside]
        return value_of_reference

    def calculate_transition(self, target, reference):

        transition = (target / (target + reference)) * 100
        transition = round(transition, 2)
        return transition

    
    def update_table(self):
      
      # -- write the results into a QTableWidget -- #
      self.window.results.rename_headers(["Samples", self.reference_nucleoside + ":" + self.nucleoside_to_quantify + "(%)"])
      self.window.results.reset_table_values()
      self.window.results.update_table(data = self.res)



    def find_sequence(self, target_seq, seq):

        tmp = re.findall(target_seq, seq)

        if len(tmp) > 1:
            self.msg.show_multiple_occurence_warning()
            return
        elif len(tmp) == 0:
            return
        else:
            return seq.find(tmp[0])


class QueriedSequence(QLineEdit):

    ''' THIS CLASS CREATE THE QLINE EDIT WIDGET TO SELECT THE SEQUENCE TO QUANTIFY '''

    def __init__(self):

        super().__init__()

        self.create_validator()
        self.setPlaceholderText("Enter the sequence to search")

    def create_validator(self):
        # restricts input to G,A,T,C

        regex = QRegExp("[GATCN(|)*]+")
        validator = QRegExpValidator(regex)
        self.setValidator(validator)

            
class FileList(QListWidget):

    ''' SELECT THE SAMPLES TO ANALYZE '''

    def __init__(self, window, samples):

        super().__init__()

        self.window = window
    
        # add sample names
        self.addItems(samples)

        # allow multiple selection
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.itemClicked.connect(self.itemClicked_event)

        self.selected_samples = samples
         
    def itemClicked_event(self):

        self.window.calc.samples = [item.text() for item in self.selectedItems()]


class SelectBase(QComboBox):

    ''' CREATE A QCOMBOBOX TO CHOOSE THE TARGET BASE TO QUANTIFY '''

    def __init__(self, window, basedefault = "C"):

        super().__init__()

        self.window = window

        nucleotides = ["G","A","T","C"]
        index = nucleotides.index(basedefault)
        
        self.addItems(nucleotides)
        self.setCurrentIndex(index)

        self.currentIndexChanged.connect(self.on_changed)

    def on_changed(self):

        self.window.transition.update_transition()
    

class ShowTransition(QLineEdit):

    ''' CREATE A QLINEEDIT TO ENTER THE SELECT TRANSITION TO QUANTIFY '''

    def __init__(self, window):

        super().__init__()

        self.window = window

        self.setReadOnly(True)
        self.setText("C:T")

    def update_transition(self):
        
        txt = self.window.canonical.currentText() + ":" + self.window.noncanonical.currentText()
        self.setText(txt)




class MessageBoxes(QMessageBox):

    ''' CREATES THE QMESSAGE BOX TO GIVE WARNING OF SEVERAL SUBSQUENCE OCCURENCES '''

    def __init__(self):

        super().__init__()

        # -- CREATE A WARNING WHEN THE SUB SEQUENCE IS FOUND SEVERAL TIMES WITHIN THE MAIN SEQUENCE (only one occurence allowed) -- #
        self.occ = QMessageBox()
        self.occ.setIcon(QMessageBox.Warning)
        self.occ.setText(
            """
            In order to perform a batch quantification of variants across samples you must enter a query sequence of : \n 
                - At least 5 nucleotides long
                - Must  enter "N" at the position you want to quantify the transition
                - Must have a single occurence.
                
            """)
            

