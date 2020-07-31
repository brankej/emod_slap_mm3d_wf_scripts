
###########################################################
# MODULES
###########################################################
import os
import argparse
import time
import numpy as np
import osgeo.gdal as gdal
import osgeo.ogr as ogr
import osgeo.osr as osr
import cv2 as cv

###########################################################
# VARIABLES
###########################################################

pc_197x = "../PointCloud_197x_sor_final.las"
pc_2007 = "../PointCloud_2007_sor_final.las"
pc_2010 = "../PointCloud_2010_sor_final.las"
pc_2019 = "../PointCloud_2019_sor_final.las"

ref_rast = "../ALS_2008_filled_half_m.tif"

size = 1
kernel_ = 5
###########################################################
# FUNCTIONS
###########################################################

def raster2array(rasterfn):
    """Input Raster to Array """
    raster = gdal.Open(rasterfn)
    band = raster.GetRasterBand(1)
    array = band.ReadAsArray()
    return array

###########################################################
###########################################################
# MAIN 
###########################################################
###########################################################



pc_list = [pc_2007, pc_2010]

for pc in pc_list:

    ras_out = pc[:-13]+"half_m_saga.tif"

    #load las to saga  
    cmd = "saga_cmd io_shapes_las 1 -FILES=%s -POINTS=%s" % (pc, "points")
    os.system(cmd)

    cmd = "saga_cmd io_gdal 0 -FILES=%s -GRIDS=%s" % (ref_rast, "grid")
    os.system(cmd)

    cmd = "saga_cmd grid_gridding 0 -INPUT=%s -FIELD=Z -OUTPUT=2 -MULTIPLE=4 -GRID_TYPE=9 -TARGET_DEFINITION=1 -TARGET_TEMPLATE=%s -TARGET_USER_SIZE=%s -TARGET_USER_FITS=0 -GRID=%s" % ("points.sg-pts","grid.sgrd" ,size,ras_out)
    os.system(cmd)

    cmd = "saga_cmd io_gdal 0 -FILES=%s -GRIDS=%s" % (ras_out, "fin_grid")
    os.system(cmd)

    '''
    cmd = "saga_cmd grid_tools 25 -GRID=%s -CLOSED=%s" % ("fin_grid.sgrd", ras_out[:-4]+"_closed_gaps.tif")
    os.system(cmd)
    '''

    cmd = "saga_cmd grid_tools 7 -INPUT=%s -RESULT=%s -THRESHOLD=0.1" % ("fin_grid.sgrd", ras_out[:-4]+"_closed_gaps.tif")
    os.system(cmd)

    ##interpolation mask
    ##make mask
    cmd = "saga_cmd grid_tools 15 -INPUT=%s -RESULT=%s -METHOD=1 -MIN=0.000000 -MAX=5000.000000 -RNEW=0.000000 -ROPERATOR=0 -NODATAOPT=1 -NODATA=1.000000 -OTHEROPT=0 -RESULT_TYPE=9 -RESULT_NODATA_CHOICE=0" % ("fin_grid.sgrd", ras_out[:-4]+"_interpol_mask.tif")
    os.system(cmd)

    #######
    ##morphological shrink and expand
    #######

    ###EINLESEN
    #read in craters
    input_mask = ras_out[:-4]+"_interpol_mask.tif"
    mask_array = raster2array(input_mask)

    ###########get necessary raster information###########
    myrast = gdal.Open(input_mask)
    NROWS = myrast.RasterXSize
    NCOLS = myrast.RasterYSize
    geotransform = myrast.GetGeoTransform()
    wkt_projection = myrast.GetProjection()
    XULCorner = geotransform[0]
    YULCorner = geotransform[3]
    Cellsize = geotransform[1]

    myband = myrast.GetRasterBand(1)
    Nodata = myband.GetNoDataValue()

    print("--- DATA LOADED ---")

    ########### morphological transformation   ###########  
    # #https://docs.opencv.org/trunk/d9/d61/tutorial_py_morphological_ops.html


    kernel = np.ones((kernel_,kernel_),np.uint8)
    #opening
    opening = cv.morphologyEx(mask_array, cv.MORPH_OPEN, kernel)

    driver = gdal.GetDriverByName('GTiff')
    dataset = driver.Create("%s_opening.tif" % (ras_out[:-4]), NROWS, NCOLS, 1, gdal.GDT_Float32 )
    dataset.SetGeoTransform((XULCorner,Cellsize,0,YULCorner,0,-Cellsize))
    dataset.SetProjection(wkt_projection)

    band_1 = dataset.GetRasterBand(1)
    band_1.WriteArray(opening)

    #flushcache
    dataset.FlushCache()

    print("--- Opening done ---")
    ########################################################################

    #############
    #POLYGONIZE
    #############
    #  get raster datasource
    src_ds = gdal.Open("%s_opening.tif" % (ras_out[:-4]))
    srcband = src_ds.GetRasterBand(1)
    #  create output datasource

    srs=osr.SpatialReference()
    srs.ImportFromWkt(src_ds.GetProjection())

    dst_layername = "%s_mask_poly" % (ras_out[:-4])
    drv = ogr.GetDriverByName("ESRI Shapefile")
    dst_ds = drv.CreateDataSource( dst_layername + ".shp" )
    dst_layer = dst_ds.CreateLayer(dst_layername, srs = srs )
    gdal.Polygonize( srcband, srcband , dst_layer, -1, [], callback=None )

    print("--- Polygonize done ---")
    ########################################################################
    print("one done")


print("all done ...")


