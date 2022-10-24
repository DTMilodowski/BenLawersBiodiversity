"""
pt1_intro_to_python_spatial.py
--------------------------------------------------------------------------------
WORKSHOP PART 1: INTRODUCTION TO SPATIAL ANALYSIS IN PYTHON
This is the first interactive component of the Forests2020 workshop: "Mapping
restoration potential using Machine Learning". This workshop is based on the
open source programming language python, and utilises the geospatial library
xarray (http://xarray.pydata.org/en/stable/) and the machine learning library
scikit-learn (https://scikit-learn.org/stable/index.html).

28/02/2019 - D. T. Milodowski
--------------------------------------------------------------------------------
"""

"""
NOTE!!!
This is a comment block, bookended by three double quotation marks
Comment blocks and comments are ignored by python, but are useful for explaining
what the code is doing
"""

# this is a comment, with a hash at the start. The line after the hash is
# ignored

"""
# Import the necessary packages
"""
import numpy as np                  # standard package for scientific computing
import xarray as xr                 # xarray geospatial package
import matplotlib.pyplot as plt     # plotting package
import seaborn as sns               # another useful plotting package
sns.set()                           # set some nice default plotting options


"""
Loading a dataset using xarray
We are going to start by loading a raster dataset into python using xarray,
before exploring how to interact with this xarray object. For later scripts, a
lot of the processing will be tucked away inside other functions, but it is
useful to know what we are dealing with.
"""

# To open a raster dataset is easy enough to do. We need the name of the file in
# question, alongside it's full path
raster_file = '' # the raster file (fyll path)
print(raster_file) # print filename to screen

# open file and store data in an xarray called agb
ds = xr.open_rasterio(raster_file)
print(type(ds))

# Let's explore the xarray structure a little
# The key properties for a data array are:
# 1) the values numpy array containing the gridded observations
print(type(ds.values))
# 2) the dimensions of the array
print(ds.dims)
# 3) the coordinates of the data
print(ds.coords)
# 4) the meta data e.g. coordinate system
print(ds.attrs)
# 5) the nodata value
print(ds.nodatavals)

# We can select an individual  band very easily using the sel() function
band = ds.sel(band=1)

# convert nodatavalues to numpy-recognised nodata (np.nan)
band.values[band.values==band.nodatavals[0]]=np.nan

# We'll explore xarray interactions further in due course, but for now, it is
# worthwhile simply plotting a map of the data. With xarray, this is really easy.

"""
Basic plotting with xarray
"""

fig, axis = plt.subplots(nrows=1, ncols=1, figsize=(8,6))
band.plot(ax=axis, cmap='viridis', add_colorbar=True,
                    cbar_kwargs={'label': 'This is a colorbar label',
                    'orientation':'horizontal'})
# other keyword arguments that are useful for plotting are
#     vmin = ? (minimum value to clip the color scale)
#     vmax = ? (maximum value to clip the color scale)
#     extend = 'max'/'min'/'both' (for use when truncating colorscale)
axis.set_aspect("equal")
fig.show()

"""
Subsets of xarrays
"""
# OK, now we can try to manipulate this a bit. It is quite easy to select a
# subset of an xarray - see http://xarray.pydata.org/en/stable/indexing.html
# We are not going to go through every example here, but a simple spatial
# subset can be taken if we know the coordinate bounds
# Note convention is often for raster datasets to have y units starting at ymax
# and dropping to ymin, as first row is at the "top" of the map, hence the
# reverse ordering of ymax and ymin when using the slice function
ymin = 0; ymax = 7 # update for your coordinates
xmin = -77; xmax = -60 # update for your coordinates
subset = band.sel(y=slice(ymax,ymin),x = slice(xmin,xmax))
# Note that since our latitudes are listed in decreasing order, we take the
# slice from max to min, which might seem initially counter-intuitive.
subset.plot(ax=axis, cmap='viridis', add_colorbar=True,
                    cbar_kwargs={'label': 'This is a colorbar label',
                    'orientation':'horizontal'})
