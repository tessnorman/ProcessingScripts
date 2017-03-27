###################################################################################################
# Urbanization Review
# Benjamin P. Stewart, Feb 2017
# Purpose: Calculate urbanization metrics for a defined country
#   1. Nighttime Lights
#   2. GHSL
###################################################################################################
import os, sys, csv, arcpy, shutil, xlsxwriter
sys.path.append(r"C:\Users\wb411133\Box Sync\AAA_BPS\Code\GOST")
from GOSTRocks.misc import *
from GOSTRocks.xlsxStuff import *
from GOSTRocks.arcpyMisc import *
from GOSTRocks.Urban.SummarizeGHSL import *
import GOSTRocks.metadataManagement
import GOSTRocks.Urban.NighttimeLightsFootprints
import GOSTRocks.Urban.NighttimeLightsThreshold
import GOSTRocks.Urban.WorldPop_Library as wp

def createFolder(bFolder, name):
    outF = os.path.join(bFolder, name)
    if not os.path.exists(outF):
        os.mkdir(outF)
    return (outF)

def calculateUrban(iso3, outputFolder, tempFolder = "C:/Temp",                   
                   cNTL=True, cGHSL=True, cGUF=True, cPopulation=True, cAdmin=True,
                   inCities = r"S:\GLOBAL\POPULATION\Cities_D\GRUMP\glpv1_gt_100000.shp", popIdx = "ES00POP", nameIdx = "NAME1",
                   inputThresholds = "S:/GLOBAL/Projects/CityLights/Data/Tabular/ThreshComp.csv",
                   urbanExtents = "NTL",
                   urbanMetricsMetadata = r"Q:\ADMINISTRATIVE\Global Product Documentation\Urbanization_Metrics.docx",
                   ghslFolder = r"S:\GLOBAL\Global_Human_Settlement_Layer\BETA\FULL\MT\MT\12",
                   datamaskFolder = r"S:\GLOBAL\Global_Human_Settlement_Layer\BETA\FULL\DATAMASK\12",
                   ghslMetadata = r"S:\GLOBAL\Global_Human_Settlement_Layer\GHSL Landsat readme.pdf",
                   gufMetadata = r"Q:\GLOBAL\URBAN\GUF\GUF_Product_Specifications_GUF_DLR_v01.pdf",
                   gufReferences = r"Q:\GLOBAL\URBAN\GUF\GUF_References.pdf",
                   gufTiles = r"Q:\GLOBAL\URBAN\GUF\GUF_Tile_outlines.shp",
                   gufFolder = r"Q:\GLOBAL\URBAN\GUF\GUF28",
                   gufMap = r"Q:\GLOBAL\URBAN\GUF\GUF_Footprint_Maps.mxd",
                   popDensity = r"S:\GLOBAL\POPULATION\Landscan2012\ArcGIS\Population\lspop2012_Density.tif",
                   popGrid = r"S:\GLOBAL\POPULATION\Landscan2012\ArcGIS\Population\lspop2012.tif",
                   popThresholds = [300,1500,5000,50000],
                   popMap = r"S:\GLOBAL\POPULATION\Landscan2012\EC_Footprints\EC_Country_Footprints.mxd",
                   popHdStyle = r"S:\GLOBAL\POPULATION\Landscan2012\EC_Footprints\HD_Cluster.lyr",
                   popUrbStyle = r"S:\GLOBAL\POPULATION\Landscan2012\EC_Footprints\Urban Clusters.lyr",
                   landscanPopMetadata = "S:/GLOBAL/POPULATION/Landscan2012/LSpopMetadata/lspop2012.htm",
                   landscanDataMetadata = "S:/GLOBAL/POPULATION/Landscan2012/LSpopMetadata/LandScan Documentation.docx",
                   admin0Polys = r"S:\GLOBAL\ADMIN\WB-2014_subadmin_D\Polygons\Admin0_Polys.shp",
                   admin1Polys = r"S:\GLOBAL\ADMIN\WB-2014_subadmin_D\Polygons\Admin1_Polys.shp",
                   admin2Polys = r"S:\GLOBAL\ADMIN\WB-2014_subadmin_D\Polygons\Admin2_Polys.shp",
                   ghslOutline = r"S:\GLOBAL\Global_Human_Settlement_Layer\BETA\index2.shp",
                   ghslSymbology = r"S:\GLOBAL\Global_Human_Settlement_Layer\BETA\FULL\GHSL_Builtup.lyr",
                   gufSymbology = r"Q:\GLOBAL\URBAN\GUF\GUF_Simple.lyr",
                   dmLyrSymbology = r"S:\GLOBAL\Global_Human_Settlement_Layer\BETA\FULL\GHSL_Datamask.lyr",
                   extentsSymbology = r"S:\GLOBAL\Global_Human_Settlement_Layer\BETA\FULL\Urban_masterExtents.lyr",
                   inNTLFolder = r'S:\GLOBAL\NightLights',
                   inNTLFolder_radCal = r'S:\GLOBAL\NightLights\rad_cal',
                   inputCountries = r"S:\GLOBAL\ADMIN\WB-2014_subadmin_D\Polygons\Admin0_Polys.shp",
                   radCalT0 = r"S:\GLOBAL\NightLights\rad_cal\F1996_0316-19970212_rad_v4.avg_vis_Corrected.tif",
                   radCalT1 = r"S:\GLOBAL\NightLights\rad_cal\F2010_0111-20101209_rad_v4.avg_vis_Corrected.tif"
                   ):
    '''Calculate a series of urbanization analyses for a specificed country
    REQUIRED PARAMETERS:
    iso3 - Country code of input copuntry
    outputFolder - location for output folder
    OPTIONAL PARAMETERS
    inCities - Shapefile of cities used in naming nighttime lights extents
    inputThresholds - CSV file containing thresholds for calculating nighttime lights extents
    urbanExtents - Shapefile to use for summarizing urban/built-up. DEFAULT "NTL" USES NIGHTTIME LIGHTS EXTENT
    ghslFolder/datamaskFolder - Folder path containing the ghsl data structure
    gufTiles - Shapefile describing the GUF extent tiles
    gufFolder - Folder containing all the GUF tiles
    gufMap - MXD for creating GUF maps
    popDensity - Raster describing population density (assumption is people per km2)
    popGrid - Raster describing population grid; people per tile
    popThresholds - numbers applied to population layers to create population extents 
        [urban density threshold, high density threshold, urban pop threshold, high density population threshold]
    popMap - MXD for creating population maps
    popHdStyle - ESRI Layer file for styling hd layers
    popUrbStyle - ESRI Layer file for styling urban layers
    cNTL/cGHSL/cGUF/cPopulation - Booleans determining if GHSL should be summarized/mapped
    '''
    #Create output folders and define output shapefiles
    baseOutputFolder = createFolder(outputFolder, iso3)   
    gisOutputFolder = createFolder(baseOutputFolder, "GIS")
    mapOutputFolder = createFolder(baseOutputFolder, "Maps")
    docsOutputFolder = createFolder(baseOutputFolder, "Documentation")
    tableOutputFolder = createFolder(baseOutputFolder, "Tabular")
           
    adminFolder = createFolder(gisOutputFolder, "ADMIN")
    
    ntlFolder = createFolder(gisOutputFolder, "NTL")        
    finalShape = os.path.join(ntlFolder, "%s_masterExtents.shp" % iso3)
    
    ghslOutputFolder = createFolder(gisOutputFolder, "GHSL")        
    ghslShape = os.path.join(ghslOutputFolder, "%s_GHSL.shp" % iso3)
    
    gufOutputFolder = createFolder(gisOutputFolder, "GUF")
    gufShape = os.path.join(gufOutputFolder, "%s_GUF.shp" % iso3)
    popOutputFolder = createFolder(gisOutputFolder, "Population")

    NTLoutputSummaryExcel = os.path.join(tableOutputFolder, "%s_NTL_Extent_Stats.xlsx" % iso3)
    GHSLoutputSummaryExcel = os.path.join(tableOutputFolder, "%s_GHSL_Extent_Stats.xlsx" % iso3)
    
    #Copy Official Metadata
    shutil.copyfile(urbanMetricsMetadata, os.path.join(docsOutputFolder, "Urbanization Metrics Overview.docx"))
    #Copy GHSL metadata
    shutil.copyfile(ghslMetadata, os.path.join(docsOutputFolder, "GHSL Landsat readme.pdf"))
    #Copy GUF metadata
    shutil.copyfile(gufMetadata, os.path.join(docsOutputFolder, "GUF Specifications readme.pdf"))
    shutil.copyfile(gufReferences, os.path.join(docsOutputFolder, "GUF References.pdf"))
    #Copy Landscan Metadata
    shutil.copyfile(landscanPopMetadata, os.path.join(docsOutputFolder, "lspop2012.htm"))
    shutil.copyfile(landscanDataMetadata, os.path.join(docsOutputFolder, "LandScan Data Creation.docx"))
    
    if cAdmin:
        tPrint("*** Summarizing data by administrative areas")
        outputAdminNTL = os.path.join(tableOutputFolder, "ADMIN2_NTL_SummaryData.csv")
        outputAdminPop = os.path.join(tableOutputFolder, "ADMIN2_Population_SummaryData.csv")
        outputAdminGen = os.path.join(tableOutputFolder, "ADMIN2_General_SummaryData.csv")
        outputAdminGHSL = os.path.join(tableOutputFolder, "ADMIN2_GHSL.csv")
        #Create admin boundary files
        admin0 = os.path.join(adminFolder, "%s_0.shp" % iso3)
        admin1 = os.path.join(adminFolder, "%s_1.shp" % iso3)
        admin2 = os.path.join(adminFolder, "%s_2.shp" % iso3)
        if not arcpy.Exists(admin0):
            arcpy.Select_analysis(admin0Polys, admin0, '"ISO3" = \'%s\'' % iso3)
        if not arcpy.Exists(admin1):
            arcpy.Select_analysis(admin1Polys, admin1, '"ISO3" = \'%s\'' % iso3)
        if not arcpy.Exists(admin2):
            arcpy.Select_analysis(admin2Polys, admin2, '"ISO3" = \'%s\'' % iso3)
        
        #Summarize Nighttime Lights Data by Admin2
        if not os.path.isfile(outputAdminNTL):
            results2 = summarizeGlobalData(admin2, "FID", 'NTL')
            writeDict(results2["Results"], outputAdminNTL, results2["Titles"])
        #Summarize Population Data by Admin2
        if not os.path.isfile(outputAdminPop):
            results2 = summarizeGlobalData(admin2, "FID", [popGrid], ['N'])
            writeDict(results2["Results"], outputAdminPop, results2["Titles"])
        #Summarize GHSL by admin boundaries
        if not os.path.isfile(outputAdminGHSL):
            summarizeGHSL_toShp(admin2, ghslFolder, datamaskFolder, ghslOutputFolder, tempFolder, ghslOutline)        
            writeShapefileXLS(xlsxwriter.Workbook(outputAdminGHSL), admin2, "GHSL")
                
    #Calculate Nighttime lights footprints
    if cNTL:
        tPrint("***Processing NTL for %s" % iso3)
        #read the urban thresholds into a data dictionary
        countries = { rows[0]:rows[1:] for rows in csv.reader(open(inputThresholds), delimiter=',') }
        newCities = os.path.join(ntlFolder, iso3 + os.path.basename(inCities))    
        thresh = 0    
        try:
            thresh = countries[iso3][0]
        except: #If the threshold is not calculated, do so            
            thresh = GOSTRocks.Urban.NighttimeLightsThreshold.calculateThreshold(iso3, inputThresholds)
        if not os.path.exists(finalShape):
            if not os.path.exists(ntlFolder):
                os.makedirs(ntlFolder)
        #Calculate NTL footprints
        if not arcpy.Exists(finalShape):
            GOSTRocks.Urban.NighttimeLightsFootprints.calculateFootprints(iso3, thresh, 
                ntlFolder, inCities, radCalT0, radCalT1, inNTLFolder, inNTLFolder_radCal, admin0Polys,
                0.02, popIdx, nameIdx)
        #Post Processing includes creating output tables, maps, and adding metadata to shapefiles
        GOSTRocks.Urban.NighttimeLightsFootprints.FPpostProcessing(docsOutputFolder,mapOutputFolder,ntlFolder,
            NTLoutputSummaryExcel, iso3, finalShape, newCities, thresh, popIdx)    
        createMapFromMXD_loop(arcpy.mapping.MapDocument(os.path.join(mapOutputFolder, "%s NighttimeLights_Extents.mxd" % iso3)),
            os.path.join(mapOutputFolder, "NTL_Map.png"), "Master Footprints", "ExtentName",
            statusDefinition = {'Master Footprints':"NOT \"ExtentName\" = '0'"})
    #Summarize GHSL within the defined urban footprints DEFAULT - Nighttime Lights Extents
    if cGHSL: 
        tPrint("***Processing GHSL for %s" % iso3)
        if urbanExtents == "NTL":
            arcpy.CopyFeatures_management(finalShape, ghslShape)
            #Delete most of the fields
            fieldsToDelete = []
            for f in arcpy.ListFields(ghslShape):
                if not f.name in ["ExtentName","gAreaKM","pop","FID","Shape"]:
                    fieldsToDelete.append(f.name)
            arcpy.DeleteField_management(ghslShape, fieldsToDelete)
        else:            
            arcpy.CopyFeatures_management(urbanExtents, ghslShape)
        summarizeGHSL_toShp(ghslShape, ghslFolder, datamaskFolder, ghslOutputFolder, tempFolder, ghslOutline)
        createGHSLexcel(ghslShape, GHSLoutputSummaryExcel)
                
        #Map GHSL       
        ghslMap = os.path.join(mapOutputFolder, "GHSL_Maps.mxd")
        if not os.path.exists(ghslMap):
            addGHSL(ghslShape, ghslMap, ghslFolder, datamaskFolder, ghslSymbology, extentsSymbology, ghslOutline)
            createMapFromMXD(arcpy.mapping.MapDocument(ghslMap), 
                os.path.join(mapOutputFolder, "GHSL_Map.png"))
            #Loop through the features in the defined layer, zoom to them and create an output map
            createMapFromMXD_loop(arcpy.mapping.MapDocument(ghslMap), 
                os.path.join(mapOutputFolder, "GHSL_Map.png"),
                "%s_GHSL" % iso3, "ExtentName")
    #Summarize GUF within the defined urban footprints DEFAULT - Nighttime Lights Extents
    if cGUF:
        tPrint("***Processing GUF for %s" % iso3)
        if urbanExtents == "NTL":
            arcpy.CopyFeatures_management(finalShape, gufShape)
        else:            
            arcpy.CopyFeatures_management(urbanExtents, gufShape)
                        
        #Identify the intersecting GUF tiles
        summarizeGUF_toShp(gufShape, gufTiles, gufFolder, tempFolder)
        gufOutMap = os.path.join(mapOutputFolder, "GUF_Maps.mxd")
        #add intersecting GUF tiles to the copied GUF map
        curTiles = selectGHSLtiles(gufShape, gufTiles, 'FileName', False)        
        addGUF(gufMap, curTiles, gufShape, gufOutMap, gufFolder, gufSymbology, extentsSymbology)
        #Loop through the features in the defined layer, zoom to them and create an output map        
        createMapFromMXD_loop(arcpy.mapping.MapDocument(gufOutMap), 
            os.path.join(mapOutputFolder, "GUF_Map.png"),
            "%s_GUF" % iso3, "ExtentName")
    
    #Calculate the population based extents, based on EC classification methodology
    if cPopulation: 
        tPrint("***Processing gridded population for %s" % iso3)
        #Names of the output rasters and summary dbf
        urbClstGrid = os.path.join(popOutputFolder, "URB_CLST")
        hdClstGrid = os.path.join(popOutputFolder, "HD_CLST_RAW")
        hdClstGridSmooth = os.path.join(popOutputFolder, "hd_clst")
        hdClstGridSmoothBinary = os.path.join(popOutputFolder, "bhd_clst")
        urbClstTbl = os.path.join(popOutputFolder, "URB_UrbanizationSummary.dbf")
        hdClstTbl = os.path.join(popOutputFolder, "HD_UrbanizationSummary.dbf")
        urbShp = os.path.join(popOutputFolder, "URB_Extents.shp")
        hdShp = os.path.join(popOutputFolder, "HD_Extents.shp")
        outPopMap = os.path.join(mapOutputFolder, "population_Extent_Map.mxd")
                
        lowDensVal = popThresholds[0]
        highDensVal = popThresholds[1]
        lowDensPop = popThresholds[2]
        highDensPop = popThresholds[3]
        
        #If the folder does not exist, create it 
        if not os.path.exists(popOutputFolder):
            os.mkdir(popOutputFolder)
        
        #Clip the population layers for processing
        tempPop = os.path.join(popOutputFolder, "populationGrid.tif")
        tempDen = os.path.join(popOutputFolder, "populationDen.tif")
        if not arcpy.Exists(tempPop):
            arcpy.Clip_management(popGrid, "#", tempPop, admin0, '', "ClippingGeometry")
        if not arcpy.Exists(tempDen):
            arcpy.Clip_management(popDensity, "#", tempDen, admin0, '', "ClippingGeometry")
        
        #Create the high density and urban rasters if they do not exist
        if not arcpy.Exists(hdClstGridSmooth):
            wp.createUrbanClusters(tempPop, tempDen, lowDensVal, urbClstGrid)
            wp.createUrbanClusters(tempPop, tempDen, highDensVal, hdClstGrid)
            tPrint("smoothing rasters")
            try:
                arcpy.env.workspace = popOutputFolder
                wp.smoothClusters(tempDen, tempPop, hdClstGrid, hdClstGridSmooth, highDensPop, 16, False)
                arcpy.CalculateStatistics_management(hdClstGridSmooth, "1", "1", "#", "OVERWRITE")
            except:
                tPrint("Threshold %s is not calculable as a high density cluster" % lowDensVal)
        
        #Summarize the output urban rasters - functions even if the rasters existed previously
        try:    
            straight = wp.summarizeWorldPop(urbClstGrid, tempPop, urbClstTbl)  
            smoothed = wp.summarizeWorldPop(hdClstGridSmooth, tempPop, hdClstTbl)              
        except:
            tPrint("Threshold %s does not have high density clusters" % lowDensVal)
        arcpy.Delete_management(hdClstGrid)
        #Convert rasters to shapefiles
        if not arcpy.Exists(urbShp):
            extractFootprints(urbClstGrid, 4999, urbShp)
        if not arcpy.Exists(hdShp):
            extractFootprints(hdClstGridSmooth, 49999, hdShp)
        
        #Map the results                
        wp.mapPop(popMap, outPopMap, hdClstGridSmooth, urbClstGrid, popHdStyle, popUrbStyle, finalShape, extentsSymbology)
        createMapFromMXD_loop(arcpy.mapping.MapDocument(outPopMap), 
            os.path.join(mapOutputFolder, "Population_Map.png"),
            "%s_masterExtents" % iso3, "ExtentName")
            
            
            
            