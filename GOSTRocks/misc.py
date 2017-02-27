import os, sys, time, math

'''
Renames all files in a directory
Used to add .dat to all ENVI files, but not their headers
'''
def renameDir(dir):
    for f in os.listdir(dir):
        title = os.path.basename(pathAndFilename)
        os.rename(pathAndFilename, os.path.join(dir, "%s.dat" % title))

def listFiles(inFolder, pattern):
    outFiles = []
    for f in os.listdir(inFolder):
        if f.endswith(pattern):
            outFiles.append(os.path.join(inFolder, f))
        elif os.path.isdir(os.path.join(inFolder, f)):
            outFiles = outFiles + listFiles(os.path.join(inFolder, f), pattern)
    return(outFiles)

'''prints the time along with the message'''
def tPrint(s):
    print"%s\t%s" % (time.strftime("%H:%M:%S"), s)

def round_to_1(x):
    return round(x, -int(math.floor(math.log10(x))))

# Create an interable range made with decimal point steps
def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
        r += step    
'''
Get the index of a specific [val] within a list of histogram values
'''
def getHistIndex(hIdx, val, maxVal=2000):
    for h in range(0, len(hIdx)):
        curH = hIdx[h]
        if curH > val:
            return(lastH)        
        lastH = h
    return(len(hIdx) -1)

'''
Convert a list of values into a percent of total 
'''    
def getHistPer(inD):
    tSum = listSum(inD)
    for hIdx in range(0,len(inD)):
        inD[hIdx] = inD[hIdx] / tSum
    return(inD)