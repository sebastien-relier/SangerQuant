#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 19:30:40 2022

@author: sebastien
"""

## LOAD PACKAGES 

from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QApplication, QSplashScreen
from PyQt5.QtGui import QPixmap
from menu import MenuBar
from layout import Layout
import sys
from time import time,sleep
import resources_rc

class Main(QMainWindow):

    ''' creates the main window with the menubar | toolbar | the layout '''
    
    def __init__(self):
        
        super().__init__()
        
        self.setWindowTitle("SangerQuant - Main Window")
        self.resize_window()
        
        ## -- create the menubar -- #
        self.menubar = MenuBar(self)
        
        # -- create the layout to add the QFileList and the graph area -- #
        self.layout_container = Layout()
        self.setCentralWidget(self.layout_container)
        
        # intialize the data storage # 
        self.data = {}
        
    def resize_window(self):
        
        screen_geometry = QDesktopWidget().screenGeometry()
        # Resize the window to match the screen size
        self.resize(screen_geometry.width(), screen_geometry.height())
        # Move the window to the top-left corner of the screen
        self.move(0, 0)
        
        
        
    
if __name__=="__main__":
    
    main = QApplication(sys.argv)
   
    # -- Splash QPixmap -- #
    splash_pixmap = QPixmap(":/icons/splash.png") # Replace with your image path
    splash = QSplashScreen(splash_pixmap)
    splash.show()
    
    start = time()
    while time() - start < 1:
       sleep(0.001)
       main.processEvents()
   
    # load and show the main screen
    screen = Main()
    screen.show()
    splash.finish(screen)

    sys.exit(main.exec_())
    