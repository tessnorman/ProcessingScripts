# Set Travel Speeds to OSM roads using Arcpy

### Purpose
This python script uses arcpy to assign speed limits to an OSM roads feature class (or a shapefile). The roads used for this example cover the country of Djibouti. The roads must have been downloaded and, if necessary, converted to shapefile or geodatabase format first.

In addition, this script adds and calculates fields (variables) for speed in different units such as meter per second and the number of minutes it takes to travel each segment. These extra fields are useful for the creation of a road network in Network Analyst and for the calculation of cost-distance rasters, but they may not be necessary depending on your ultimate goal.

Name of script: [set_max_speed_to_osm_roads_with_arcpy.py](set_max_speed_to_osm_roads_with_arcpy.py)

### Script explanation
*OBS. Always set the path according to your own directory.*

Import the arcpy module.

```python
import arcpy, arcinfo
```

Define the road feature class you will be working with and print message when done. In this case, the roads are a feature class called **only_roads_osm_ln** covering the country of Djibouti and were previously downloaded from [Geofabrik](www.geofabrik.de) (http://download.geofabrik.de/africa/djibouti.html).

```python
roadlayer= r"E:\WBG\Djibouti\osm\dj_roads.gdb\roads\only_roads_osm_ln"
print "layer defined"
```
Add/calculate fields (variables). In this case, these fields include: speed in km/h, speed in meters/s, speed in meters/min, seconds to travel each segment, minutes to travel each segment, the length of each segment in meters.
Print message when done.

Add field for speed in km/h (This is the field that we will assign speed limits to later):
```python
arcpy.AddField_management(in_table=roadlayer, field_name="speed_kmh", field_type="DOUBLE", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
```
Add field for speed in m/s:
```python
arcpy.AddField_management(in_table=roadlayer, field_name="speed_ms", field_type="DOUBLE", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
```
Add field for speed in m/min:
```python
arcpy.AddField_management(in_table=roadlayer, field_name="speed_mmin", field_type="DOUBLE", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
```
Add field for seconds (to travel a segment):
```python
arcpy.AddField_management(in_table=roadlayer, field_name="seconds", field_type="DOUBLE", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
```
Add field for minutes (to travel a segment):
```python
arcpy.AddField_management(in_table=roadlayer, field_name="minutes", field_type="DOUBLE", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
# add meters field by calculating geometry and renaming the field to "meters"
```
Calculate the length of each segment in minutes:

```python
arcpy.AddGeometryAttributes_management(Input_Features=roadlayer, Geometry_Properties="LENGTH", Length_Unit="METERS", Area_Unit="", Coordinate_System="")
```
Rename the field calculated in previous step from `LENGTH` to `meters`:
```python
arcpy.AlterField_management(in_table=roadlayer, field="LENGTH", new_field_name="meters", new_field_alias="", field_type="DOUBLE", field_length="8", field_is_nullable="NULLABLE", clear_field_alias="false")
```
print message when done:
```python
print "fields added"
```
Assign speed limits to the field **speed_kmh**. You can assign the speed limits you see fit depending on the country and area or vehicle type you are working with. OSM Wiki gives suggestions for what speed limit each type of road should have, but not for all countries. You should inspect the road layer first to see what types of road segments you have. The field 'highway' contains information for what type of road each segment is.
In this case, the speed limits assigned are as follows:
- Trunk - 90km/h
- Primary - 80km/h
- Secondary - 60km/h
- Tertiary - 50km/h
- Residential - 25km/h
- unclassified, track, construction, road, path - 20km/h
- Everything else: 1km/h

Print message when done.
```python
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
```
Calculate m/s speeds and m/min speeds. Print message when done.
```python
arcpy.CalculateField_management(
    in_table=roadlayer, field="speed_ms", expression=
    "!speed_kmh!/3.6",
    expression_type="PYTHON", code_block="")

arcpy.CalculateField_management(
    in_table=roadlayer, field="speed_mmin", expression=
    "!speed_kmh!/0.06",
    expression_type="PYTHON", code_block="")

print "speeds calculated"
```
Calculate seconds and minutes fields. Print message when done.
```python
arcpy.CalculateField_management(
    in_table=roadlayer, field="seconds", expression=
    "!meters!/!speed_ms!",
    expression_type="PYTHON", code_block="")

arcpy.CalculateField_management(
    in_table=roadlayer, field="minutes", expression=
    "!seconds!/60",
    expression_type="PYTHON", code_block="")

print "seconds and minutes calculated"
```
