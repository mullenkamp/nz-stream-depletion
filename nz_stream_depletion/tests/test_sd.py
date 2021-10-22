#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 10:01:15 2021

@author: mike
"""

# from . import main
import numpy as np


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
stream_cond = stream_k * stream_thick * stream_width

# aquitard
tard_k = 1000000 # m/d
tard_thick = 1 # m
tard_sy = 0.1

# upper aquifer
trans1 = 500
s1 = 0.05


#######################################3
### Tests

sdf1 = theis_jenkins(time1, trans, big_s, sep_distance)

sdf2 = hunt2003(time1, trans, big_s, 0, 1, 1, stream_cond, sep_distance)

sdf3 = hunt2003(time1, trans, big_s, tard_k, tard_thick, tard_sy, stream_cond, sep_distance)




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









































