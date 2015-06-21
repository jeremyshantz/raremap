#!/bin/bash
cd /home/jshantz/dev/raremap/layers/main/regions/
rm /home/jshantz/dev/raremap/layers/main/regions/*.geojson
rm /home/jshantz/dev/blog/deploy/map/data/*

for i in *.shp
do
  	ogr2ogr -f GeoJSON -s_srs EPSG:3857 -t_srs EPSG:4326 ${i%.*}.geojson $i
done 

cp /home/jshantz/dev/raremap/layers/main/regions/*.geojson /home/jshantz/dev/blog/deploy/map/data/
