import numpy as np
import collections

import matplotlib
matplotlib.use('Agg')
matplotlib.rc('text', usetex=True)
matplotlib.rcParams['text.latex.preamble']=[r"\usepackage{amsmath}"]
import matplotlib.pyplot as plt

import insets

def coreplot(ax, xvals, yvals, ystd, color, myls, mlabel, mzorder):
    yupper = np.minimum(yvals + ystd, 1)
    ylower = yvals - ystd
    color = color
    linestyle = myls

    coef = 12
    _dash = 1
    _dot = 0.3
    _dashspace = 0.8
    _dotspace = 0.5
    mydash = []
    if myls == 'solid':
        mydash = []
    elif myls == 'dashed':
        mydash = [_dash, _dashspace]
    elif myls == 'dotted':
        mydash = [_dot, _dotspace]
    elif myls == 'dashdot':
        mydash = [_dash, _dashspace, _dot, _dashspace]
    elif myls == 'dashdotdot':
        mydash = [_dash, _dashspace, _dot, _dashspace, _dot, _dashspace]
    elif myls == 'dashdashdot':
        mydash = [_dash, _dashspace, _dashspace, _dashspace, _dot, _dashspace]
    mydash = [x * coef for x in mydash]

    ax.plot(xvals, yvals, color=color, dashes = mydash, lw=4, label=mlabel, zorder=mzorder)
    return

def save_prcplot(filename, data, phenodf, xlim, ylim, xticks, yticks, plot_legend = False, plot_inset = False):
    ''' Use the same plot params for different benchmarks.
    '''

    kelly_colors_hex = [
        '#FFB300', # Vivid Yellow
        '#803E75', # Strong Purple
        '#FF6800', # Vivid Orange
        '#A6BDD7', # Very Light Blue
        '#C10020', # Vivid Red
        '#CEA262', # Grayish Yellow
        '#817066', # Medium Gray
    
        # The following don't work well for people with defective color vision
        '#007D34', # Vivid Green
        '#F6768E', # Strong Purplish Pink
        '#00538A', # Strong Blue
        '#FF7A5C', # Strong Yellowish Pink
        '#53377A', # Strong Violet
        '#FF8E00', # Vivid Orange Yellow
        '#B32851', # Strong Purplish Red
        '#F4C800', # Vivid Greenish Yellow
        '#7F180D', # Strong Reddish Brown
        '#93AA00', # Vivid Yellowish Green
        '#593315', # Deep Yellowish Brown
        '#F13A13', # Vivid Reddish Orange
        '#232C16', # Dark Olive Green
        ]

    banskt_colors_hex = [
        '#2D69C4', # blue 
        '#FFB300', # Vivid Yellow
        '#93AA00', # Vivid Yellowish Green
        '#CC2529', # red
        '#535154', # gray
        '#6B4C9A', # purple
        '#922428', # dark brown
        '#948B3D', # olive
        ]

    bordercolor = '#333333'
    borderwidth = 2
    colors = banskt_colors_hex
    figsize = (13, 12)
    axis_font_size = 35
    label_font_size = 30
    legend_font_size = 25
    
    
    fig = plt.figure(figsize = figsize)
    ax1 = fig.add_subplot(111)
    ax2 = ax1.twinx()
    
    mlabels = {'blore':   'B-LORE',
               'probit':  'BVSR probit',
               'linear':  'BVSR linear',
               'finemap': 'FINEMAP',
               'jam':     'JAM',
               'bimbam':  'BIMBAM',
               'snptest': 'META',
              }
    

    mcolors = {'blore':   colors[3],
               'probit':  colors[0],
               'linear':  colors[1],
               'finemap': colors[2],
               'jam':     colors[6],
               'bimbam':  colors[5],
               'snptest': colors[4],
              }


    mzorder = {'blore':   100,
               'probit':  50,
               'linear':  40,
               'finemap': 30,
               'jam':     10,
               'bimbam':  20,
               'snptest': 60,
              }

    
    for key in ['blore', 'probit', 'linear', 'finemap', 'jam', 'bimbam', 'snptest']:
        val = data[key]
        if not val == 0:
            if len(val[0]) > 0:
                x = val[0]
                y = val[2]
                err = val[4]
                if plot_legend:
                    coreplot(ax1, x, y, err, mcolors[key], 'solid', mlabels[key], mzorder[key])
                else:
                    coreplot(ax1, x, y, err, mcolors[key], 'solid', None, mzorder[key])
                y = val[1]
                err = val[3]
                coreplot(ax2, x, y, err, mcolors[key], 'dashed', None, mzorder[key])
            
    mxlabel = r'Top ranked SNPs'
    my1label = r'Recall'
    my2label = r'Precision'
    
    font_properties = {'family':'sans-serif', 'weight': 'bold', 'size': axis_font_size, 'color':bordercolor}
    ax1.set_xlabel(mxlabel, font_properties, labelpad = 15)
    ax1.set_ylabel(my1label, font_properties, labelpad = 20)
    ax2.set_ylabel(my2label, font_properties, labelpad = 20)
    
    for ax in [ax1, ax2]:
     
        if xlim is not None: ax.set_xlim(xlim)
        if ylim is not None: ax.set_ylim(ylim)
        if xticks is not None: ax.set_xticks(xticks)
        if yticks is not None: ax.set_yticks(yticks)
        
        h, l = ax.get_legend_handles_labels()
        if len(l) > 0:
            legend = ax.legend(loc='upper left', bbox_to_anchor=(0.02, 0.98),
                               handlelength = 3.0,
                               handletextpad = 2.0,
                               markerscale=5,
                               ncol = 1,
                               frameon = True, borderpad = 1.5, labelspacing = 1.5
                               #title = legendtitle
                              )
            for l in legend.legendHandles:
                l.set_alpha(1)
            lframe = legend.get_frame()
            lframe.set_edgecolor(bordercolor)
            lframe.set_linewidth(borderwidth)
            for fonts in ([legend.get_title()] + legend.texts):
                fonts.set_fontsize(legend_font_size)
                fonts.set_color(bordercolor)
    
        ax.tick_params(axis='both', which = 'major',
                       length = 10, width = borderwidth, pad=10,
                       labelsize = label_font_size,
                       color = bordercolor,
                       labelcolor = bordercolor,
                       bottom = True, top = False, left = True, right = True
                      )
        font_properties = {'family':'sans-serif', 'weight': 'bold', 'size': label_font_size}
        xticks = ax.get_xticks()
        yticks = ax.get_yticks()
        xticklabels = ['{:g}'.format(x) for x in xticks]
        yticklabels = ['{:3.1f}'.format(x) for x in yticks]
        ax.set_xticklabels(xticklabels, font_properties)
        ax.set_yticklabels(yticklabels, font_properties)

        for side, border in ax.spines.items():
            border.set_linewidth(borderwidth)
            border.set_color(bordercolor)
        ax.grid(color='dimgray', lw=0.5, alpha=0.5)
    
    plt.tight_layout()
    if plot_inset:
        iax = insets.add_vert(fig, ax1, 0.4, 0.4, 0.55, 0.07, [1, 3, 1])
        insets.coreplot(iax, phenodf, bordercolor, borderwidth, label_font_size, axis_font_size)
    plt.savefig(filename, bbox_inches='tight')
    plt.show()
