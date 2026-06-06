
import numpy as np

# ----------------------------
# Generate Solar Spectrum (Blackbody)
# ----------------------------

def planck_lambda(wavelength_m, T):
    """
    Planck function B_lambda
    wavelength in meters
    T in Kelvin
    Returns spectral radiance (arbitrary units fine)
    """
    h = 6.62607015e-34
    c = 2.99792458e8
    k = 1.380649e-23

    numerator = 2.0 * h * c**2
    denominator = (wavelength_m**5) * (np.exp(h*c / (wavelength_m*k*T)) - 1.0)

    return numerator / denominator
