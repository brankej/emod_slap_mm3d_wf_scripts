# emod_slap_mm3d_wf_scripts


For [MICMAC v1.1](https://github.com/micmacIGN/micmac/tree/MMASTER_v1.1)


## Digital Aerial

usage: _micmac_workflow_digital_aerial.py [-h] [-tp TP] [-o ORI] [-o_sub O_SUB] [-o_giv O_GIV] [-d_m D_M] [-out OUT]
                                         [-cl {ALL,NONE,TP,ORI,DM,OUTPUT}] [-e EXTENSION] [-x X_OFF] [-y Y_OFF]
                                         [-z ZOOM] [-r RESOL] [-c CAM] [-p POS] [-t_res T_RES] [-n NBVI] [-s_n S_NB]
                                         [-d DEFCOR] [-reg REGUL] [-szw SZW] [-o_sub_n O_SUB_N]
                                         [-o_img O_IMG [O_IMG ...]]_


**MicMac Workflow Runner for Digital Aerial Imagery**

optional arguments:
-  -h, --help            show this help message and exit

_ARGS for PROGRAM STAGES_
-  -tp TP, -TIEPOINTS TP
                        DO SETUP ?: Camera Positions ## Tie Points ## Tie Point Improvement, default = 0 / else 1
-  -o ORI, -ORI ORI      DO SETUP ?: INTERIOR ORIENTATION ## EXTERIOR ORIENTATION, default = 0 / else 1
-  -o_sub O_SUB, -O_SUB O_SUB
                        DO SETUP ?: Initialize TAPAS with subset of the first "n" images FLAG -o_sub_n; ,default = 0 /
                        else 1
-  -o_giv O_GIV, -O_GIV O_GIV
                        DO SETUP ?: Initialize TAPAS with subset of given images FLAG -o_img; ,default = 0 / else 1
-  -d_m D_M, -DENSE_M D_M
                        DO SETUP ?: Orthophoto ## Dense Matching, default = 0 / else 1
-  -out OUT, -OUTPUT OUT
                        DO SETUP ?: OUTPUT, default = 0 / else 1
-  -cl {ALL,NONE,TP,ORI,DM,OUTPUT}, -CLEAN {ALL,NONE,TP,ORI,DM,OUTPUT}
                        DO Cleanup ?: Remove Folders from different STAGES {"ALL", "NONE", "TP", "ORI", "DM" ,
                        "OUTPUT"} ,default = NONE

_ARGS for VARIABLES & FILES_
-  -e EXTENSION, -EXTENSION EXTENSION
                        image file type (JPG, jpg, TIF, tif ,png..., default=tif).
-  -x X_OFF, -X_OFF X_OFF
                        X (easting) offset for ply file overflow issue (default=0).
-  -y Y_OFF, -Y_OFF Y_OFF
                        Y (northing) offset for ply file overflow issue (default=0).
-  -z ZOOM, -ZOOM ZOOM   Last step in pyramidal dense correlation (default=2, can be in [8,4,2,1])
-  -r RESOL, -RESOL RESOL
                        Ground resolution (in meters)
-  -c CAM, -CAM CAM      Basic distortion models easily accessible in MicMac (RadialBasic, RadialStd, RadialExtended,
                        Fraser, FraserBasic), default = RadialStd.
-  -p POS, -POSITIONS POS
                        Filename of Camera Positions. txt / csv File with MicMac Readable Header
-  -t_res T_RES, -TAPIOCA_RES T_RES
                        Find Tie points using [number] px windows. 1/2 resolution image = best value for RGB bayer
                        sensor
-  -n NBVI, -NBVI NBVI   Number Visible Images for DenseMatching ,default = 3; min=2
-  -s_n S_NB, -S_N S_NB  Number Schnaps minimum remaining Tie Points. mm3d default = 1000 ,default = 2000
-  -d DEFCOR, -DEFCOR DEFCOR
                        DenseMatching Correlation Threshold. zero is none. mm3d default = 0.2 ,default = 0.1; min=0
-  -reg REGUL, -REGUL REGUL
                        Regularization Factor (Smoothing). If your data does have some sharp transitions (side of
                        buildings for instance), they will be smoothed. 0.9 = real smooth / 0.9 > more noisy ,default
                        = 0.02; min=0
-  -szw SZW, -SZW SZW    Correlation Window Size (1 means 3x3) ,default = 1
-  -o_sub_n O_SUB_N, -O_SUB_N O_SUB_N
                        Initialize TAPAS with subset of the first "n" images; default 5
-  -o_img O_IMG [O_IMG ...], -O_IMG O_IMG [O_IMG ...]
                        Initialize TAPAS with subset of given images exp. "-img IMG05342.jpg IMG2314.jpg"


## Scanned Aerial

usage: _micmac_workflow_scanned_aerial.py [-h] [-fid FID] [-a_fid A_FID] [-tp TP] [-tp_m TP_M] [-o ORI] [-o_sub O_SUB]
                                         [-o_giv O_GIV] [-d_m D_M] [-out OUT] [-cl {ALL,NONE,TP,ORI,DM,OUTPUT}]
                                         [-e EXTENSION] [-x X_OFF] [-y Y_OFF] [-z ZOOM] [-r RESOL] [-c CAM]
                                         [-i_fid I_FID] [-p POS] [-t_res T_RES] [-n NBVI] [-s_n S_NB] [-d DEFCOR]
                                         [-reg REGUL] [-szw SZW] [-o_sub_n O_SUB_N] [-o_img O_IMG [O_IMG ...]]_

**MicMac Workflow Runner for Scanned Aerial Imagery**

optional arguments:
-  -h, --help            show this help message and exit

_ARGS for PROGRAM STAGES_
-  -fid FID, -FIDUCIALS FID
                        DO SETUP ?: Fiducials ## Resampling to Scan Resolution, default = 0 / else 1
-  -a_fid A_FID, -AUTO_FIDUCIALS A_FID
                        DO SETUP ?: AUTO Fiducials with KUGELHUPF ## Resampling to Scan Resolution, default = 0 / else
                        1
-  -tp TP, -TIEPOINTS TP
                        DO SETUP ?: Camera Positions ## Tie Points ## Tie Point Improvement, default = 0 / else 1
-  -tp_m TP_M, -TIEPOINT_MASK TP_M
                        DO SETUP ?: Tie Point Masking, default = 0 / else 1
-  -o ORI, -ORI ORI      DO SETUP ?: INTERIOR ORIENTATION ## EXTERIOR ORIENTATION, default = 0 / else 1
-  -o_sub O_SUB, -O_SUB O_SUB
                        DO SETUP ?: Initialize TAPAS with subset of the first "n" images FLAG -o_sub_n; ,default = 0 /
                        else 1
-  -o_giv O_GIV, -O_GIV O_GIV
                        DO SETUP ?: Initialize TAPAS with subset of given images FLAG -o_img; ,default = 0 / else 1
-  -d_m D_M, -DENSE_M D_M
                        DO SETUP ?: Orthophoto ## Dense Matching, default = 0 / else 1
-  -out OUT, -OUTPUT OUT
                        DO SETUP ?: OUTPUT, default = 0 / else 1
-  -cl {ALL,NONE,TP,ORI,DM,OUTPUT}, -CLEAN {ALL,NONE,TP,ORI,DM,OUTPUT}
                        DO Cleanup ?: Remove Folders from different STAGES {"ALL", "NONE", "TP", "ORI", "DM" ,
                        "OUTPUT"} ,default = NONE

_ARGS for VARIABLES & FILES_
-  -e EXTENSION, -EXTENSION EXTENSION
                        image file type (JPG, jpg, TIF, tif ,png..., default=tif).
-  -x X_OFF, -X_OFF X_OFF
                        X (easting) offset for ply file overflow issue (default=0).
-  -y Y_OFF, -Y_OFF Y_OFF
                        Y (northing) offset for ply file overflow issue (default=0).
-  -z ZOOM, -ZOOM ZOOM   Last step in pyramidal dense correlation (default=2, can be in [8,4,2,1])
-  -r RESOL, -RESOL RESOL
                        Ground resolution (in meters)
-  -c CAM, -CAM CAM      Basic distortion models easily accessible in MicMac (RadialBasic, RadialStd, RadialExtended,
                        Fraser, FraserBasic), default = RadialStd.
-  -i_fid I_FID, -INIT_FID_IMG I_FID
                        Initial Image to Use for Fiducial Measurements, default = 1st. Image.
-  -p POS, -POSITIONS POS
                        Filename of Camera Positions. txt / csv File with MicMac Readable Header
-  -t_res T_RES, -TAPIOCA_RES T_RES
                        Find Tie points using [number] px windows. 1/2 resolution image = best value for RGB bayer
                        sensor
-  -n NBVI, -NBVI NBVI   Number Visible Images for DenseMatching ,default = 3; min=2
-  -s_n S_NB, -S_N S_NB  Number Schnaps minimum remaining Tie Points. mm3d default = 1000 ,default = 2000
-  -d DEFCOR, -DEFCOR DEFCOR
                        DenseMatching Correlation Threshold. zero is none. mm3d default = 0.2 ,default = 0.1; min=0
-  -reg REGUL, -REGUL REGUL
                        Regularization Factor (Smoothing). If your data does have some sharp transitions (side of
                        buildings for instance), they will be smoothed. 0.9 = real smooth / 0.9 > more noisy ,default
                        = 0.02; min=0
-  -szw SZW, -SZW SZW    Correlation Window Size (1 means 3x3) ,default = 1
-  -o_sub_n O_SUB_N, -O_SUB_N O_SUB_N
                        Initialize TAPAS with subset of the first "n" images; default 5
-  -o_img O_IMG [O_IMG ...], -O_IMG O_IMG [O_IMG ...]
                        Initialize TAPAS with subset of given images exp. "-img IMG05342.jpg IMG2314.jpg"



## Scanned Aerial [without Campari]
for unsure camera positions

usage: _micmac_workflow_scanned_aerial_est.py [-h] [-fid FID] [-a_fid A_FID] [-tp TP] [-tp_m TP_M] [-o ORI]
                                             [-o_sub O_SUB] [-o_giv O_GIV] [-d_m D_M] [-out OUT]
                                             [-cl {ALL,NONE,TP,ORI,DM,OUTPUT}] [-e EXTENSION] [-x X_OFF] [-y Y_OFF]
                                             [-z ZOOM] [-r RESOL] [-c CAM] [-i_fid I_FID] [-p POS] [-t_res T_RES]
                                             [-n NBVI] [-s_n S_NB] [-d DEFCOR] [-reg REGUL] [-szw SZW]
                                             [-o_sub_n O_SUB_N] [-o_img O_IMG [O_IMG ...]]_

**MicMac Workflow Runner for Scanned Aerial Imagery**

optional arguments:
-  -h, --help            show this help message and exit

_ARGS for PROGRAM STAGES_
-  -fid FID, -FIDUCIALS FID
                        DO SETUP ?: Fiducials ## Resampling to Scan Resolution, default = 0 / else 1
-  -a_fid A_FID, -AUTO_FIDUCIALS A_FID
                        DO SETUP ?: AUTO Fiducials with KUGELHUPF ## Resampling to Scan Resolution, default = 0 / else
                        1
-  -tp TP, -TIEPOINTS TP
                        DO SETUP ?: Camera Positions ## Tie Points ## Tie Point Improvement, default = 0 / else 1
-  -tp_m TP_M, -TIEPOINT_MASK TP_M
                        DO SETUP ?: Tie Point Masking, default = 0 / else 1
-  -o ORI, -ORI ORI      DO SETUP ?: INTERIOR ORIENTATION ## EXTERIOR ORIENTATION, default = 0 / else 1
-  -o_sub O_SUB, -O_SUB O_SUB
                        DO SETUP ?: Initialize TAPAS with subset of the first "n" images FLAG -o_sub_n; ,default = 0 /
                        else 1
-  -o_giv O_GIV, -O_GIV O_GIV
                        DO SETUP ?: Initialize TAPAS with subset of given images FLAG -o_img; ,default = 0 / else 1
-  -d_m D_M, -DENSE_M D_M
                        DO SETUP ?: Orthophoto ## Dense Matching, default = 0 / else 1
-  -out OUT, -OUTPUT OUT
                        DO SETUP ?: OUTPUT, default = 0 / else 1
-  -cl {ALL,NONE,TP,ORI,DM,OUTPUT}, -CLEAN {ALL,NONE,TP,ORI,DM,OUTPUT}
                        DO Cleanup ?: Remove Folders from different STAGES {"ALL", "NONE", "TP", "ORI", "DM" ,
                        "OUTPUT"} ,default = NONE
                      
_ARGS for VARIABLES & FILES_
-  -e EXTENSION, -EXTENSION EXTENSION
                        image file type (JPG, jpg, TIF, tif ,png..., default=tif).
-  -x X_OFF, -X_OFF X_OFF
                        X (easting) offset for ply file overflow issue (default=0).
-  -y Y_OFF, -Y_OFF Y_OFF
                        Y (northing) offset for ply file overflow issue (default=0).
-  -z ZOOM, -ZOOM ZOOM   Last step in pyramidal dense correlation (default=2, can be in [8,4,2,1])
-  -r RESOL, -RESOL RESOL
                        Ground resolution (in meters)
-  -c CAM, -CAM CAM      Basic distortion models easily accessible in MicMac (RadialBasic, RadialStd, RadialExtended,
                        Fraser, FraserBasic), default = RadialStd.
-  -i_fid I_FID, -INIT_FID_IMG I_FID
                        Initial Image to Use for Fiducial Measurements, default = 1st. Image.
-  -p POS, -POSITIONS POS
                        Filename of Camera Positions. txt / csv File with MicMac Readable Header
-  -t_res T_RES, -TAPIOCA_RES T_RES
                        Find Tie points using [number] px windows. 1/2 resolution image = best value for RGB bayer
                        sensor
-  -n NBVI, -NBVI NBVI   Number Visible Images for DenseMatching ,default = 3; min=2
-  -s_n S_NB, -S_N S_NB  Number Schnaps minimum remaining Tie Points. mm3d default = 1000 ,default = 2000
-  -d DEFCOR, -DEFCOR DEFCOR
                        DenseMatching Correlation Threshold. zero is none. mm3d default = 0.2 ,default = 0.1; min=0
-  -reg REGUL, -REGUL REGUL
                        Regularization Factor (Smoothing). If your data does have some sharp transitions (side of
                        buildings for instance), they will be smoothed. 0.9 = real smooth / 0.9 > more noisy ,default
                        = 0.02; min=0
-  -szw SZW, -SZW SZW    Correlation Window Size (1 means 3x3) ,default = 1
-  -o_sub_n O_SUB_N, -O_SUB_N O_SUB_N
                        Initialize TAPAS with subset of the first "n" images; default 5
-  -o_img O_IMG [O_IMG ...], -O_IMG O_IMG [O_IMG ...]
                        Initialize TAPAS with subset of given images exp. "-img IMG05342.jpg IMG2314.jpg"