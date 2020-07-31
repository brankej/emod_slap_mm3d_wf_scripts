###########################################################
#### MicMac Workflow Runner for Digital Aerial Imagery
####
#### ref: https://github.com/luc-girod/MicMacWorkflowsByLucGirod/blob/master/DroneNadir.sh
#### Branke, J. 
###########################################################


###########################################################
#### MODULES
###########################################################
import os
import argparse
import time
import shutil


###########################################################
#### PARSER
###########################################################

parser = argparse.ArgumentParser(description='MicMac Workflow Runner for Digital Aerial Imagery')

## STAGES
parser.add_argument('-tp', "-TIEPOINTS",dest='tp', type=int, default=0, help='DO SETUP ?:  Camera Positions ## Tie Points ## Tie Point Improvement, default = 0 / else 1')
parser.add_argument('-o', "-ORI",dest='ori', type=int, default=0, help='DO SETUP ?:  INTERIOR ORIENTATION ## EXTERIOR ORIENTATION, default = 0 / else 1')
parser.add_argument('-o_sub', "-O_SUB",dest='o_sub', type=int, default=0, help='DO SETUP ?: Initialize TAPAS with subset of  the first "n" images FLAG -o_sub_n; ,default = 0 / else 1')
parser.add_argument('-o_giv', "-O_GIV",dest='o_giv', type=int, default=0, help='DO SETUP ?: Initialize TAPAS with subset of given images FLAG -o_img; ,default = 0 / else 1')
parser.add_argument('-d_m', "-DENSE_M",dest='d_m', type=int, default=0, help='DO SETUP ?:  Orthophoto ## Dense Matching, default = 0 / else 1')
parser.add_argument('-out', "-OUTPUT",dest='out', type=int, default=0, help='DO SETUP ?:  OUTPUT, default = 0 / else 1')
parser.add_argument('-cl', "-CLEAN",dest='cl', type=str, default="NONE",choices=["ALL", "NONE", "TP", "ORI", "DM", "OUTPUT"], help='DO Cleanup ?: Remove Folders from different STAGES {"ALL", "NONE", "TP", "ORI", "DM" , "OUTPUT"} ,default = NONE ')

## VALUES
parser.add_argument('-e', '-EXTENSION', dest='extension',type=str,  default="tif", help='image file type (JPG, jpg, TIF, tif ,png..., default=tif).')
parser.add_argument('-x', "-X_OFF",dest='x_off', type=int, default=0, help='X (easting) offset for ply file overflow issue (default=0).')
parser.add_argument('-y', "-Y_OFF",dest='y_off', type=int, default=0, help='Y (northing) offset for ply file overflow issue (default=0).')
parser.add_argument('-z', "-ZOOM",dest='zoom', type=int, default=2, help='Last step in pyramidal dense correlation (default=2, can be in [8,4,2,1])')
parser.add_argument('-r', "-RESOL",dest='resol', type=float, default=0.5, help='Ground resolution (in meters)')
parser.add_argument('-c', "-CAM",dest='cam', type=str, default="RadialStd", help='Basic distortion models easily accessible in MicMac (RadialBasic, RadialStd, RadialExtended, Fraser, FraserBasic), default = RadialStd.')
parser.add_argument('-p', "-POSITIONS",dest='pos', type=str, help='Filename of Camera Positions. txt / csv File with MicMac Readable Header')
parser.add_argument('-t_res', "-TAPIOCA_RES",dest='t_res', type=int, default=5000, help='Find Tie points using [number] px windows. 1/2 resolution image = best value for RGB bayer sensor')
parser.add_argument('-n', "-NBVI",dest='nbvi', type=int, default=3, help='Number Visible Images for DenseMatching ,default = 3; min=2')
parser.add_argument('-s_n', "-S_N",dest='s_nb', type=int, default=2000, help='Number Schnaps minimum remaining Tie Points. mm3d default = 1000 ,default = 2000')
parser.add_argument('-d', "-DEFCOR",dest='defcor', type=float, default=0.1, help='DenseMatching Correlation Threshold. zero is none. mm3d default = 0.2 ,default = 0.1; min=0')
parser.add_argument('-reg', "-REGUL",dest='regul', type=float, default=0.02, help='Regularization Factor (Smoothing). If your data does have some sharp transitions (side of buildings for instance), they will be smoothed. 0.9 =  real smooth / 0.9 > more noisy ,default = 0.02; min=0') # http://forum-micmac.forumprod.com/can-t-display-depth-map-t1601.html#p6371  ## http://forum-micmac.forumprod.com/c3dc-defcor-and-zreg-parameters-t1280.html#p5143
parser.add_argument('-szw', "-SZW",dest='szw', type=int, default=1, help='Correlation Window Size (1 means 3x3) ,default = 1')
parser.add_argument('-o_sub_n', "-O_SUB_N",dest='o_sub_n', type=int, default=5, help='Initialize TAPAS with subset of  the first "n" images; default 5')
parser.add_argument('-o_img', "-O_IMG", dest='o_img', type=str, nargs='+', help='Initialize TAPAS with subset of given images exp. "-img IMG05342.jpg IMG2314.jpg"') 



