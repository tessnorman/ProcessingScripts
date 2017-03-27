import os, sys, shutil, arcpy
sys.path.append(r"C:\Users\wb411133\Box Sync\AAA_BPS\Code\GOST")
import GOSTRocks.arcpyMisc
import GOSTRocks.misc

inShp = r"Q:\Projects\MapGeneration\HRV SHP\HRV_LAU2_Pov.shp"
shpJoinField = "Area_ID"
inTable = r"Q:\Projects\MapGeneration\hrv_hbs_2011_percap_model_output.csv"
tableJoinField = "MUN_ID"
outputFolder = r"Q:\Projects\MapGeneration\Maps"
outMXD = r"Q:\Projects\MapGeneration\MapDoc_Testing.mxd"
joinFields = ['ae_fgt0_23919_ALL','pop_ALL','ae_fgt1_23919_ALL','ae_fgt2_23919_ALL','ae_fgt0_27262_ALL','ae_fgt1_27262_ALL','ae_fgt2_27262_ALL','pc_fgt0_2426_ALL','pc_fgt1_2426_ALL','pc_fgt2_2426_ALL','pc_fgt0_3023_ALL','pc_fgt1_3023_ALL','pc_fgt2_3023_ALL','pc_fgt0_4851_ALL','pc_fgt1_4851_ALL','pc_fgt2_4851_ALL','pc_fgt0_4932_ALL','pc_fgt1_4932_ALL','pc_fgt2_4932_ALL','pc_fgt0_7954_ALL','pc_fgt1_7954_ALL','pc_fgt2_7954_ALL','pc_fgt0_9703_ALL','pc_fgt1_9703_ALL','pc_fgt2_9703_ALL','pc_fgt0_15909_ALL','pc_fgt1_15909_ALL','pc_fgt2_15909_ALL','pc_fgt0_18011_ALL','pc_fgt1_18011_ALL','pc_fgt2_18011_ALL','pc_fgt0_19405_ALL','pc_fgt1_19405_ALL','pc_fgt2_19405_ALL','value','pc_ge_0','pc_ge_1','pc_ge_2','pc_gini','X','Y','goZ_ae_fgt0_23919_ALL','goS_ae_fgt0_23919_ALL','goP_ae_fgt0_23919_ALL','goZ_ae_fgt1_23919_ALL','goS_ae_fgt1_23919_ALL','goP_ae_fgt1_23919_ALL','goZ_ae_fgt2_23919_ALL','goS_ae_fgt2_23919_ALL','goP_ae_fgt2_23919_ALL','goZ_ae_fgt0_27262_ALL','goS_ae_fgt0_27262_ALL','goP_ae_fgt0_27262_ALL','goZ_ae_fgt1_27262_ALL','goS_ae_fgt1_27262_ALL','goP_ae_fgt1_27262_ALL','goZ_ae_fgt2_27262_ALL','goS_ae_fgt2_27262_ALL','goP_ae_fgt2_27262_ALL','goZ_pc_fgt0_2426_ALL','goS_pc_fgt0_2426_ALL','goP_pc_fgt0_2426_ALL','goZ_pc_fgt1_2426_ALL','goS_pc_fgt1_2426_ALL','goP_pc_fgt1_2426_ALL','goZ_pc_fgt2_2426_ALL','goS_pc_fgt2_2426_ALL','goP_pc_fgt2_2426_ALL','goZ_pc_fgt0_3023_ALL','goS_pc_fgt0_3023_ALL','goP_pc_fgt0_3023_ALL','goZ_pc_fgt1_3023_ALL','goS_pc_fgt1_3023_ALL','goP_pc_fgt1_3023_ALL','goZ_pc_fgt2_3023_ALL','goS_pc_fgt2_3023_ALL','goP_pc_fgt2_3023_ALL','goZ_pc_fgt0_4851_ALL','goS_pc_fgt0_4851_ALL','goP_pc_fgt0_4851_ALL','goZ_pc_fgt1_4851_ALL','goS_pc_fgt1_4851_ALL','goP_pc_fgt1_4851_ALL','goZ_pc_fgt2_4851_ALL','goS_pc_fgt2_4851_ALL','goP_pc_fgt2_4851_ALL','goZ_pc_fgt0_4932_ALL','goS_pc_fgt0_4932_ALL','goP_pc_fgt0_4932_ALL','goZ_pc_fgt1_4932_ALL','goS_pc_fgt1_4932_ALL','goP_pc_fgt1_4932_ALL','goZ_pc_fgt2_4932_ALL','goS_pc_fgt2_4932_ALL','goP_pc_fgt2_4932_ALL','goZ_pc_fgt0_7954_ALL','goS_pc_fgt0_7954_ALL','goP_pc_fgt0_7954_ALL','goZ_pc_fgt1_7954_ALL','goS_pc_fgt1_7954_ALL','goP_pc_fgt1_7954_ALL','goZ_pc_fgt2_7954_ALL','goS_pc_fgt2_7954_ALL','goP_pc_fgt2_7954_ALL','goZ_pc_fgt0_9703_ALL','goS_pc_fgt0_9703_ALL','goP_pc_fgt0_9703_ALL','goZ_pc_fgt1_9703_ALL','goS_pc_fgt1_9703_ALL','goP_pc_fgt1_9703_ALL','goZ_pc_fgt2_9703_ALL','goS_pc_fgt2_9703_ALL','goP_pc_fgt2_9703_ALL','goZ_pc_fgt0_15909_ALL','goS_pc_fgt0_15909_ALL','goP_pc_fgt0_15909_ALL','goZ_pc_fgt1_15909_ALL','goS_pc_fgt1_15909_ALL','goP_pc_fgt1_15909_ALL','goZ_pc_fgt2_15909_ALL','goS_pc_fgt2_15909_ALL','goP_pc_fgt2_15909_ALL','goZ_pc_fgt0_18011_ALL','goS_pc_fgt0_18011_ALL','goP_pc_fgt0_18011_ALL','goZ_pc_fgt1_18011_ALL','goS_pc_fgt1_18011_ALL','goP_pc_fgt1_18011_ALL','goZ_pc_fgt2_18011_ALL','goS_pc_fgt2_18011_ALL','goP_pc_fgt2_18011_ALL','goZ_pc_fgt0_19405_ALL','goS_pc_fgt0_19405_ALL','goP_pc_fgt0_19405_ALL','goZ_pc_fgt1_19405_ALL','goS_pc_fgt1_19405_ALL','goP_pc_fgt1_19405_ALL','goZ_pc_fgt2_19405_ALL','goS_pc_fgt2_19405_ALL','goP_pc_fgt2_19405_ALL','goZ_pc_gini','goS_pc_gini','goP_pc_gini','goZ_pc_ge_0','goS_pc_ge_0','goP_pc_ge_0','goZ_pc_ge_1','goS_pc_ge_1','goP_pc_ge_1','goZ_pc_ge_2','goS_pc_ge_2','goP_pc_ge_2']

layerName = "FUBAR"
inMXD = r"Q:\Projects\MapGeneration\MapDoc.mxd"
outGDB = r"Q:\Projects\MapGeneration\Maps.gdb"
outTable = "%s/%s" % (outGDB, os.path.basename(inTable)[:-4])

#Join Table to Shapefile
if not arcpy.Exists(outTable):
    arcpy.CopyRows_management(inTable, outTable)
    arcpy.JoinField_management(inShp, shpJoinField, outTable, tableJoinField)

#Open template Arcpy Document
shutil.copy(inMXD, outMXD)
mxd = arcpy.mapping.MapDocument(outMXD)
df = arcpy.mapping.ListDataFrames(mxd)[0]

#Add shapefile to document
newLyr = arcpy.mapping.Layer(inShp)
newLyr.name = layerName
arcpy.mapping.AddLayer(df, newLyr, "TOP")

mxd.save()

GOSTRocks.arcpyMisc.createMapFromColumns(mxd, layerName, outputFolder)