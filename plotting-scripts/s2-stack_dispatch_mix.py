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
mpl.rcParams['xtick.direction'] = 'out'
mpl.rcParams['ytick.direction'] = 'out'
mpl.rcParams['xtick.major.size'] = 2.5
mpl.rcParams['ytick.major.size'] = 2.5

# font and fontsize
    # reference: https://ask.sagemath.org/question/8882/change-legend-font-when-plotting/
    # reference on font family: https://matplotlib.org/examples/api/font_family_rc.html
plt.rc('font',**{'family':'sans-serif','sans-serif':['Arial'],'size':8})

#%% color palette
# colors from: http://colorbrewer2.org/#type=diverging&scheme=BrBG&n=4

# colorblind-friendly
color_wind    = '#beaed4'#1b7837'   # green, dark
color_solar   = '#fdc086' #'#a6dba0'   # green, light
color_natgas  = '#386cb0' #'#4393c3'   # blue, medium
color_storage = '#7fc97f' #'#c2a5cf'   # purple, light
color_unmet   = '#e0e0e0'   # grey, light

# dispatch shares
colors = [color_wind, color_solar, color_natgas, color_storage, color_unmet]    

#%% specify file path and file name

file_path = '../Output_Data/'

# variable demand
file_name = ['1-unmet_demand-cp0/1-unmet_demand-cp0_20200218_124557',
             '2-unmet_demand-cp200/2-unmet_demand-cp200_20200216_134342',
             '3-unmet_demand-wind-solar-storage/3-unmet_demand-wind-solar-storage_20200216_144503',
             '4-unmet_demand-wind-storage/4-unmet_demand-wind-storage_20200216_154754',
             '5-unmet_demand-solar-storage/5-unmet_demand-solar-storage_20200216_164608',
             '6-unmet_demand-wind-solar/6-unmet_demand-wind-solar_20200216_165156',
             '7-unmet_demand-solar-only/7-unmet_demand-solar-only_20200216_171908',
             '8-unmet_demand-wind-only/8-unmet_demand-wind-only_20200216_172442']

# constant demand
file_name_c = ['1-unmet_demand_constant-cp0/1-unmet_demand-cp0_20200218_114235',
             '2-unmet_demand_constant-cp200/2-unmet_demand-cp200_20200218_141812',
             '3-unmet_demand_constant-wind-solar-storage/3-unmet_demand_constant-wind-solar-storage_20200218_153457',
             '4-unmet_demand_constant-wind-storage/4-unmet_demand_constant-wind-storage_20200218_163438',
             '5-unmet_demand_constant-solar-storage/5-unmet_demand_constant-solar-storage_20200218_175529',
             '6-unmet_demand_constant-wind-solar/6-unmet_demand_constant-wind-solar_20200218_182400',
             '7-unmet_demand_constant-solar-only/7-unmet_demand_constant-solar-only_20200218_183605',
             '8-unmet_demand_constant-wind-only/8-unmet_demand_constant-wind-only_20200218_184040']

plot_title = ['wind + solar + storage + natural gas',
              'wind + solar + storage + natural gas\n@ \$200/t' + '$\mathregular{CO_2}$',
              'wind + solar + storage',
              'wind + storage',
              'solar + storage',
              'wind + solar',
              'solar only',
              'wind only']

# case names for saving plots
#savefig_name = ['case1', 'case2', 'case3', 'case4', 
#                'case5', 'case6','case7','case8']

directory = '../figures'
if not os.path.exists(directory):
    os.mkdir(directory)

#%% read and plot results
rows = 4
cols = 2
index = ['0','1','2','3','4','5','6','7']
coords = dict(zip(index, [(row,col) for row in range(rows) for col in range(cols)]))
fig, ax = plt.subplots(rows, cols, figsize=(8,12), sharex=True, sharey=True) 
#fig = plt.figure(figsize=(8,12))

