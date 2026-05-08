#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 19:30:40 2022

@author: sebastien
"""

## LOAD PACKAGES 


from PyQt6.QtWidgets import QMainWindow, QApplication, QSplashScreen
from PyQt6.QtGui import QPixmap, QGuiApplication
from menu import MenuBar
from layout import Layout
import sys
from time import time, sleep
from trace_color import Color
import resources_rc

class Main(QMainWindow):

    ''' creates the main window with the menubar | toolbar | the layout '''

    def __init__(self):

        super().__init__()

        self.setWindowTitle("SangerQuant - Main Window")
        self._resize_window()

        ## -- create the menubar -- #
        self.menubar = MenuBar(self)

        ## -- create the layout to add the QFileList and the graph area -- ##
        self.layout_container = Layout()
        self.setCentralWidget(self.layout_container)

        ## -- set trace color status -- ## 
        self.trace_color = Color()

        ## -- intialize the data storage -- ##
        self.data = {}

    def _resize_window(self):

        screen = QGuiApplication.primaryScreen().geometry()
        # Resize the window to match the screen size
        self.resize(screen.width(), screen.height())
        # Move the window to the top-left corner of the screen
        self.move(0, 0)

if __name__=="__main__":

    main = QApplication(sys.argv)
    
    screen = Main() # create MainWindow

    # create splash screen
    splash_pixmap = QPixmap(":/icons/splash.png") # Replace with your image path
    splash = QSplashScreen(splash_pixmap)
    
    # get screen geometry to place the splash in the middle
    screen_size = main.primaryScreen().geometry()
    splash.move(1200, 1200)
    
    
    splash.show()

    start = time()
    while time() - start < 1:
       sleep(0.001)
       main.processEvents()
    
    # load and show the main screen
    
    screen.show()
    

    sys.exit(main.exec())
    