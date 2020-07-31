

###########################################################
# MODULES
###########################################################
import os
import argparse
import time

parser = argparse.ArgumentParser(description='CC WORKFLOW for PHG POINTCLOUDS from MICMAC')
parser.add_argument('-PHG', type=str, help='Photogrammetric Pointcloud Output from MICMAC')

#python .\cloudcompare_cmd.py -PHG PointCloud_2010.ply

args = parser.parse_args()

phg_raw = args.PHG

###########################################################
# VARIABLES
###########################################################

start_time = time.time()
#PATHS
CC_path = 'C:\PROGRA~1\CloudCompare\CloudCompare.exe'
als08 = "ALS_2008_dense_schmirn_AOI.las"
#phg_raw = "PointCloud_197x.ply"
offset_matrix = "offset_matrix_cc.txt"
reoffset_matrix = "re_offset_matrix_cc.txt"

#TO BE CREATED
counter = 0
logfile = "cc_log_"+phg_raw[:-4]+"_P"+str(counter)+".txt"
ending = ".las"
final_aoi = "Z 4 -499.75 7500.25 -499.75 9999.75 1499.75 9999.75 1499.75 7500.25"
als08_offsetted = als08[:-4]+"_offsetted"+ending
phg_sor = phg_raw[:-4]+"_sor"+ending
phg_edit_stable_aoi = phg_sor[:-4]+"_crop_stable_aoi"+ending
als08_stable_aoi = als08[:-4]+"_crop_stable_aoi"+ending
phg_final = phg_sor[:-4]+"_final"+ending

#
#stable_aoi = "Z 6 -324.00 9879.50 -352.50 9313.50 1451.50 9813.50 1258.00 10392.00 1062.625 10515.50 590.875 10515.00" ##watch the order!
fobj = open("stable_areas.txt")
kamm = next(fobj)
tal_east = next(fobj)
tal_west = next(fobj)
fobj.close()

kamm = kamm[:-3]
tal_east = tal_east[:-3]
tal_west = tal_west[:-3]

###########################################################
# FUNCTIONS
###########################################################

def get_filename(name,cloudname_raw):
    d = os.listdir("./")
    for i in d:
        if name in i and cloudname_raw[:-4] in i:
            #print(i)
            icp_matrix = i
    return icp_matrix


def rename_output(cloudname_raw):
    matrix = get_filename("REGISTRATION_MATRIX",cloudname_raw)
    raster = get_filename("RASTER_Z", cloudname_raw)

    ## clean possible previously created files
    outmatrix = cloudname_raw[:-4]+"_icp_matrix.txt"
    outraster = cloudname_raw[:-4]+"_rasterized_half_m.tif"

    if os.path.exists(outmatrix):
        os.remove(outmatrix)

    if os.path.exists(outraster):
        os.remove(outraster)

    os.rename(matrix, outmatrix)
    os.rename(raster, outraster)

###########################################################
###########################################################
# MAIN 
###########################################################
###########################################################


###########################################################
#PART I
#load PHG ply -> apply SOR -> SAVE as LAS
###########################################################
counter = counter + 1

if os.path.exists(phg_sor):
    ##save time in multi mode
    print("-----------------------------")
    print("--- Taking previously filtered PHG; done ---")
    print("-----------------------------")
    pass

else:
    logfile = "cc_log_"+phg_raw[:-4]+"_P"+str(counter)+".txt"

    cmd = "%s -SILENT -LOG_FILE %s -AUTO_SAVE OFF -O -GLOBAL_SHIFT 0 0 0 %s -SOR 6 1.0 -C_EXPORT_FMT LAS -SAVE_CLOUDS FILE %s" % (CC_path, logfile, phg_raw, phg_sor)
    os.system(cmd)
    print("-----------------------------")
    print("--- PHG PLY -> SOR -> LAS; done ---")
    print("-----------------------------")

###########################################################
#PART II
#load ALS -> apply REOFFSET -> SAVE as LAS
###########################################################
counter = counter + 1

if os.path.exists(als08_offsetted):
    ##save time in multi mode
    print("-----------------------------")
    print("--- Taking previously offsetted ALS; done ---")
    print("-----------------------------")
    pass
else:
    logfile = "cc_log_"+phg_raw[:-4]+"_P"+str(counter)+".txt"

    cmd = "%s -SILENT -LOG_FILE %s -AUTO_SAVE OFF -O -GLOBAL_SHIFT AUTO %s -APPLY_TRANS %s -C_EXPORT_FMT LAS -SAVE_CLOUDS FILE %s" % (CC_path, logfile, als08, reoffset_matrix, als08_offsetted)
    os.system(cmd)
    print("-----------------------------")
    print("--- ALS LAS -> OFFSETTED -> LAS; done ---")
    print("-----------------------------")


###########################################################
#PART III
#crop stable aoi for ICP
###########################################################

############
# ALS & PHG
############

############
## KAMM
############
cmd = '%s -SILENT -AUTO_SAVE OFF -O -GLOBAL_SHIFT 0 0 0 %s -O -GLOBAL_SHIFT 0 0 0 %s -CROP2D %s -C_EXPORT_FMT LAS -SAVE_CLOUDS FILE "%s %s"' % (CC_path, als08_offsetted, phg_sor, kamm, als08_stable_aoi[:-4]+"_kamm"+ending, phg_edit_stable_aoi[:-4]+"_kamm"+ending) 
os.system(cmd)

