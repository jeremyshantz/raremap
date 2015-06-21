import processing
import os
from os import listdir
from os.path import isfile, join, basename

root = QgsProject.instance().layerTreeRoot()
crs = QgsCoordinateReferenceSystem(3857, QgsCoordinateReferenceSystem.EpsgCrsId)
outputcrs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
basepath = '/home/jshantz/dev/raremap'

commonpath =  basepath + '/layers/main/common/'
regionpath = basepath + '/layers/main/regions/'
dumppath =  basepath + '/layers/main/dump/'
dumppath2 =  basepath + '/layers/main/dump2/'
outputpath =  basepath + '/layers/output/' # geojson goes here

def doCommonNames():

  removeGroup('common')
  emptyFolder(commonpath)
  emptyFolder(regionpath)
 # emptyFolder(dumppath)
 # emptyFolder(dumppath2)
  emptyFolder(outputpath)
  
  # split
  processing.runalg("qgis:splitvectorlayer", basepath+'/layers/main/commonnames.shp', 'MWShapeID', commonpath)

  files = [ f for f in listdir(commonpath) if isfile(join(commonpath,f)) and f.endswith('.shp') ]
  for f in files:
    doSingleCommonName(join(commonpath, f))
  
def doSingleCommonName(path):
    
  newname = os.path.splitext(basename(path))[0].replace('commonnames_', '') + '.shp'
  output = join(regionpath, newname)
  vlayer = QgsVectorLayer(path, newname, "ogr") 
  
  extent = vlayer.extent()
  extentstr = '%.2f, %.2f, %.2f, %.2f' % (extent.xMinimum(), extent.xMaximum(), extent.yMinimum(), extent.yMaximum())
  tile_width = 100
  tile_height = 60

  result = processing.runalg('qgis:vectorgrid', extentstr, tile_width, tile_height, 0, output)
 # result = processing.runalg('gdalogr:clipvectorsbypolygon', result['OUTPUT'], path, None, output)
  
  layer2 = QgsVectorLayer(output, newname, "ogr")
  layer2.setCrs(crs)
  
  
  QgsVectorFileWriter.writeAsVectorFormat(layer2, output, "utf-8", crs, "ESRI Shapefile")
  
  QgsMapLayerRegistry.instance().addMapLayer(layer2, False)
  root.findGroup('common').insertChildNode(0, QgsLayerTreeLayer(layer2))
  
  #saveAsGeoJson(output)

def doTiles():

  try:
    # emptyFolder(dumppath)

    # split each region into its tiles
    files = [ f for f in listdir(regionpath) if isfile(join(regionpath,f)) and f.endswith('.shp') ]
    for f in files:
        processing.runalg("qgis:splitvectorlayer", join(regionpath, f), 'id', dumppath)

    # process each tile
    files = [ f for f in listdir(dumppath) if isfile(join(dumppath,f)) and f.endswith('.shp') ]
    for f in files:
      doSingleTile(join(dumppath, f))
      
    
    # emptyFolder(dumppath)
  except Exception as ex:
    print ex

def doSingleTile(path):

  try:
    newname = 'R' + os.path.splitext(basename(path))[0].replace('.shp', '').replace('id', '').replace('MWShapeID', '').replace('__', '_')

    tempoutput = join(dumppath2, newname) + '.shp'
    
    vlayer = QgsVectorLayer(path, newname, "ogr") 
    vlayer.setCrs(crs)
    
    extent = vlayer.extent()
    extentstr = '%.2f, %.2f, %.2f, %.2f' % (extent.xMinimum(), extent.xMaximum(), extent.yMinimum(), extent.yMaximum())
    tile_width = 2
    tile_height = 2

    t1 = join(dumppath2, newname) + '_GRID.shp'
    
    result = processing.runalg('qgis:vectorgrid', extentstr, tile_width, tile_height, 0, tempoutput)
    
    vlayer = QgsVectorLayer(t1, newname, "ogr") 
    vlayer.setCrs(crs)
    print(path)
    print(t1)
    # result['OUTPUT']
   # result = processing.runalg('gdalogr:clipvectorsbypolygon', t1, path, None, tempoutput)
    
    vlayer = QgsVectorLayer(tempoutput, newname, "ogr") 
    vlayer.setCrs(crs)
    print(tempoutput)
    
  except Exception as ex:
    print ex + ' ' + path
    
def emptyFolder(path):
  # delete all the files from disk
  files = [ f for f in listdir(path) if isfile(join(path,f))]
  for f in files: 
    os.remove(join(path,f))

def removeGroup(group):
  root.removeChildNode(root.findGroup('common'))
  root.insertGroup(0, "common")

def saveAsGeoJson(path):
  name = os.path.splitext(basename(path))[0]
  name = join(outputpath, name) + '.geojson'
  layer = QgsVectorLayer(path, "name", "ogr") 
  QgsVectorFileWriter.writeAsVectorFormat(layer, name, "utf-8", layer.crs(), "GeoJson")
      
#emptyFolder(outputpath)
doCommonNames()
doTiles()

#doSingleCommonName('/home/jshantz/dev/raremap/layers/main/commonnames_MWShapeID_0.shp')
#doSingleTile('/home/jshantz/dev/raremap/layers/main/dump/MWShapeID_0.shp_id_31.shp')