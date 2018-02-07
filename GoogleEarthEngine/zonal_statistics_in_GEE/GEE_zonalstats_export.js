//By: Jia Jun Lee
//import raster (for NDVI, google has made this available)

//define feature collection (vector)
var p2_cover_1=ee.FeatureCollection('ft: insert fusion table id');

//reduce region does the zonal stats. for-loop does it repetitively for index 0-482. wrap in feature collection.
var index;
var allFeatures = [];
for (index = 0; index <= 482; index++) {
  var cd = evalSites2.filterMetadata('uniqueID', 'equals', index);
  var stats = ndvi04.reduceRegion({ reducer: ee.Reducer.mean(), geometry: cd,scale: 30,maxPixels: 10e15  });
  allFeatures.push(ee.Feature(null, {index:index, ndvi:stats}));

}

//export feature collection to CSV in google drive
var allFeaturesCollection = ee.FeatureCollection(allFeatures);
Export.table.toDrive({
    collection:allFeaturesCollection,
    description:"SEZ_NDVI_046_real",
    fileFormat:'CSV'
});
