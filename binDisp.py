import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
from mask import buildDiscMask

# --- Load FITS cube ---
hdul = fits.open("../cubes/ioRot_m00.fits")
cube = hdul[0].data
hdr = hdul[0].header

# --- Define wavelength bins ---
bins = [(3.4 + 0.1*i, 3.5 + 0.1*i) for i in range(8)]
channels = [[29,32],[33,39],[40,45],[46,52],[53,59],[60,66],[67,74],[75,82]]

# --- Create figure ---
fig, axes = plt.subplots(2, 4, figsize=(12, 6))
axes = axes.flatten()

mask = buildDiscMask( cube )
# mx, my = np.where( mask > 0 )

# mask out loki
noLokiCube = cube.copy()
for i in range(30,35):
  for j in range(36,43):
    noLokiCube[:,i,j] = 0

for i in range(0,8):
    ax = axes[i]

    c1 = channels[i][0]
    c2 = channels[i][1]
    wmin = bins[i][0]
    wmax = bins[i][1]
    img = np.zeros( [cube.shape[1],cube.shape[2]] )
    for j in range(cube.shape[1]):
      for k in range(cube.shape[2]):
        if mask[j,k] > 0:
          img[j,k] = np.median(noLokiCube[c1:c2, j, k], axis=0)

    im = ax.imshow(img, origin='lower',vmin=1000,vmax=6000)
    ax.set_title(f"{wmin:.2f}–{wmax:.2f} µm")
    ax.axis('off')

# Optional: shared colorbar
fig.colorbar(im, ax=axes, shrink=0.7)

# axes[7].imshow( mask, origin='lower')

# plt.tight_layout()
plt.show()