#for i in range(len(file_name)):
for i, ix in enumerate(index):
    # -------------------------------------------------------------------------
    # read data

    # read data from .csv files as dataframes
        # reference: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html
    df = pd.read_csv(file_path + file_name[i] + '.csv')
    df_c = pd.read_csv(file_path + file_name_c[i] + '.csv')
    
    # assign data to variable names
    cost_unmet_demand = df['var cost unmet demand ($/kWh)'].values
    dispatch_natgas = df['dispatch natgas (kW)'].values
    dispatch_solar = df['dispatch solar (kW)'].values
    dispatch_wind = df['dispatch wind (kW)'].values
    dispatch_storage = df['dispatch from storage (kW)'].values
    dispatch_to_storage = df['dispatch to storage (kW)'].values
    unmet_demand = df['dispatch unmet demand (kW)'].values
    
    cost_unmet_demand_c = df_c['var cost unmet demand ($/kWh)'].values
    dispatch_natgas_c = df_c['dispatch natgas (kW)'].values
    dispatch_solar_c = df_c['dispatch solar (kW)'].values
    dispatch_wind_c = df_c['dispatch wind (kW)'].values
    dispatch_storage_c = df_c['dispatch from storage (kW)'].values
    dispatch_to_storage_c = df_c['dispatch to storage (kW)'].values
    unmet_demand_c = df_c['dispatch unmet demand (kW)'].values

    # -------------------------------------------------------------------------
    # calculations

    # assume: amount dispatched to storage from each generation technology is 
    # proportional to amount dispatched from that technology
    
    # total generation (without storage)
    tot_gen = dispatch_natgas + dispatch_solar + dispatch_wind
    tot_gen_c = dispatch_natgas_c + dispatch_solar_c + dispatch_wind_c
    
    # proportion of total generation dispatched to storage
        # reference: https://stackoverflow.com/questions/26248654/numpy-return-0-with-divide-by-zero
    a = dispatch_to_storage
    b = tot_gen
    r = np.divide(a, b, out=np.zeros_like(a), where=b!=0)
    c = dispatch_to_storage_c
    d = tot_gen_c
    r_c = np.divide(c, d, out=np.zeros_like(c), where=d!=0)

    # -------------------------------------------------------------------------
    # plot results

    # stack up dispatch and unmet demand
        # generation dispatched to meet demand = dispatch_technology * (1 - r)
    dispatch_mix = np.vstack([dispatch_wind * (1 - r), 
                              dispatch_solar * (1 - r), 
                              dispatch_natgas * (1 - r),
                              dispatch_storage,
                              unmet_demand])
    dispatch_mix_c = np.vstack([dispatch_wind_c * (1 - r_c), 
                              dispatch_solar_c * (1 - r_c), 
                              dispatch_natgas_c * (1 - r_c),
                              dispatch_storage_c,
                              unmet_demand_c])

    # plot
#    ax = fig.add_subplot(4,2,i+1)  
#    ax[coords[ix]].stackplot(cost_unmet_demand, dispatch_mix, colors=colors)
#    plt.sca(ax[coords[ix]])
    plt.stackplot(cost_unmet_demand, dispatch_mix, colors=colors)

    # -------------------------------------------------------------------------
    # plot settings

    # axes
#    ax[coords[ix]].set_xlim(min(cost_unmet_demand), max(cost_unmet_demand))
#    ax[coords[ix]].set_xscale('log')
#    ax[coords[ix]].xaxis.set_major_formatter(FormatStrFormatter('%.6g'))
#    ax[coords[ix]].set_ylim(0,1)
#    ax[coords[ix]].set_yticks([0,0.2,0.4,0.6,0.8,1])
#    ax[coords[ix]].yaxis.set_major_formatter(FormatStrFormatter('%.2g'))
#    # reference for disabling minor ticks: 
#        # https://stackoverflow.com/questions/10781077/how-to-disable-the-minor-ticks-of-log-plot-in-matplotlib
#    plt.minorticks_off()
#
#    # title, axis labels, and legend
#    ax[coords[ix]].set_title(plot_title[i], fontsize=10, fontweight='bold')
#    xlabel = 'Cost of Unmet Demand [$/kWh]'
#    ylabel = 'Dispatch\n(1 = average demand)'
##    legend = ['Wind', 'Solar', 'Natural gas', 'Storage', 'Unmet demand']
#    ax[coords[ix]].set_xlabel(xlabel, fontsize=10)
#    ax[coords[ix]].set_ylabel(ylabel, fontsize=10)
##    ax.legend(legend, frameon=False, ncol=2, loc='upper center', 
##          bbox_to_anchor=(0.5,-0.25), fontsize=9)
    
    # -------------------------------------------------------------------------
    # save plot

#    fig.savefig(file_path + 'plots/' + 's2-dispatch mix_' + savefig_name[i] + '.svg', 
#                dpi=600, bbox_inches='tight', pad_inches=0.2)

    plt.show()
