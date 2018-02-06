********************************************************************************
**********Author: Therese Norman
**********Date created: 2017-11-20
**********Purpose: Restructure data into time series from panel.
********************************************************************************

***set workspace, import data and panel settings
cd "E:\WBG\Somalia\WB Market-Violence\Stata\data\data_TNM"
master_panel.dta, clear
xtset uniqueID timem
set more off

*******from long to wide only market prices growth and violence
local varlist g_rSorg g_wMaize g_rice g_weahtf g_cowpeas g_sugar g_tealeaves ///
g_oil g_diesel g_soap d_dwfatals5 lndwfatals5

keep timem uniqueIDmarket `varlist'
reshape wide `varlist', i(timem) j(uniqueIDmarket)
save mktprices_growth_violence_wideTS.dta
