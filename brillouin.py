"""
description: functions to automate peak fitting, plotting and outputting fit
values to brillouin data
author: Rohan Isaac
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import spectra as sp
from uncertainties import ufloat


def par_val(fit_obj, fit_param):
    p = fit_obj.out.params[fit_param]
    return p.value


def full_param(fit_obj, fit_param):
    p = fit_obj.out.params[fit_param]
    return ufloat(p.value, p.stderr)


def fit_file(fname):
    """
    Fit a single file in three sections, and return the three fit objects
    """
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


def plot_fit(l, b1, b2, save_path, filename, spacing=0.56, crossed=False):
    arr_height = 85

    # compute the plain values, no uncertainties
    l1 = par_val(l, 'p0_center')
    l2 = par_val(l, 'p1_center')
    l3 = par_val(l, 'p2_center')
    p1 = par_val(b1, 'p1_center')
    p2 = par_val(b1, 'p2_center')
    p3 = par_val(b2, 'p1_center')
    p4 = par_val(b2, 'p2_center')

    fsr_icm = 1 / (2 * spacing)  # 1/cm
    fsr_ch = (l3 - l1) / 2  # ch

    wn_ch = fsr_icm / fsr_ch

    if not crossed:
        f1 = wn_ch * (p1 - l1)
        f2 = wn_ch * (l2 - p2)
        f3 = wn_ch * (p3 - l2)
        f4 = wn_ch * (l3 - p4)
    else:
        f1 = wn_ch * (p2 - l1)
        f2 = wn_ch * (l2 - p1)
        f3 = wn_ch * (p4 - l2)
        f4 = wn_ch * (l3 - p3)

    fig, ax = plt.subplots(figsize=(12, 4))

    # data
    plt.step(b1.x, b1.y, 'b')
    plt.step(b2.x, b2.y, 'b')

    # fits
    plt.plot(b1.x, b1.out.best_fit, 'r', lw=2)
    plt.plot(b2.x, b2.out.best_fit, 'r', lw=2)

    # brillouin peaks
    for i in [p1, p2, p3, p4]:
        plt.axvline(i, color='gray', ls='--', lw=1, alpha=0.5)
        # plt.text(i-4, 15, "{0:.2f}".format(i), rotation='vertical')

    # laser peaks
    for i in [l1, l2, l3]:
        plt.axvline(i, color='gray', ls='-', lw=3, alpha=1)
        # plt.text(i-4, 15, "{0:.2f}".format(i), rotation='vertical')

    # set plot limits
    plt.xlim(0, 256)
    plt.ylim(0, 96)

    # remove all but bottom axis
    plt.xticks(np.arange(0, 257, 32))
    plt.yticks([])
    ax.spines["left"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.xaxis.set_ticks_position('bottom')

    if not crossed:
        for pa, pb in [(l1, p1), (l2, p2), (l2, p3), (l3, p4)]:
            ax.annotate("",
                        xy=(pa, arr_height), xycoords='data',
                        xytext=(pb, arr_height), textcoords='data',
                        arrowprops=dict(arrowstyle="<|-|>",
                                        connectionstyle="arc3", color='gray',
                                        alpha=0.7),
                        )
        for pos, val in zip([30, 80, 155, 205], [f1, f2, f3, f4]):
            plt.text(pos, arr_height + 3, "{0:.3f}/cm".format(val))
    else:  # crossed
        # plot offset
        for pa, pb in [(l1, p2), (l2, p4)]:
            ax.annotate("",
                        xy=(pa, arr_height + 10), xycoords='data',
                        xytext=(pb, arr_height + 10), textcoords='data',
                        arrowprops=dict(arrowstyle="<|-|>",
                                        connectionstyle="arc3", color='gray',
                                        alpha=0.7),
                        )
        for pa, pb in [(l2, p1), (l3, p3)]:
            ax.annotate("",
                        xy=(pa, arr_height), xycoords='data',
                        xytext=(pb, arr_height), textcoords='data',
                        arrowprops=dict(arrowstyle="<|-|>",
                                        connectionstyle="arc3", color='gray',
                                        alpha=0.7),
                        )
        for pos, val in zip([30, 80, 155, 205], [f1, f2, f3, f4]):
            plt.text(pos, arr_height + 3, "{0:.3f}/cm".format(val))

    handles = [mlines.Line2D([], [], ls='--', c='gray', lw=1,
                             label='Brillouin peak'),
               mlines.Line2D([], [], ls='-', c='gray',
                             lw=2, label='Laser peak'),
               mlines.Line2D([], [], ls='-', c='blue', lw=1, label='Raw data'),
               mlines.Line2D([], [], ls='-', c='red', lw=2, label='Best fit')]

    ax.set_position([0.05, 0.2, 0.9, 0.6])
    plt.xlabel('Channel number')
    title = 'Filename: {}, Spacing: {:.2} cm, {:.5f} wn/ch'.format(filename,
                                                                   spacing,
                                                                   wn_ch)
    plt.title(title, y=-0.30, bbox=dict(facecolor='gray', alpha=0.3))
    plt.legend(handles=handles, loc='lower center',
               bbox_to_anchor=(0.5, 1.05), ncol=4)
    if save_path is None:
        return fig
    else:
        fig.savefig(save_path)
        return


def calculate_shifts(a, b, c, spacing=0.56, crossed=False):
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

    fsr_icm = 1 / (2 * spacing)  # 1/cm
    fsr_ch = (l3 - l1) / 2  # ch

    wn_ch = fsr_icm / fsr_ch

    if not crossed:
        f1 = wn_ch * (p1 - l1)
        f2 = wn_ch * (l2 - p2)
        f3 = wn_ch * (p3 - l2)
        f4 = wn_ch * (l3 - p4)
    else:
        f1 = wn_ch * (p2 - l1)
        f2 = wn_ch * (l2 - p1)
        f3 = wn_ch * (p4 - l2)
        f4 = wn_ch * (l3 - p3)

    return f1, f2, f3, f4, (f1 + f2 + f3 + f4) / 4
