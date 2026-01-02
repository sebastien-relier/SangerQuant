# SangerQuant
SangerQuant is a Sanger trace viewer and a mismatch quantifier made with PyQt5.  <br> SangerQuant is specifically designed to ensure fast quantification of mismatch rates at any selected position. <br>
This application supports .ab1 file format as input.

<p align="center">
<img width="600" height="400" alt="Screenshot from 2025-10-30 16-08-01" src="https://github.com/user-attachments/assets/2fc2cff0-9330-41e2-8336-3d5def48e828" align="middle" />
</p>

# Statement of Need
<p align="justify"> 
Sanger sequencing remains the gold standard for identifying individual DNA sequences. Beyond sequence identification, it enables quantification of mismatch rates at specific positions by comparing the heights of overlapping peaks. This capability is invaluable for assessing the stoichiometry of RNA modifications, such as m5C, m7G, m1A, and ac4C, and for identifying genetic variants in mixed DNA populations. 
<br>
<br>
However, existing software tools are limited to Sanger trace visualization and basic DNA sequence identification.  A critical gap exists in software capable of precisely quantifying peak heights to accurately determine mismatch rates. SangerQuant fills this gap by integrating Sanger trace visualization with advanced mismatch identification and quantification.
</p>

# Key features
- Supports .ab1 file format
- Visualize individual Sanger Traces
- Quantify the heights of overlapping peaks to identify mismatch rate at any position
- Analyze mismatch rate across samples for comparison
- Cross-samples comparison of sequence quality to ensure dataset reliability
- Subset Traces and export into svg format for quick embedding into scientific articles

# Installation
## Linux
This app is available as a standalone executable. Download the sangerquant zip folder [here](https://github.com/sebastien-relier/SangerQuant/releases/tag/v1.0.0)

### Instructions
- Download sangerquant.zip <br>
- Open Terminal (Ctrl + Alt + T) <br>
- cd *directory*. Replace *directory* with the directory path containing sangerquant.zip <br>
- unzip sangerquant.zip <br>
- Run sangerquant with the command: cd sangerquant; ./sangerquant <br>

# Tutorial
## Import data
- Click on "File" of the menubar and click on "Import" <br>
- Select .ab1 files from sanger traces and click open. Use mouse left click while pressing *shift* to select multiple files <br>
- Click open on the pop-up window to import the selected files

## Explore traces
- Click on a filename in the list to display the trace
- Use the scrollbar at the top or your mouse wheel to navigate along the sequence
- To navigate directly to a specific sequence in the trace, enter the sequence in the textbox located below the trace

## Change trace appearance
- Show/Hide the sequence below the trace by clicking on "Trace" and Check/Uncheck "Show_sequence"
- Fill/Unfill the area under curve by clicking on "Trace" and Check/UnCheck "Fill"
- Adjust peaks height through moving the left slidebar below the trace on the right
- Zoom-in or zoom-out by moving the right slidebar below the trace on the right
