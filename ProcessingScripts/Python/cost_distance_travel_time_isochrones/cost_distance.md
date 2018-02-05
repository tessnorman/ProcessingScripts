# Cost distance with Arcpy

### Purpose
This python script uses arcpy to create a cost distance raster. In this case, a cost-distance raster is created with travel times from health centers in Djibouti. The travel times can also be referred to as 'isochrones' or 'isodistances' from locations.
In addition, the script creates a shapefile with an isochrone line one hour away from each health center.

Name of script: **cost_distance_with_arcpy.py**

OBS: This script requires a road layer with speeds such as the one created using the script [set_max_speed_to_osm_roads_with_arcpy.py](set_max_speed_to_osm_roads_with_arcpy.py).

### Script explanation

Import the arcpy module.
```
import arcpy, arcinfo
arcpy.CheckOutExtension("Spatial")
```
Define road feature class and print message when done. Edit the path accordingly.
```
roadlayer= r"E:\WBG\Djibouti\osm\dj_roads.gdb\roads\only_roads_osm_ln"
print "layer defined"
```
Add and calculate field 'minutes per meter'. This field contains information on how many minutes it takes to travel one meter at each segment. The value is multiplied by 10,000 since this information will be used to create the raster in the next step and raster files don't deal well with decimals.
Print message when done.
```
arcpy.AddField_management(in_table=roadlayer, field_name="min_per_m", field_type="SHORT", field_precision="", field_scale="", field_length="", field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")

arcpy.CalculateField_management(
    in_table=roadlayer, field="min_per_m", expression=
    "1/!speed_mmin!*10000",
    expression_type="PYTHON", code_block="")

print "minutes to move one second calculated"
```
Convert the road layer to raster format with cell size 100 meters (you can choose any size you wish). Edit path accordingly.
```
arcpy.FeatureToRaster_conversion(in_features=roadlayer, field="min_per_m", out_raster="E:/WBG/Djibouti/osm/osmroad_ras", cell_size="100")
```
Set processing extent before next step. A polygon shapefile of the country of Djibouti is used to set the processing extent. This is done to make sure that the subsequent calculations cover the whole country. Edit path accordingly.
```
arcpy.env.extent = r"E:\WBG\Djibouti\GIS\djibouti_country.shp"
```
Reclassify the raster. Do this to make sure No Data is assigned a value (50 in this case. I also changed the value 600 to 50). This means that it takes 50/10000 minutes (0.3 seconds) to travel 1 meter wherever there is no other value assigned. Arguably, this value could be higher or lower depending on your goal. The way the isochrones look will depend on this value.
Edit path accordingly. A new raster called **osmroad_cd** is created.
```
roadraster = "E:/WBG/Djibouti/osm/osmroad_ras"
arcpy.gp.Reclassify_sa(roadraster, "VALUE", "600 50;NODATA 50", "E:/WBG/Djibouti/osm/osmroad_cd", "DATA")
```
Set mask before the next step. A polygon shapefile of the country of Djibouti is used to set the mask. This is done to make sure that the subsequent analysis is 'masked' to the country. Otherwise the resulting output would be a rectangle, rather than follow the country border, which looks ugly. Edit path accordingly.
```
arcpy.env.mask = r"E:\WBG\Djibouti\GIS\djibouti_country.shp"
```
Run the cost distance tool. For this step you need a shapefile of your points of interest. In this case, health centers (**HealthCenters_wGPS.shp**) are used as the points of interest and this layer is defined first. Set path accordingly. A new raster called **tthealth** is created.
```
points=r"E:\WBG\Djibouti\GIS\HealthCenters_wGPS.shp"
cdraster = "E:/WBG/Djibouti/osm/osmroad_cd"
arcpy.gp.CostDistance_sa(points, cdraster, "E:/WBG/Djibouti/osm/tt_health", "", "", "", "", "", "", "")
```
Use the divide tool to get units back to travel time in minutes from point locations (remember that the units were multiplied by 10,000 to avoid a decimal problem). Set path accordingly. A new raster called **tthealthc** is created.
```
tt_ras="E:/WBG/Djibouti/osm/tt_health"
arcpy.gp.Divide_sa(tt_ras, "10000", "E:/WBG/Djibouti/osm/tthealthc.tif")
```
Lastly, create a "contour line" (isochrone line) at 60 minutes from point locations. Set path accordingly. A shapefile called **contour1h** is created. Print message when done.

```
tt_min_ras="E:/WBG/Djibouti/osm/tthealthc.tif"
arcpy.gp.ContourList_sa(tt_min_ras, "E:/WBG/Djibouti/osm/contour1h.shp", "60")

print "all done"
```
The output should look like this (after symbolizing, etc.)

![alt text](cost_distance_djibouti.jpg "Cost-Distance isochrones Djibouti")
