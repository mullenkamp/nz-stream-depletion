#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 19 09:08:03 2021

@author: mike
"""
import inspect
import numpy as np
import pandas as pd
from typing import Optional, List, Any, Union
from .methods import theis_1941, hunt_1999, hunt_2003, hunt_2009, ward_lough_2011

############################################
### Parameters

method_dict = {'theis_1941': theis_1941, 'hunt_1999': hunt_1999, 'hunt_2003': hunt_2003, 'hunt_2009': hunt_2009, 'ward_lough_2011': ward_lough_2011}


###############################################
### Main class


class SD(object):
    """

    """

    def __init__(self):
        """
        Initialise the SD class and provide all stream depletion methods and the input parameter requirements.
        """
        self.all_methods = {m: inspect.getfullargspec(f).args for m, f in method_dict.items()}
        _ = [m.remove('n_days') for k, m in self.all_methods.items()]

        pass


    def load_aquifer_data(self, sep_distance: int, pump_aq_trans: int, pump_aq_s: float, upper_aq_trans: Optional[int] = None, upper_aq_s: Optional[float] = None, lower_aq_trans: Optional[int] = None, lower_aq_s: Optional[float] = None, aqt_k: Optional[int] = None, aqt_thick: Optional[int] = None, aqt_s: Optional[float] = None, stream_k: Optional[int] = None, stream_thick: Optional[int] = None, stream_width: Optional[int] = None):
        """
        This method is where the physical properties of the aquifer(s) and the stream are assigned and processed. The minimum required data includes the sep_distance, pump_aq_trans, and the pump_aq_s. It will determine which stream depletion methods are available based on the input data.

        Parameters
        ----------
        sep_distance : int
            The separation distance from the pumped well to the stream.
        pump_aq_trans : int
            The pumped (confined) aquifer transmissivity (m2/day).
        pump_aq_s : float
            The storage coefficient of the pumped aquifer.
        upper_aq_trans: int
            The surficial aquifer transmissivity (m2/day).
        upper_aq_s : float
            The storage coefficient of the surficial aquifer.
        lower_aq_trans: int
            The confined aquifer transmissivity (m2/day).
        lower_aq_s : float
            The storage coefficient (specific storage) of the confined aquifer.
        aqt_k : int
            The aquitard hydraulic conductivity (m/day).
        aqt_s : float
            The aquitard storage coefficient.
        aqt_thick : int
            The aquitard vertical thickness (m).
        stream_k : int
            Streambed hydraulic conductivity (m/day).
        stream_thick : int
            The streambed vertical thickness (m).
        stream_width : int
            The streambed width (m).

        Returns
        -------
        list
            of available methods based on the input data

        """
        ## Preprocessing
        saved_args = {k: v for k, v in locals().items() if ((v is not None) and (k != 'self'))}

        ## Get available methods given the input parameters
        avail_methods = [m for m, p in self.all_methods.items() if set(p).issubset(set(saved_args))]

        self.available_methods = avail_methods
        self.params = saved_args

        return avail_methods


    def _select_method(self, method: Optional[str] = None):
        """

        """
        if isinstance(method, str):
            if method in self.available_methods:
                m = method
            else:
                raise ValueError('method is not available given the input parameters.')
        else:
            m = self.available_methods[-1]

        return m


    def calc_sd_ratio(self, n_days: int, method: Optional[str] = None):
        """
        Calculate the stream depletion ratio for a specific number of pumping days for a specific method. If no method is provided, it will choose the highest ranking method based on the available methods.

        Parameters
        ----------
        n_days : int
            The number of pumping days.
        method : str or None
            The stream depletion method to use. It must be one of the available methods based on the input data. None will select the highest ranking method based on the available methods.

        Returns
        -------
        float
        """
        ## Select the method
        m = self._select_method(method)

        required_params = self.all_methods[m]

        ## Calc the SD
        params = {p: v for p, v in self.params.items() if p in required_params}
        params['n_days'] = n_days

        sd_ratio = method_dict[m](**params)

        return sd_ratio


    def calc_sd_ratios(self, n_days: int, method: Optional[str] = None):
        """
        Calculate the stream depletion ratios for all pumping days up to the n_days for a specific method. If no method is provided, it will choose the highest ranking method based on the available methods.

        Parameters
        ----------
        n_days : int
            The number of pumping days.
        method : str or None
            The stream depletion method to use. It must be one of the available methods based on the input data. None will select the highest ranking method based on the available methods.

        Returns
        -------
        list
        """
        ## Select the method
        m = self._select_method(method)

        required_params = self.all_methods[m]

        ## Calc the SD
        days = range(1, n_days+1)

        params = {p: v for p, v in self.params.items() if p in required_params}

        sd_ratios = []
        for t in days:
            params['n_days'] = t

            sd_ratio = method_dict[m](**params)

            sd_ratios.extend([sd_ratio])

        return sd_ratios


    def calc_sd_extraction(self, extraction: pd.Series, method: Optional[str] = None):
        """
        Calculate the stream depleting extraction for all days in the extraction time series for a specific method. If no method is provided, it will choose the highest ranking method based on the available methods.

        Parameters
        ----------
        extraction : pd.Series
            The extraction time series. It must contain a pd.DatetimeIndex. If the series is irregular, it will make it regular and pad the missing times with zero. Currently, only daily data is allowed as input.
        method : str or None
            The stream depletion method to use. It must be one of the available methods based on the input data. None will select the highest ranking method based on the available methods.

        Returns
        -------
        list
        """
        ## Preprocess the pd.Series
        if not isinstance(extraction.index, pd.DatetimeIndex):
            raise TypeError('extraction Series must have a DatetimeIndex.')

        extract1 = extraction.resample('D').mean().fillna(0)
        n_days1 = len(extract1)

        ## Calc the SD
        sd_ratios = np.array(self.calc_sd_ratios(n_days1, method))

        ## Make diff arrays
        extract2 = np.diff(extract1.values, prepend=0)
        extract3 = extract2.reshape(len(extract2), 1)

        sd_rate = extract3 * sd_ratios

        ## Add arrays together
        total_len = np.sum(sd_rate.shape)
        combo = np.zeros(total_len)

        for i, a in enumerate(sd_rate):
            combo[i:(i+n_days1)] = combo[i:(i+n_days1)] + a

        sd_rate3 = pd.Series(combo[:len(extract2)], index=extract1.index)

        return sd_rate3



























































