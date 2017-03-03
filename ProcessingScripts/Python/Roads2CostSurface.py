# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# Roads2CostSurface in ArcPy Keith Garrett 
# Description: This script converts vector data of transportation features, like roads, and adds border delays and delays caused by other features, such as open water, 
# into a raster dataset in which every square kilometer equals the number of minutes it takes to cross that particular kilometer at the maximum legal or technological speed.
# This Cost Surface layer can then be used for a series of related accessability analyses. The result allows one to calculate relative accessibility/cost of transportation to any location in the region of interest from any other region. 
# It has not yet been tested, debugged, or streamlined.  Please use feel free to edit!
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy

# Check out any necessary licenses
arcpy.CheckOutExtension("spatial")


# Local variables:
wpath = [input]
fpath = [input]

OpenWater = 
BorderDelays = 
Roads = wpath + 
Input_raster_or_constant_value_2 = "60"

#CS stands for Cost Surface layer, R is for Roads, F is for Ferry, W is for Water, B is for Borders, N is for "Not present", C is for "Proposed Corrdidor improvement"
CS_RFW = wpath + "\\CS_RFW"
CS_BNCN_Reclass = wpath + "\\CS_BNCN_Reclass"
CS_BNCN_float = wpath + "\\CS_BNCN_float"
CS_OpenWater_400 = wpath + "\\CS_OpenWater_400"
RF = wpath + "\\RF"
CS_BNCN_ReclassA = wpath + "\\CS_BNCN_ReclassA"
CS_W = wpath + "\\CS_W"
CS_BNCN_MPKm = wpath + "\\CS_BNCN_MPKm"
Brder = wpath + "\\Brder"
Times_Brder1 = wpath + "\\Times_Brder1"
Reclass_Time1 = wpath + "\\Reclass_Time1"
CS_BCN_MPKm = wpath + "\\CS_BCN_MPKm"

# This converts the vector data to raster data based on a specified attribute and addresses some of the data clean up that needs to happen with those values. Your vector data needs to have 
arcpy.gp.PolylineToRaster(Roads,"Speed_est", RF)
arcpy.gp.Reclassify_sa(Times_Brder1, "Value", "60 60;60 90 90;90 150 150;150 300 300;300 1500 1500;NODATA 0", Reclass_Time1, "NODATA")
arcpy.gp.Reclassify_sa(RF, "VALUE", "0 5;19.981000900268555 21.366519632559257 20;21.366519632559257 31.874700975929912 30;31.874700975929912 46.254317551068688 45;46.254317551068688 51.268747946501705 50;51.268747946501705 70.367828423224509 70;70.367828423224509 90.27806675803204 90;90.27806675803204 100.78624810140269 100;100.78624810140269 120 120;400 400;401 520 30;NODATA 5", CS_BNCN_ReclassA, "NODATA")

# This converts a vector dataset of the open water into a raster dataset
arcpy.PolygonToRaster_conversion(OpenWater, "GridCode_1", CS_OpenWater_400, "CELL_CENTER", "NONE", "1000")

# This converts the prior data into a raster dataset with a time value and assembles them
arcpy.gp.Reclassify_sa(CS_OpenWater_400, "VALUE", "1 1;NODATA 5", CS_W, "NODATA")
arcpy.gp.Plus_sa(CS_BNCN_ReclassA, CS_W, CS_RFW)

# This reclass cleans up new invalid values created by the stacking of different feature types to give the entire area a consistent value in Minutes Per Kilometer. 
arcpy.gp.Reclassify_sa(CS_RFW, "VALUE", "6 1;10 10;21 1;25 20;31 30;35 30;46 1;50 50;51 1;55 50;71 1;75 70;91 1;95 90;105 100;125 120;NODATA 5", CS_BNCN_Reclass, "NODATA")

# This converts the data to a data type that can accomodate decimal points, which is required on division. 
arcpy.gp.Float_sa(CS_BNCN_Reclass, CS_BNCN_float)

# This converts the speed value of the road raster into a minutes per kilometer value
arcpy.gp.RasterCalculator_sa("float(60)/\"%CS_BNCN_float%\"", CS_BNCN_MPKm)

# Assembles the final CS layer from Roads, Borders, Water against which Cost Distance functions in spatial analyst can be run. 
arcpy.gp.Plus_sa(Reclass_Time1, CS_BNCN_MPKm, CS_BCN_MPKm)

