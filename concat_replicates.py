import os
import re
import csv
import pandas as pd
import argparse
from collections import defaultdict as dd
from collections import OrderedDict as od

# set command line arguments
parser = argparse.ArgumentParser(description='concatenates csv files based on metadata')
parser.add_argument('metadatafile', help='file containing list of files and metadata')
parser.add_argument('csvdir',help='directory containing csv files to be concatenated')
parser.add_argument('-o','--outputdir', help='where to write the output files',default='outdir')

# given the code for an experiment and the list of files 
# for each replicate, read each file and concatenate into 
# a single csv file
def concat(code,replist):
    #print "code:",code
    # want to output in order of replicate
    ordered_dict = od(sorted(replist.items(), key=lambda x:int(x[0])))
    dataframes=[]
    for rep,filelist in ordered_dict.items():
        for file in filelist:
            #print rep,file
            fullpath = args.csvdir+'/'+file+'_1.csv'
            if os.path.isfile(fullpath):
                df = pd.read_csv(fullpath)
                # add a replicate column
                df['replicate']=rep
                dataframes.append(df)
            else:
                print "no file",fullpath
        # add replicate column to dataframe
    
    # concatenate and output to csv, ignoring the index    
    uberdf = pd.concat(dataframes,ignore_index=True)
    outputfile = args.outputdir+'/'+code+'.csv'
    print outputfile
    uberdf.to_csv(outputfile,index=False)

def main(args):
    df = pd.read_csv(args.metadatafile)
    if not os.path.exists(args.outputdir):
        os.makedirs(args.outputdir)
        
    # drop rows that describe metadata sheets only (no Code)
    df.dropna(subset=['Code'],inplace=True)
    
    # remove the rows where Conditions are undefined
    undef="undefined"
    df = df.query('Conditions != @undef')
    
    # make a dictionary to store, for each code, the list of 
    # filenames for each replicate
    codemap = dd(lambda: dd(list))
    for row_index, row in df.iterrows():
        filename = row['Filename']
        code = row['Code']
        # extract the replicate and then remove to get code only
        pattern = re.compile('-(\d+)')
        m = re.search(pattern,code)
        replicate = m.group(1)
        codeonly = re.sub(pattern,'',code)
        #print filename,code,codeonly,replicate
        codemap[codeonly][replicate].append(filename)
        
    for code,replist in codemap.items():
        concat(code,replist)
        #for rep,files in filelist.items():
            #print code,rep,files
            

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)
