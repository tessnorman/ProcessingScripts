////////////////////////////////////////////////////////////////////////////////
////////////////Using the OSRM command to calculate travel times////////////////
////////////////Therese Norman 02-02-2016                       ////////////////
////////////////////////////////////////////////////////////////////////////////


***install files
net install osrmtime, from("http://www.uni-regensburg.de/wirtschaftswissenschaften/vwl-moeller/medien/osrmtime")

net get osrmtime, from("http://www.uni-regensburg.de/wirtschaftswissenschaften/vwl-moeller/medien/osrmtime")
shell osrminstall.cmd

****Prepare map (already downloaded the OSM data-morocco-latest.osm.pbf)
osrmprepare, mapfile("C:/scratch/Morocco/morocco-latest.osm.pbf") profile(car)

****import a shapefile with long and lat coordinates of ward centroids and convert to .dta (this could come from anywhere, just needs to be a dataset with long and lat coordinates)
****This will be the file I will work with
clear
cd C:/scratch/Morocco/
shp2dta using 5kfishnet_label, data("Origins")  coor("Origins_coordinates")
shp2dta using Market_Cities_sub, data("Destinations")  coor("Destinations_coordinates")
use Origins.dta


/*If you want to calculate travel times between all coordinate combinations
generate Origin and Destination datasets in order to create pairwaise combinations.
Then use cross command to join as pairwise combinations-this will expand the dataset.*/

egen coord=concat(Lat Long),  punct(,)   /*easier to work with the coordinates if they are in one variable*/
keep wardID coord
save Origin_Morocco.dta, replace
rename wardID wardID_dest
rename coord coord_dest
save DestMorocco.dta, replace

use Origin_Morocco.dta
cross using DestMorocco
split coord, destring p(,)
rename coord1 lat_origin
rename coord2 long_origin
split coord_dest, destring p(,)
rename coord_dest1 lat_dest
rename coord_dest2 long_dest

save OD_MRA.dta, replace


****calculate travel time and distances:
osrmtime lat_origin long_origin lat_dest long_dest , mapfile("C:\Scratch\Morocco\morocco-latest.osrm")

****merge on population and calculate MP index
gen distKM=(distance+jumpdist1*2+jumpdist2*2)/1000   /*these calculations are arbitrary, my choice to calculate total travel distance this way*/
replace distKM=0 if distance==0
gen distHour=(duration+jumpdist1/2+jumpdist2/2)/3600 /*these calculations are arbitrary, my choice to calculate total travel time this way*/
replace distHour=0 if duration==0
rename wardID wardID_origin
rename wardID_dest wardID
merge m:1 wardID using centroidWardp.dta   /*merge on population on to destination ward ID*/
label var wardID_origin "Origin ID"
label var wardID "Destination ID"
label var distKM "Distance from origin to destination in km"
label var distHour "Travel time from origin to destination in hours"

****calculate travel time index with different lambdas including own ward 
gen MP005= POP*exp(-0.05*distHour)
gen MP01= POP*exp(-0.1*distHour)
gen MP05= POP*exp(-0.5*distHour)
gen MP1= POP*exp(-1*distHour)
gen MP3p8= POP*exp(-3.8*distHour)
gen MP5= POP*exp(-5*distHour)
gen MP7p5= POP*exp(-7.5*distHour)

****calculate travel time index with different lambdas excluding own ward 
gen own =0
replace own=1 if wardID==wardID_origin
gen MPdom005= POP*exp(-0.05*distHour) if own==0
gen MPdom01= POP*exp(-0.1*distHour) if own==0
gen MPdom05= POP*exp(-0.5*distHour) if own==0
gen MPdom1= POP*exp(-1*distHour) if own==0
gen MPdom3p8= POP*exp(-3.8*distHour) if own==0
gen MPdom5= POP*exp(-5*distHour) if own==0
gen MPdom7p5= POP*exp(-7.5*distHour) if own==0

label var MP005 "Market Potential (access to pop) using OSM 2016, lambda:0.005"
label var MP01 "Market Potential (access to pop) using OSM 2016, lambda:0.01"
label var MP05  "Market Potential (access to pop) using OSM 2016, lambda:0.5"
label var MP1  "Market Potential (access to pop) using OSM 2016, lambda:1"
label var MP3p8  "Market Potential (access to pop) using OSM 2016, lambda:3.8"
label var MP5  "Market Potential (access to pop) using OSM 2016, lambda:5"
label var MP7p5 "Market Potential (access to pop) using OSM 2016, lambda:7.5"

label var MPdom005 "Market Potential excluding own (access to pop) using OSM 2016, lambda:0.005"
label var MPdom01 "Market Potential excluding own (access to pop) using OSM 2016, lambda:0.01"
label var MPdom05  "Market Potential excluding own (access to pop) using OSM 2016, lambda:0.5"
label var MPdom1  "Market Potential excluding own (access to pop) using OSM 2016, lambda:1"
label var MPdom3p8  "Market Potential excluding own (access to pop) using OSM 2016, lambda:3.8"
label var MPdom5  "Market Potential excluding own (access to pop) using OSM 2016, lambda:5"
label var MPdom7p5 "Market Potential excluding own (access to pop) using OSM 2016, lambda:7.5"

***collapse dataset and sum up over wardID
collapse (sum) MP005 MP01 MP05 MP1 MP3p8 MP5 MP7p5 MPdom005 MPdom01 MPdom05 MPdom1 MPdom3p8 MPdom5 MPdom7p5, by(wardID_origin)
rename wardID_origin wardID
save MP_OSM_MRA.dta, replace
