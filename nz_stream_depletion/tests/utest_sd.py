#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 10:01:15 2021

@author: mike
"""

# from . import main
import numpy as np
import pandas as pd

##########################################3
### Parameters

# Pumped aquifer
trans = 500 # m/d
big_s = 0.05

# Well
pump_q = 50 # l/s
sep_distance = 500 # m

time1 = 6 # days
time2 = 7 # days
time1 = 30 # days
time1 = 150 # days

# streambed
stream_k = 1000 # m/d
stream_thick = 1 # m
stream_width = 1 # m
stream_cond = stream_k * stream_thick / stream_width

# aquitard
tard_k = 0.1 # m/d
tard_thick = 10 # m
tard_sy = 0.1

# upper aquifer
trans1 = 500
s1 = 0.05

flow_csv = '/media/nvme1/git/nz-flow-naturalisation/flownat/data/sample_flow.csv'


#######################################3
### Tests

extraction = pd.read_csv(flow_csv, index_col='time', parse_dates=True, infer_datetime_format=True, dayfirst=True).streamflow

sdf1 = theis_jenkins(time1, trans, big_s, sep_distance)

sdf2 = hunt1999(time1, trans, big_s, stream_k, stream_thick, stream_width, sep_distance)

sdf3 = hunt2003(time1, trans, big_s, tard_k, tard_thick, tard_sy, stream_k, stream_thick, stream_width, sep_distance)




sdf1 = theis_jenkins(time1, trans, big_s, sep_distance)
sdf2 = theis_jenkins(time2, trans, big_s, sep_distance)

sdf_list = []

for i in range(30):
    sdf1 = theis_jenkins(i+1, trans, big_s, sep_distance)
    sdf_list.extend([sdf1])


np.diff(sdf_list)

sdf_list = []

for i in range(30):
    sdf1 = hunt2003(i+1, trans, big_s, 0, 1, 1, stream_cond, sep_distance)
    sdf_list.extend([sdf1])


diff1 = np.diff([0] + sdf_list)

diff2 = pd.Series(list(diff1), index=list(range(1, 31)))

times = list(range(1, 151))

tj1 = np.vectorize(theis_jenkins)

sdf3 = tj1(times, trans, big_s, sep_distance)



def tj2(times, trans, big_s, sep_distance):
    """

    """
    sdf_list = []

    for i in times:
        sdf1 = theis_jenkins(i+1, trans, big_s, sep_distance)
        sdf_list.extend([sdf1])

    return np.array(sdf_list)


sdf4 = tj2(times, trans, big_s, sep_distance)


diff1 = np.diff([0] + sdf4)

diff2 = pd.Series(list(diff1), index=times)



wl1 = ward_lough2011(150, trans1, s1, trans, big_s, tard_k, tard_thick, stream_k, stream_thick, stream_width, sep_distance)


self = SD()
avail = self.load_input_data(100, 100, 0.1)

sd_rates = self.calc_sd_extraction_multiple_days(extraction)




































