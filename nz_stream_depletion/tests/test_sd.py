#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 10:01:15 2021

@author: mike
"""

from nz_stream_depletion import SD
# from .main import SD
import os
import numpy as np
import pandas as pd
import pytest

##########################################3
### Parameters

base_path = os.path.realpath(os.path.dirname(__file__))
data_path = os.path.join(os.path.split(base_path)[0], 'data')

# Pumped aquifer
pump_aq_trans = 1000 # m/d
pump_aq_s = 0.1

# Well
pump_q = 50 # l/s
sep_distance = 500 # m

time1 = 6 # days
time2 = 7 # days
time1 = 30 # days
n_days = 150 # days

# streambed
stream_k = 1000 # m/d
stream_thick = 1 # m
stream_width = 1 # m
stream_cond = stream_k * stream_thick / stream_width

# aquitard
aqt_k = 0.1 # m/d
aqt_thick = 10 # m
aqt_s = 0.1

# upper aquifer
upper_aq_trans = 500
upper_aq_s = 0.05

flow_csv = os.path.join(data_path, 'sample_flow.csv')

params1 = {'pump_aq_trans': pump_aq_trans, 'pump_aq_s': pump_aq_s, 'sep_distance': sep_distance}

params2 = {'pump_aq_trans': pump_aq_trans, 'pump_aq_s': pump_aq_s, 'sep_distance': sep_distance, 'stream_k': stream_k, 'stream_thick': stream_thick, 'stream_width': stream_width}

params3 = {'pump_aq_trans': pump_aq_trans, 'pump_aq_s': pump_aq_s, 'sep_distance': sep_distance, 'stream_k': stream_k, 'stream_thick': stream_thick, 'stream_width': stream_width, 'aqt_k': aqt_k, 'aqt_thick': aqt_thick, 'aqt_s': aqt_s}

params4 = {'pump_aq_trans': pump_aq_trans, 'pump_aq_s': pump_aq_s, 'sep_distance': sep_distance, 'stream_k': stream_k, 'stream_thick': stream_thick, 'stream_width': stream_width, 'aqt_k': aqt_k, 'aqt_thick': aqt_thick, 'aqt_s': aqt_s, 'upper_aq_trans': upper_aq_trans, 'upper_aq_s': upper_aq_s}

params_list = [params1, params2, params3, params4]

#######################################3
### Tests

extraction = pd.read_csv(flow_csv, index_col='time', parse_dates=True, infer_datetime_format=True, dayfirst=True).streamflow


@pytest.mark.parametrize('params', params_list)
def test_sd(params):
    self = SD()
    avail = self.load_aquifer_data(**params)

    sd_ratio = self.calc_sd_ratio(n_days)
    sd_ratios = self.calc_sd_ratios(n_days)

    sd_rates = self.calc_sd_extraction(extraction)

    assert sd_rates.sum() > 1000




































