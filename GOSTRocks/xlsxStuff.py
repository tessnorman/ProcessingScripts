import xlsxwriter, arcpy

'''
Writes the contents of a shapefile to a xls document
inShp = Path to input shapefile to write 
sheet = name of shape to create
workbook = excel.newworkbook()
'''
def writeShapefileXLS(workbook, inShp, sheetName, sortField="FID", sortOrder="A", ignoreFields=["FUBAR"], moveFields=-1, colStyles={}):
    sheet = workbook.add_worksheet(sheetName)
    #get and write fieldnames
    fieldNames = []
    for f in arcpy.ListFields(inShp):
        if not f.name == "Shape":
            fieldNames.append(f.name)
    #If the move fields object has been defined, adjust column order
        #Each object is a tuple of column name and new index        
    if moveFields != -1:
        for fIdx in moveFields:
            fieldNames.pop(fieldNames.index(fIdx[0]))
            fieldNames.insert(fIdx[1], fIdx[0])
            
    printIdx = 0
    for fIdx in range(0, len(fieldNames)):
        if not fieldNames[fIdx] in ignoreFields:
            sheet.write(0, printIdx, fieldNames[fIdx])
            printIdx = printIdx + 1
    #Create a search cursor and write results to output sheet
    sc = arcpy.SearchCursor(inShp, sort_fields="%s %s"%(sortField, sortOrder))
    fCount = 1
    for feat in sc:
        printIdx = 0
        for fIdx in range(0, len(fieldNames)):
            if not fieldNames[fIdx] in ignoreFields:
                if fieldNames[fIdx] in colStyles.keys():                    
                    sheet.write(fCount, printIdx, feat.getValue(fieldNames[fIdx]), colStyles[fieldNames[fIdx]])
                sheet.write(fCount, printIdx, feat.getValue(fieldNames[fIdx]))
                printIdx = printIdx + 1
        fCount += 1
    return(workbook)

