import numpy as np
from astropy.io import fits
from glob import glob
from scipy.ndimage import rotate
from bldBg import buildBackground
from bldTl import buildTelluric
from sys import argv

script, epoch = argv

# List of FITS files
dir = "../"+epoch+"/"+epoch+"cubes/"
files = sorted(glob(dir+"cube*.fits"))

# Read data into a list
data = []
for f in files:
    with fits.open(f) as hdul:
        data.append(hdul[0].data)
        parang = float(hdul[0].header.get('LBT_PARA'))

# Stack into a 4-D array: (n_files, z, y, x)
stack = np.stack(data, axis=0)

# Median combine across files
median_cube = np.median(stack, axis=0)

# Rotate to north up
rotated_cube = np.empty_like(median_cube)
Ndelta = 10.3        # Angle between Io north and celestial north

for i in range(median_cube.shape[0]):
    rotated_cube[i] = rotate(
        median_cube[i],
#       angle=26.3,      
#       angle=180+26.3, 
        angle=180+Ndelta-parang,    # see rotNotes.txt
        reshape=False,      # keeps same XY dimensions
        order=3,            # cubic interpolation
        mode='constant',    # fill empty pixels
        cval=0.0
    )

model_cube = buildBackground( rotated_cube )

bgdiv_cube = rotated_cube / model_cube 

tellc_cube = buildTelluric  ( rotated_cube )

final_cube = bgdiv_cube / tellc_cube 

# Copy header from first file
with fits.open(files[0]) as hdul:
    header = hdul[0].header

# Write results as FITS
fits.writeto("../"+epoch+"/ioRot_"+epoch+"_bgrdModel_v3.fits", \
                   model_cube, header, overwrite=True)

fits.writeto("../"+epoch+"/ioRot_"+epoch+"_noBgrdSbtrctd.fits", \
                   rotated_cube, header, overwrite=True)

fits.writeto("../"+epoch+"/ioRot_"+epoch+".fits", \
                   final_cube, header, overwrite=True)

# Sum up slices 79 to 88 = 4.06 to 4.18 into a 2D image
wideBand = np.zeros( [ final_cube.shape[1], final_cube.shape[2] ] )
for i in range(79,88):
  wideBand = wideBand + final_cube[i,:,:]
fits.writeto("../"+epoch+"/sum7988_"+epoch+".fits", \
                    wideBand, header, overwrite=True)
