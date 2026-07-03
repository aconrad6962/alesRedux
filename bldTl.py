import numpy as np
from astropy.modeling import models, fitting
from astropy.io import fits
from glob import glob
from mask import buildDiscMask
from scipy.ndimage import rotate
from astropy.convolution import AiryDisk2DKernel, convolve_fft

def gaussPeak( y0, x0, data, size ):
  # -----------------------------
  # Extract region around peak
  # -----------------------------
  y_min = max(0, y0 - size)
  y_max = min(data.shape[0], y0 + size)
  x_min = max(0, x0 - size)
  x_max = min(data.shape[1], x0 + size)

  sub = data[y_min:y_max, x_min:x_max]

  # coordinate grid
  y, x = np.mgrid[0:sub.shape[0], 0:sub.shape[1]]

  # -----------------------------
  # Gaussian fit
  # -----------------------------
  g_init = models.Gaussian2D(
    amplitude=sub.max(),
    x_mean=sub.shape[1]/2,
    y_mean=sub.shape[0]/2,
    x_stddev=3,
    y_stddev=3
  )

  fit = fitting.LevMarLSQFitter()
  g_fit = fit(g_init, x, y, sub)

  return g_fit.amplitude.value

def buildTelluric( cube ):

  dir = "../../cubes/telluric/"
  files = sorted(glob(dir+"cube*.fits"))

  # Read data into a list
  data = []
  for f in files:
    with fits.open(f) as hdul:
        data.append(hdul[0].data)

  # Stack into a 4-D array: (n_files, z, y, x)
  stack = np.stack(data, axis=0)

  # Median combine across files
  median_cube = np.median(stack, axis=0)

  #  extract the 1D spec to go into each spaxal
  x0 = 32     # pixel location of star in telluric cube
  y0 = 32
  spec = np.zeros( median_cube.shape[0] )
  for i in range( median_cube.shape[0] ):
    slice = median_cube[i,:,:]
    spec[i] = gaussPeak( x0, y0, slice, 3 )

  #  Normalize
  spec /= np.max(np.abs(spec))
  print( spec )

  #  Build the model (still deconvolved)
  mask = buildDiscMask( cube )
  decon_cube = np.ones_like(cube)
  for i, j in np.argwhere(mask > 0):
      decon_cube[:, i, j] = spec

  #  Convolve by the diffraction limit (someday vary by slice)
  radius = 3       # Size in pixels of Airy pattern (to first null)
  model_cube = np.zeros_like(cube)
  for i in range(decon_cube.shape[0]):
    psf = AiryDisk2DKernel(radius)
    model_cube[i,:,:] = convolve_fft(decon_cube[i,:,:], psf )
  print( model_cube[:,32,32] )

  return model_cube
