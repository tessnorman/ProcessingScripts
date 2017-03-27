# Geospatial Operational Support Team (GOST)
## Introduction
This repository is the evolving, growing workspace where GOST stores libraries and scripts for operationalizing the many initatives currently on going in the geospatial realm within the World Bank Group. The basic structure of the repository separates the code into two sections:

### GOSTRocks
This library was created by Ben Stewart, and contains often re-used functions for processing geospatial data in an ArcPy framework. The library includes functions for 
- performing zonal statistics on multiple numerical and categorical raster datasets
- writing shapefiles to excel tables
- the Urban library, meant to centralize the numerous urbanization metrics GOST calculates, including nighttime lights urban extents, population grid mapping of urban areas, standard mapping of built-up areas (GHSL and GUF).

### ProcessingScripts
This folder contains a number of commonly used scripts for processing geospatial data. The folder is structured by the language of the processing code, but is not a library structure as in the **GOSTRocks** Library.

### Criticality Analysis  
This road network analysis uses an Origin-Destination approach to assess which road segments are most critical to maintaining connectivity across a network. See folder for more details
