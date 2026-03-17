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
However, existing software tools are limited to Sanger trace visualization and basic DNA sequence identification.  A critical gap exists in software capable of quantifying peak heights from several files at once. SangerQuant allows quantification nucleotide mismatch proportion in several samples
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

## Windows
This app is available as a standalone executable. Download the sangerquant zip folder [here](https://github.com/sebastien-relier/SangerQuant/releases/tag/v1.0.0)

### Instructions

# Tutorial
## How to Quantify Mismatch
### Quantify peaks height at a specific position from a single trace
- Left-click on a peak from the trace to quantify peak heights, raw value will appear below the sample list on the bottom left

### Batch quantify mismatch at a specific position
- Navigate to Analyses > Quantify mismatch in the menu.
- In the popup window, enter your sequence in the top textbox.
    - Replace the base you want to quantify with an N.
    - Example: To quantify the base at the position marked as C% in GCATGGCC%GTTCTT, enter GCATGGCNGTTCTT.
- From the list, use your left mouse button to select the samples you want to analyze.
- Adjust the combobox values to specify the mutation you want to quantify.
 - Click Preview to display the quantification results in the table.
- To export:
   - Use the Export button to save all data.
   - Or, right-click on specific rows, select Copy, and paste into your preferred worksheet software (e.g., Excel).

## How to Identify Mismatches De Novo
1. Access the De Novo Mismatch Identification Tool
    - Navigate to Analyses > Find mismatches in the menu.   
2. Select Samples
    - From the list, use your left mouse button to select the samples you want to analyze.
4. Load the Reference Sequence
    - Paste your reference sequence in FASTA format into the textbox below the sample list.
5. Navigate the Mismatch Plot
    - Use your scroll wheel to zoom in or out.
    - Click on a bar of interest to display its position in the main window.
6. Export the Mismatch Plot
    - Click the Export button to save the plot.








