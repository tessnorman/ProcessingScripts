********************************************************************************
**********Author: Therese Norman
**********Date created: 2018-03-16
**********Data: origin-destination travel time matrix (eg: )
**********Purpose: Estimate distance discounting factor
********************************************************************************

**set workspace
cd E:\WBG\GOST\OSRMtool\Uganda

**open up O-D travel times dataset.
use "osrm_traveltimes_uganda.dta", clear

/*If you haven't already, merge on any relevant
variables to perform this analysis. At a minimum, you need a "size" variable for
all destinations for the Market Potential calculations - in this case we use
Population. You also need the sector-specific dependent variables for all origins
- in this case we use Employment per sector.

In this case, the variables that will be used for the analysis are:
mixcode3 - unique ID of origin
mixcode3dest - unique ID of destination
distMin - Travel time in minutes between origin and destination
POP - Population of destination
emptot11 - total employment of origin
foodEmp11 -  food-processing employment of origin
farmEmp11 -  farm employment of origin
otherEmp11 -  manufacturing (not food) employment of origin
tradeEmp11 -  retail and wholesale employment of origin

*/

************************** Prepare the data

**generate a dummy variable 'D' identifying 1 observation for each origin.
** 	This dummy will be used for the regressions later.
gsort mixcode3 mixcode3_dest /*sort observations*/
bysort mixcode3: gen D=mixcode3_dest== mixcode3_dest[1] /*tag first observation in each group*/

/* Create a variable identifying if origin and destination are the same.
The internal population may or may not be counted toward total market potential.*/
gen own =0
replace own=1 if mixcode3==mixcode3_dest


** log the dependent variables to normalize their distributions (if necessary).
** leave missing values blank, only perform the analysis where there is any employment.
local sectors emptot11 foodEmp11 farmEmp11 otherEmp11 tradeEmp11
foreach var of varlist `sectors' {
	gen ln`var'=ln(`var')
}
** take a look at how many missing values there are
misstable sum `sectors' if D==1

**save before estimations
save osrm_traveltimes_uganda, replace

************************** Estimate lambda
display "$S_TIME  $S_DATE"

**write the results to an excel table
putexcel set "lambdas.xlsx", replace

local sectors emptot11 foodEmp11 farmEmp11 otherEmp11 tradeEmp11
local c=65 /*counter for letters in alphabet for use in output excel. 65=A, 66=B, 67=C, etc.*/
foreach var of varlist `sectors' {
	local c=`c'+1
	putexcel set "lambdas.xlsx", modify
	putexcel A1="lambda", bold
	putexcel `=char(`c')'1="R2_`var'", bold


	local row=2 /*counter for rows in output excel, one row per lambda*/
	forval i=0.001(0.001)0.101 { /*try all lambdas in increments*/
		tempvar MP
		quietly gen `MP'=  POP*exp(-`i'*distMin) if own==0 /*formula to calculate MP*/
		tempvar sum`MP'
		quietly egen `sum`MP''=total(`MP'), by(mixcode3) /*sum up MP over origins*/
		tempvar ln`sum`MP''
		gen `ln`sum`MP'''=ln(`sum`MP'') /*take log to normalize distribution*/
		quietly reg ln`var' `ln`sum`MP''' if D==1 /*regress dependent variable of sector `var' on MP with lambda `i'*/
		quietly putexcel A`row'=(`i') `=char(`c')'`row'=(e(r2))  /*write lambda and R2 of regression output to excel*/
		local ++row
	}
	di "`var'" /*display sector to keep track of where the calculations are*/
}

*
/*
For the excel file: Import sheet. Sort lambdas by highest R2. Create temporary
variables and locals (to be held in memory after loop finishes) of the most
optimal lambda (with highest R2). Save in locals as both number and string.
Sort in order of size of lambda and create a line graph of lambdas versus R2
for each sector.
*/

set more off
import excel using lambdas.xlsx, first clear
unab R2sectors: R2* /*local for all sectors (they all start with R2)*/
foreach var of varlist `R2sectors' {
	gsort -`var'
		tempvar lambdaOpt
		gen `lambdaOpt' =lambda[1]
		local lOpt`var' =`lambdaOpt'
		di "`lOpt`var''"
		tempvar lambdaOpt_str
		tostring `lambdaOpt', generate(`lambdaOpt_str') force format(%9.0g)
		local lambdaOpt`var'_s = subinstr(`lambdaOpt_str',".","_",.)
	sort lambda
	quietly line `var' lambda, title("Lambda vs `var'") ytitle("R2")
	quietly graph export graph_`var'.png, as(png) replace
}

/*
Open up the travel times file again. Calculate MP by using the optimal lambdas
for each sector. Also calculate MP by using a few set lambdas. (these may or
may not be the same as the optimal lambdas). Aggregate over origin location,
label variables and save output as both dta and excel file. Done.
*/

use osrm_traveltimes_uganda, clear

foreach var of varlist `sectors' {
	gen MPopt`lambdaOptR2_`var'_s'`var'=  POP*exp(-`lOptR2_`var''*distMin)
}

****calculate travel time index with different set lambdas excluding own
gen MP_7 = POP*exp(-0.7*distMin)   if own==0
gen MP_07= POP*exp(-0.07*distMin)  if own==0
gen MP_02= POP*exp(-0.02*distMin)  if own==0
gen MP_01= POP*exp(-0.01*distMin)  if own==0
gen MP_004= POP*exp(-0.004*distMin) if own==0

****calculate travel time index with different set lambdas including own
gen MPiequalj_7=  POP*exp(-0.7*distMin)
gen MPiequalj_07= POP*exp(-0.07*distMin)
gen MPiequalj_02= POP*exp(-0.02*distMin)
gen MPiequalj_01= POP*exp(-0.01*distMin)
gen MPiequalj_004= POP*exp(-0.004*distMin)

unab MPvars: MP*
collapse (sum) `MPvars' , by(mixcode3)

****label variables
foreach var in `sectors' {
		label var MPopt`lambdaOptR2_`var'_s'`var' "Market Potential, optimal lambda for `var': `lOptR2_`var''"
}
label var MPiequalj_7 "Market Potential (access to pop) using OSM, lambda:0.7"
label var MPiequalj_07 "Market Potential (access to pop) using OSM, lambda:0.07"
label var MPiequalj_02 "Market Potential (access to pop) using OSM, lambda:0.02"
label var MPiequalj_01 "Market Potential (access to pop) using OSM, lambda:0.01"
label var MPiequalj_004 "Market Potential (access to pop) using OSM, lambda:0.004"
label var MP_7 "Market Potential excluding own (access to pop) using OSM, lambda:0.7"
label var MP_07 "Market Potential excluding own (access to pop) using OSM, lambda:0.07"
label var MP_02 "Market Potential excluding own (access to pop) using OSM, lambda:0.02"
label var MP_01 "Market Potential excluding own (access to pop) using OSM, lambda:0.01"
label var MP_004 "Market Potential excluding own (access to pop) using OSM, lambda:0.004"

save MP_final, replace
export excel using MP_final.xlsx, replace firstrow(variables)
display "$S_TIME  $S_DATE"
