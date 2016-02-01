# Bishes ain't shit

		gdal_rasterize -3d -l ras100yr_dpth -a_nodata -9999 -tr 0.00115 0.00115 -tap -ot Float32 -co tiled=yes -co bigtiff=yes -co compress=lzw ras100yr_dpth.vrt ras100yr_dpth.tif

		gdaladdo -ro --config COMPRESS_OVERVIEW DEFLATE ras100yr_dpth.tif 2 4 8 16