args = parser.parse_args()

## STAGES
tp = args.tp
ori = args.ori
o_sub = args.o_sub
o_giv = args.o_giv
dense = args.d_m
output = args.out
clean = args.cl

## VALUES
extension = args.extension
x_off = args.x_off
y_off = args.y_off
zoom = args.zoom
resol = args.resol
cameramodel = args.cam
CamPos = args.pos
tapioca_res = args.t_res
s_nb = args.s_nb
nbvi = args.nbvi
defcor = args.defcor
regul = args.regul
szw = args.szw
o_sub_n = args.o_sub_n
o_img = args.o_img





###########################################################
#### VARIABLES
###########################################################
start_time = time.time()


ending = ".*." + extension

###########################################################
#### FUNCTIONS
###########################################################

def remove_file_or_dir(path: str) -> None:
    """ Remove a file or directory 
    https://stackoverflow.com/questions/6996603/how-to-delete-a-file-or-folder
    """
    try:
        shutil.rmtree(path)
    except NotADirectoryError:
        os.remove(path)

######################################################################################################################
### MAIN
######################################################################################################################




##############################################################################################
### SETUP 
### Camera Positions ## Tie Points ## Tie Point Improvement
##############################################################################################

if tp == 1:
    print('\x1b[7;32;44m' +'--- STARTING: ---'+ '\x1b[0m')
    print('\x1b[7;32;44m' +'--- Camera Positions ## Tie Points ## Tie Point Improvement ---'+ '\x1b[0m')
    print('\x1b[7;32;44m' + '-----------------------------' + '\x1b[0m')

    ##1. Read in image centers
    cmd="mm3d OriConvert OriTxtInFile %s Nav-Brut-RTL NameCple=FileImagesNeighbour.xml MTD1=1" % (CamPos)
    print("--> %s"%(cmd))
    os.system(cmd)


    ##2. Tapioca (tie points)  ## best: Find Tie points using 1/2 resolution image (best value for RGB bayer sensor)
    cmd="mm3d Tapioca File FileImagesNeighbour.xml %i NoMin=1 Detect=digeo > tapioca.txt" % (tapioca_res) 
    print("--> %s"%(cmd))
    os.system(cmd)


    ##3. Schnaps (improved tie points) #filter TiePoints (better distribution, avoid clogging)
    cmd="mm3d Schnaps %s HomolOut=_Schnaps MoveBadImgs=1 NbWin=%i > schnaps.txt" % (ending, s_nb)
    print("--> %s"%(cmd))
    os.system(cmd)

    print('\x1b[7;32;44m' +'--- ENDED SUCCESSFULLY: ---'+ '\x1b[0m')
    print('\x1b[7;32;44m' +'--- Camera Positions ## Tie Points ## Tie Point Improvement ---'+ '\x1b[0m')
    print('\x1b[7;32;44m' + '-----------------------------' + '\x1b[0m')

else:
    print('\x1b[7;32;44m' +'--- SKIPPED: ---'+ '\x1b[0m')
    print('\x1b[7;32;44m' +'--- Camera Positions ## Tie Points ## Tie Point Improvement ---'+ '\x1b[0m')
    print('\x1b[7;32;44m' + '-----------------------------' + '\x1b[0m')



