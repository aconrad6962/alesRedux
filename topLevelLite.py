import nales
import os
from datetime import datetime
import numpy as np
from astropy.io import fits

print('Top of top level', flush=True)

def printTime(s):
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  print( s, timestamp, flush=True )

# From within wavecal/
os.chdir('wavecal')
printTime( "before organize" )
wave_cal_ims, light_leak = nales.organize_wavecal_frames('raw/')
printTime( "after organize" )

os.chdir('..')
median_sky = fits.getdata('science_target/median_sky.fits')

printTime( "after build sky" )

printTime( "before cubifier" )

cubifier = nales.Cubifier(
wave_cal_ims,
median_sky,
sky_var=np.ones_like(median_sky), # Uniform variance works well
start_offsets=(73, 192), # REQUIRED - (x, y) from inspecting NB39
)
# Save for later use
import pickle
with open('science_target/Cubifier.pkl', 'wb') as f:
  pickle.dump(cubifier, f)

printTime( "after cubifier" )

printTime( "before extractor" )

extractor = nales.CubeExtractor(
cubifier='science_target/Cubifier.pkl',
frame_ids='science_target/target_frames.pkl',
bad_pixel_file='wavecal/bad_and_neighbors_bpm_and_these_darks.pkl',
raw_directory='science_target/raw/'
)
extractor.run(output_dir='cubes/', n_sky_frames=50)

printTime( "after extractor" )
