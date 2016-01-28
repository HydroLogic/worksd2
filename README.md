# Notes from lab machine 


### Command Line

#### GDAL
Create a ~30m grid from floodplain results
```Bash
*gdal_rasterize -a fldht_m -l hr_floodplain_complete_binned_final -a_nodata -9999 -tr 0.00034 0.00034 -tap -ot Float32 hr_floodplain_complete_fh.vrt harris30m_100yr_fp_1.tif
*gdal_rasterize -at -burn 1 -init 0 -ot Byte -tr 0.0002778 0.0002778 -co COMPRESS=LZW -a_nodata -9999 -l dfirm19011C_poly dfirm19011C_poly.shp dfirm19011C_poly.tif

```



## SQL & pgSQL

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