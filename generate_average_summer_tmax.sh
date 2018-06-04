#!/bin/bash

# combine all time slices into one file
cdo mergetime raw_data/TMAX/cru_ts4.*.nc raw_data/TMAX/TMAX_1961_2010.nc

# Make JJA climatology
cdo -timmean -selmon,6,7,8 raw_data/TMAX/TMAX_1961_2010.nc raw_data/TMAX/jja.nc

# Make DJF climatology
cdo -timmean -selmon,10,11,12 -shifttime,-2mon raw_data/TMAX/TMAX_1961_2010.nc \
        raw_data/TMAX/djf.nc

# Merge to get a new 2D field where max [jja.nc; djf.nc] is selected at each
# grid cell, and add 10K
cdo -addc,10 -ifthenelse -gec,0 -sub raw_data/TMAX/djf.nc raw_data/TMAX/jja.nc \
        raw_data/TMAX/djf.nc raw_data/TMAX/jja.nc \
        raw_data/TMAX/avg_summer_TMAX.nc

rm raw_data/TMAX/TMAX_1961_2010.nc
rm raw_data/TMAX/jja.nc
rm raw_data/TMAX/djf.nc
