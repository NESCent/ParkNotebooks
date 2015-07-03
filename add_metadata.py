# takes the list of filenames and codes and parses the codes, 
# adding metadata as per Park 1948
import re
import pandas as pd
import argparse

# set command line arguments
parser = argparse.ArgumentParser(description='use codes to add metadata columns to Park notebook file list')
parser.add_argument('inputfile', help='input csv file')
parser.add_argument('-o','--outputfile', help='where to write the output',default='out.csv')

# The first part of the code (I / II / III) defines the media volume
def parseVolume(codestr):
    resultDict = {'I':8,'II':40,'III':80}
    pattern = re.compile('^(I+)-')
    m = re.search(pattern,codestr)
    if (m):
    	result = resultDict[m.group(1)]
    	#print codestr,result
    	return result
    else:
		print "did not find volume in",codestr

# The second part of the code defines whether this is an 
# experiment ('E') or control ('C')
def parseExpType(codestr):
    resultDict = {'E':'experiment','C':'control'}
    pattern = re.compile('-([EC])-')
    m = re.search(pattern,codestr)
    if (m):
    	result = resultDict[m.group(1)]
    	#print codestr,result
    	return result
    else:
		print "did not find expType in",codestr

# The third part of the code defines the experimental conditions
# There are two sets of conditions; one for experiments (which define
# the relative abundance of species) and one for controls (which 
# defines the single species
def parseConditions(codestr,expType):
    # check for unknown codes
    if (checkUndefinedCode(codestr)):
        return "undefined"
    # dictionaries of code definitions
    controlConditions = {'b':'T. confusum','c':'T. castaneum'}
    expConditions = {'a':'b = c','b':'b > c','c':'b < c'}    
    pattern = re.compile('-([abc])-')
    m = re.search(pattern,codestr)
    result = ""
    if (m):
    	if (expType == 'experiment'):
    		result = expConditions[m.group(1)]
    	elif (expType == 'control'):
    	    result = controlConditions[m.group(1)]
    	#print codestr,result
        return result
    else:
        return None

# The (usually) last part of the code defines the replicate number
def parseReplicate(codestr):
    pattern = re.compile('-(\d+)')
    m = re.search(pattern,codestr)
    result = m.group(1)
    #print codestr,result
    return result
   
# Some of the populations were grown under parasite-free conditions, 
# indicated by a 'S' in the code
def parseSterile(codestr):
    pattern = re.compile('-S')
    if (re.search(pattern,codestr)):
        return "sterile"
    else:
        return "nonsterile"

# Some of the code contain extra two-letter identifiers
# (e.g. 'ee' or 'pp'). We don't know what these mean
def checkUndefinedCode(codestr):
    pattern = re.compile('-[a-z][a-z]-')
    if (re.search(pattern,codestr)):
        return True
    else:
        return False
        
def main(args):
    df = pd.read_csv(args.inputfile)
    codes = df['Code']
    pattern = re.compile('^I')
    volumes=[]
    expTypes=[]
    conditions=[]
    replicates=[]
    sterile=[]
    for c in codes:
        if not (pd.isnull(c)):
            if (re.match(pattern,c)):
            	volumes.append(parseVolume(c))
            	expType = parseExpType(c)
                expTypes.append(expType)
                conditions.append(parseConditions(c,expType))
                replicates.append(parseReplicate(c))
                sterile.append(parseSterile(c))
                #print c,volume,expType,condition,replicate
            else:
                print c,"not null, no match"
        else:
            volumes.append(None)
            expTypes.append(None)
            conditions.append(None)
            replicates.append(None)
            sterile.append(None)
            
    newdf = pd.DataFrame({"Filename":df['filename'],
        "Code":codes,
        "Volume":volumes,
        "ExperimentType":expTypes,
        "Conditions":conditions,
        "Replicate":replicates,
        "Sterile":sterile,
        "Date started":df['Date started'],
        "Comment":df['Comment']})
    df3 = newdf.set_index('Filename')
    df3.to_csv(args.outputfile,columns=['Code','Volume','ExperimentType','Conditions','Replicate','Sterile','Date started','Comment'])

if __name__ == '__main__':
    args = parser.parse_args()
    main(args)

