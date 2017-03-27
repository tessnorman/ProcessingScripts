import os, sys, glob, string
import pandas as pd
import numpy as np

#User parameters 
statsType = "STANDARD" #Other statistics types can be included here, eventually
inputFolder = r"C:\Temp\LCA_Analysis"
outputFile = r"S:\COUNTRY\LCA\Infrastructure\AnalysisResults\Summarized_%s.csv" % statsType
baselineSolution = r"S:\COUNTRY\LCA\Infrastructure\AnalysisResults\baseline2.csv"
analysisColumn = "TOTAL_DISTANCE"

def getFastest(curData, cName):
    curData = curData[curData[cName] > 0]
    allResults = []
    for curO in curData.groupby('ORIGIN'):
        totalDistance = curO[1]['TOTAL_DISTANCE'].sum()
        minDistance = curO[1]['TOTAL_DISTANCE'].min()
        minDest = curO[1]['DEST'][curO[1]['TOTAL_DISTANCE'].argmin()]
        allResults.append([curO[0],minDest,minDistance,totalDistance])
    
    return pd.DataFrame(allResults,columns=["ORIGIN","DEST",cName+"_MIN",cName])
        
def readData(inFile, cName):
    curD = pd.read_csv(inFile)
    curD.columns = [x.upper() for x in curD.columns]
    #Split the route column into origin and destination
    namesDF = pd.DataFrame(curD.NAME.str.split(" - ").tolist(), columns=['ORIGIN','DEST'])
    curD2 = pd.concat([curD.reset_index(),namesDF], axis=1)
    #Remove extra columns
    for col in curD2:
        if not col in ["ORIGIN","DEST",cName]:
            curD2 = curD2.drop(col, 1)
    return curD2
    
def main():
    #Read in baseline data+
    inData = readData(baselineSolution, analysisColumn)
    print inData.columns
    fastestData = getFastest(inData, analysisColumn)
    fTotal = fastestData[analysisColumn].sum()
    fMin = fastestData[analysisColumn + "_MIN"].min()
    
    inFiles = glob.glob("%s\\*.csv" % inputFolder)
    allRes = []
    for f in inFiles:
        tempD = readData(f, analysisColumn)
        tempDFastest = getFastest(tempD, analysisColumn)
        #Compare the total distance between the fastest and the current disruption
        tempTotal = tempDFastest[analysisColumn].sum()
        tempMin = tempDFastest[analysisColumn + "_MIN"].min()
        cutoff = 0
        if fastestData.shape[0] > tempDFastest.shape[0] :
            cutoff = 1
        
        allRes.append([int(os.path.basename(f)[1:6]), cutoff, round((tempTotal - fTotal), 3), round((tempMin - fMin), 3)])
    curDF = pd.DataFrame(allRes, columns=['FID', 'CutOff', 'TotalDiff', 'MinDiff'])
    print curDF
    curDF.to_csv(outputFile)
        
        
if __name__ == '__main__':
    main()