##############################################################################################
### SETUP 
### INTERIOR ORIENTATION ## EXTERIOR ORIENTATION
##############################################################################################


if ori == 1:

    print('\x1b[7;32;44m' +'--- STARTING: ---'+ '\x1b[0m')
    print('\x1b[7;32;44m' +'--- INTERIOR ORIENTATION ## EXTERIOR ORIENTATION ---'+ '\x1b[0m')
    print('\x1b[7;32;44m' + '-----------------------------' + '\x1b[0m')


    if o_sub == 1:

        img_list = []
        for i in os.listdir("."):
            if i.endswith(".%s" % (extension)):
                img_list.append(i)

        imgs = "|".join(img_list[0:o_sub_n])

        ##6. Tapas I (camera calibration) on Subset
        cmd='mm3d Tapas %s "%s" Out=Sample4Calib SH=_Schnaps LibFoc=0 > tapas_I.txt' %(cameramodel, imgs)
        print("--> %s"%(cmd))
        os.system(cmd)

        ##6. Tapas II (camera calibration) on All
        cmd="mm3d Tapas %s %s InCal=Sample4Calib Out=Relative SH=_Schnaps LibFoc=0 > tapas_II.txt" %(cameramodel, ending)
        print("--> %s"%(cmd))
        os.system(cmd)


    elif o_giv == 1:
        
        imgs = "|".join(o_img)

        ##6. Tapas I (camera calibration) on Subset
        cmd='mm3d Tapas %s "%s" Out=Sample4Calib SH=_Schnaps LibFoc=0 > tapas_I.txt' %(cameramodel, imgs)
        print("--> %s"%(cmd))
        os.system(cmd)

        ##6. Tapas II (camera calibration) on All
        cmd="mm3d Tapas %s %s InCal=Sample4Calib Out=Relative SH=_Schnaps LibFoc=0 > tapas_II.txt" %(cameramodel, ending)
        print("--> %s"%(cmd))
        os.system(cmd)

    else:
        ## normal on all
        ##6. Tapas II (camera calibration)
        cmd="mm3d Tapas %s %s Out=Relative SH=_Schnaps LibFoc=0 > tapas.txt" %(cameramodel, ending)
        print("--> %s"%(cmd))
        os.system(cmd)

    ##AperiCloud (generate sparse cloud) 
    cmd="mm3d AperiCloud %s Relative" % (ending)
    print("--> %s"%(cmd))
    os.system(cmd)

    ##8. Bascule (georeferencing) 
    cmd="mm3d CenterBascule %s Relative Nav-Brut-RTL All-Ground > bascule.txt" % (ending) 
    print("--> %s"%(cmd))																
    os.system(cmd)

    ##CAMPARI
    cmd="mm3d Campari %s All-Ground All-Campari EmGPS=[Nav-Brut-RTL,0.5] SH=_Schnaps > campari.txt" % (ending) 
    print("--> %s"%(cmd))																	
    os.system(cmd)

    print('\x1b[7;32;44m' +'--- ENDED SUCCESSFULLY: ---'+ '\x1b[0m')
    print('\x1b[7;32;44m' +'--- INTERIOR ORIENTATION ## EXTERIOR ORIENTATION ---'+ '\x1b[0m')
    print('\x1b[7;32;44m' + '-----------------------------' + '\x1b[0m')

else:
    print('\x1b[7;32;44m' +'--- SKIPPED: ---'+ '\x1b[0m')
    print('\x1b[7;32;44m' +'--- INTERIOR ORIENTATION ## EXTERIOR ORIENTATION ---'+ '\x1b[0m')
    print('\x1b[7;32;44m' + '-----------------------------' + '\x1b[0m')


##############################################################################################
### SETUP 
### Orthophoto ## Dense Matching
##############################################################################################

