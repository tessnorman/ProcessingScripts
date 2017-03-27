# Criticality Analysis
Critical segments in a road network are identified through an iterative process where every road segment is removed from the netowrk, and an origin-destination matrix is run, and compared against the original, un-disturbed model.

## Required Setup
In order to properly execute the tool, you need the following datasets
- Road Network Dataset
- Origins Dataset
- Destination Dataset (can be the same as the origins)
- Road mid-points dataset (these are the road segments that are tested for criticality - this can be a subset of the complete mid-points dataset)

## Demo Instructions
There are two ways to perform the analysis - an arctoolbox and a stand-alone python script.

### ArcToolbox
In the **SampleData** folder, there are sample datasets. In order to perform the analysis, perform the following steps
1. Build the road network
2. In ArcMap, add the road network and the cities
3. Add the **GOST_Criticality_Analysis** toolbox to ArcMap
4. Run an OD Matrix on the road network, with the cities as the origins and destinations
5. Save the lines attribute table
6. Run the tool **Criticality_Analysis_Base**

### Python Script
1. Build the road network dataset
2. Create the road mid-points dataset
3. Open python script and modify input datasets

## Python Script
Once you have completed the above steps, the python script **Processing\Criticality_Analysis_Summaries.py** is used to summarize the results.
