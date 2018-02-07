#-------------------------------------------------------------------------------
# Name:        Set max speed to osm roads
# Purpose:     Add max speed depending on type of road in OSM data.
#               Download OSM data first--> roadlayer.
# Author:      Therese Norman
#
# Created:     30/01/2018
#-------------------------------------------------------------------------------

import arcpy, arcinfo

# define road feature class
roadlayer= r"E:\WBG\Djibouti\osm\dj_roads.gdb\roads\only_roads_osm_ln"
print "layer defined"

# add fields needed (speed km/h, speed m/s, speed m/min, seconds, minutes, meters)
arcpy.AddField_management(in_table=roadlayer, field_name="speed_kmh", field_type="DOUBLE", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=roadlayer, field_name="speed_ms", field_type="DOUBLE", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=roadlayer, field_name="speed_mmin", field_type="DOUBLE", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=roadlayer, field_name="seconds", field_type="DOUBLE", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
arcpy.AddField_management(in_table=roadlayer, field_name="minutes", field_type="DOUBLE", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
# add meters field by calculating geometry and renaming the field to "meters"
arcpy.AddGeometryAttributes_management(Input_Features=roadlayer, Geometry_Properties="LENGTH", Length_Unit="METERS", Area_Unit="", Coordinate_System="")
arcpy.AlterField_management(in_table=roadlayer, field="LENGTH", new_field_name="meters", new_field_alias="", field_type="DOUBLE", field_length="8", field_is_nullable="NULLABLE", clear_field_alias="false")

print "fields added"

#assign speeds
arcpy.CalculateField_management(
    in_table=roadlayer, field="speed_kmh", expression=
    "90 if !highway! == 'trunk' else ( \
    80 if !highway! == 'primary' or !highway! == 'primary_link' else ( \
    60 if !highway! == 'secondary' or !highway! == 'secondary_link' else ( \
    50 if !highway! == 'tertiary' or !highway! == 'tertiary_link' else ( \
    25 if !highway! == 'residential' else ( \
    20 if !highway! == 'track' or !highway! == 'service' or \
    !highway! == 'construction' or !highway! == 'path' or \
    !highway! == 'road' or !highway! ==  'unclassified' \
    else 1)))))",
    expression_type="PYTHON", code_block="")

print "speed assignment done"

#calculate m/s speeds and m/min speeds
arcpy.CalculateField_management(
    in_table=roadlayer, field="speed_ms", expression=
    "!speed_kmh!/3.6",
    expression_type="PYTHON", code_block="")

arcpy.CalculateField_management(
    in_table=roadlayer, field="speed_mmin", expression=
    "!speed_kmh!/0.06",
    expression_type="PYTHON", code_block="")

print "speeds calculated"

#calculate seconds and minutes
arcpy.CalculateField_management(
    in_table=roadlayer, field="seconds", expression=
    "!meters!/!speed_ms!",
    expression_type="PYTHON", code_block="")

arcpy.CalculateField_management(
    in_table=roadlayer, field="minutes", expression=
    "!seconds!/60",
    expression_type="PYTHON", code_block="")

print "seconds and minutes calculated"
