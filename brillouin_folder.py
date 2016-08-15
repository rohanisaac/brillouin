#!/usr/bin/env python
"""
description: Script for processing a folder of brillouin files, performing
peak fitting, plotting and computing brillouin shifts and outputing to a csv
file
author: Rohan Isaac
"""
import os
from brillouin import fit_file, plot_fit, calculate_shifts

# ----------------------------------------------------------------------------
# Set user defined variables here
spacing = 0.56  # cm
crossed = False  # case-sensitive
folder = 'sample_data'
# end user defined parameters
# ----------------------------------------------------------------------------

def process_folder(fol, spacing, crossed):
    folname = os.path.abspath(fol)
    out_file = open(os.path.join(folname, 'output.csv'), 'w')
    out_file.write("Filename, F1, u_F1, F2, u_F2, F3, u_F3, F4, u_F4, F_avg, u_F_avg\n")

    for f in os.listdir(folname):
        if f.endswith('.DAT'):
            fname = os.path.join(folname, f)

            a, b, c = fit_file(fname)
            plot_fit(a, b, c, fname[:-3]+'pdf', filename=f, spacing=spacing, crossed=crossed)
            f1, f2, f3, f4, favg = calculate_shifts(a, b, c, spacing=spacing, crossed=crossed)
            out_file.write("{},{},{},{},{},{},{},{},{},{},{}\n".format(f, f1.n, f1.s , f2.n, f2.s, f3.n, f3.s, f4.n, f4.s, favg.n, favg.s))
    out_file.write("\nFolder{}\nSpacing:{} cm\nCrossed:{}\n".format(fol, spacing, crossed))
    out_file.close()

def main():
    process_folder(folder, spacing, crossed)

if __name__ == '__main__':
    main()
