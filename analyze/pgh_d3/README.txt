
Data from http://pittsburghpa.gov/dcp/gis/gis-data (Census Data link)

Things I did to this data before importing it into d3:
ogr2ogr -f GeoJSON -t_srs -t_srs "+proj=longlat +ellps=WGS84 +no_defs +towgs84=0,0,0" neighborhoods.json Neighborhood/Neighborhood.shp
(changing it from Shapefiles into GeoJSON)

topojson neighborhoodstopo.json neighborhoods.json
(changing it from GeoJSON to TopoJSON)

