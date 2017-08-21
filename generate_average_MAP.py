#!/usr/bin/env python

"""
Generate a Mean Annual Precipitation (MAP) across all CRU data we've downloaded

That's all folks.
"""
__author__ = "Martin De Kauwe"
__version__ = "1.0 (21.09.2017)"
__email__ = "mdekauwe@gmail.com"

import numpy as np
import sys
import matplotlib.pyplot as plt
from netCDF4 import Dataset
import os
import glob

def main(fdir):

    nslices = 5     # 1961-2010, in 10 year slices
    nyears = 10
    nrows = 360
    ncols = 720
    latitudes = np.linspace(-89.75, 89.75, nrows)
    longitudes = np.linspace(-179.75, 179.75, ncols)

    data = np.zeros((nslices, nyears, nrows, ncols))
    i = 0
    for fname in glob.glob(os.path.join(fdir, '*.nc')):

        st = int(os.path.basename(fname).split(".")[2])
        en = int(os.path.basename(fname).split(".")[3])
        years = np.arange(st, en+1)

        f = Dataset(fname, 'r')
        time = len(f.dimensions['time'])

        temp = f.variables["pre"][:,:,:]

        # average months to get annual data
        temp = temp.reshape(10, 12, nrows, ncols).sum(axis=1)

        data[i,:,:,:] = temp

        i += 1

    # average years to get MAT
    data = data.reshape(nslices*nyears, nrows, ncols).mean(axis=0)

    # make plot look sensible, exclude super high and 0
    #data_plt = np.where(data==0, np.nan, data)
    #data_plt = np.where(data_plt>4000, np.nan, data_plt)
    #plt.imshow(data_plt, origin='lower')
    #plt.colorbar()
    #plt.show()

    data.tofile("MAP_1960_2010.bin")

if __name__ == "__main__":

    fdir = "raw_data/PRE"
    main(fdir)
