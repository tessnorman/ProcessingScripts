################################################################################
# Fetch or modify ArcGIS Metadata
# Benjamin Stewart, February 2015
# Purpose: Fetch or set ArcGIS metadata 
################################################################################

import os, tempfile, re, time
from xml.etree.ElementTree import ElementTree, Element, SubElement, Comment, tostring

#PUBLIC METHODS Y'ALL
'''prints the time along with the message'''
def tPrint(s):
    print"%s %s" % (time.strftime("%H:%M:%S", time.gmtime()), s)

'''
Get metadata from the listed data file (usually a shapefile)
---path: file path to the data
--RETURNS: Dictionary object with Title, Summary, Description, list of keywords, and credits
'''
def fetchMetadata(path):
    tree = GetMetadataElementTree(path)
    title = GetElementText(tree, pathDictionary["Title"][0])
    abstract = GetElementText(tree, pathDictionary["Description"][0])    
    if abstract == "":
        abstract = GetElementText(tree, pathDictionary["Description"][1])        
    purpose = GetElementText(tree, pathDictionary["Summary"][0])
    if purpose == "":
        purpose = GetElementText(tree, pathDictionary["Summary"][1])
    useLimitations = GetElementText(tree, pathDictionary["Limitations"][0])
    
    searchkeys = ListElementsText(tree, pathDictionary["Keywords"][0])
    themekeys = ListElementsText(tree, pathDictionary["Keywords"][1])
    keywords = searchkeys
    
    return {'Title': title, 'Description':abstract, 'Keywords': keywords, 'Summary':purpose, \
        'Limitations': useLimitations}

def setMetadata(path, values, outPath="C:/Temp/XXXml.xml"):
    tree = GetMetadataElementTree(path)
    for vKey in values.keys():
        v = values[vKey]
        mPath = pathDictionary[vKey]
        #Fetch the tree element for the current item
        pathSplit = mPath[0].split("/")
        e = tree.find(pathSplit[0])
        for eIdx in pathSplit[1:]:            
            eCur = e.find(eIdx)            
            if eCur is None:                
                eCur = SubElement(e, eIdx)
            e = eCur
            if eIdx == pathSplit[-1]:                
                e.text = v            
    tree.write(path) 

#PRIVATE METHODS and stuff... stay the f%^k out!

pathDictionary = {'Title': ['dataIdInfo/idCitation/resTitle'], 
                  'Description': ["dataIdInfo/idAbs"], 
                  'Keywords': ["dataIdInfo/searchKeys/keyword"], 
                  'Summary': ["dataIdInfo/idPurp"], 
                  'Credits': ["dataIdInfo/idCredit"], 
                  'Limitations': ["dataIdInfo/resConst/Consts/useLimit"]}
                  
#Returns the specified element's text if it exists or an empty string if not.
def GetElementText(tree, elementPath):    
    element = tree.find(elementPath)    
    return re.sub('<[^>]*>', '', element.text) if element != None and element.text[:8] != "REQUIRED:" else ""

#Returns a ist of the text values of all instances of the specified element, or an empty string if none are found.
def ListElementsText(tree, elementPath):
    elements = tree.findall(elementPath)
    if elements:
        return [element.text for element in elements]
    else:
        return ""

#Creates and returns an ElementTree object from the specified dataset's metadata
def GetMetadataElementTree(dataset):
    #xmlfile = CreateDummyXMLFile()
    #arcpy.MetadataImporter_conversion(dataset, xmlfile)
    tree = ElementTree()
    tree.parse(dataset)
    #os.remove(xmlfile)
    return tree

#This is not currently used, 
def CreateDummyXMLFile():
    tempdir = tempfile.gettempdir()
    fd, filepath = tempfile.mkstemp(".xml", text=True)
    with os.fdopen(fd, "w") as f:
        f.write("<metadata />")
        f.close()
    return filepath