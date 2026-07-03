from astropy.io import fits
from astropy.modeling import models, fitting
from matplotlib.patches import Circle
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Load FITS file
# -----------------------------
# filename = "../cubes/all8/ioRot_m06.fits"
filename = "../cubes/ioRot_m00.fits"
hdul = fits.open(filename)
data = hdul[0].data
hdul.close()

# remove NaNs if present
data = np.nan_to_num(data)

fig, axes = plt.subplots(2, 4, figsize=(16, 8))
fig.suptitle("Io with ALES (UT 03jan2026)",
  fontsize=20, fontweight='bold', y=0.98)
axes = axes.flatten()
wvals = [3.426, 3.443, 3.459, 3.475, 3.491, 3.506, 3.522, 3.537, 3.553, 3.568, 3.583,
  3.598, 3.613, 3.628, 3.643, 3.658, 3.673, 3.688, 3.702, 3.717, 3.731, 3.745, 3.760,
  3.774, 3.788, 3.803, 3.817, 3.831, 3.844, 3.858, 3.872, 3.885, 3.899, 3.913, 3.926,
  3.939, 3.953, 3.966, 3.979, 3.992, 4.005, 4.018, 4.031, 4.044, 4.057, 4.070, 4.083,
  4.095, 4.108, 4.120, 4.133, 4.145 ]
# 4.095, 4.108, 4.120, 4.133, 4.145, 4.158, 4.170, 4.183 ]
print(wvals)

# Plot info = y,x are as read from js9
pi = [
      { 'name':'Loki'          , 'y': 33, 'x':40, 'topcut':13},
      { 'name':'Near Mbali'    , 'y': 20, 'x':24, 'topcut':13},
      { 'name':'A'             , 'y': 35, 'x':34, 'topcut':13},
      { 'name':'B'             , 'y': 27, 'x':36, 'topcut':13},
      { 'name':'C'             , 'y': 23, 'x':34, 'topcut':13},
      { 'name':'D'             , 'y': 23, 'x':38, 'topcut':13}]
# xy are above reversed and minus 1
circles = [
    (39, 32, "Loki"       , (45, 42), 0),
    (23, 19, "Near Mbali" , ( 4,  3), 0),
    (33, 34, "A"          , (38, 50), 0),
    (35, 26, "B"          , (53, 29), 0),
    (33, 22, "C"          , (24, 50), 0),
    (37, 22, "D"          , (53, 10), 0),
]

lowcut = 33
topCutMin = 13
for i in range(len(pi)):
  topcut = pi[i]['topcut']
  wsize = data.shape[0] - lowcut             #  trim both sides
  spec = np.full(wsize-topCutMin,np.nan)
  for j in range(wsize-topcut):
    slice = data[lowcut+1+j,:,:]
    sval  = slice[pi[i]['y']-1, pi[i]['x']-1]
    spec[j] = sval
  ax = axes[i]
  ax.set_title(pi[i]['name'])
  ax.plot(wvals,spec)
  print(spec)

# Plot the full disk tiwce in the lower right with spec points annotated
for i, max in zip((6,7),(5000,20000)):
  ax = axes[i]

  # --- Load FITS cube ---
  hdul = fits.open("../cubes/ioRot_m00.fits")
  cube = hdul[0].data

  LokiCube = cube.copy()
# if i == 6:
  if i == 12:
    # mask out loki
    for i in range(30,35):
      for j in range(36,43):
        LokiCube[:,i,j] = 0

  img = np.zeros( [cube.shape[1],cube.shape[2]] )
  for j in range(cube.shape[1]):
    for k in range(cube.shape[2]):
      img[j,k] = np.median(LokiCube[60:74, j, k], axis=0)  # 60-74 = 3.9-4.1`

  im = ax.imshow(img, origin='lower',vmin=100,vmax=max)
  ax.set_title("3.9 to 4.1 micons, peak = %d" % max)
  ax.set_xticks([])
  ax.set_yticks([])

  for x, y, label, textpos, r in circles:
    circ = Circle((x, y), radius=r, edgecolor='yellow', facecolor='none', lw=2)
    ax.add_patch(circ)

    ax.annotate(
        label,
        xy=(x, y),
        xytext=textpos,
        fontsize=18,
        color='yellow',
        arrowprops=dict(arrowstyle="->", color='yellow', lw=1.5)
    )

plt.show()
