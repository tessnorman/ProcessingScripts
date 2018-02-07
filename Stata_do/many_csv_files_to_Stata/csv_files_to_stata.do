********************************************************************************
**********Author: Therese Norman
**********Date created: 2018-01-03
**********Data: zonal stats Crop suitability
**********Purpose: convert csv files to Stata format.
********************************************************************************

clear
cd "E:\WBG\FirmLocation\Uganda\UgandaGIS\gis_data\Environment\cropSuitability_FAOGAEZ"

local satafiles: dir . files "*.csv"
foreach file of local satafiles {
    insheet using `file',clear
	rename value newUnitID
	local outfile = subinstr("`file'",".csv","",.)
	rename mean crop_`outfile'
	renvars crop_`outfile', trim(9)
	drop oid count area
    save `outfile'_suit.dta
}

clear
cd "E:\WBG\FirmLocation\Uganda\UgandaGIS\gis_data\Environment\cropSuitability_FAOGAEZ"
mergeall newUnitID using "E:\WBG\FirmLocation\Uganda\UgandaGIS\gis_data\Environment\cropSuitability_FAOGAEZ", dta

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

cd "E:\WBG\FirmLocation\Uganda\Stata_Excel\create_variables_for_new_unit"
save allcrops, replace
