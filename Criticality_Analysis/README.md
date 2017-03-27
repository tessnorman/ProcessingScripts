#Criticality Analysis
Through a combination of ArcGIS Network analysis and python summaries, the most critical network connections in a network can be identified

##Required Setup
In order to properly execute the tool, you need the following datasets
- Road Network Dataset
- Origins Dataset
- Destination Dataset (can be the same as the origins)

##Demo Instructions
In the **SampleData** folder, there are sample datasets. In order to perform the analysis, perform the following steps
1. Build the road network
2. In ArcMap, add the road network and the cities
3. Add the **GOST_Criticality_Analysis** toolbox to ArcMap
4. Run an OD Matrix on the road network, with the cities as the origins and destinations
5. Save the lines attribute table
6. Run the tool **Criticality_Analysis_Base**

###Python Script
Once you have completed the above steps, the python script **Processing\Criticality_Analysis_Summaries.py** is used to summarize the results.