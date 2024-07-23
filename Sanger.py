# -*- coding: utf-8 -*-
# reliersl 10/27/2022

## IMPORT PACKAGES
import argparse
import sys
import pandas as pd
import os
from ab1Parser import ab1Parser


cb = {
      "DATA9":"G",
      "DATA10":"A",
      "DATA11":"T",
      "DATA12":"C",
      }


class CheckArg:

    ''' Check the input into the program '''
    
    def __init__(self):
    
        super().__init__()
        pass

    def check_format(self, file):

        if (".ab1" in file):
            pass
        else:
            print("Error, input file is not in ab1 format !")
            sys.exit(0)

    def seq_exist(self, seq = None):
        
        if seq is None:
            print("Error, sub sequence does not exist ! Enter the sequence after -s flag")
            sys.exit(0)
        
    def convert_seq_to_regex(self, seq = None):
        
        if ('/' in seq):
            seq = seq.replace("/","|")
            
        return seq
            
    def check_base(self, seq = None):
        
        bases = ["G", "A", "T", "C", "/", ".", "*"]
            
        count = [seq.count(b) for b in bases]
        
        if sum(count) != len(seq):
            print("Error, the sequence has non canonical base ! /n The sequence must be composed of : G,A,T,C, / or N")
            sys.exit(0)
        
        
## MAIN
if __name__=="__main__":
    
    usage = "Reads ab1 file and extracts sequence"
    
    ## --------- 
    
    # CREATE ARGUMENTS
    parser = argparse.ArgumentParser(
                    prog = 'SangerVG',
                    description = 'Reads ab1 file and export a subsequence to svg format',
                    epilog = 'Text at the bottom of help')
                    
    parser.add_argument("-f", "--filename")    
    parser.add_argument("-s", "--subseq")
    parser.add_argument("-b", "--batch")
    parser.add_argument("-t", "--transition", default="all")
    args = parser.parse_args()
    
    # ----------
    
    # process subseq to look at
    
    target = args.subseq
    base_to_quant = target.find("*")
    target = target.replace("*","")
    

    
    
    
    # import files
    dirs = os.listdir(args.batch)
    
    for d in dirs:
        print(d)
        if (".ab1" in d) == False:
            continue
        
        ## create filepath
        filepath = args.batch + "/" + d
        print(filepath)
        
        # Check filename extension
        checkarg = CheckArg()
        checkarg.check_format(filepath)
        
        # Check subsequence
        checkarg.seq_exist(args.subseq)
        checkarg.check_base(args.subseq)
        
        subseq = checkarg.convert_seq_to_regex(args.subseq)
        
        ## ----------
        
        ## IMPORT SEQUENCES AND DATA FROM TRACES
        process_abi = ab1Parser()
        
        seq = process_abi.import_seq(filepath)
        traces = process_abi.get_traces(filepath)
        plocs = process_abi.get_ploc(filepath)
        
        
        
        res = {}
        for data in ["DATA9", "DATA10", "DATA11", "DATA12"]:
            
            trace = traces[data]
            
            tmp = []
            for p in plocs:
            
                tmp.append(trace[p])
              
            res[data] = tmp
        
        
        df = pd.DataFrame(res)
        df.columns = ["G","A","T","C"]
        df["Sequence"] = list(seq)
        
        print(df)
        
        ## check subsequence existence
        pos = seq.find(target)
        
        #print(df.iloc[213:225,:])
        subset = df.iloc[pos:pos+len(subseq),:]
        print(subset)
        
        
        
        sys.exit(0)
        df = df[["Sequence", "G","A","T","C"]]
    
       
        output_filename = filepath.replace(".ab1", "_quantifications_heights.csv")
    
    
        
        
        df.to_csv(output_filename, sep = ",", index = False)
        
        print(df)    
        
        
        
    
        
        
    
    
        
        
    
    
        



    

    
    

