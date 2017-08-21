#!/usr/bin/env python

"""
Generate an aridity index from the rainfall and pet data Aacross all CRU data
we've downloaded

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
import calendar


def main(fdir1, fdir2):

    nslices = 5     # 1961-2010, in 10 year slices
    nyears = 10
    nrows = 360
    ncols = 720
    latitudes = np.linspace(-89.75, 89.75, nrows)
    longitudes = np.linspace(-179.75, 179.75, ncols)

    data = np.zeros((nslices, nyears, nrows, ncols))
    data2 = np.zeros((nslices, nyears, nrows, ncols))
    i = 0
    for fname in glob.glob(os.path.join(fdir1, '*.nc')):

        st = int(os.path.basename(fname).split(".")[2])
        en = int(os.path.basename(fname).split(".")[3])
        years = np.arange(st, en+1)

        f = Dataset(fname, 'r')
        time = len(f.dimensions['time'])

        temp = f.variables["pre"][:,:,:]

        # sum months to get annual data
        ppt = temp.reshape(10, 12, nrows, ncols).sum(axis=1)

        # Now get the matching PET file
        fn = os.path.join(fdir2, os.path.basename(fname).replace("pre", "pet"))
        f = Dataset(fn, 'r')
        time = len(f.dimensions['time'])
        temp = f.variables["pet"][:,:,:]

        # sum months to get annual data
        pet = temp.reshape(10, 12, nrows, ncols).sum(axis=1)

        # Convert PET mm/day to mm/year, accounting for leap years
        for j,yr in enumerate(years):

            if calendar.isleap(yr):
                pet[j,:,:] *= 366.
            else:
                pet[j,:,:] *= 365.

        # store it
        data[i,:,:,:] = ppt
        data2[i,:,:,:] = pet

        i += 1

    # average years to get avg aridity_index
    data = data.reshape(nslices*nyears, nrows, ncols).mean(axis=0)
    data2 = data2.reshape(nslices*nyears, nrows, ncols).mean(axis=0)

    aridity_index = np.where(np.logical_and(data>0.0, data2>0.0), data / data2, 0.0)
    # make plot look sensible, exclude super high and 0
    data_plt = np.where(aridity_index==0.0, np.nan, aridity_index)
    data_plt = np.where(data_plt>0.5, np.nan, data_plt)
    plt.imshow(data_plt, origin='lower')
    plt.colorbar()
    plt.show()

    aridity_index.tofile("AI_1960_2010.bin")

if __name__ == "__main__":

    fdir1 = "raw_data/PRE"
    fdir2 = "raw_data/PET"
    main(fdir1, fdir2)
