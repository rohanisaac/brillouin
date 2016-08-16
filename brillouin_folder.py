#!/usr/bin/env python
"""
description: Script for processing a folder of brillouin files, performing
peak fitting, plotting and computing brillouin shifts and outputing to a csv
file
author: Rohan Isaac
"""
import os
from brillouin import fit_file, plot_fit, calculate_shifts, peak_widths

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

    # write header (shifts, avg, peak_widths (laser and brillouin))
    out_file.write("Filename,")
    out_file.write("".join(["F{0},u_F{0},".format(i) for i in range(1, 5)]))
    out_file.write("F_avg,u_F_avg,")
    out_file.write("".join(["l{0},u_l{0},".format(i) for i in range(1, 4)]))
    out_file.write("".join(["b{0},u_b{0},".format(i) for i in range(1, 5)]))
    out_file.write("\n")

    for f in os.listdir(folname):
        if f.endswith('.DAT'):
            fname = os.path.join(folname, f)

            a, b, c = fit_file(fname)
            plot_fit(a, b, c, fname[:-3] + 'pdf',
                     filename=f, spacing=spacing, crossed=crossed)
            shifts = calculate_shifts(
                a, b, c, spacing=spacing, crossed=crossed)
            fwhms = peak_widths(a, b, c)
            out_file.write(f+',')
            out_file.write(
                "".join(["{},{},".format(a.n, a.s) for a in shifts]))
            out_file.write("".join(["{},{},".format(a.n, a.s) for a in fwhms]))
            out_file.write("\n")
    out_file.write("\nFolder{}\nSpacing:{} cm\nCrossed:{}\n".format(
        fol, spacing, crossed))
    out_file.close()


def main():
    process_folder(folder, spacing, crossed)

if __name__ == '__main__':
    main()
