#!/bin/bash
cd /home/jshantz/dev/raremap/layers/main/clipped/

for i in *.shp
do

  ogr2ogr -f GeoJSON -s_srs EPSG:3857 -t_srs EPSG:4326 /home/jshantz/dev/raremap/layers/output/${i%.*}.geojson $i

done 

cd /home/jshantz/dev/raremap/layers/main/regions/

for i in *.shp
do

  ogr2ogr -f GeoJSON -s_srs EPSG:3857 -t_srs EPSG:4326 /home/jshantz/dev/raremap/layers/output/${i%.*}.geojson $i

done 

cd /home/jshantz/dev/raremap/layers/main/
