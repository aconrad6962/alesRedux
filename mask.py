import numpy as np
from scipy.ndimage import binary_closing, binary_fill_holes
from skimage.filters import threshold_otsu
from skimage.draw import disk

def buildMask( cube ):

  # cube shape: (nz, ny, nx)
  image = np.nanmedian(cube, axis=0)
  
  # automatic threshold
  thresh = threshold_otsu(image)
  mask = image > thresh
  
  # clean edges / AO speckles
  mask = binary_closing(mask, structure=np.ones((3,3)))
  
  # fill interior of the disk
  mask = binary_fill_holes(mask)
  
  mask = mask.astype(int)
  
  return mask  

def buildDiscMask( cube ):
  # Define circle parameters
  center_y, center_x = 29, 34  # (row, column) for skimage
  radius = 17

  mask = np.zeros( [cube.shape[1],cube.shape[2]] )

  # Get the indices of pixels within the circle
  rr, cc = disk((center_y, center_x), radius, shape=mask.shape)

  # Set the pixel values to white (or any value, e.g., 1.0)
  mask[rr, cc] = 1.0

  return mask
