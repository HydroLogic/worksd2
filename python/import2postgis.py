__author__ = 'ifadmin'

import os, sys
from osgeo import ogr

baseDir = r'F:\01_GIS_DATA\NHD_HighRes'

os.chdir(baseDir)

hucList = []
for dir in os.listdir(baseDir):
    if dir.startswith("NHD"):
        hucList.append(dir)

print hucList

import psycopg2
conn = psycopg2.connect("dbname=flood user=ifadmin port=XXX password=XXX")
cursor = conn.cursor()


hucFlowDict = []
hucLineDict = []
hucAreaDict = []
hucWatBdDict = []

for huc in hucList:
    huc2 = huc[4:6]
    huc4 = huc[4:8]
    print "Working on HUC" + huc2
    hucDir = os.path.join(baseDir, huc)
    #All input files names as variables
    #First linefiles
    hucFlow = os.path.join(hucDir, "NHDFlowline.shp")
    hucFlowDict.setdefault(huc2,[]).append(hucFlow)
    hucLine = os.path.join(hucDir, "NHDLine.shp")
    hucLineDict.setdefault(huc2,[]).append(hucLine)
    #Polygons now
    hucArea = os.path.join(hucDir, "NHDArea.shp")
    hucAreaDict.setdefault(huc2,[]).append(hucFlow)
    hucWatBd = os.path.join(hucDir, "NHDWaterbody.shp")
    hucWatBdDict.setdefault(huc2,[]).append(hucFlow)


cursor.execute('create table if not exists ')


