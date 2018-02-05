# Travel Time Speeds and Cost Distance Analysis

This directory contains two python scripts that uses arcpy to
1. [Assign travel speeds to an OSM road layer](set_max_speed_to_osm_roads_with_arcpy.py). Explanation: [set_travel_speeds.md](set_travel_speeds.md).
2. [Create a cost distance (isochrone) raster](cost_distance_with_arcpy.py). Explanation: [cost_distance.md](cost_distance.md).

This analysis uses OSM roads covering Djibouti as the main input. The resulting output is a raster file showing travel times from health centers in Djibouti as in the screenshot below.

![Cost-Distance isochrones Djibouti](cost_distance_djibouti.jpg)

<p align="center">
  <img src="cost_distance_djibouti.jpg" />
</p>
