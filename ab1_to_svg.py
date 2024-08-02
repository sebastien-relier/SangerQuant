# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 09:57:10 2023

@author: reliersl
"""

## IMPORT PACKAGES
import sys
import argparse
import re
import matplotlib.pyplot as plt
import os

from ImportDataset import ImportAb1


def subseq_not_match(data):
    
    # extract file whose subsequence is not here
    unmatch = []
    for key in data:
        
        seq = data[key]["Sequence"]
        match = re.search(subseq, seq)
        
        if match is None:
            unmatch.append(key)
            
    return unmatch


def create_matching_error(unmatch):
    
    if unmatch != []:
        
        print(" \n ERROR ! The Targeted Sequence Is Not Found In The Following Files : \n")
        
        for f in unmatch:
            print("- ", f)
        print("\n Exit program")
    
        sys.exit(0)
    else:
        pass

def get_plot_limits(subseq, full_sequence):
    
    match = re.search(subseq, full_sequence)
    
    
    left = int(match.span()[0])
    right = int(match.span()[1])
    limits = [ploc[left - 1 - int(args.window)], ploc[right + 1 + int(args.window)]]

    return limits


def get_divisors(n):
    
    if n == 1:
        return 1, 1
    else:
    
        res = [i for i in range(1, n)]
    
        res.sort(reverse= True)
    
        for i in res:
            
            if n%i == 0:
                break
            else:
                continue
        
        c = int(n / i)
        print(c)
        
        return int(c), int(i)

def create_sanger_plot(traces, limits, title):
    
    # create the line plot of sanger traces
    
    colors = ["black","green","red","blue"]
    for key, col in zip(traces,colors):
            #
            tmp = list(traces[key][limits[0]:limits[1]])
            
            plt.plot(tmp, c = col)
            plt.title(title)
            
            # remove ticks
            plt.tick_params(left=False, labelleft=False) #remove ticks
            plt.tick_params(bottom=False, labelbottom=False) #remove 
            
            # remove frame
            plt.box(False)
            
    

def extract_data_from_dataset(filename):
    
    # extract the sequence, peak location (ploc), and x,y value (traces) from a ab1 file store in dataset dict
    
    sequence = sanger.dataset[filename]["Sequence"]
    ploc = sanger.dataset[filename]["Peak_location"]
    traces = sanger.dataset[filename]["Traces"]
    
    return sequence, ploc, traces

## MAIN
if __name__=="__main__":
    
    usage = "Reads ab1 file and extracts sequence"
    
    ## --------- 
    ## CREATE ARGUMENTS
    parser = argparse.ArgumentParser(
                    prog = 'SangerVG',
                    description = 'Reads ab1 file and export a subsequence to svg format',
                    epilog = 'Text at the bottom of help')
          
    # File import 
    file_import = parser.add_mutually_exclusive_group(required = True)          
    file_import.add_argument("-f", "--filenames", nargs = "+", default = None)
    file_import.add_argument("-F", "--batch", nargs= 1, default = None) 
    
    parser.add_argument("-s", "--subseq", required = True)
    parser.add_argument("-w", "--window", default = 0)
    parser.add_argument("-e", "--export", default = "preview")
    parser.add_argument("-o", "--output", default = False, type = str)
    args = parser.parse_args()
    
    
    # ----------
    ## Quality control before import 
    '''
    if (".ab1" in args.filenames) == False:
        print("Wrong filename extension. Must be ab1 file")
        sys.exit(0)
    '''
    # ---------
    ## CHECK THE SEQUENCE
    count = [args.subseq.count(x) for x in ["G","A","T","C","*"]]
    if (sum(count) != len(args.subseq)):
        print("Wrong Alphabet ! Sequence must be G,A,T,C or * for any letter")
           
    # 
    subseq = args.subseq.replace("*",".")    
    
    
    
    ## import dataset
    if args.batch != None:
        
        batch = args.batch[0]
        
        tmp = os.listdir(batch)
        filenames = [batch + x for x in tmp if (".ab1" in x)]
    else:
        filenames = args.filenames
    
    
    
    # parse ab1 files
    sanger = ImportAb1(filenames)
            
    # control the presence of the target sequence in the main sequence
    unmatch = subseq_not_match(sanger.dataset)     
    
    # display error if there is any
    create_matching_error(unmatch)
    
    
    
    # CREATE THE GRID PLOT

    # define plot grid row and columns
    number_of_plot = len(filenames)
    row, col = get_divisors(number_of_plot)
    
    plt.figure(0)
    k = 0
    for i in range(row):
        
        for j in range(col):
            
            plt.subplot2grid((row,col), (i,j))
    
            # get current file to process
            filename = list(sanger.dataset.keys())[k]
            
            # extract sequence, peak loc and traces from dataset
            full_sequence, ploc, traces = extract_data_from_dataset(filename)
            
            # get the limits of the plots
            limits = get_plot_limits(subseq, full_sequence)
        
            
            create_sanger_plot(traces, limits, filenames[k - 1])
    
            k += 1
            
            
    # create output filename
    if args.output == False:
        output_filename = args.filenames[-1].replace(".ab1","")
    else:
        output_filename = args.output
    
   
    # export or preview the results
    if args.export == "preview":
        plt.show()
    elif args.export == "export":
        plt.savefig("{}.svg".format(output_filename), format="svg", dpi=200)
    else:
        print("Wrong argument")
        sys.exit(0)
    
    
        
        
        
        