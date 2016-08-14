#!/usr/bin/env python

"""
description: Brillouin peak fitting script
author: Rohan Isaac
"""
import os
from brillouin import fit_file, plot_fit, calculate_shifts

# ----------------------------------------------------------------------------
# Set user defined variables here
spacing = 0.56  # cm
crossed = False  # case-sensitive
# end user defined parameters
# ----------------------------------------------------------------------------

folname = os.path.abspath('sample_data')
out_file = open(os.path.join(folname, 'output.csv'), 'w')
out_file.write("Filename, F1, F2, F3, F4, F_avg\n")

for f in os.listdir(folname):
    if f.endswith('.DAT'):
        fname = os.path.join(folname, f)

        a, b, c = fit_file(fname)
        plot_fit(a, b, c, fname[:-3]+'pdf')
        f1, f2, f3, f4, favg = calculate_shifts(a, b, c, d=0.56, crossed=False)
        out_file.write("{},{},{},{},{},{}\n".format(f, f1, f2, f3, f4, favg))

out_file.close()
