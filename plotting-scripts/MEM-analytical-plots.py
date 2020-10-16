#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 19 14:29:21 2020

@author: Becca

Creating plots to mimic analytical framework cost of unmet demand paper
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.legend import Legend
import os

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
plt.rc('font',**{'family':'sans-serif','sans-serif':['Arial'],'size':9})

# color palette
color_genline    = '#1c7837'   # green, dark
color_gen   = '#99c4a5'   # green, light
color_unmet   = '#a2a2a2'   # grey, light

colors = [color_gen, color_unmet]    

exponent_d = -1.25 #cost of unmet demand = 10^(exponent)
exponent_v = -0.5

file_path = '../Output_Data/'

# user input: choose files
file_name_dispatchable = '1-unmet_demand-cp0/1-unmet_demand-cp0_'
file_name_variable = '7-unmet_demand_constant-solar-only/7-unmet_demand_constant-solar-only_'
file_exp_d = 'exp%.2f' % exponent_d
file_exp_v = 'exp%.2f' % exponent_v

directory = '../figures'

df_d = pd.read_csv(file_path + file_name_dispatchable + file_exp_d + '.csv')
df_v = pd.read_csv(file_path + file_name_variable + file_exp_v + '.csv')
    
# assign data to variable names   
df_v = df_v.sort_values(by=['dispatch solar (kW)'],ascending=True)
df_v = df_v.reset_index(drop=True)
df_v1 = df_v.iloc[:6054,:]
df_v2 = df_v.iloc[6054:,:]
df_v2 = df_v2.sort_values(by=['cutailment solar (kW)'],ascending=True)
df_v = pd.concat([df_v1,df_v2], ignore_index=True)
df_d = df_d.sort_values(by=['demand (kW)'],ascending=False)
demand_d = df_d['demand (kW)'].values
demand_v = df_v['demand (kW)'].values
dispatch_gen = df_d['dispatch natgas (kW)'].values
dispatch_var = df_v['dispatch solar (kW)'].values
unmet_demand_d = df_d['dispatch unmet demand (kW)'].values
unmet_demand_v = df_v['dispatch unmet demand (kW)'].values
curtailment_var = df_v['cutailment solar (kW)'].values  # note typo in csv

hours = len(dispatch_gen)
    
# set up figure layout and size
fig, ax = plt.subplots(1,2, figsize=(6,3), sharex=True, sharey=False)
    
# plot 
ax[0].plot(range(hours), dispatch_gen, color = color_genline, linewidth=1)
ax[0].plot(range(hours), demand_d, 'k', linewidth=1)
ax[0].stackplot(range(hours), np.vstack([dispatch_gen, unmet_demand_d]), 
                     colors=colors)
ax[1].plot(range(hours), dispatch_var, color = color_genline, linewidth=1)
ax[1].plot(range(hours), demand_v, 'k', linewidth=1)
ax[1].stackplot(range(hours), np.vstack([dispatch_var, unmet_demand_v, curtailment_var]), 
                     colors=[color_gen, color_unmet, color_gen])

ax[0].set_xlim(0,8760)
ax[0].set_ylim(0,1.6)
ax[1].set_ylim(0,1.6)
for which in ['right', 'top']:
    ax[0].spines[which].set_visible(False)
    ax[1].spines[which].set_visible(False)
ax[0].set_xlabel('Hour of year', fontweight='bold')
ax[0].xaxis.set_label_coords(1.1, -.15)
ax[0].set_ylabel('Generation or Demand \n[fraction of mean demand]', 
              fontweight='bold')

ax[0].text(2000, 1.4, 'unmet demand', fontsize = 7)
ax[0].annotate("",
            xy=(500, 1.2), xycoords='data',
            xytext=(2200, 1.4), textcoords='data',
            arrowprops=dict(arrowstyle="->",connectionstyle="arc3",
            lw=0.5))
ax[1].text(1700, 0.5, 'unmet demand', fontsize = 7)
#ax[0].text(6000,0.7, 'generation', fontsize=7, color=color_genline)
#ax[1].text(6500,0.9, 'generation', fontsize=7, color=color_genline)
ax[0].text(4000, 1, 'Demand', fontsize = 7,fontweight='bold')
ax[1].text(4000, 1.02, 'Demand', fontsize = 7,fontweight='bold')
ax[0].text(800, 0.96, 'Generation', fontsize = 7,fontweight='bold', color=color_genline)
ax[1].text(5600, 0.8, 'Generation', fontsize = 7,fontweight='bold', color=color_genline)
ax[1].text(6000, 1.4, 'curtailed \ngeneration', fontsize = 7, color=color_genline)
ax[1].annotate("",
            xy=(7800, 1.2), xycoords='data',
            xytext=(7000, 1.4), textcoords='data',
            arrowprops=dict(arrowstyle="->",connectionstyle="arc3",
            lw=0.5, color=color_genline))
ax[0].annotate('A', xy=(-0.2, 1.1), xycoords='axes fraction', 
                                 horizontalalignment='left', verticalalignment='top',
                                 weight='bold', fontsize='large')
ax[1].annotate('B', xy=(-0.2, 1.1), xycoords='axes fraction', 
                                 horizontalalignment='left', verticalalignment='top',
                                 weight='bold', fontsize='large')
ax[0].annotate('cost of unmet demand = $0.06/kWh', xy=(0.08, 1.05), xycoords='axes fraction', 
                                 horizontalalignment='left', verticalalignment='top',
                                 fontsize=8, style='italic')
ax[1].annotate('cost of unmet demand = $0.32/kWh', xy=(0.08, 1.05), xycoords='axes fraction', 
                                 horizontalalignment='left', verticalalignment='top',
                                 fontsize=8, style='italic')

#plt.show()
#
#fig.savefig(directory + '/figure4-MEM_analytic_plots' + '.svg', 
#            dpi=600, bbox_inches='tight', pad_inches=0.2) 


## Make anaytic plots of costs 
file_name = 'analytic-values.csv' 
#assuming fixed costs for solar and NG, no variable cost, fixed demand = 1, 
#max demand = 1.5
os.chdir('..')
df_analytic = pd.read_csv(file_name)

f, ax = plt.subplots(3,1, figsize=(4,10), sharex=True, sharey=False)
ax[0].semilogx(df_analytic['c-unmet'], df_analytic['system-cost-d'],ls='--',c='C3')
ax[0].semilogx(df_analytic['c-unmet'], df_analytic['system-cost-v'],ls='--',c='C0')
ax[1].semilogx(df_analytic['c-unmet'], df_analytic['cost-of-E-d'],ls='--',c='C3')
ax[1].semilogx(df_analytic['c-unmet'], df_analytic['cost-of-E-v'],ls='--',c='C0')
ax[2].semilogx(df_analytic['c-unmet'], df_analytic['losses-d'],ls='--',c='C3')
ax[2].semilogx(df_analytic['c-unmet'], df_analytic['losses-v'],ls='--',c='C0')

#ax[2].set_ylim(0,1)


plt.show()