if dense == 1:

    print('\x1b[7;32;44m' +'--- STARTING: ---'+ '\x1b[0m')
    print('\x1b[7;32;44m' +'--- Orthophoto ## Dense Matching ---'+ '\x1b[0m')
    print('\x1b[7;32;44m' + '-----------------------------' + '\x1b[0m')

    cmd="mm3d Malt Ortho %s All-Campari NbVI=%i ZoomF=%i ResolTerrain=%f DefCor=%f CostTrans=2 EZA=1 HrOr=1 Regul=%f SzW=%i > malt.txt" % (ending, nbvi, zoom, resol, defcor, regul, szw)
    print("--> %s"%(cmd))
    os.system(cmd)


    cmd="mm3d Tawny Ortho-MEC-Malt Out=Orthophotomosaic.tif > tawny.txt" 
    print("--> %s"%(cmd))
    os.system(cmd)


    if zoom == 1 and resol == 0.5:
        etappe = "9"
    if zoom == 2 and resol == 0.5:
        etappe = "8"
    if zoom == 4 and resol == 0.5:
        etappe = "7"
    if zoom == 8 and resol == 0.5:
        etappe = "6"


    cmd="mm3d Nuage2Ply MEC-Malt/NuageImProf_STD-MALT_Etape_%s.xml Attr=Ortho-MEC-Malt/Orthophotomosaic.tif Out=PointCloud.ply Normale=7 Mesh=0 Offs=[%s,%s,0] > nuage.txt" % (etappe, x_off, y_off)
    print("--> %s"%(cmd))
    os.system(cmd)


    print('\x1b[7;32;44m' +'--- ENDED SUCCESSFULLY: ---'+ '\x1b[0m')
    print('\x1b[7;32;44m' +'--- Orthophoto ## Dense Matching ---'+ '\x1b[0m')
    print('\x1b[7;32;44m' + '-----------------------------' + '\x1b[0m')

else:
    print('\x1b[7;32;44m' +'--- SKIPPED: ---'+ '\x1b[0m')
    print('\x1b[7;32;44m' +'--- Orthophoto ## Dense Matching ---'+ '\x1b[0m')
    print('\x1b[7;32;44m' + '-----------------------------' + '\x1b[0m')


##############################################################################################
### END
### OUTPUT
##############################################################################################


if output == 1:

    if os.path.exists("OUTPUT"):
        pass 
    else:
        os.mkdir("OUTPUT")


    os.chdir("MEC-Malt")
    mec_malt_list = os.listdir(".")

    finalDEMs = []
    finalCORRs = []

    for i in mec_malt_list:
        if i.startswith("Z_Num") and i.endswith(".tif"):
            finalDEMs.append(i)
        if i.startswith("Correl_STD-MALT_Num") and i.endswith(".tif"):
            finalCORRs.append(i)
        else:
            pass
        
    finalDEM = finalDEMs[-1]
    finalCORR = finalCORRs[-1]

    finalDEMstr =finalDEM[:-4]+".tfw"
    finalCORRstr = finalCORR[:-4]+".tfw"

    #make tfw file for correlation rast
    shutil.copy(finalDEMstr, finalCORRstr)

    results = [finalDEM, finalDEMstr , finalCORR, finalCORRstr]
    names = ["DEM.tif", "DEM.tfw", "CORR.tif", "CORR.tfw"]

    #COPY CORR AND DEM TO OUTPUT
    for i in range(len(results)):
        shutil.copy("%s" % (results[i]), "../OUTPUT/%s" % (names[i]))

    os.chdir("..")

    # COPY ORTHO
    shutil.copy("Ortho-MEC-Malt/Orthophotomosaic.tif", "OUTPUT/OrthoImg.tif")
    shutil.copy("Ortho-MEC-Malt/Orthophotomosaic.tfw", "OUTPUT/OrthoImg.tfw")

    # COPY PC
    shutil.copy("PointCloud.ply", "OUTPUT/PC.ply")


##############################################################################################
### SETUP 
### CLEANING
##############################################################################################

