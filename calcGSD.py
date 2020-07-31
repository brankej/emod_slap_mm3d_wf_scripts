'''
not works with encoding and
#!/usr/bin/python
# -*- coding: utf-8 -*-
'''

###########################################################
# MODULES
###########################################################
import os
import argparse
import pandas as pd
from osgeo import gdal
from osgeo import ogr
import numpy as np
from PIL import Image
import statistics


###########################################################
# PARSER
###########################################################

##https://books.google.at/books?id=f3zUKZZ_WjMC&pg=PA30&dq=%22ground+sample+distance%22&redir_esc=y&hl=de#v=onepage&q=%22ground%20sample%20distance%22&f=false

parser = argparse.ArgumentParser(description='Calc GSD. Returns GSD in [mm]')
parser.add_argument('-f', "--focal",dest='f', type=float,required=True,help='Focal Length [mm]')
parser.add_argument('-fi', "--film",dest='fi', type=float,required=True,help='Filmwidth [mm]')
#parser.add_argument('-R', "--fhag",type=float, help='Flightheigth above Ground [m]')
parser.add_argument('-e', "--ele",dest='e',type=str,required=True,help='Raster for Calculating Flightheigth above Ground in Combination with CAMPOS [m]')
parser.add_argument('-c', "--campos",dest='c',type=str,required=True,help='Camera Positions XYZ in MicMac Format (no header / 3 lines to skip /N X Y Z /separated by tab) [m]')
parser.add_argument('-i', "--image",dest='i',required=True,type=str, help='Reference Image for Pixelsize Calculation')


args = parser.parse_args()


focal = args.f
f_width = args.fi
#fhag = args.R
dem = args.e
campos = args.c
img = args.i

##2019 0.006 100.5 2750


###########################################################
# VARIABLES
###########################################################
Image.MAX_IMAGE_PIXELS = 1000000000


###########################################################
# FUNCTIONS
###########################################################

### https://pcjericks.github.io/py-gdalogr-cookbook/raster_layers.html

def coord2pixelOffset(rasterfn,x,y):
    raster = gdal.Open(rasterfn)
    geotransform = raster.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    xOffset = int((x - originX)/pixelWidth)
    yOffset = int((y - originY)/pixelHeight)
    return xOffset,yOffset

def raster2array(rasterfn):
    raster = gdal.Open(rasterfn)
    band = raster.GetRasterBand(1)
    array = band.ReadAsArray()
    return array

def calcGSD(p, f, R):
    R = R*1000
    (p/f)*R
    k=(p/f)*R
    return(k)

def ImageWidth(img):
    im = Image.open(img)
    xsize = im.size[0]
    return(xsize)

###########################################################
###########################################################
# MAIN
###########################################################
###########################################################

# get Image x size
im_x = ImageWidth(img)


pix = f_width / im_x

# dem 2 array
array = raster2array(dem)

# get camposes
camposes = pd.read_csv(campos, sep="\t", skiprows=3, header=None)#

#empty list for camposes
GSD_list = []
Z_list = []
AGH_list = []

# get all info
for i in range(0, len(camposes)):

    tmp_name = camposes[0][i]
    tmp_x = camposes[1][i]
    tmp_y = camposes[2][i]
    tmp_z = camposes[3][i]

    #print(tmp_name)
    ## heigth from dem
    k = coord2pixelOffset(dem,tmp_x,tmp_y)

    wgs84_height = array[k[1], k[0]]

    agh = tmp_z - wgs84_height  ##above ground height
    #print("AGH:  ", agh, "[m]")


    tmp_GSD = calcGSD(pix,focal,agh)  #fagh

    #print("GSD:  ", tmp_GSD, "[mm]")

    GSD_list.append(tmp_GSD)
    Z_list.append(tmp_z)
    AGH_list.append(agh)




z = statistics.mean(Z_list)
k = statistics.mean(GSD_list)
a = statistics.mean(AGH_list)

print("mean AGH = ", round(a,3), " [m]")
print("mean Z = ", round(z,3), " [m]")
print("mean GSD = ", round(k,3), " [mm]    ", round(k/10,3), " [cm]    ", round(k/1000,3), " [m]")
print("Calculation done!")
