import numpy as np
import os
import pandas as pd
from sklearn import linear_model
from get_plotvals import LDResult

def read_simres(simdir, key, locusprefixes, causal_rsids, zmax, muvar):
    res = None
    #blore_path   = 'blore/meta_without_feature/zmax{:d}_mu{:s}_pi0.01_sig0.01/blore_meta_res/{:s}.res'
    blore_path   = 'blore/meta_without_feature/zmax{:d}_mu{:s}_pi0.01_sig0.01/blore_meta_res/{:s}.gen.res'
    #blore_path   = 'blore_reduced_summary/meta_without_feature/zmax{:d}_mu{:s}_pi0.01_sig0.01/blore_meta_res/{:s}.res'
    #blore_path   = 'blore_cvar/meta_without_feature/zmax{:d}_mu{:s}_pi0.01_sig0.01/blore_meta_res/{:s}.res'
    probit_path  = 'pimass/c{:d}_1e6_probit/output/{:s}.mcmc.txt'
    linear_path  = 'pimass/c{:d}_1e6_linear/output/{:s}.mcmc.txt'
    finemap_path = 'finemap/c{:d}/{:s}.snp'
    jam_path     = 'jam/{:s}.out'
    bimbam_path  = 'bimbam/c{:d}_logistic/output/{:s}.pip.txt'
    snptest_path = 'snptest/meta/{:s}.meta.out'
    #if key == 'blore':   res = blore  (simdir, blore_path,   locusprefixes, causal_rsids, zmax, muvar)
    #if key == 'finemap': res = finemap(simdir, finemap_path, locusprefixes, causal_rsids, zmax)
    if key == 'probit':  res = pimass (simdir, probit_path,  locusprefixes, causal_rsids, zmax)
    if key == 'linear':  res = pimass (simdir, linear_path,  locusprefixes, causal_rsids, zmax)
    if key == 'bimbam':  res = bimbam (simdir, bimbam_path,  locusprefixes, causal_rsids, zmax)
    if key == 'jam':     res = jam    (simdir, jam_path,     locusprefixes, causal_rsids)
    if key == 'snptest': res = snptest(simdir, snptest_path, locusprefixes, causal_rsids)
    if key.startswith('blore'):   res = blore  (simdir, blore_path,   locusprefixes, causal_rsids, zmax, muvar)
    if key.startswith('finemap'): res = finemap(simdir, finemap_path, locusprefixes, causal_rsids, zmax)
    return res


def read_locusprefixes(locusfile):
    with open(locusfile, 'r') as mfile:
        locusprefixes = mfile.readlines()
    locusprefixes = [x.strip() for x in locusprefixes]
    return locusprefixes


def read_causal_rsids(causal_snps_file):
    causal_rsid = dict()
    with open(causal_snps_file, 'r') as mfile:
        rsidlist = list()
        locus_name = ''
        for line in mfile:
            if line.startswith('#'):
                causal_rsid[locus_name] = rsidlist
            else:
                mline =  line.split()
                if mline[0].startswith('Causality'):
                    locus_name = mline[1]
                    rsidlist = list()
                else:
                    rsidlist.append(mline[0])
        causal_rsid[locus_name] = rsidlist
    return causal_rsid


def blore(simdir, filepath, locusprefixes, causal_rsids, zmax, muvar):
    thisres = list()
    for locus in locusprefixes:
        locusres = list()
        outfile = os.path.join(simdir, filepath.format(zmax, muvar, locus))
        causals = causal_rsids[locus]
        with open(outfile, 'r') as mfile:
            next(mfile)
            for mline in mfile:
                mline_split = mline.split()
                rsid = mline_split[0]
                prob = float(mline_split[4])
                causality = 1 if rsid in causals else 0
                mres = LDResult(locus = locus,
                                rsid = rsid,
                                stat = prob,
                                ld = 1,
                                causality = causality)
                locusres.append(mres)
        thisres.append(locusres)
    return thisres


def pimass(simdir, filepath, locusprefixes, causal_rsids, zmax):
    thisres = list()
    for locus in locusprefixes:
        locusres = list()
        outfile = os.path.join( simdir, filepath.format(zmax, locus))
        causals = causal_rsids[locus]
        with open(outfile, 'r') as mfile:
            next(mfile)
            for mline in mfile:
                mline_split = mline.split()
                rsid = mline_split[0].strip()
                prob = float(mline_split[3])
                causality = 1 if rsid in causals else 0
                mres = LDResult(locus = locus,
                                rsid = rsid,
                                stat = prob,
                                ld = 1,
                                causality = causality)
                locusres.append(mres)
        thisres.append(locusres)
    return thisres