###
if clean == "ALL":
    files = ["Ori-Relative", "Ori-Sample4Calib", "Ori-All-Ground", "Ori-All-Campari","AperiCloud_Relative.ply", "Homol", "Homol_Schnaps", "Ori-InterneScan", "Ori-Nav-Brut-RTL", "FileImagesNeighbour.xml", "SauvApero.xml", "Schnaps_poubelle.txt", "Poubelle","schnaps.txt", "tapioca.txt", "WarnApero.txt", "MEC-Malt", "Ortho-MEC-Malt", "Pyram", "PointCloud.ply", "tapas.txt", "tapas_I.txt", "tapas_II.txt", "bascule.txt", "campari.txt" , "nuage.txt", "tawny.txt", "malt.txt", "Pastis", "Tmp-MM-Dir", "OUTPUT"]

    print('\x1b[7;32;44m' +'--- CLEANUP %s---' % (clean) + '\x1b[0m')
    print('\x1b[7;32;44m' + '-----------------------------' + '\x1b[0m')
    for i in files:
        if os.path.exists(i):
            remove_file_or_dir(i)
    print('\x1b[7;32;44m' +'--- TIDIED UP ---'+ '\x1b[0m')
    print('\x1b[7;32;44m' + '-----------------------------' + '\x1b[0m')

###
if clean == "TP":
    files = ["Homol", "Homol_Schnaps", "Ori-InterneScan", "Ori-Nav-Brut-RTL", "FileImagesNeighbour.xml", "Schnaps_poubelle.txt", "schnaps.txt", "tapioca.txt"]

    print('\x1b[7;32;44m' +'--- CLEANUP %s---' % (clean) + '\x1b[0m')
    print('\x1b[7;32;44m' + '-----------------------------' + '\x1b[0m')
    for i in files:
        if os.path.exists(i):
            remove_file_or_dir(i)
    print('\x1b[7;32;44m' +'--- TIDIED UP ---'+ '\x1b[0m')
    print('\x1b[7;32;44m' + '-----------------------------' + '\x1b[0m')

###
if clean == "ORI":
    files = ["Ori-Relative", "Ori-Sample4Calib", "Ori-All-Ground", "Ori-All-Campari","AperiCloud_Relative.ply", "tapas.txt", "tapas_I.txt", "tapas_II.txt", "bascule.txt", "campari.txt", "Poubelle"]

    print('\x1b[7;32;44m' +'--- CLEANUP %s---' % (clean) + '\x1b[0m')
    print('\x1b[7;32;44m' + '-----------------------------' + '\x1b[0m')
    for i in files:
        if os.path.exists(i):
            remove_file_or_dir(i)
    print('\x1b[7;32;44m' +'--- TIDIED UP ---'+ '\x1b[0m')
    print('\x1b[7;32;44m' + '-----------------------------' + '\x1b[0m')

###
if clean == "DM":
    files = ["MEC-Malt", "Ortho-MEC-Malt", "Pyram", "PointCloud.ply", "nuage.txt", "tawny.txt", "malt.txt"]

    print('\x1b[7;32;44m' +'--- CLEANUP %s---' % (clean) + '\x1b[0m')
    print('\x1b[7;32;44m' + '-----------------------------' + '\x1b[0m')
    for i in files:
        if os.path.exists(i):
            remove_file_or_dir(i)
    print('\x1b[7;32;44m' +'--- TIDIED UP ---'+ '\x1b[0m')
    print('\x1b[7;32;44m' + '-----------------------------' + '\x1b[0m')

###
if clean == "OUTPUT":
    files = ["OUTPUT"]

    print('\x1b[7;32;44m' +'--- CLEANUP %s---' % (clean) + '\x1b[0m')
    print('\x1b[7;32;44m' + '-----------------------------' + '\x1b[0m')
    for i in files:
        if os.path.exists(i):
            remove_file_or_dir(i)
    print('\x1b[7;32;44m' +'--- TIDIED UP ---'+ '\x1b[0m')
    print('\x1b[7;32;44m' + '-----------------------------' + '\x1b[0m')


if clean == "NONE":
    print('\x1b[7;32;44m' +'--- SKIPPED: ---'+ '\x1b[0m')
    print('\x1b[7;32;44m' +'--- CLEANUP == %s---' % (clean) + '\x1b[0m')
    print('\x1b[7;32;44m' + '-----------------------------' + '\x1b[0m')




##############################################################################################
print('\x1b[7;32;44m' + '--- Calculation completed ---' + '\x1b[0m')
print('\x1b[7;32;44m'+"--- Calculation took %s minutes ---" % ((time.time() - start_time)/60) + '\x1b[0m')
print('\x1b[7;32;44m' + '-----------------------------' + '\x1b[0m')