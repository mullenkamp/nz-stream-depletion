#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 10:10:20 2021

@author: mike
"""
import numpy as np
import math
from typing import Optional, List, Any, Union
from scipy.special import erfc, k0

############################################
### Parameters



############################################
### Functions



def q_4(t, K, epsilon, l):
    """
    This calculates the total flow depletion lost from a stream when a well abstracts a flow
    Q from a delayed-yield (semi-confined) aquifer. All input and output variables are
    dimensionless with the following definitions:
    Q_4=flow depletion/Q  t'=t*T/(S*L^2)  Lambda'=Lambda*L/T  Epsilon=S/Sigma  K=(K'/B')*L^2/T
    NOTE: Setting K'=0 for any value of epsilon gives the solution obtained by B.Hunt(1999)
    GROUND WATER,37(1),98-102 for either a completely confined or completely unconfined aquifer.

    """
    if t <= 0:
        q_4 = 0
    else:
        n = 8
        q_4 = 0
        for i in range(1, n + 1):
            q_4 = q_4 + stehcoef(i, n) * g_4(i * np.log(2) / t, K, epsilon, l)
        q_4 = q_4 * np.log(2) / t
    return q_4


def g_4(p, K, epsilon, l):
    m0 = np.sqrt(p * (p + K * (1 + epsilon)) / (p + epsilon * K))
    g_4 = l * np.e ** (-m0) / (p * (l + 2 * m0))
    return g_4


def stehcoef(i, n):
    """
    This calculates the coefficient c(i) in the Stehfest algorithm for Laplace transform inversion. The integer n must be even.

    """
    M = int(round(n / 2, 0))
    upperlimit = min([i, M])
    lowerlimit = int(math.floor((i + 1) / 2))
    stehcoef = 0
    for K in range(lowerlimit, upperlimit + 1):
        num = math.factorial(2 * K) * K ** M
        denom = math.factorial(M - K) * math.factorial(K) * math.factorial(K - 1) * math.factorial(
            i - K) * math.factorial(2 * K - i)
        stehcoef = stehcoef + num / denom
    stehcoef = stehcoef * (-1) ** (i + M)
    return stehcoef


def q_5(t, epsilon, K, x_0, Alpha):
    """

    """
    if t <= 0:
        q_5 = 0
    else:
        n = 6
        q_5 = 0
        for i in range(1, n + 1):
            q_5 = q_5 + stehcoef(i, n) * q_5_transform(i * np.log(2) / t, epsilon, K, x_0, Alpha)
        q_5 = q_5 * np.log(2) / t

    return q_5


def q_5_transform(p, epsilon, K, x_0, Alpha):
    """

    """
    M = np.sqrt(p * (p + K * (1 + epsilon)) / (p + epsilon * K))
    q_5_transform = Alpha * k0(M) / (p * (2 * np.pi + Alpha * k0(M * x_0)))

    return q_5_transform


def q_15(t, T_2, S_2, K, Lambda):
    """

    """
    if t <= 0:
        q_15 = 0
    else:
        n = 8
        q_15 = 0
        for i in range(1, n + 1):
            q_15 = q_15 + stehcoef(i, n) * g_15(i * np.log(2) / t, T_2, S_2, K, Lambda)
        q_15 = q_15 * np.log(2) / t

    return q_15


def g_15(p, T_2, S_2, K, Lambda):
    """

    """
    b11 = p + K
    b12 = K
    b22 = S_2 * p + K
    a = (b11 + b22 / T_2) / 2
    b = (b12**2 - b11 * b22) / T_2
    gamma1 = a + np.sqrt(a**2 + b)
    V1 = (b11 - gamma1) / b12
    L1 = 1 + T_2 * V1**2
    gamma2 = a - np.sqrt(a**2 + b)
    V2 = (b11 - gamma2) / b12
    L2 = 1 + T_2 * V2**2
    delta = np.sqrt(gamma1) * (np.sqrt(gamma2) + Lambda / L2) + np.sqrt(gamma2) * (np.sqrt(gamma1) + Lambda / L1)
    num = np.exp(-np.sqrt(gamma1)) * np.sqrt(gamma2) / L1 + np.exp(-np.sqrt(gamma2)) * np.sqrt(gamma1) / L2
    g_15 = (Lambda / p) * num / delta

    return g_15


def q_16(t, T_1, S_1, K, Lambda):
    """

    """
    if t <= 0:
        Q_16 = 0
    else:
        n = 8
        Q_16 = 0
        for i in range(1, n+1):
            Q_16 = Q_16 + stehcoef(i, n) * g_16(i * np.log(2) / t, T_1, S_1, K, Lambda)
        Q_16 = Q_16 * np.log(2) / t
        Q_16 = Q_16 * 2 * np.pi * Lambda

    return Q_16


def g_16(p, T_1, S_1, K, Lambda):
    """

    """
    b11 = p * S_1 + K
    b12 = -K
    b22 = p + K
    a = (b11 / T_1 + b22) / 2
    b = (b12 ** 2 - b11 * b22) / T_1
    gamma1 = a + np.sqrt(a ** 2 + b)
    V1 = (gamma1 * T_1 - b11) / b12
    L1 = T_1 + V1 ** 2
    beta1 = ((gamma1 * T_1 - b11) / b12) / (2 * np.pi * p)
    gamma2 = a - np.sqrt(a ** 2 + b)
    V2 = (gamma2 * T_1 - b11) / b12
    L2 = T_1 + V2 ** 2
    beta2 = ((gamma2 * T_1 - b11) / b12) / (2 * np.pi * p)
    delta = 4 * np.sqrt(gamma1 * gamma2) + 2 * Lambda * (np.sqrt(gamma1) / L2 + np.sqrt(gamma2) / L1)
    a1 = ((Lambda / L2 + 2 * np.sqrt(gamma2)) * beta1 * np.exp(-np.sqrt(gamma1)) - Lambda * beta2 * np.exp(-np.sqrt(gamma2)) / L2) / (L1 * delta)
    a2 = ((Lambda / L1 + 2 * np.sqrt(gamma1)) * beta2 * np.exp(-np.sqrt(gamma2)) - Lambda * beta1 * np.exp(-np.sqrt(gamma1)) / L1) / (L2 * delta)
    g_16 = a1 + a2

    return g_16


def theis_1941(n_days, pump_aq_trans, pump_aq_s, sep_distance):
    """
    This is the Theis (1941) solution using the complementary error function derived by Glover and Balmer (1954).

    Parameters
    ----------
    n_days : int
        The number of pumping days.
    pump_aq_trans : int
        The pumped aquifer transmissivity (m2/day).
    pump_aq_s : float
        The storage coefficient of the pumped aquifer.
    sep_distance : int
        The separation distance from the pumped well to the stream.

    Returns
    -------
    float
        Stream depletion ratio
    """
    sdf = (sep_distance ** 2) * pump_aq_s / pump_aq_trans
    per = erfc(np.sqrt(sdf / (4 * n_days)))
    return per


def hunt_1999(n_days, pump_aq_trans, pump_aq_s, stream_k, stream_thick, stream_width, sep_distance):
    """
    This is the Hunt (1999) solution for stream depletion in a stream that partially penetrates an aquifer.

    Parameters
    ----------
    n_days : int
        The number of pumping days.
    pump_aq_trans : int
        The pumped aquifer transmissivity (m2/day).
    pump_aq_s : float
        The storage coefficient of the pumped aquifer.
    stream_k : int
        Streambed hydraulic conductivity (m/day).
    stream_thick : int
        The streambed vertical thickness (m).
    stream_width : int
        The streambed width (m).
    sep_distance : int
        The separation distance from the pumped well to the stream.

    Returns
    -------
    float
        Stream depletion ratio
    """
    stream_cond = stream_k * stream_width / stream_thick
    t = n_days * pump_aq_trans / (pump_aq_s * sep_distance**2)
    epsilon = pump_aq_s / 0.1
    stream_cond2 = stream_cond * sep_distance / pump_aq_trans
    output = q_4(t, 0, epsilon, stream_cond2)

    return output


def hunt_2003(n_days, pump_aq_trans, pump_aq_s, aqt_k, aqt_thick, aqt_s, stream_k, stream_thick, stream_width, sep_distance):
    """
    The Hunt (2003) solution builds upon the Hunt (1999) solution by adding a lower hydraulic conductivity layer (aquitard) above the pumped aquifer.

    Parameters
    ----------
    n_days : int
        The number of pumping days.
    pump_aq_trans : int
        The pumped aquifer transmissivity (m2/day).
    pump_aq_s : float
        The storage coefficient of the pumped aquifer.
    aqt_k : int
        The aquitard hydraulic conductivity (m/day).
    aqt_thick : int
        The aquitard vertical thickness (m).
    aqt_s : float
        The aquitard storage coefficient.
    stream_k : int
        Streambed hydraulic conductivity (m/day).
    stream_thick : int
        The streambed vertical thickness (m).
    stream_width : int
        The streambed width (m).
    sep_distance : int
        The separation distance from the pumped well to the stream.

    Returns
    -------
    float
        Stream depletion ratio
    """
    stream_cond = stream_k * stream_width / stream_thick
    k_b = aqt_k / aqt_thick
    t = n_days * pump_aq_trans / (pump_aq_s * sep_distance**2)
    k = k_b * sep_distance**2 / pump_aq_trans
    epsilon = pump_aq_s / aqt_s
    stream_cond2 = stream_cond * sep_distance / pump_aq_trans
    output = q_4(t, k, epsilon, stream_cond2)

    return output


def hunt_2009(n_days, pump_aq_trans, pump_aq_s, lower_aq_trans, lower_aq_s, aqt_k, aqt_thick, stream_k, stream_thick, stream_width, sep_distance):
    """
    The Hunt (2009) solution builds upon the Hunt (1999) solution by adding an aquitard directly below the pumped surfical aquifer and a confined aquifer below the aquitard.

    Parameters
    ----------
    n_days : int
        The number of pumping days.
    pump_aq_trans : int
        The pumped aquifer transmissivity (m2/day).
    pump_aq_s : float
        The storage coefficient of the pumped aquifer.
    lower_aq_trans: int
        The confined aquifer transmissivity (m2/day).
    lower_aq_s : float
        The storage coefficient (specific storage) of the confined aquifer.
    aqt_k : int
        The aquitard hydraulic conductivity (m/day).
    aqt_thick : int
        The aquitard vertical thickness (m).
    stream_k : int
        Streambed hydraulic conductivity (m/day).
    stream_thick : int
        The streambed vertical thickness (m).
    stream_width : int
        The streambed width (m).
    sep_distance : int
        The separation distance from the pumped well to the stream.

    Returns
    -------
    float
        Stream depletion ratio
    """
    stream_cond = stream_k * stream_width / stream_thick
    k_b = aqt_k / aqt_thick
    t = n_days * pump_aq_trans / (pump_aq_s * sep_distance**2)
    t_2 = lower_aq_trans/pump_aq_trans
    s_2 = lower_aq_s/pump_aq_s
    k = k_b * (sep_distance**2) / pump_aq_trans
    stream_cond2 = stream_cond * sep_distance / pump_aq_trans

    ratio = q_15(t, t_2, s_2, k, stream_cond2)

    return ratio


def ward_lough_2011(n_days, pump_aq_trans, pump_aq_s, upper_aq_trans, upper_aq_s, aqt_k, aqt_thick, stream_k, stream_thick, stream_width, sep_distance):
    """
    The Ward and Lough (2011) solution is conceptually very similar to the Hunt (2009) solution except that the pumped aquifer is the confined aquifer.

    Parameters
    ----------
    n_days : int
        The number of pumping days.
    pump_aq_trans : int
        The pumped (confined) aquifer transmissivity (m2/day).
    pump_aq_s : float
        The storage coefficient of the pumped aquifer.
    upper_aq_trans: int
        The surficial aquifer transmissivity (m2/day).
    upper_aq_s : float
        The storage coefficient of the surficial aquifer.
    aqt_k : int
        The aquitard hydraulic conductivity (m/day).
    aqt_thick : int
        The aquitard vertical thickness (m).
    stream_k : int
        Streambed hydraulic conductivity (m/day).
    stream_thick : int
        The streambed vertical thickness (m).
    stream_width : int
        The streambed width (m).
    sep_distance : int
        The separation distance from the pumped well to the stream.

    Returns
    -------
    float
        Stream depletion ratio
    """
    stream_cond = stream_k * stream_width / stream_thick
    k_b = aqt_k / aqt_thick
    t = n_days * pump_aq_trans / (pump_aq_s * sep_distance**2)
    t_1 = upper_aq_trans/pump_aq_trans
    s_1 = upper_aq_s/pump_aq_s
    k = k_b * (sep_distance**2) / pump_aq_trans
    stream_cond2 = stream_cond * sep_distance / pump_aq_trans

    ratio = q_16(t, t_1, s_1, k, stream_cond2)

    return ratio
