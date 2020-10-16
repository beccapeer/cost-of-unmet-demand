"""
file name: stack_daily_generation.py
    plot daily-averaged demand and generation for each technology for selected
    values of lost load (= costs of unmet demand)
"""

#%% import modules

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.legend import Legend

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
plt.rc('font',**{'family':'sans-serif','sans-serif':['Arial'],'size':9})

#%% color palette
# colors from: http://colorbrewer2.org/#type=diverging&scheme=BrBG&n=4

# colorblind-friendly
color_wind    = '#beaed4'#1b7837'   # green, dark
color_solar   = '#fdc086' #'#a6dba0'   # green, light
color_natgas  = '#386cb0' #'#4393c3'   # blue, medium
color_storage = '#7fc97f' #'#c2a5cf'   # purple, light
color_unmet   = '#e0e0e0'   # grey, light

# dispatch shares
colors = [color_wind, color_solar, color_natgas, color_storage, color_unmet,
          color_wind, color_solar]    

#%% specify file path and file name

# user input: choose exponents of 10 to specify value of lost load (= second part of filename for plots)
exponents = [1]

file_path = '../Output_Data/'

# user input: choose main filename
file_name1 = '2-unmet_demand-cp200/2-unmet_demand-cp200_'
#'2-unmet_demand-cp200/2-unmet_demand-cp200_'
#'1-unmet_demand-cp0/1-unmet_demand-cp0_'
#'3-unmet_demand-wind-solar-storage/3-unmet_demand-wind-solar-storage_'
#'4-unmet_demand-wind-storage/4-unmet_demand-wind-storage_'
#'5-unmet_demand-solar-storage/5-unmet_demand-solar-storage_'
#'6-unmet_demand-wind-solar/6-unmet_demand-wind-solar_'
#'7-unmet_demand-solar-only/7-unmet_demand-solar-only_'
#'8-unmet_demand-wind-only/8-unmet_demand-wind-only_'

savefig_name = 'case2'

directory = file_path + 'figures'
if not os.path.exists(directory):
    os.mkdir(directory)
    

#%% read in hourly results, calculate daily averages, and plot results

for exponent in exponents:
    
    # -------------------------------------------------------------------------
    # read data as dataframes
        # reference: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html
    
    # file to read in (varies with cost of unmet demand)    
    file_name2 = 'exp%.2f' % exponent

    # read data    
    df = pd.read_csv(file_path + file_name1 + file_name2 + '.csv')
    
    # assign data to variable names
    demand = df['demand (kW)'].values
    dispatch_wind = df['dispatch wind (kW)'].values
    dispatch_solar = df['dispatch solar (kW)'].values
    dispatch_natgas = df['dispatch natgas (kW)'].values
    dispatch_from_storage = df['dispatch from storage (kW)'].values
    dispatch_to_storage = df['dispatch to storage (kW)'].values
    unmet_demand = df['dispatch unmet demand (kW)'].values
    curtailment_wind = df['cutailment wind (kW)'].values    # note typo in csv
    curtailment_solar = df['cutailment solar (kW)'].values  # note typo in csv
    
    # -------------------------------------------------------------------------
    # calculations
        # assume: amount dispatched to storage from each generation technology 
        # is proportional to amount dispatched from that technology

    # total generation (without storage)
    tot_gen = dispatch_wind + dispatch_solar + dispatch_natgas

    # proportion of total generation dispatched to storage
        # reference: https://stackoverflow.com/questions/26248654/numpy-return-0-with-divide-by-zero
    a = dispatch_to_storage
    b = tot_gen
    r = np.divide(a, b, out=np.zeros_like(a), where=b!=0)
    
    # generation dispatched to meet demand
    dispatch_wind_minus_to_storage = dispatch_wind * (1 - r)
    dispatch_solar_minus_to_storage = dispatch_solar * (1 - r)
    dispatch_natgas_minus_to_storage = dispatch_natgas * (1 - r)

    # -------------------------------------------------------------------------
    # daily averages
    
    # "sinks" = demand, storage charge
    demand_daily = np.mean(demand.reshape(-1,24), axis=1)
    dispatch_to_storage_daily = np.mean(dispatch_to_storage.reshape(-1,24), axis=1)
    
    # "sources" = wind, solar, natgas, storage discharge, unmet demand
    dispatch_wind_daily = np.mean(dispatch_wind_minus_to_storage.reshape(-1,24), axis=1)
    dispatch_solar_daily = np.mean(dispatch_solar_minus_to_storage.reshape(-1,24), axis=1)
    dispatch_natgas_daily = np.mean(dispatch_natgas_minus_to_storage.reshape(-1,24), axis=1)
    dispatch_from_storage_daily = np.mean(dispatch_from_storage.reshape(-1,24), axis=1)
    unmet_demand_daily = np.mean(unmet_demand.reshape(-1,24), axis=1)

    # curtailment
    curtailment_wind_daily = np.mean(curtailment_wind.reshape(-1,24), axis=1)
    curtailment_solar_daily = np.mean(curtailment_solar.reshape(-1,24), axis=1)
    
    # stack up daily averages of sources and curtailment                           
    dispatch_daily = np.vstack([dispatch_wind_daily,
                                dispatch_solar_daily,
                                dispatch_natgas_daily,
                                dispatch_from_storage_daily,
                                unmet_demand_daily])
    
    curtailment_daily = np.vstack([curtailment_wind_daily,
                                   curtailment_solar_daily])
    
    # -------------------------------------------------------------------------
    # plot results
    
    # hours in year, days in year
    hours = len(dispatch_natgas)
    days = int(hours/24)
    
    # set up figure layout and size
    fig, ax = plt.subplots(1,1, figsize=(4.5,1.8), sharex=True, sharey=True)
    
    # plot daily averages of sinks, sources, and curtailment
    ax.plot(range(days), demand_daily, 'k', linewidth=1)
