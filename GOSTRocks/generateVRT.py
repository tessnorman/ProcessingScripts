import os, sys, glob, fnmatch
sys.path.append(r"C:\Users\wb411133\Box Sync\AAA_BPS\Code\GOST")
from GOSTRocks.misc import generateVRT
vrtFiles = []
for root, dirnames, filenames in os.walk(r"Q:\GLOBAL\NTL\VIIRS\Annual"):
    for f in filenames:
        if fnmatch.fnmatch(f, "*vcm-orm-ntl*"):
            vrtFiles.append(os.path.join(root, f))
print vrtFiles
generateVRT(vrtFiles, "Q:\GLOBAL\NTL\VIIRS\Annual\2015_Annual.vrt")

