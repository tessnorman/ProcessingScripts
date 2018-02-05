#-------------------------------------------------------------------------------
# Name:        cost distance tool
# Purpose:      cost distance tool for OSM road data
#
# Author:      Therese Norman
#
# Created:     30/01/2018
#-------------------------------------------------------------------------------

import arcpy, arcinfo
arcpy.CheckOutExtension("Spatial")

# define road feature class
roadlayer= r"E:\WBG\Djibouti\osm\dj_roads.gdb\roads\only_roads_osm_ln"
print "layer defined"


# Add and calculate field 'minutes per meter'
arcpy.AddField_management(in_table=roadlayer, field_name="min_per_m", field_type="SHORT", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")

arcpy.CalculateField_management(
    in_table=roadlayer, field="min_per_m", expression=
    "1/!speed_mmin!*10000",
    expression_type="PYTHON", code_block="")

print "minutes to move one second calculated"

#convert to raster
arcpy.FeatureToRaster_conversion(in_features=roadlayer, field="min_per_m", out_raster="E:/WBG/Djibouti/osm/osmroad_ras", cell_size="100")

#set processing extent
arcpy.env.extent = r"E:\WBG\Djibouti\GIS\djibouti_country.shp"

# reclassify (mostly to make sure no data is assigned a value)
roadraster = "E:/WBG/Djibouti/osm/osmroad_ras"
arcpy.gp.Reclassify_sa(roadraster, "VALUE", "600 50;NODATA 50", "E:/WBG/Djibouti/osm/osmroad_cd", "DATA")

#set mask
arcpy.env.mask = r"E:\WBG\Djibouti\GIS\djibouti_country.shp"

# run cost distance tool
points=r"E:\WBG\Djibouti\GIS\HealthCenters_wGPS.shp"
cdraster = "E:/WBG/Djibouti/osm/osmroad_cd"
arcpy.gp.CostDistance_sa(points, cdraster, "E:/WBG/Djibouti/osm/tt_health", "", "", "", "", "", "", "")

#Use divide tool to get units back to travel time in minutes from point locations
tt_ras="E:/WBG/Djibouti/osm/tt_health"
arcpy.gp.Divide_sa(tt_ras, "10000", "E:/WBG/Djibouti/osm/tthealthc.tif")

#calculate contour line at 60 min from point locations
tt_min_ras="E:/WBG/Djibouti/osm/tthealthc.tif"
arcpy.gp.ContourList_sa(tt_min_ras, "E:/WBG/Djibouti/osm/contour1h.shp", "60")

print "all done"
