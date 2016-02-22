#!/usr/bin/env python
# Brillouin peak fitting script
# -----------------------------
# author: Rohan Isaac
#
# Splits data, fits elastic and inelastic peaks separately, all with Lorentzian
from argparse
import os
import sys
import numpy as np
import matplotlib
matplotlib.use('TkAgg')  # otherwise tk stuff crashes
import matplotlib.pyplot as plt
sp = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'spectra'))
sys.path.append(sp)
import spectra as sp
import all_functions as af


def plotfit(obj, ndir, fname):
    fig = plt.figure()
    fig.clear()
    # fig.set_size_inches(11, 8.5)
    obj.out.plot_fit()
    plt.title(fname.replace('_', ' ').title()[:-4])
    plt.xlim(min(obj.x), max(obj.x))
    plt.savefig(ndir + fname)
    plt.close()


def main():
    parser = argparse.ArgumentParser(description='Brillouin processing script')
    parser.add_argument(
        'input_dir',
        help='Input directory containing .DAT files from brillouin system')
    parser.add_argument(
        'spacing',
        help='Spacing of FabryPerot (cm)',
        type=float, default='0.54')
    parser.add_argument(
        '-c', '--crossed',
        help='Brillouin peaks are crossed',
        action='store_true', default=False)
    args = parser.parse_args()

    print args
    print args.input_dir, args.spacing, args.crossed
    print type(args.spacing)

    exit()
    spacing = args.spacing
    folname = args.input_dir
    crossed = args.crossed

    # redirect output to log file
    # sys.stdout = open(folname + '/output.txt', 'w')
    wfil = open(folname + '/output.csv', 'w')
    for f in os.listdir(folname):
        fname = folname + '/' + f
        if os.path.isdir(fname):
            continue
        if not (f.endswith('DAT')):
            continue
        # create a subfolder for all output
        bdir, fil = os.path.split(fname)
        filx = fil.split('.')[0]
        ndir = bdir + '/' + filx + '/'
        if not os.path.exists(ndir):
            os.makedirs(ndir)

        # redirect all console out to log file
        sys.stdout = open(ndir + 'output.txt', 'w')
        print(fname)

        # get data
        x = np.arange(256)
        y = np.genfromtxt(fname, skip_header=12)

        # extract inelastic ranges
        b1x, b1y = af.copy_range(x, y, 21, 110)
        b2x, b2y = af.copy_range(x, y, 146, 235)

        # fit elastic data assuming laser peak positions
        l = sp.Spectra(x, y)
        l.peak_pos = [4, 127, 253]
        l.num_peaks = 3
        l.build_model(bg_ord=0)
        l.fit_data()
        l.output_results()

        plotfit(l, ndir, 'elastic_fit.pdf')

        # inelastic range 1
        b1 = sp.Spectra(b1x, b1y)
        b1.find_peaks(width=5, threshold=20, limit=4)
        b1.build_model(bg_ord=0)
        b1.fit_data()
        b1.output_results()

        plotfit(b1, ndir, 'inelastic1_fit.pdf')

        # inelastic range 2
        b2 = sp.Spectra(b2x, b2y)
        b2.find_peaks(width=5, threshold=20, limit=4)
        b2.build_model(bg_ord=0)
        b2.fit_data()
        b2.output_results()

        plotfit(b2, ndir, 'inelastic2_fit.pdf')

        las = l.output_results(pandas=True)
        br1 = b1.output_results(pandas=True)  # should be sorted?
        br2 = b2.output_results(pandas=True)

        def oc(obj, peak):
            """Return center of peak in object"""
            return obj.loc['p%s_center' % peak, 'value']

        # note all br fits have 4 peaks, only 2 center are relevant
        # differences between laser and brillouin peaks
        if crossed:
            # (l_0) b1_1 b1_2 (l_1) b2_1 b2_2 (l_2)
            sh = [
                  oc(br1, 2) - oc(las, 0),
                  oc(las, 1) - oc(br1, 1),
                  oc(br2, 2) - oc(las, 1),
                  oc(las, 2) - oc(br2, 1)
            ]
        else:
            # (l_0) b1_1 b1_2 (l_1) b2_1 b2_2 (l_2)
            sh = [
                  oc(br1, 1) - oc(las, 0),
                  oc(las, 1) - oc(br1, 2),
                  oc(br2, 1) - oc(las, 1),
                  oc(las, 2) - oc(br2, 2)
            ]

        fsr = 1.0 / (2.0 * spacing)
        freqsh = [(fsr / 256.0) * (s) for s in sh]
        freqs = [str(s) for s in freqsh]
        wfil.write(f + ',')  # filename
        wfil.write(",".join(freqs))  # frequencies
        wfil.write('\n')
        # print freqsh
        l.output_results()
        b1.output_results()
        b2.output_results()

    wfil.close()

if __name__ == '__main__':
    main()
