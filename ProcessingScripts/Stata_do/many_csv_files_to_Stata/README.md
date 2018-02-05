# Convert many csv files into one Stata file

### Purpose
This do script quickly converts previously created csv files into one Stata file. Each csv file represents zonal stats of different crops for Ugandan subcounties. Since each file has the same variable names, the variables have to be renamed to match the given crop.

Name of script: [csv_files_to_stata.do](csv_files_to_stata.do)

Click here for explanation and script for the creation of the [(zonal stats of 18 different crop-suitability-rasters for Ugandan subcounties)](/../../Python/zonal_stats_crop_suitability/README.md).

### Script explanation
*OBS. Always set the path according to your own directory.*

Set the working directory to be the same as the folder containing all the csv files
```
clear
cd "E:\WBG\FirmLocation\Uganda\UgandaGIS\gis_data\Environment\cropSuitability_FAOGAEZ"
```
Define a local macro with all csv files.
```
local satafiles: dir . files "*.csv"
```
The following loop:
1. Imports each csv file
2. Renames the variable 'value' (the unique identifier) to 'newUnitID'
3. Defines a local macro with the imported file name stripped of .csv extension.
4. Renames the variable 'mean' (the zonal stats value) to crop_+file name created in previous step.
5. Trim the variable name and keep only the first 9 characters (eg. crop_bana in the case of banana)
6. Drop unnessary create_variables_for_new_unit
7. Save each file.
```
foreach file of local satafiles {
  insheet using `file',clear
	rename value newUnitID
	local outfile = subinstr("`file'",".csv","",.)
	rename mean crop_`outfile'
	renvars crop_`outfile', trim(9)
	drop oid count area
    save `outfile'_suit.dta
}
```
Clear and set working directory again.
```
clear
cd "E:\WBG\FirmLocation\Uganda\UgandaGIS\gis_data\Environment\cropSuitability_FAOGAEZ"
```
Merge all Stata files (there is one for each crop) into one.
```
mergeall newUnitID using "E:\WBG\FirmLocation\Uganda\UgandaGIS\gis_data\Environment\cropSuitability_FAOGAEZ", dta
```
Label variables (all the 18 crops).
```
label var	crop_bana	"banana -avg kg DW/ha-attainable yield low input level rain-fed, bp 61-90"
label var	crop_casv	"cassava -avg kg DW/ha-attainable yield low input level rain-fed bp, 61-90"
label var	crop_coco	"cocoa -avg kg DW/ha-attainable yield low input level rain-fed, bp 61-90"
label var	crop_coff	"coffee -avg kg DW/ha-attainable yield low input level rain-fed,  bp 61-90"
label var	crop_cott	"cotton- avg kg DW/ha-attainable yield low input level rain-fed, bp 61-90"
label var	crop_grnd	"groundnut -avg kg DW/ha-attainable yield low input level rain-fed, bp 61-90"
label var	crop_maiz	"maize -avg kg DW/ha-attainable yield low input level rain-fed, bp 61-90"
label var	crop_pmlt	"pearl millet- avg kg DW/ha-attainable yield low input level rain-fed, bp 61-90"
label var	crop_ricd	"rice dryland- avg kg DW/ha-attainable yield low input level rain-fed, bp 61-90"
label var	crop_ricw	"rice wetland -avg kg DW/ha-attainable yield low input level rain-fed, bp 61-90"
label var	crop_sorg	"sorghum -avg kg DW/ha-attainable yield low input level rain-fed, bp 61-90"
label var	crop_soyb	"soybean -avg kg DW/ha-attainable yield low input level rain-fed, bp 61-90"
label var	crop_spot	"sweet potato -avg kg DW/ha-attainable yield low input level rain-fed, bp 61-90"
label var	crop_sugc	"sugarcane -avg kg DW/ha-attainable yield low input level rain-fed, bp 61-90"
label var	crop_teas	"teas -avg kg DW/ha-attainable yield low input level rain-fed, bp 61-90"
label var	crop_toba	"tobacco -avg kg DW/ha-attainable yield low input level rain-fed, bp 61-90"
label var	crop_whea	"wheat -avg kg DW/ha-attainable yield low input level rain-fed, bp 61-90"
label var	crop_wpot	"white potato -avg kg DW/ha-attainable yield low input level rain-fed, bp 61-90"
```
Save the final Stata file **allcrops** in desired directory.
```
cd "E:\WBG\FirmLocation\Uganda\Stata_Excel\create_variables_for_new_unit"
save allcrops, replace
```
