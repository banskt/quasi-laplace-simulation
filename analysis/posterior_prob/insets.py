import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

import matplotlib
matplotlib.rc('text', usetex=True)
matplotlib.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
import matplotlib.pyplot as plt

def add_vert(fig, ax, hfrac, vfrac, hoffset, voffset, ratios):

    bbox = ax.get_position()
    axleft = bbox.x0
    axwidth = bbox.width
    axbottom = bbox.y0
    axheight = bbox.height

    iax_left   = axleft   + hoffset * axwidth
    iax_bottom = axbottom + voffset * axheight
    iax_width  = hfrac * axwidth
    iax_height = [(vfrac / sum(ratios)) * x * axheight for x in ratios]

    iax = [None for x in ratios]
    for i, x in enumerate(ratios):
        iax[i] = fig.add_axes([iax_left, iax_bottom, iax_width, iax_height[i]])
        iax_bottom += iax_height[i]
    
    return iax

def visual_aid(data, xvals, nbins = 10):  
    bins = np.percentile(data, np.linspace(0, 100, nbins + 1))
    binidx = np.digitize(data, bins)
    x = np.zeros(nbins)
    y = np.zeros(nbins)
    for i in range(nbins):
        xsplit = xvals[np.where(binidx == i + 1)]
        ysplit = data[np.where(binidx == i + 1)]
        x[i] = np.median(xsplit)
        y[i] = np.median(ysplit)
    return x, y

def coreplot(iax, df, bordercolor, borderwidth, label_font_size, axis_font_size):
    
    nsample = df.shape[0]
    xvals   = np.array(df['xval'])
    logprob = np.array(df['logistic_prob'])
    linpred = np.array(df['linear_pred'])
    
    case_xvals   = df[df['pheno'] == 1]['xval']
    ctrl_xvals   = df[df['pheno'] == 0]['xval']
    case_logprob = df[df['pheno'] == 1]['logistic_prob']
    ctrl_logprob = df[df['pheno'] == 0]['logistic_prob']
    case_linpred = df[df['pheno'] == 1]['linear_pred']
    ctrl_linpred = df[df['pheno'] == 0]['linear_pred']


    bins = np.linspace(np.min(xvals), np.max(xvals), 21)
    ncase, _ = np.histogram(case_xvals, bins = bins)
    nctrl, _ = np.histogram(ctrl_xvals, bins = bins)
    ncase = ncase / nsample
    nctrl = nctrl / nsample
    
    colors = ['#C10020', '#FF6800', '#007D34', '#93AA00', ]

    # Plot the histograms in iax[0] and iax[2]
    x = [(bins[i] + bins[i+1]) / 2 for i in range(bins.shape[0] - 1)] # centers of the bins
    xnew = np.linspace(x[0], x[-1], 101) # for a smooth plot
    
    f2 = interp1d(x, nctrl, kind='cubic')
    iax[0].plot(xnew, -f2(xnew), color=bordercolor, lw=borderwidth, zorder=10) # plotting inverted distribution
    iax[0].fill_between(xnew, -f2(xnew), 0, color=bordercolor, alpha=0.1, zorder=5)
    ctrlmax = max(f2(xnew))

    f2 = interp1d(x, ncase, kind='cubic')
    iax[2].plot(xnew,  f2(xnew), color=bordercolor, lw=borderwidth, zorder=10)
    iax[2].fill_between(xnew, f2(xnew), 0, color=bordercolor, alpha=0.1, zorder=5)
    casemax = max(f2(xnew))
    
    ymax = max(ctrlmax, casemax) * 1.1
    iax[0].set_ylim(-ymax, 0)
    iax[2].set_ylim(0, ymax)
    for ax in [iax[0], iax[2]]:
        ax.axis('off')

        
    # Plot the scatterplots and visual aids
    case_idx = np.random.choice(case_xvals.shape[0], int(case_xvals.shape[0] / 5), replace=False)
    ctrl_idx = np.random.choice(ctrl_xvals.shape[0], int(ctrl_xvals.shape[0] / 5), replace=False)
    iax[1].scatter(case_xvals[case_idx], case_logprob[case_idx], alpha=0.4, s=1, color=colors[0], zorder=30)
    iax[1].scatter(ctrl_xvals[ctrl_idx], ctrl_logprob[ctrl_idx], alpha=0.4, s=1, color=colors[1], zorder=30)
    iax[1].scatter(case_xvals[case_idx], case_linpred[case_idx], alpha=0.4, s=1, color=colors[2], zorder=20)
    iax[1].scatter(ctrl_xvals[ctrl_idx], ctrl_linpred[ctrl_idx], alpha=0.4, s=1, color=colors[3], zorder=20)
    x, y = visual_aid(logprob, xvals, nbins = 10)
    iax[1].plot(x, y, lw = 3, color= bordercolor, dashes = [5, 4], zorder=40)
    x, y = visual_aid(linpred, xvals, nbins = 10)
    iax[1].plot(x, y, lw = 3, color= bordercolor, dashes = [5, 4], zorder=40)
    
    iax[1].set_ylim(-0.2, 1.2)
    iax[1].set_yticks([0.0, 0.5, 1.0])
    iax[1].set_xticks([])
    iax[1].tick_params(axis='both', which = 'major',
                       length = 4, width = borderwidth, pad=5,
                       direction = 'out',
                       color = bordercolor,
                       labelcolor = bordercolor,
                       bottom = False, top = False, left = True, right = False
                       )
    font_properties = {'family':'sans-serif', 'weight': 'normal', 'size': label_font_size}
    iax[1].set_xticklabels(iax[1].get_xticks(), font_properties)
    iax[1].set_yticklabels(iax[1].get_yticks(), font_properties)
    
    for side, border in iax[1].spines.items():
        border.set_linewidth(borderwidth)
        border.set_color(bordercolor)

    xmin = np.percentile(xvals, 1)
    xmax = np.percentile(xvals, 99)
    for ax in iax:
        ax.set_xlim(xmin, xmax)
        
    #mylabel = r'$\boldsymbol{p(\phi = 1)}$'
    mylabel = r"$\boldsymbol{y_{\text{pred}}}$" + " or\n" + r"$\boldsymbol{p(\phi = 1)}$"
    mxlabel = r'$\boldsymbol{\sum_i x_i \beta_i}$'
    iax[1].set_ylabel(mylabel, {'size': axis_font_size, 'color': bordercolor}, labelpad = 15)

    xlabel = iax[1].xaxis.get_label()
    xlab_xpos, xlab_ypos = xlabel.get_position()
    xlabel.set_position([1.0, xlab_ypos])
    xlabel.set_horizontalalignment('right')
    iax[1].set_xlabel(mxlabel, {'size': axis_font_size, 'color': bordercolor}, labelpad = 15)
        
    return
