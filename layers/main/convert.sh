#!/bin/bash
cd /home/jshantz/dev/raremap/layers/main/dump2/

for i in *.shp
do
	# echo ogr2ogr -f GeoJSON -s_srs EPSG:3857 -t_srs EPSG:4326 ${i%.*}.geojson $i
	echo ogr2ogr /home/jshantz/dev/raremap/layers/main/clipped/${i%.*}.shp $i
echo ogr2ogr -nlt POLYGON   -clipsrc  ../dump/MWShapeID_0.shp_id_302.shp ./testclip4.shp  ./R_0_302.shp -skipfailures

done 

