********************************************************************************
**********Author: Therese Norman
**********Date created: 2018-01-12
**********Data: master_panel_2018_01_11_wideTS.dta
**********Purpose: Granger Causality tests per product and market
********************************************************************************

***set workspace, import data and timeseries settings
use "E:\WBG\Somalia\WB Market-Violence\Stata\data\data_TNM\master_panel_2018_01_11_wideTS.dta"
cd "E:\WBG\Somalia\WB Market-Violence\tables"

tsset timem

/*Run Granger causality for products*/
set more off
putexcel set "Granger_Causality_Per_Market3.xlsx", replace
local products g_rSorg g_wMaize g_rice g_cowpeas g_diesel g_oil g_soap g_sugar g_tealeaves g_weahtf
order *, seq /*The variables have to be in sequential order*/

foreach var of local products {
	putexcel set "Granger_Causality_Per_Market3.xlsx", sheet("`var'")  modify
	putexcel A1=("`var'") A1=bold("on")
	putexcel C1=("Granger Causality Test: Wald test")
	putexcel A1:H1=halign("left") A1:H1=border("bottom","thick") A1:H1=bold("on")
	putexcel A3=("Market") B2=("H0: Violence does not Granger-cause Price") ///
	B3=("chi2") C3=("p-value") D3=("Causality 1: YES") ///
	E2=("H0: Price does not Granger-cause Violence") E3=("chi2") F3=("p-value") ///
	G3=("Causality 1: YES") I3=("Optimum lag")

	local row=4
	local i=0
	unab good : `var'*
	foreach x of local good {
		local labmarket: variable label `x'  /* <- save variable label in local `labmarket'*/
		local i=`i'+1
		capture varsoc `x' lndwfatals5`i', maxlag(10) /* <- make sure each variable pair has the same ending numbers, i.e. same market*/
		capture mata: stats = st_matrix("r(stats)") /* <- Use Mata to calculate optimum lag value by finding minimum AIC in matrix*/
		capture mata: result = select((1::rows(stats)), (stats[,7] :== colmin(stats[,7])))
		capture mata: st_numscalar("lag", result) /*save row number as a scalar*/
		capture local opt_lag = lag-1 /* <- optimum lag is the row number of minimum AIC minus 1*/
		capture noisily var `x' lndwfatals5`i', lags(`opt_lag') /* <- make sure each variable pair has the same ending numbers, i.e. same market*/
		capture vargranger /* <- The G-C wald test*/
		putexcel A`row'=("`labmarket'")
		matrix results = r(gstats)
		matrix a = results[1,1]
		matrix b = results[1,3]
		matrix c = results[3,1]
		matrix d = results[3,3]
		putexcel B`row' =matrix(a) C`row' =matrix(b) E`row' =matrix(c) F`row' =matrix(d) ///
		D`row'=formula(=IF(NOT(ISBLANK(C`row')),IF(C`row'<0.05,1,0),0.01)) ///
		G`row'=formula(=IF(NOT(ISBLANK(F`row')),IF(F`row'<0.05,1,0),0.01)) ///
		I`row'=("`opt_lag'")
		putexcel B`row':C`row'=nformat("number_d2") E`row':F`row'=nformat("number_d2")
		local ++row
	}
	putexcel D49=formula(=SUM(D3:D46)) G49=formula(=SUM(G3:G46))
}
