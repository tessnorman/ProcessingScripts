#-------------------------------------------------------------------------------
# Name:         Zonal Stats Suitability crops attainable yeild Uganda
# Purpose:      Clip crop rasters to Uganda country, change spatial resolution
#               to higher (0.01). Run zonal stats on rasters for newUnit raster,
#               export to tables and then convert to .csv files.
# Author:       Therese Norman
#
# Created:     02/01/2017
#-------------------------------------------------------------------------------

import arcpy, os
from arcpy import env

env.workspace = r"E:\WBG\FirmLocation\GISfirmLocation\farming_001\Suitability_FAO_GAEZ\rasters"
print arcpy.env.workspace
arcpy.env.overwriteOutput = True
arcpy.CheckOutExtension("Spatial")
print 'Check out extension complete'
rasters = arcpy.ListRasters()
print arcpy.ListRasters()

#convert shapefile into raster (already done)
NewUnit = r"E:/WBG/FirmLocation/Uganda/UgandaGIS/gis_data/Environment/LessFavoredAgLand/newUnitPop_LFAL_WGS.shp"
arcpy.FeatureToRaster_conversion(in_features=NewUnit, field="newUnitID", out_raster="E:/WBG/FirmLocation/Uganda/UgandaGIS/gis_data/Environment/LessFavoredAgLand/newUnitRas001", cell_size="0.01")
NewUnitRas ="E:/WBG/FirmLocation/Uganda/UgandaGIS/gis_data/Environment/LessFavoredAgLand/newUnitRas001"

#Define clip extent
UgandaCountry = r"E:\WBG\FirmLocation\Uganda\UgandaGIS\UgandaCountry.shp"
#clip rasters to Uganda
for raster in rasters:
    print raster
    clipoutraster = r"E:\WBG\FirmLocation\Uganda\UgandaGIS\gis_data\Environment\cropSuitability_FAOGAEZ/Ug"+raster
    arcpy.Clip_management(in_raster=raster, rectangle="28.801 -1.698 35.552 4.477", out_raster=clipoutraster, in_template_dataset=UgandaCountry, nodata_value="#", clipping_geometry="NONE", maintain_clipping_extent="NO_MAINTAIN_EXTENT")
    raster_name = os.path.basename(raster).rstrip(os.path.splitext(raster)[1]) #use this to name output
    rasterNameParts = raster_name.split('_') #make name shorter, only use this part since it contains the crop name
    print rasterNameParts[2] #print to make sure the output name is what I want it to be
    crop = rasterNameParts[2]
    resampleoutraster = r"E:/WBG/FirmLocation/Uganda/UgandaGIS/gis_data/Environment/cropSuitability_FAOGAEZ/"+crop+"_001.tif" #define outraster
    arcpy.Resample_management(in_raster=clipoutraster, out_raster=resampleoutraster, cell_size="0.01", resampling_type="NEAREST") #change resolution to match NewUnitRas
    print "resample %s done" % (crop)
    zonalouttable = "E:/WBG/FirmLocation/Uganda/UgandaGIS/gis_data/Environment/cropSuitability_FAOGAEZ/"+crop+"_zonal" #define location and name of output table
    arcpy.gp.ZonalStatisticsAsTable_sa(NewUnitRas, "VALUE", resampleoutraster, zonalouttable, "DATA", "MEAN") #zonal stats
    outLocation = "E:/WBG/FirmLocation/Uganda/UgandaGIS/gis_data/Environment/cropSuitability_FAOGAEZ/" #define output location for csv file
    print "zonal stats %s done" % (crop)
    arcpy.TableToTable_conversion(in_rows=zonalouttable, out_path=outLocation, out_name=crop+"_zonaltbl.csv") #convert output table to csv file

print 'Complete'
arcpy.CheckInExtension("Spatial")