############
## TAL_EAST
############
cmd = '%s -SILENT -AUTO_SAVE OFF -O -GLOBAL_SHIFT 0 0 0 %s -O -GLOBAL_SHIFT 0 0 0 %s -CROP2D %s -C_EXPORT_FMT LAS -SAVE_CLOUDS FILE "%s %s"' % (CC_path, als08_offsetted, phg_sor, tal_east, als08_stable_aoi[:-4]+"_tal_east"+ending, phg_edit_stable_aoi[:-4]+"_tal_east"+ending) 
os.system(cmd)

############
##TAL_WEST
############
cmd = '%s -SILENT -AUTO_SAVE OFF -O -GLOBAL_SHIFT 0 0 0 %s -O -GLOBAL_SHIFT 0 0 0 %s -CROP2D %s -C_EXPORT_FMT LAS -SAVE_CLOUDS FILE "%s %s"' % (CC_path, als08_offsetted, phg_sor, tal_west, als08_stable_aoi[:-4]+"_tal_west"+ending, phg_edit_stable_aoi[:-4]+"_tal_west"+ending)
os.system(cmd)


print("-----------------------------")
print("--- Preprocessing CROP; done ---")
print("--- MERGING NOW! ---")
print("-----------------------------")


############
# MERGE ALS
############
cmd = '%s -SILENT -AUTO_SAVE OFF -O -GLOBAL_SHIFT 0 0 0 %s -O -GLOBAL_SHIFT 0 0 0 %s -O -GLOBAL_SHIFT 0 0 0 %s -MERGE_CLOUDS -C_EXPORT_FMT LAS -SAVE_CLOUDS FILE %s' % (CC_path, als08_stable_aoi[:-4]+"_kamm"+ending, als08_stable_aoi[:-4]+"_tal_east"+ending, als08_stable_aoi[:-4]+"_tal_west"+ending, als08_stable_aoi) 
os.system(cmd)

############
# MERGE PHG
############
cmd = '%s -SILENT -AUTO_SAVE OFF -O -GLOBAL_SHIFT 0 0 0 %s -O -GLOBAL_SHIFT 0 0 0 %s -O -GLOBAL_SHIFT 0 0 0 %s -MERGE_CLOUDS -C_EXPORT_FMT LAS -SAVE_CLOUDS FILE %s' % (CC_path, phg_edit_stable_aoi[:-4]+"_kamm"+ending, phg_edit_stable_aoi[:-4]+"_tal_east"+ending, phg_edit_stable_aoi[:-4]+"_tal_west"+ending, phg_edit_stable_aoi) 
os.system(cmd)


###############################
print("-----------------------------")
print("--- crop stable aoi for ICP; done ---")
print("-----------------------------")


###########################################################
#PART IV
#ICP on stable AOI
###########################################################
counter = counter + 1
logfile = "cc_log_"+phg_raw[:-4]+"_P"+str(counter)+".txt"

cmd = '%s -SILENT -LOG_FILE %s -AUTO_SAVE OFF -O -GLOBAL_SHIFT 0 0 0 %s -O -GLOBAL_SHIFT 0 0 0 %s -ICP -REFERENCE_IS_FIRST -ADJUST_SCALE -RANDOM_SAMPLING_LIMIT 5000000 -FARTHEST_REMOVAL -ROT XYZ' % (CC_path, logfile, als08_stable_aoi, phg_edit_stable_aoi)
os.system(cmd)
print("-----------------------------")
print("--- ICP on stable AOI; done ---")
print("-----------------------------")


#CALL ICP MATRIX FUNCTION
icp_matrix = get_filename("REGISTRATION_MATRIX",phg_raw)

###########################################################
#PART V
#apply ICP MATRIX -> CLIP AOI-> apply OFFSET MATRIX -> LAS
###########################################################
counter = counter + 1
logfile = "cc_log_"+phg_raw[:-4]+"_P"+str(counter)+".txt"

cmd = "%s -SILENT -LOG_FILE %s -AUTO_SAVE OFF -O -GLOBAL_SHIFT 0 0 0 %s -APPLY_TRANS %s -CROP2D %s -APPLY_TRANS %s -C_EXPORT_FMT LAS -SAVE_CLOUDS FILE %s" % (CC_path, logfile, phg_sor, icp_matrix, final_aoi, offset_matrix ,phg_final) 
os.system(cmd)
print("-----------------------------")
print("--- apply ICP MATRIX -> CLIP AOI-> apply OFFSET MATRIX -> LAS; done ---")
print("-----------------------------")


###########################################################
#PART VI
#RASTERIZE
###########################################################
counter = counter + 1
logfile = "cc_log_"+phg_raw[:-4]+"_P"+str(counter)+".txt"

cmd = "%s -SILENT -LOG_FILE %s -AUTO_SAVE OFF -O -GLOBAL_SHIFT AUTO %s -RASTERIZE -GRID_STEP 0.5 -VERT_DIR 2 -PROJ AVG -EMPTY_FILL INTERP -OUTPUT_RASTER_Z" % (CC_path, logfile, phg_final) 
##-EMPTY_FILL CUSTOM_H -CUSTOM_HEIGHT 0 || -EMPTY_FILL INTERP
os.system(cmd)
print("-----------------------------")
print("--- apply ICP MATRIX -> apply OFFSET MATRIX -> LAS; done ---")
print("-----------------------------")

# RENAME OUTPUT
rename_output(phg_raw)

print("-----------------------------")
print("--- CC Workflow done")
print("-----------------------------")
print(" ")
print("-----------------------------")
print('\x1b[7;32;44m' + '--- Calculation completed ---' + '\x1b[0m')
print('\x1b[7;32;44m'+"--- Calculation Duration took %s minutes ---" % ((time.time() - start_time)/60) + '\x1b[0m') 
print("-----------------------------")