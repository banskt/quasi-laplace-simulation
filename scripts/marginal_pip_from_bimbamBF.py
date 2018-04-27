import numpy as np
import os
import collections
import argparse

INFO_FIELDS = ['cstates', 'bfcomp']
class BFResult(collections.namedtuple('_BFResult', INFO_FIELDS)):
    __slots__ = ()

def parse_args():

    parser = argparse.ArgumentParser(description='Calculate PIPs from the BIMBAM output')

    parser.add_argument('-o', '--outdir',
                        type=str,
                        dest='outdir',
                        metavar='DIR',
                        help='BIMBAM output directory')

    parser.add_argument('-l', '--locusprefix',
                        type=str,
                        dest='locusprefix',
                        metavar='STR',
                        help='prefix of locusname')

    parser.add_argument('-p', '--modelpi',
                        type=float,
                        dest='modelpi',
                        metavar='real',
                        help='Pi obtained from B-LORE for this locus')


    opts = parser.parse_args()
    return opts


opts = parse_args()
outdir = opts.outdir
locusprefix = opts.locusprefix
model_pi = opts.modelpi

# Read the rsid and log10BFs from BIMBAM summary file
summaryfile = os.path.join(outdir, locusprefix + '.summary.txt')
log10bflist = list()
rsidlist = list()
with open(summaryfile, 'r') as mfile:
    for i in range(13):
        next(mfile)
    for mline in mfile:
        if mline.startswith('##') or mline.startswith('\n'): 
            break
        else:
            mlinesplit = mline.split()
            rsid = mlinesplit[0].strip()
            log10bfs = [float(x.strip()) for x in mlinesplit[1:]]
            log10bflist.append(log10bfs)
            rsidlist.append(rsid)
log10bfmat = np.array(log10bflist)

# Calculate the priors for each model
nsnps = len(rsidlist)
model_log10prior_c0 = 0 * np.log10(model_pi) + (nsnps - 0) * np.log10(1 - model_pi)
model_log10prior_c1 = 1 * np.log10(model_pi) + (nsnps - 1) * np.log10(1 - model_pi)
model_log10prior_c2 = 2 * np.log10(model_pi) + (nsnps - 2) * np.log10(1 - model_pi)

# Calculate the likelihood of each model

res = list()

# Model with 0 SNP:
stat = 0 + model_log10prior_c0
model = list([])
thisres = BFResult(bfcomp = stat, cstates = model)
res.append(thisres)
# Models with 1 SNP
for i in range(nsnps):
    stat = log10bfmat[i,i] + model_log10prior_c1
    model = list([rsidlist[i]])
    thisres = BFResult(bfcomp = stat, cstates = model)
    res.append(thisres)
# Models with 2 SNPs
for i in range(nsnps - 1):
    for j in range(i+1, nsnps):
        stat = log10bfmat[i,j] + model_log10prior_c2
        model = list([rsidlist[i], rsidlist[j]])
        thisres = BFResult(bfcomp = stat, cstates = model)
        res.append(thisres)

bfcomps = np.array([x.bfcomp for x in res])
probsum_all_models = np.sum(np.power(10, bfcomps))

pip = collections.defaultdict(lambda:0)
for i, rsid in enumerate(rsidlist):
    bfcomps_rsid = [x.bfcomp for x in res if rsid in x.cstates]
    probsum_rsid = np.sum(np.power(10, bfcomps_rsid))
    pip[rsid] = probsum_rsid / probsum_all_models

pipfile = os.path.join(outdir, locusprefix + '.pip.txt')
with open(pipfile, 'w') as mfile:
    mfile.write('rsid\tPIP\n')
    for rsid in rsidlist:
        mfile.write('{:s}\t{:f}\n'.format(rsid, pip[rsid]))
