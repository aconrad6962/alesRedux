from sol import solSpec
import numpy as np
from mask import buildDiscMask
from astropy.io import fits
from astropy.convolution import AiryDisk2DKernel, convolve_fft

def buildBackground( cube ):
  mask = buildDiscMask( cube )
# fits.writeto("./mask.fits", mask, overwrite=True)

  #  Get solar specctrum (normalized)
  wave, solar_flux = solSpec( 2.78, 4.29 )

  # Select short-wavelength indices
  shortwave_range = (2.8, 3.4)
  sw = (wave >= shortwave_range[0]) & (wave <= shortwave_range[1])

  #  Compute scale factor as median of flux at shorter wavelengths
  short_fluxes = []
  for i, j in np.argwhere(mask > 0):
    short_fluxes.append( cube[ sw, i, j ] )
  C = np.median( short_fluxes )

  #  Build the model (still convolved)
  decon_cube = np.zeros_like(cube)
  for i, j in np.argwhere(mask > 0):
    decon_cube[:, i, j] = C * solar_flux

  #  Convolve by the diffraction limit (someday vary by slice)
  radius = 3       # Size in pixels of Airy pattern (to first null)
  model_cube = np.zeros_like(cube)
  for i in range(decon_cube.shape[0]):
    psf = AiryDisk2DKernel(radius)
    model_cube[i,:,:] = convolve_fft(decon_cube[i,:,:], psf )

  return model_cube
