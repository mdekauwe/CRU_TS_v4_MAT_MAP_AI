#!/usr/bin/env python

"""
For each location on David's list, extract the MAT, MAP, AI & elevation

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
import pandas as pd
import csv
import requests

def main():

    df = pd.read_csv("SITE_LIST.csv", header=0, sep=",")
    places = df.Sitename.values

    lats_needed = df["Lat_deg"].values
    lons_needed = df["Long_deg"].values

    # Fix units to help match the 0.5 degree data
    lats_neededx = [float(x_round(float(i))) for i in lats_needed]
    lons_neededx = [float(x_round(float(i))) for i in lons_needed]
    lats_neededr = [float(i) for i in lats_needed]
    lons_neededr = [float(i) for i in lons_needed]

    lats_neededx = dict(zip(places, lats_neededx))
    lons_neededx = dict(zip(places, lons_neededx))
    lats_neededr = dict(zip(places, lats_neededr))
    lons_neededr = dict(zip(places, lons_neededr))

    fp  = open('sites_and_bioclimatic_stuff.csv', "w")

    s = "%s,%s,%s,%s,%s,%s,%s,%s" % ("site","lat","lon","elev","mat","map","ai","pet")
    print(s, end="\n", file=fp)

    nrows = 360
    ncols = 720
    #f = Dataset("raw_data/PRE/cru_ts4.00.1971.1980.pre.dat.nc", 'r')
    #lon = f.variables['lon'][:]
    #print(lon)
    latitudes = np.linspace(-89.75, 89.75, nrows)
    longitudes = np.linspace(-179.75, 179.75, ncols)


    mapx = np.fromfile("MAP_1960_2010.bin").reshape(nrows, ncols)
    matx = np.fromfile("MAT_1960_2010.bin").reshape(nrows, ncols)
    aix = np.fromfile("AI_1960_2010.bin").reshape(nrows, ncols)
    petx = np.fromfile("PET_1960_2010.bin").reshape(nrows, ncols)
    plt.imshow(petx[50:200,550:650])
    plt.colorbar()
    plt.show()
    for p in places:

        r = np.where(latitudes==lats_neededx[p])[0][0]
        c = np.where(longitudes==lons_neededx[p])[0][0]

        if p.strip() == "Cape Tribulation Crane":
            print(r, c)

        #if p.strip() == "Cape Tribulation Crane":
        #    c -= 1
        #print(p.strip(), r, c, lats_neededr[p], lons_neededr[p], lats_neededx[p], lons_neededx[p])
        # get elevation
        e = requests.get('http://api.geonames.org/gtopo30JSON?lat=%f&lng=%f&username=mdekauwe' % (lats_neededr[p], lons_neededr[p]))
        elev = e.json()['gtopo30']

        s = "%s,%s,%s,%s,%s,%s,%s,%s" % (p.strip(), lats_neededr[p],
                                      lons_neededr[p], elev, matx[r,c],
                                      mapx[r,c], aix[r,c], petx[r,c])
        print(s, end="\n", file=fp)

    fp.close()

def x_round(x):
    # Need to round to nearest .25 or .75 to match the locations in CRU
    val = round(x * 4.0) / 4.0
    valx = str(val).split(".")
    v1 = valx[0]
    v2 = valx[1]

    if v2 <= "25":
        v2 = "25"
    else:
        v2 = "75"
    valx = float("%s.%s" % (v1, v2))

    return (valx)

if __name__ == "__main__":

    main()
