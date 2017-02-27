import os, sys

        
'''
LIST functions - these are basic mathematical functions for lists
'''
def listCumSum(inD, rev=False):
    outD = [0] * len(inD)
    if not rev:
        outD[0] = inD[0]
        for idx in range(0,len(inD)):
            outD[idx] = outD[(idx - 1)] + inD[idx]
    else:
        outD[len(outD)-1] = inD[len(outD)-1]
        for idx in range(len(inD)-2, 0, -1):
            outD[idx] = outD[(idx + 1)] + inD[idx]
    return(outD)

def listAdd(d1, d2):
    outD = [0] * len(d1)
    for idx in range(0, len(d1)):
        outD[idx] = d1[idx] + d2[idx]
    return(outD)


def listSum(l):
    sum = 0
    for e in l:
        sum += float(e)
    return(sum)
    
def listAvg(l):
    sum = 0
    for e in l:
        sum += float(e)
    return sum*1.0/len(l) 
    
def listMin(l):
    min = l[0]
    for e in l:
        if e < min:
            min = e
    return min
    
def listMax(l, idx=False):
    max = l[0]
    mIdx = 0
    for e in range(0,len(l)):
        if l[e] > max:
            max = l[e]
            mIdx = e
    if idx:
        return mIdx
    return max
    
def listSD(l):
    mean = listAvg(l)
    sd = 0
    for e in l:
        sd += (mean-e)**2
    return sd/len(l)