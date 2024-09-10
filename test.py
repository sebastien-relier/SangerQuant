#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 22:18:50 2024

@author: sebastien
"""

import pyqtgraph as pg
from PyQt5.QtGui import QColor

# Define the x-axis labels and corresponding colors
x_labels = ['A', 'B', 'C', 'D']
colors = [QColor(255, 0, 0),  # Red
          QColor(0, 255, 0),  # Green
          QColor(0, 0, 255),  # Blue
          QColor(255, 255, 0)]  # Yellow

# Create a custom colormap
color_map = pg.ColorMap(pos=[0.0, 0.25, 0.5, 0.75, 1.0],  # Position of colors
                        color=colors)  # Corresponding colors

# Create a plot widget
pw = pg.plot()

# Assign the custom colormap to the x-axis
pw.getAxis('bottom').setTicks([[(i, x_labels[i]) for i in range(len(x_labels))]], [color_map])

# Example data
x = [0, 1, 2, 3]
y = [10, 20, 15, 25]

# Plot the data
pw.plot(x, y, pen=None, symbol='o')
pg.QtGui.QApplication.exec_()