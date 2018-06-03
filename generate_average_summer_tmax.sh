#!/bin/bash

# combine all time slices into one file

cdo mergetime raw_data/TMP*.nc raw_data/TMP/merged_TMP_1961_2010.nc

# calculate monthly max across all years

cdo ymonmax raw_data/TMP/merged_TMP_1961_2010.nc raw_data/TMP/merged_TMAX_1961_2010.nc

# calculate seasonal mean

cdo seasmean raw_data/TMP/merged_TMAX_1961_2010.nc raw_data/TMP/merged_TMAX_seasmean_1961_2010.nc

rm raw_data/TMP/merged_TMAX_1961_2010.nc raw_data/TMP/merged_TMP_1961_2010.nc
