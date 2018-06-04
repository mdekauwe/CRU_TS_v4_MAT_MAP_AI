#!/bin/bash

# combine all time slices into one file

cdo mergetime raw_data/TMP/cru_ts4.00*.nc raw_data/TMP/merged_TMP_1961_2010.nc

# Delete final year as it isn't complte and will mess up seasonal calcs
cdo delete,year=2010 raw_data/TMP/merged_TMP_1961_2010.nc raw_data/TMP/merged_TMP_1961_2009.nc
rm raw_data/TMP/merged_TMP_1961_2010.nc

# calculate monthly max across all years

cdo ymonmax raw_data/TMP/merged_TMP_1961_2009.nc raw_data/TMP/merged_TMAX_1961_2009.nc

# calculate seasonal mean

cdo seasmean raw_data/TMP/merged_TMAX_1961_2009.nc raw_data/TMP/merged_TMAX_seasmean_1961_2009.nc

rm raw_data/TMP/merged_TMAX_1961_2009.nc raw_data/TMP/merged_TMP_1961_2009.nc
