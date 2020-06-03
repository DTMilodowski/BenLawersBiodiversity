"""
================================================================================
visualise_high_res_data.py
--------------------------------------------------------------------------------
basic workflow to visualise the high resolution datasets that are to be analysed
during the STFC project.
================================================================================
"""
import numpy as np
import xarray as xr

import matplotlib.pyplot as plt
import seaborn as sns
sns.set()
plt.rcParams["axes.axisbelow"] = False

"""
Load in some data - update as required
"""
data_dir = '/path/to/your/data/'
raster_file = 'filename.tif'

# load lidar tch
raster=xr.open_rasterio('%s/%s' % (data_dir,raster_file))
n_bands = raster.values.shape[0]

#apply nodata values
for ii in range(n_bands):
    raster.values = raster.values.astype('float')
    raster.values[raster.values==raster.nodatavals[ii]]=np.nan

"""
# Calculate NDVI
"""
# need to specify which band correspond to red and near-infrared
red_band = 1 # this will need to be changed to the right band
nir_band = 2 # this will need to be changed to the right band
red = raster.sel(red_band)
nir = raster.sel(nir_band)
ndvi.values=(nir-red)/(nir+red)

# Other indices are similarly easy to calculate

"""
Create mask
"""
ndvi_threshold = 0.6
ndvi_mask = ndvi.values>=0.6 # this creates a 2D array with pixels marked True
                             # if the ndvi value is above or equal to the
                             # threshold

# we can alse apply the mask easily
ndvi_masked = ndvi.copy(deep=True)
ndvi_masked.values[ndvi_mask==False]=np.nan

# and do the same for the original raster bands - I'll make a copy, but you
# could equally just mask the bands in the original raster object
raster_masked = raster.copy(deep=True)
for ii in range(n_bands):
    raster_masked.values[ndvi_mask==False]= np.nan

"""
Calculating coefficient of variation for moving window
"""
window_width = 5 # must be an odd number as it is the window width in pixels,
                 # centred on the target pixel. This defines the scale
buffer = (window_width-1)/2 # we need to deal with boundaries, so specify a
                            # buffer accordingly
CVar = raster.copy(deep=True)
CVar.values[:,:,:]=np.nan # set all values to nan as a default

#-----------------------------
# define some useful functions
def calculate_CVar(data):
    return np.std(data)/np.mean(data)

def calculate_CVar_skipnan(data):
    nanmask = np.isfinite(data)
    return np.std(data[nanmask])/np.mean(data[nanmask])
#-----------------------------

# now loop through the array and calculate the local coefficient of variation
# for each band - this might take a while
n_bands,rows,cols = CVar.values.shape
for ii in range(buffer,rows-buffer):
    for jj in range(buffer,cols-buffer):
        for bb in range(n_bands):
            raster_sub = raster_masked.values[bb,ii-buffer:ii+buffer,jj-buffer:jj+buffer]
            CV.values[bb,ii,jj] = calculate_CVar_skipnan(raster_sub)

"""
Simple plot for one band
"""
fig, axis = plt.subplots(nrows=1, ncols=1, figsize=(8,6))
CV.sel(band=1).plot(ax=axis, cmap='viridis', add_colorbar=True,
                    cbar_kwargs={'label': 'Coeff. of Variation for band 1',
                    'orientation':'horizontal'})
axis.set_aspect('equal')
fig.show()

# write to file
figure_name = 'this_is_a_test.png'
fig.savefig(figure_name)