#    ax.plot(range(days), dispatch_to_storage_daily, color=color_storage, linewidth=1)
    p = ax.stackplot(range(days), np.vstack([dispatch_daily, curtailment_daily]), 
                     colors=colors)

    # -------------------------------------------------------------------------
    # plot settings
    
    # axes
    ax.set_ylim([0,3])
    ax.set_yticks([0,1,2,3])
 
    # title, axis labels, legend
        # reference on multiple legends: https://jakevdp.github.io/PythonDataScienceHandbook/04.06-customizing-legends.html
    title = 'cost of unmet demand = $%.6g' % 10**exponent + '/kWh'
    xlabel = 'Day of year'
    ylabel = 'Demand or generation\n(1 = average demand)'
    legend_a = ['Demand']
    legend_b = ['Wind', 'Solar', 'Natural gas', 'Storage', 'Unmet demand']
#    ax.set_title(title, fontsize=10)
    ax.set_xlabel(xlabel, fontsize=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.text(190,1.7, 'natural gas',color=colors[2],weight='bold', 
            size=7, style='italic')
    ax.annotate("",xy=(215, 0.9), xycoords='data',
            xytext=(215, 1.65), textcoords='data',
            arrowprops=dict(arrowstyle="-",connectionstyle="arc3",
            lw=0.5, color=colors[2]))
    ax.text(30,2, 'curtailed wind',color=colors[0],weight='bold', 
            size=7, style='italic')
    ax.annotate("",xy=(60, 1.4), xycoords='data',
            xytext=(80, 1.95), textcoords='data',
            arrowprops=dict(arrowstyle="-",connectionstyle="arc3",
            lw=0.5, color=colors[0]))
    ax.text(130,1.8, 'solar',color=colors[1],weight='bold', 
            size=7, style='italic')
    ax.annotate("",xy=(145, 0.6), xycoords='data',
            xytext=(145, 1.75), textcoords='data',
            arrowprops=dict(arrowstyle="-",connectionstyle="arc3",
            lw=0.5, color=colors[1]))
    ax.text(290,1.6, 'demand',color='k',weight='bold', 
            size=7, style='italic')
    ax.annotate("",xy=(260, 1.05), xycoords='data',
            xytext=(290, 1.55), textcoords='data',
            arrowprops=dict(arrowstyle="-",connectionstyle="arc3",
            lw=0.5, color='k'))
    ax.text(310,0.1, 'wind',color='k',weight='bold', 
            size=7, style='italic')
    ax.annotate(title, xy=(0.28, 0.95), xycoords='axes fraction', 
                                 horizontalalignment='left', verticalalignment='top',
                                 fontsize=8, style='italic')
    ax.annotate('B', xy=(-0.15, 1.15), xycoords='axes fraction', 
                                 horizontalalignment='left', verticalalignment='top',
                                 weight='bold', fontsize='large')
    for which in ['right', 'top']:
        ax.spines[which].set_visible(False)
#    ax.legend(labels=legend_a, fancybox=False, frameon=False, 
#              loc='upper left', bbox_to_anchor=(0,-0.65), fontsize=9)
#    leg = Legend(ax, p, labels=legend_b, fancybox=False, frameon=False, 
#                 loc='upper left', bbox_to_anchor=(0,-0.35), ncol=3, fontsize=9)
#    ax.add_artist(leg)
    # adjust spacing within and around subplots
        # references: 
            # https://stackoverflow.com/questions/37558329/matplotlib-set-axis-tight-only-to-x-or-y-axis
            # https://matplotlib.org/api/_as_gen/matplotlib.pyplot.subplots_adjust.html
    plt.autoscale(enable=True, axis='x', tight=True)
    
    # -------------------------------------------------------------------------
    # save plot
    
    fig.savefig('../figures/' 
                + '1b-daily dispatch_' + savefig_name + file_name2 + '.svg', 
                dpi=600, bbox_inches='tight', pad_inches=0.2)
    
    plt.show()
