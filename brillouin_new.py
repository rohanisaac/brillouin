#!/usr/bin/env python

"""
Brillouin peak fitting script

Author: Rohan Isaac
Description: Splits Brillouin data, fits elastic and inelastic peaks
separately, all with lorentzians
"""
import numpy as np
import matplotlib.pyplot as plt
import spectra as sp
import os

# ---------------------------------------------------------------------------
# Start user defined parameters

spacing = 0.54
crossed = True

# End user defined parameters
# ---------------------------------------------------------------------------

# load folder
folname = os.path.abspath('sample_data')

# x data always the same
x = np.arange(256)

def oc(obj, peak):
    """Return center of peak in object"""
    return obj.loc['p%s_center' % peak, 'value']

def copy_range(x, y, xmin, xmax):
    """Copy a subrange"""
    r1 = np.argmin(np.abs(x-xmin))
    r2 = np.argmin(np.abs(x-xmax))
    # print r1,r2
    if r1 < r2:
        return x[r1:r2], y[r1:r2]
    elif r1 > r2:
        return x[r2:r1], y[r2:r1]
    else:
        print "Error, no subrange"
        return

for f in os.listdir(folname):
    if f.endswith('.DAT'):
        # full file name
        full_name = os.path.join(folname, f)

        # remove extenstion
        base_name = f.split('.')[0]

        # make sub folder
        sub_path = os.path.join(folname, base_name)
        if not os.path.exists(sub_path):
            os.makedirs(sub_path)

        # get data
        y = np.genfromtxt(full_name, skip_header=12)

        # extract inelastic ranges
        b1x, b1y = copy_range(x, y, 21, 110) # don't really need this
        b2x, b2y = copy_range(x, y, 146, 235)

        # fit elastic data assuming laser peak positions
        l = sp.Spectra(x, y)
        l.peak_pos = [4, 127, 253]
        l.num_peaks = 3
        l.build_model(bg_ord=0)
        l.fit_data()
        l.output_results()

        # inelastic range 1
        b1 = sp.Spectra(b1x, b1y)
        b1.smooth_data(window_size=5, order=3)
        b1.find_peaks(width=5, threshold=0, limit=4, smooth=True)
        b1.build_model(bg_ord=0)
        b1.fit_data()
        b1.output_results()

        # inelastic range 2
        b2 = sp.Spectra(b2x, b2y)
        b2.smooth_data(window_size=5, order=3)
        b2.find_peaks(width=5, threshold=0, limit=4, smooth=True)
        b2.build_model(bg_ord=0)
        b2.fit_data()
        b2.output_results()

        las = l.output_results(pandas=True)
        br1 = b1.output_results(pandas=True)  # should be sorted?
        br2 = b2.output_results(pandas=True)

        # note all br fits have 4 peaks, only 2 center are relevant
        # differences between laser and brillouin peaks
        if crossed:
            # (l_0) b1_1 b1_2 (l_1) b2_1 b2_2 (l_2)
            sh = [oc(br1, 2) - oc(las, 0),
                  oc(las, 1) - oc(br1, 1),
                  oc(br2, 2) - oc(las, 1),
                  oc(las, 2) - oc(br2, 1)
                  ]
        else:
            # (l_0) b1_1 b1_2 (l_1) b2_1 b2_2 (l_2)
            sh = [oc(br1, 1) - oc(las, 0),
                  oc(las, 1) - oc(br1, 2),
                  oc(br2, 1) - oc(las, 1),
                  oc(las, 2) - oc(br2, 2)
                  ]

        fsr = 1.0 / (2.0 * spacing)
        freqsh = [(fsr / 256.0) * (s) for s in sh]
        freqs = [str(s) for s in freqsh]
        # wfil.write(f + ',')  # filename
        # wfil.write(",".join(freqs))  # frequencies
        # wfil.write('\n')
        # print freqsh
        l.output_results()
        b1.output_results()
        b2.output_results()

# wfil.close()
