"""
file name: stack_dispatch_mix.py
    plot dispatch mix and unmet demand as function of value of lost load 
    (= cost of unmet demand)
"""

#%% import modules

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import FormatStrFormatter

#%% global plot settings

# set rcParams back to default values
    # reference: https://stackoverflow.com/questions/26413185/how-to-recover-matplotlib-defaults-after-setting-stylesheet
mpl.rcParams.update(mpl.rcParamsDefault)

# ticks
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['xtick.major.size'] = 2.5
mpl.rcParams['ytick.major.size'] = 2.5

# font and fontsize
    # reference: https://ask.sagemath.org/question/8882/change-legend-font-when-plotting/
    # reference on font family: https://matplotlib.org/examples/api/font_family_rc.html
plt.rc('font',**{'family':'sans-serif','sans-serif':['Calibri'],'size':9})

#%% color palette
# colors from: http://colorbrewer2.org/#type=diverging&scheme=BrBG&n=4

# colorblind-friendly
color_wind    = '#1b7837'   # green, dark
color_solar   = '#a6dba0'   # green, light
color_natgas  = '#4393c3'   # blue, medium
color_storage = '#c2a5cf'   # purple, light
color_unmet   = '#e0e0e0'   # grey, light

# dispatch shares
colors = [color_wind, color_solar, color_natgas, color_storage, color_unmet]    

#%% specify file path and file name

file_path = '../Output_Data/'

file_name = ['1-unmet_demand-cp0/1-unmet_demand-cp0_20190226_221554',
             '2-unmet_demand-cp200/2-unmet_demand-cp200_20190227_020128',
             '3-unmet_demand-wind-solar-storage/3-unmet_demand-wind-solar-storage_20190227_101927',
             '4-unmet_demand-wind-storage/4-unmet_demand-wind-storage_20190227_000042',
             '5-unmet_demand-solar-storage/5-unmet_demand-solar-storage_20190227_121954',
             '6-unmet_demand-wind-solar/6-unmet_demand-wind-solar_20190226_223652']

plot_title = ['wind + solar + storage + natural gas\n(base case)',
              'wind + solar + storage + natural gas\n@ \$200/t' + '$\mathregular{CO_2}$',
              'wind + solar + storage',
              'wind + storage',
              'solar + storage',
              'wind + solar']

# case names for saving plots
savefig_name = ['case1', 'case2', 'case3', 'case4', 'case5', 'case6']

directory = file_path + 'plots'
if not os.path.exists(directory):
    os.mkdir(directory)

#%% read and plot results

for i in range(len(file_name)):

    # -------------------------------------------------------------------------
    # read data

    # read data from .csv files as dataframes
        # reference: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html
    df = pd.read_csv(file_path + file_name[i] + '.csv')
    
    # assign data to variable names
    cost_unmet_demand = df['var cost unmet demand ($/kWh)'].values
    dispatch_natgas = df['dispatch natgas (kW)'].values
    dispatch_solar = df['dispatch solar (kW)'].values
    dispatch_wind = df['dispatch wind (kW)'].values
    dispatch_storage = df['dispatch from storage (kW)'].values
    dispatch_to_storage = df['dispatch to storage (kW)'].values
    unmet_demand = df['dispatch unmet demand (kW)'].values

    # -------------------------------------------------------------------------
    # calculations

    # assume: amount dispatched to storage from each generation technology is 
    # proportional to amount dispatched from that technology
    
    # total generation (without storage)
    tot_gen = dispatch_natgas + dispatch_solar + dispatch_wind
    
    # proportion of total generation dispatched to storage
        # reference: https://stackoverflow.com/questions/26248654/numpy-return-0-with-divide-by-zero
    a = dispatch_to_storage
    b = tot_gen
    r = np.divide(a, b, out=np.zeros_like(a), where=b!=0)

    # -------------------------------------------------------------------------
    # plot results

    # stack up dispatch and unmet demand
        # generation dispatched to meet demand = dispatch_technology * (1 - r)
    dispatch_mix = np.vstack([dispatch_wind * (1 - r), 
                              dispatch_solar * (1 - r), 
                              dispatch_natgas * (1 - r),
                              dispatch_storage,
                              unmet_demand])

    # plot
    fig, ax = plt.subplots(1,1, figsize=(3,2.2), sharex=True, sharey=True)    
    ax.stackplot(cost_unmet_demand, dispatch_mix, colors=colors)

    # -------------------------------------------------------------------------
    # plot settings

    # axes
    ax.set_xlim(min(cost_unmet_demand), max(cost_unmet_demand))
    ax.set_xscale('log')
    ax.xaxis.set_major_formatter(FormatStrFormatter('%.6g'))
    ax.set_ylim(0,1)
    ax.set_yticks([0,0.2,0.4,0.6,0.8,1])
    ax.yaxis.set_major_formatter(FormatStrFormatter('%.2g'))
    # reference for disabling minor ticks: 
        # https://stackoverflow.com/questions/10781077/how-to-disable-the-minor-ticks-of-log-plot-in-matplotlib
    plt.minorticks_off()

    # title, axis labels, and legend
    ax.set_title(plot_title[i], fontsize=10, fontweight='bold')
    xlabel = 'Value of lost load [$/kWh]'
    ylabel = 'Dispatch\n(1 = average demand)'
    legend = ['Wind', 'Solar', 'Natural gas', 'Storage', 'Unmet demand']
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.legend(legend, frameon=False, ncol=2, loc='upper center', 
          bbox_to_anchor=(0.5,-0.25), fontsize=9)
    
    # -------------------------------------------------------------------------
    # save plot

#    fig.savefig(file_path + 'plots/' + 's2-dispatch mix_' + savefig_name[i] + '.svg', 
#                dpi=600, bbox_inches='tight', pad_inches=0.2)

    plt.show()
