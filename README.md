# Notes from lab machine 


## Needed lists that I could need and need some more:

### HUC Zone List ConUSA
		huclist = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18"]
### State Lists ConUSA
		stateabbreviations = ['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']
		statenames = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]


### Command Line

#### CSVkit

Print column names: ```csvcut -n data.csv ```


#### OGR
Select from 2010 Census Housing Block files 
```Shell
for /R %f in (*.shp) do ogr2ogr -sql "SELECT * FROM %~nf where HOUSING10 > 0 or POP10 > 0" %~nf_small.shp %f
```

#### GDAL
Create a ~30m grid from floodplain results
```Shell

gdal_rasterize -a fldht_m -l hr_floodplain_complete_binned_final -a_nodata -9999 -tr 0.00034 0.00034 -tap -ot Float32 hr_floodplain_complete_fh.vrt harris30m_100yr_fp_1.tif

gdal_rasterize -at -burn 1 -init 0 -ot Byte -tr 0.0002778 0.0002778 -co COMPRESS=LZW -a_nodata -9999 -l dfirm19011C_poly dfirm19011C_poly.shp dfirm19011C_poly.tif

gdal_translate -a_nodata -9999 -co tiled=yes -co bigtiff=yes -co compress=lzw ras100yrfldht.vrt conusa_100yr.tif

Read from a zip file: 

ogrinfo -ro /vsizip/wbdhu8_a_us_march2015.gdb.zip/wbdhu8_a_us_march2015.gdb

ogr2ogr PG:"dbname='shapes' host='localhost' port='5433'" /vsizip/Trecks.gdb.zip/Trecks.gdb
```
#### AWS
```Shell

aws s3 mb s3://dfirm-raw
make_bucket: s3://dfirm-raw/

```


## SQL & pgSQL

### Basic Operators

Create a new user for the database:
Unix shell [ubuntu](https://help.ubuntu.com/community/PostgreSQL): 
		sudo -u postgres createuser -D -A -P myuser
		sudo -u postgres createdb -O myuser mydb


Create the postgis extentsions:
```SQL
CREATE EXTENSION postgis;
CREATE EXTENSION postgis_topology;
CREATE EXTENSION fuzzystrmatch;
CREATE EXTENSION postgis_tiger_geocoder;
```

### Geometry and PostGIS

Add a geometry column for latitude and longitude
		SELECT AddGeometryColumn ('fema_aal','res2013_fixedriv_v2_location','geom',4269,'POINT',2);
Populate the geometry column (in this case our lat/long was in character format so we had to cast to real)
		UPDATE fema_aal.res2013_fixedriv_v2_location SET geom = ST_SetSRID(ST_MakePoint("LON"::real, "LAT"::real),4269);
Create a GIS index
		CREATE INDEX idx_res2013_geom_lonlat ON fema_aal.res2013_fixedriv_v2_location USING GIST (geom);
Cluster the points
		CLUSTER idx_res2013_geom_lonlat ON fema_aal.res2013_fixedriv_v2_location;
Vacuum and Analyze the table
		VACUUM ANALYZE fema_aal.res2013_fixedriv_v2_location;
		CREATE INDEX idx_zctas_thepoint_meter ON zctas
  		USING GIST (thepoint_meter);
Random Shit
		ALTER TABLE zctas ALTER COLUMN thepoint_meter SET NOT NULL;
		CLUSTER idx_zctas_thepoint_meter ON zctas;
		VACUUM ANALYZE zctas;
Join county level areas - 
```SQL
create table fema_aal.final_county_elem_aal_agg as
SELECT 
"county_aal_proj"."cntyname",
"county_elem_aal_agg"."countyfips",
"county_aal_proj"."population",
"county_elem_aal_agg"."ele_tiv",
"county_elem_aal_agg"."ele_guaal",
(ele_guaal/population) as ele_aalpca,
"county_aal_proj"."totalloss",
"county_aal_proj"."totlosspca",
"county_elem_aal_agg"."geom"
FROM "fema_aal"."county_elem_aal_agg"
join "fema_aal"."county_aal_proj"
on "county_elem_aal_agg"."countyfips"="county_aal_proj"."countyfips";
```


Now do a zonal statistic with points that fall within the HU8 geometry
```SQL
create table fema_aal.huc8fema_elemres_join as
SELECT  
hu8.huc
,sum(ele."TIV"::real) ele_tiv
,sum(ele."GU_AAL"::real) ele_guaal
,sum(hu8.totalloss) fema_totloss
,hu8.geom
from fema_aal.huc8_aal_proj as hu8
left join fema_aal.res2013_fixedriv_v2_location as ele
on ST_Intersects(hu8.geom, ele.geom)
group by hu8.huc, hu8.geom;
```

### General postgis functions

Creating a concave hull around points, where the percent is lower the more closer to the actual points they are, the true/false at the end means whether or not holes are allowed in the polygon...
```SQL
SELECT ST_ConcaveHull( ST_Collect(geom),0.50, true ) geom
FROM temp01test WHERE geom IS NOT NULL;
```






### NHD Processing
SQL Code for combining nhd lines with value added attributes
```SQL
CREATE TABLE temp.ca_nhdvaa_ln as 
SELECT ln.comid,ln.gnis_id,ln.gnis_name,
ln.reachcode,ln.ftype,vaa.streamorde,
vaa.fromnode,vaa.tonode,vaa.hydroseq,
vaa.levelpathi,vaa.terminalpa,vaa.pathlength,
vaa.totdasqkm, ln.geom_4269 as geom
FROM hymodel.nhdflow_ln  as ln
left join hymodel.nhdflow_vaa_tbl as vaa on  ln.comid = vaa.comid
```








