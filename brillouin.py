"""
description: functions to automate peak fitting, plotting and outputting fit
values to brillouin data
author: Rohan Isaac
"""

import numpy as np
import matplotlib.pyplot as plt
import spectra as sp
from uncertainties import ufloat

def fit_file(fname):
    """Fit file including three subsections, and return the three fit objects"""
    x = np.arange(256)
    y = np.genfromtxt(fname, skip_header=12)

    # fit the main peaks first
    l = sp.Spectra(x, y)
    l.peak_pos = [4, 127, 253]
    l.num_peaks = 3
    l.build_model(bg_ord=0)
    l.fit_data()

    # extract inelastic ranges
    b1x = x[21:110]
    b1y = y[21:110]
    b2x = x[146:235]
    b2y = y[146:235]

    # inelastic range 1
    b1 = sp.Spectra(b1x, b1y)
    b1.smooth_data(window_size=5, order=3)
    b1.find_peaks(width=5, threshold=0, limit=4, smooth=True)
    b1.build_model(bg_ord=0)
    b1.fit_data()

    # inelastic range 2
    b2 = sp.Spectra(b2x, b2y)
    b2.smooth_data(window_size=5, order=3)
    b2.find_peaks(width=5, threshold=0, limit=4, smooth=True)
    b2.build_model(bg_ord=0)
    b2.fit_data()

    return l, b1, b2


def plot_fit(l, b1, b2, save_path):
    fig, ax = plt.subplots(figsize=(12,4))
    plt.step(b1.x,b1.y,'b')
    plt.step(b2.x,b2.y,'b', label='data')
    plt.plot(b1.x,b1.out.best_fit,'r', lw=2)
    plt.plot(b2.x,b2.out.best_fit,'r', lw=2, label='fit')
    #for i in [4, 127, 253]:
    #    plt.axvline(i, color='gray', lw=5)
    plt.xlim(0,256)
    plt.ylim(0,96)
    plt.legend()
    plt.xticks(np.arange(0,257,32))
    plt.yticks(np.arange(0,127,32))
    fig.savefig(save_path)

def full_param(fit_obj, fit_param):
    p = fit_obj.out.params[fit_param]
    return ufloat(p.value, p.stderr)

def calculate_shifts(a, b, c, d=0.56, crossed=False):
    """
    Assuming spectra is of the form:
    L1 P1 P2 L2 P3 P4 L3
    """

    l1 = full_param(a, 'p0_center')
    l2 = full_param(a, 'p1_center')
    l3 = full_param(a, 'p2_center')
    p1 = full_param(b, 'p1_center')
    p2 = full_param(b, 'p2_center')
    p3 = full_param(c, 'p1_center')
    p4 = full_param(c, 'p2_center')

    fsr_icm = 1/(2*d)  # 1/cm
    fsr_ch = (l3 - l1)/2  # ch

    wn_ch = fsr_icm/fsr_ch

    if not crossed:
        f1 = wn_ch * (p1-l1)
        f2 = wn_ch * (l2-p2)
        f3 = wn_ch * (p3-l2)
        f4 = wn_ch * (l3-p4)
    else:
        f1 = wn_ch * (p2-l1)
        f2 = wn_ch * (l2-p1)
        f3 = wn_ch * (p4-l2)
        f4 = wn_ch * (l3-p3)

    return f1, f2, f3, f4, (f1 + f2 + f3 + f4)/4