def finemap(simdir, filepath, locusprefixes, causal_rsids, zmax):
    thisres = list()
    for locus in locusprefixes:
        locusres = list()
        outfile = os.path.join( simdir, filepath.format(zmax, locus))
        causals = causal_rsids[locus]
        with open(outfile, 'r') as mfile:
            next(mfile)
            for mline in mfile:
                mlinesplit = mline.split()
                rsid = mlinesplit[1]
                prob = float(mlinesplit[3])
                causality = 1 if rsid in causals else 0
                mres = LDResult(locus = locus,
                                rsid = rsid,
                                stat = prob,
                                ld = 1,
                                causality = causality)
                locusres.append(mres)
        thisres.append(locusres)
    return thisres


def jam(simdir, filepath, locusprefixes, causal_rsids):
    thisres = list()
    for locus in locusprefixes:
        locusres = list()
        outfile = os.path.join(simdir, filepath.format(locus))
        causals = causal_rsids[locus]
        with open(outfile, 'r') as mfile:
            next(mfile)
            for mline in mfile:
                mlinesplit = mline.split()
                rsid = mlinesplit[0]
                prob = float(mlinesplit[1])
                if prob == 0.0:
                    prob = np.nan
                causality = 1 if rsid in causals else 0
                mres = LDResult(locus = locus,
                                rsid = rsid,
                                stat = prob,
                                ld = 1,
                                causality = causality)
                locusres.append(mres)
        thisres.append(locusres)
    return thisres

def bimbam(simdir, filepath, locusprefixes, causal_rsids, zmax):
    thisres = list()
    for locus in locusprefixes:
        locusres = list()
        outfile = os.path.join(simdir, filepath.format(zmax, locus))
        causals = causal_rsids[locus]
        with open(outfile, 'r') as mfile:
            next(mfile)
            for mline in mfile:
                mlinesplit = mline.split()
                rsid = mlinesplit[0]
                prob = float(mlinesplit[1])
                causality = 1 if rsid in causals else 0
                mres = LDResult(locus = locus,
                                rsid = rsid,
                                stat = prob,
                                ld = 1,
                                causality = causality)
                locusres.append(mres)
        thisres.append(locusres)
    return thisres

def snptest(simdir, filepath, locusprefixes, causal_rsids):
    thisres = list()
    for locus in locusprefixes:
        locusres = list()
        outfile = os.path.join(simdir, filepath.format(locus))
        causals = causal_rsids[locus]
        with open(outfile, 'r') as mfile:
            for mline in mfile:
                if not mline.startswith('#') and not mline.startswith('chr'):
                    mlinesplit = mline.split()
                    rsid = mlinesplit[1]
                    pval = float(mlinesplit[5])
                    causality = 1 if rsid in causals else 0
                    mres = LDResult(locus = locus,
                                    rsid = rsid,
                                    stat = -np.log10(pval),
                                    ld = 1,
                                    causality = causality)
                    locusres.append(mres)
        thisres.append(locusres)
    return thisres

def read_inset_data(locidir, simdir, snplistfile, locusprefixes, study):
    phenofile = os.path.join(simdir, 'samples/{:s}/phenotypes.sample'.format(study))
    colnames = ['dum', 'missing', 'father', 'mother', 'sex', 'age', 'pheno']
    dropnames = ['dum', 'missing', 'father', 'mother']
    phenodf = pd.read_csv(phenofile, delimiter=' ', names = colnames, header=None, skiprows=2, index_col=0)
    phenodf.drop(dropnames, inplace=True, axis=1)
    
    colnames = ['beta']
    betadf = pd.read_csv(snplistfile, header=None, names=colnames, delimiter = '\t', index_col=0)
    betadf.index = [x.strip() for x in betadf.index.tolist()]
    
    colnames = ['ref', 'alt'] + phenodf.index.tolist()
    for l, locusprefix in enumerate(locusprefixes):
        dosagefile = os.path.join(locidir, '{:s}/{:s}.matgen'.format(study, locusprefix))
        dosage = pd.read_csv(dosagefile, header=None, names=colnames, delimiter=',', index_col=0)
        common_snps = [x for x in dosage.index.tolist() if x in betadf.index.tolist()]
        locusgt = dosage.loc[common_snps].drop(['ref', 'alt'], axis=1)
        if l == 0:
            gt = locusgt
        else:
            gt = gt.append(locusgt)
    
    mbeta = betadf.loc[gt.index.tolist()]
    phenodf['xval'] = np.dot(np.array(gt).T, (np.array(mbeta)))

    X = np.array(gt).T
    y = np.array(phenodf['pheno'])
    if phenodf['pheno'].isnull().any():
        ivalid = np.where(~np.isnan(y))[0]
        X = X[ivalid, :]
        y = y[ivalid]

    clf = linear_model.LogisticRegression(C=1e5)
    clf.fit(X, y)    
    ols = linear_model.LinearRegression()
    ols.fit(X, y)

    phenodf = phenodf.dropna(axis=0)
    phenodf['logistic_prob'] = clf.predict_proba(X)[:, 1]
    phenodf['linear_pred'] = ols.predict(X)
    return phenodf
