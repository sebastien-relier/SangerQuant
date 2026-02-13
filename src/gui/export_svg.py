#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 07:09:46 2024

@author: sebastien
"""


"""
Batch export of selected subsequences in SVG format
"""

import re
import math
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import (
    QWidget, QPushButton, QGridLayout, QListWidget,
    QSpinBox, QAbstractItemView, QFileDialog,
    QRadioButton, QMessageBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from qline import QHSeparationLine
from buttons import CancelButton, CreateLabel, HelpButton, EnterSequence


# ============================================================
#                       MAIN WINDOW
# ============================================================

class ExportSVG(QWidget):
    """Window used to preview and export subsequence traces"""

    def __init__(self, main):
        super().__init__(None)

        self.main = main
        self.setWindowTitle("SangerQuant - Batch Export of Selected Subsequences")
        self.resize(800, 600)

        self._create_widgets()
        self._create_canvas()
        self._create_layout()

        self.traceplotter = TracePlotter(self)

    # --------------------------------------------------------

    def _create_widgets(self):
        """Create UI widgets"""

        self.sample_list = SampleList(self.main.data)

        self.target_sequence = EnterSequence(
            placeholder="Enter the sequence subset to export (ex: GCATGGCNGTTCTT)"
        )

        self.number_of_peak = TraceExtraLength(self)

        self.apply = ApplyButton(self)
        self.export = ExportButton(self)
        self.cancel = CancelButton(self)
        self.help_button = HelpButton(name="export_svg")

        self.alert = Alert()

    # --------------------------------------------------------

    def _create_canvas(self):
        """Create matplotlib canvas"""

        self.fig, self.axes = plt.subplots()
        self.canvas = FigureCanvas(self.fig)

        # Remove all axes decorations
        for spine in self.axes.spines.values():
            spine.set_visible(False)

        self.axes.set_xticks([])
        self.axes.set_yticks([])

    # --------------------------------------------------------

    def _create_layout(self):
        """Create and arrange layout"""

        grid = QGridLayout()

        # Sequence input
        grid.addWidget(self.target_sequence, 0, 0, 1, 12)

        # Sample list
        grid.addWidget(CreateLabel(text="Select samples:"), 1, 0)
        grid.addWidget(self.sample_list, 2, 0, 9, 4)

        grid.addWidget(QHSeparationLine(), 11, 0, 1, 4)

        # Options
        grid.addWidget(CreateLabel(text="Number of surrounding peaks"), 12, 0, 1, 4)
        grid.addWidget(CreateLabel(text="Peaks:"), 13, 0)
        grid.addWidget(self.number_of_peak, 13, 1, 1, 3)

        # Buttons
        grid.addWidget(self.help_button, 14, 8)
        grid.addWidget(self.cancel, 14, 9)
        grid.addWidget(self.apply, 14, 10)
        grid.addWidget(self.export, 14, 11)

        # Plot canvas
        grid.addWidget(self.canvas, 1, 4, 13, 8)

        self.setLayout(grid)
        self.grid = grid


# ============================================================
#                       SAMPLE LIST
# ============================================================

class SampleList(QListWidget):
    """List of available samples"""

    def __init__(self, data):
        super().__init__()
        self.data = data
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.addItems(list(self.data.keys()))


# ============================================================
#                       TRACE PLOTTER
# ============================================================

class TracePlotter:
    """Handle trace extraction and plotting"""

    def __init__(self, window):
        self.window = window
        self.colors = {"G": "black", "T": "red", "A": "green", "C": "blue"}

    # --------------------------------------------------------

    def create_plot(self):
        """Create figure from selected samples"""

        sequence = self.window.target_sequence.text()

        # Validate input
        if self.window.alert.control_input_sequence_requirement(sequence) == "FAILED":
            return

        self._filter_matching_samples()
        self._prepare_data()

        n = len(self.window.sample_to_analyze)
        rows, cols = self._get_smallest_grid(n)

        self.window.fig, self.window.axes = plt.subplots(rows, cols)

        self._plot_traces(n, rows, cols)

        if n < len(self.window.sample_list.selectedItems()):
            self.window.alert.warning_unmatch_seq()

    # --------------------------------------------------------

    def _plot_traces(self, n, rows, cols):
        """Plot all traces"""

        fontsize = 40 ** (18 / (18 + n))

        axes = self.window.axes
        if not (rows == 1 and cols == 1):
            axes = axes.flatten()

        for i in range(n):
            subset = self.subset_data[i]
            trace = subset["Trace"]
            start = subset["Start"]
            end = subset["End"]

            ax = axes if (rows == 1 and cols == 1) else axes[i]

            for nuc in trace.keys():
                ax.plot(trace[nuc][start:end], color=self.colors[nuc])

            ax.axis("off")
            ax.set_title(subset["Name"], fontsize=fontsize)

        # Remove extra axes
        total = rows * cols
        if total > n:
            for ax in axes[n:]:
                ax.remove()

    # --------------------------------------------------------

    def _filter_matching_samples(self):
        """Keep only samples matching query sequence"""

        selected = [item.text() for item in self.window.sample_list.selectedItems()]
        query = self.window.target_sequence.text().replace("N", ".")

        unmatched = []

        for sample in selected:
            seq = self.window.main.data[sample]["Seq"]
            if re.search(query, seq) is None:
                unmatched.append(sample)

        self.window.sample_to_analyze = list(set(selected) - set(unmatched))
        self.window.alert.unmatch = unmatched

    # --------------------------------------------------------

    def _prepare_data(self):
        """Extract subset data for plotting"""

        query = self.window.target_sequence.text().replace("N", ".")
        self.subset_data = {}

        for i, sample in enumerate(self.window.sample_to_analyze):

            data = self.window.main.data[sample]

            seq = data["Seq"]
            ploc = list(data["Ploc"])
            traces = data["Traces"]

            limits, subseq = self._get_plot_limits(query, seq, ploc)
            start, end = limits

            self.subset_data[i] = {
                "Name": sample,
                "SubSequence": subseq,
                "Trace": traces,
                "Start": start,
                "End": end,
            }

    # --------------------------------------------------------

    def _get_smallest_grid(self, n):
        """Return optimal rows/cols grid"""

        m = math.floor(math.sqrt(n))

        if m * m >= n:
            return m, m

        return m, math.ceil(n / m)

    # --------------------------------------------------------

    def _get_plot_limits(self, subseq, full_sequence, ploc):
        """Compute trace boundaries"""

        surrounding = self.window.number_of_peak.value()
        match = re.search(subseq, full_sequence)

        target_pos = subseq.find(".")
        ploc = list(ploc)

        if match is not None:
            left = match.span()[0] + target_pos - surrounding - 1
            right = match.span()[0] + target_pos + surrounding + 1
            return [ploc[left], ploc[right]], match[0]

    # --------------------------------------------------------

    def preview_plot(self):
        """Refresh canvas preview"""

        canvas = FigureCanvas(self.window.fig)
        canvas.draw()
        self.window.grid.addWidget(canvas, 1, 4, 12, 8)


# ============================================================
#                       UI COMPONENTS
# ============================================================

class TraceExtraLength(QSpinBox):
    """Spinbox controlling surrounding peak count"""

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.setValue(2)
        self.setMinimum(0)
        self.setMaximum(10)


class ApplyButton(QPushButton):
    """Preview button"""

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.setText("Preview")
        self.setIcon(QIcon(":/icons/preview.png"))
        self.clicked.connect(self.create_preview_plot)

    def create_preview_plot(self):
        self.window.traceplotter.create_plot()
        self.window.traceplotter.preview_plot()


class ExportButton(QPushButton):
    """Export button"""

    def __init__(self, window):
        super().__init__()
        self.window = window
        self.setText("Export")
        self.setIcon(QIcon(":/icons/export2.png"))
        self.clicked.connect(self.export_svg)

    def export_svg(self):
        self.window.traceplotter.create_plot()
        self.window.traceplotter.preview_plot()

        dialog = QFileDialog(self)
        dialog.setWindowTitle("Save as")
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dialog.setViewMode(QFileDialog.ViewMode.Detail)
        dialog.setNameFilter(".png;;.tiff;;.jpg;;.svg;;")

        if dialog.exec():
            file_path = dialog.selectedFiles()[0]
            file_filter = dialog.selectedNameFilter()
            plt.savefig(file_path + file_filter)


# ============================================================
#                       ALERT SYSTEM
# ============================================================

class Alert(QWidget):
    """Handle warning and error messages"""

    def __init__(self):
        super().__init__(None, Qt.WindowStaysOnTopHint)

        self.msg = QMessageBox()
        self.unmatch = []

        self.wrong_sequence = self._create_alert(
            icon=QMessageBox.Critical,
            title="Error ! Wrong input sequence",
            text=(
                "The input sequence is missing critical informations:\n"
                "- Sequence must contain a letter N\n"
                "- Sequence can't be shorter than 10 nucleotides\n\n"
                "Example: GCATGGCNGTTCTT"
            )
        )

    # --------------------------------------------------------

    def control_input_sequence_requirement(self, sequence):
        if "N" not in sequence:
            self.wrong_sequence.show()
            return "FAILED"

        if len(sequence) < 10:
            return "FAILED"

    # --------------------------------------------------------

    def _create_alert(self, icon=None, title=None, text=None):
        self.msg.setIcon(icon)
        self.msg.setWindowTitle(title)
        self.msg.setText(text)
        return self.msg

    # --------------------------------------------------------

    def warning_unmatch_seq(self):
        if not self.unmatch:
            return

        text = "Warning ! Queried sequence not found in:"
        for sample in self.unmatch:
            text += f"\n{sample}"

        msg = self._create_alert(
            icon=QMessageBox.Warning,
            title="Warning ! Sequence not found",
            text=text,
        )
        msg.show()
          