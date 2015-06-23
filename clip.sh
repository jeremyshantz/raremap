#!/bin/bash
cd /home/jshantz/dev/raremap/layers/main/dump2/

for i in *.shp
do

	ogr2ogr -nlt POLYGON  -skipfailures -clipsrc /home/jshantz/dev/raremap/layers/main/dump/${i%.*} /home/jshantz/dev/raremap/layers/main/clipped/${i%.*} /home/jshantz/dev/raremap/layers/main/dump2/$i

done 

cd /home/jshantz/dev/raremap/layers/main/
