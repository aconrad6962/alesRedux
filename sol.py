from planck import planck_lambda
import numpy as np

def solSpec( min, max ):
  # wavelength grid (microns)
  wave = np.linspace(min, max, 98)

  # Convert to meters
  wave_m = wave * 1e-6

  # Solar temperature
  T_sun = 5778  # Kelvin

  solar_flux = planck_lambda(wave_m, T_sun)

  # Normalize
  solar_flux /= np.nanmedian(solar_flux)

  return wave, solar_flux
