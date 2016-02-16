from __future__ import division
import numpy as np
import re
import os
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal


def wl2wn(wl):
    """Converts wavelength (nm) to wavenumber (1/cm)"""
    return (10.0**7)/wl


def wn2wl(wn):
    """Converts wavenumber (1/cm) to wavelength (nm)"""
    return (10.0**7)/wn


# copy range from x,y data based on x values
def copy_range(x, y, xmin, xmax):
    r1 = np.argmin(abs(x-xmin))
    r2 = np.argmin(abs(x-xmax))
    # print r1,r2
    if r1 < r2:
        return x[r1:r2], y[r1:r2]
    elif r1 > r2:
        return x[r2:r1], y[r2:r1]
    else:
        print "Error, no subrange"


# write two column data to file:
def write2col(fname, x, y, delim='\t'):
    if not os.path.exists(os.path.dirname(fname)):
        os.makedirs(os.path.dirname(fname))
    with open(fname, 'w') as f:
        for xi, yi in zip(x, y):
            f.write("%s%s%s\n" % (xi, delim, yi))
    return


def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)


def brillouin_getxy(fname):
    x = np.arange(256)
    y = np.genfromtxt(fname, skiprows=12)
    return x, y


def find_nearest(array, value):
    idx = (np.abs(array-value)).argmin()
    return array[idx]


def find_nearest_index(array, value):
    """Returns the position(s) of the point(s) in the list closes to the
    passed point"""
    return (np.abs(array-value)).argmin()

