import numpy as np
import os
import argparse
import collections

import stylesheet
import precision_recall_scores as prs
import iotools
import get_plotvals

def parse_args():

    parser = argparse.ArgumentParser(description='Plot precision and recall of PIPs')

    parser.add_argument('--outfile',
                        type=str,
                        dest='outfile',
                        metavar='STR',
                        help='path of the output file')

    parser.add_argument('--whichplot',
                        nargs='*',
                        type=str,
                        dest='whichplot',
                        metavar='STR',
                        help='list of methods, allowed values: blore, finemap, probit, linear, jam, bimbam')

    parser.add_argument('--basedir',
                        type=str,
                        dest='basedir',
                        metavar='STR',
                        help='where to find the simulation directories')

    parser.add_argument('--locidir',
                        type=str,
                        dest='locidir',
                        metavar='STR',
                        help='where to find the loci directories')

    parser.add_argument('--locusfile',
                        type=str,
                        dest='locusfile',
                        metavar='STR',
                        help='file containing the locus prefixes to be analyzed')

    parser.add_argument('--start',
                        type=int,
                        dest='startsim',
                        metavar='INT',
                        help='starting simulation number')

    parser.add_argument('--end',
                        type=int,
                        dest='endsim',
                        metavar='INT',
                        help='last simulation number')

    parser.add_argument('--cmax',
                        type=int,
                        dest='cmax',
                        metavar='INT',
                        help='maximum number of causal SNPs allowed')


    parser.add_argument('--credible',
                        dest='use_credible',
                        action='store_true',
                        help='if set, ranks each locus separately')

    parser.add_argument('--inset',
                        dest='plot_inset',
                        action='store_true',
                        help='if set, plots the inset of logistic vs linear model from combined study')

    parser.add_argument('--thin',
                        default=5,
                        type=int,
                        dest='thinby',
                        metavar='INT',
                        help='factor to thin the scatterplot of logistic vs linear model')


    parser.add_argument('--legend',
                        dest='plot_legend',
                        action='store_true',
                        help='if set, plots the legend')


    opts = parser.parse_args()
    return opts


opts = parse_args()
locusfile = os.path.abspath(opts.locusfile)
outfile = os.path.abspath(opts.outfile)
basedir = os.path.abspath(opts.basedir)
locidir = os.path.abspath(opts.locidir)

if not os.path.exists(os.path.dirname(outfile)):
    os.makedirs(os.path.dirname(outfile))

locusprefixes = iotools.read_locusprefixes(locusfile)

res = collections.defaultdict(lambda:0)
for key in opts.whichplot:
    res[key] = list()

for sim in range(opts.startsim, opts.endsim + 1):
    simname = 'sim{:03d}'.format(sim)
    print ('Reading {:s}'.format(simname))
    simdir = os.path.join(basedir, simname)
    causal_snps_file = os.path.join(simdir, 'samples', 'causal.snplist')
    causal_rsids = iotools.read_causal_rsids(causal_snps_file)
    for key in opts.whichplot:
        thisres = iotools.read_simres(simdir, key, locusprefixes, causal_rsids, opts.cmax, '0')
        res[key].append(thisres)

nmax = 0
plotvals = collections.defaultdict(lambda:0)
for key in opts.whichplot:
    if opts.use_credible:
        data = list()
        for x in res[key]:
            data += x
    else:
        data = [[y for z in x for y in z] for x in res[key]]
    maxlen = max([len(x) for x in data])
    if maxlen > nmax:
        nmax = maxlen
    plotvals[key] = get_plotvals.precision_recall_threshold(data)

if opts.plot_inset:
    print('Reading data for logistic vs linear model inset')
    simname = 'sim{:03d}'.format(opts.startsim)
    simdir = os.path.join(basedir, simname)
    snplistfile = os.path.join(simdir, 'samples/G1/snps.effectsize')
    study = 'combined'
    phenodf = iotools.read_inset_data(locidir, simdir, snplistfile, locusprefixes, study)
else:
    phenodf = None

print ("Reading complete.")
xlim = [0, int(0.15 * nmax)]
ylim = [0, 0.9]
xtextpos = [xlim[1]/6, xlim[1] - (xlim[1] / 3)]
xticks = None
yticks = np.arange(0, 0.91, 0.1)

stylesheet.save_prcplot(outfile, plotvals, phenodf, xlim, ylim, xtextpos, xticks, yticks, opts.plot_legend, opts.plot_inset, opts.thinby)
