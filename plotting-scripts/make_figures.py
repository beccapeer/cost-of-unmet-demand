#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 19:04:35 2020

@author: Becca

Creating line figures for cost of unmet demand paper
"""

# import packages
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import FormatStrFormatter
from helpers import get_file_name

## GLOBAL PLOT SETTINGS
## set rcParams back to default values
mpl.rcParams.update(mpl.rcParamsDefault)

## ticks
mpl.rcParams['xtick.direction'] = 'in'
mpl.rcParams['ytick.direction'] = 'in'
mpl.rcParams['xtick.major.size'] = 2.5
mpl.rcParams['ytick.major.size'] = 2.5

## font and fontsize
    # reference: https://ask.sagemath.org/question/8882/change-legend-font-when-plotting/
    # reference on font family: https://matplotlib.org/examples/api/font_family_rc.html
plt.rc('font',**{'family':'sans-serif','sans-serif':['Arial'],'size':8})


## specify path for output files
file_path = '../Output_Data/'

## Use this NEW_FILES flag to either run the old files or updated ones based on "new_input_sheets/create_input_sheets.sh"
NEW_FILES = True
NEW_FILES = False
app = 'new_' if NEW_FILES else ''
DATE = '2020102' if NEW_FILES else ''


## variable demand scenarios
file_name1 = f'{app}1-unmet_demand-cp0/{app}1-unmet_demand-cp0_20200218_124557'
legend1 = 'wind + solar + storage + natural gas'

file_name2 = f'{app}2-unmet_demand-cp200/{app}2-unmet_demand-cp200_20200216_134342'
legend2 = 'wind + solar + storage + natural gas @ \$200/t' + '$\mathregular{CO_2}$'

file_name3 = f'{app}3-unmet_demand-wind-solar-storage/{app}3-unmet_demand-wind-solar-storage_20200216_144503'
legend3 = 'wind + solar + storage'

file_name4 = f'{app}4-unmet_demand-wind-storage/{app}4-unmet_demand-wind-storage_20200216_154754'
legend4 = 'wind + storage'

file_name5 = f'{app}5-unmet_demand-solar-storage/{app}5-unmet_demand-solar-storage_20200216_164608'
legend5 = 'solar + storage'

file_name6 = f'{app}6-unmet_demand-wind-solar/{app}6-unmet_demand-wind-solar_20200216_165156'
legend6 = 'wind + solar'

file_name8 = f'{app}7-unmet_demand-solar-only/{app}7-unmet_demand-solar-only_20200216_171908'
legend8 = 'solar only'

file_name7 = f'{app}8-unmet_demand-wind-only/{app}8-unmet_demand-wind-only_20200216_172442'
legend7 = 'wind only'

## constant demand scenarios
file_namec1 = f'{app}1-unmet_demand_constant-cp0/{app}1-unmet_demand-cp0_20200218_114235'
legend1 = 'wind + solar + storage + natural gas'

file_namec2 = f'{app}2-unmet_demand_constant-cp200/{app}2-unmet_demand-cp200_20200218_141812'
legend2 = 'wind + solar + storage + natural gas @ \$200/t' + '$\mathregular{CO_2}$'

file_namec3 = f'{app}3-unmet_demand_constant-wind-solar-storage/{app}3-unmet_demand_constant-wind-solar-storage_20200218_153457'
legend3 = 'wind + solar + storage'

file_namec4 = f'{app}4-unmet_demand_constant-wind-storage/{app}4-unmet_demand_constant-wind-storage_20200218_163438'
legend4 = 'wind + storage'

file_namec5 = f'{app}5-unmet_demand_constant-solar-storage/{app}5-unmet_demand_constant-solar-storage_20200218_175529'
legend5 = 'solar + storage'

file_namec6 = f'{app}6-unmet_demand_constant-wind-solar/{app}6-unmet_demand_constant-wind-solar_20200218_182400'
legend6 = 'wind + solar'

file_namec8 = f'{app}7-unmet_demand_constant-solar-only/{app}7-unmet_demand_constant-solar-only_20200218_183605'
legend8 = 'solar only'

file_namec7 = f'{app}8-unmet_demand_constant-wind-only/{app}8-unmet_demand_constant-wind-only_20200218_184040'
legend7 = 'wind only'

file_name = [file_name1, file_name2, file_name3, file_name4, 
             file_name5, file_name6, file_name7, file_name8]
file_namec = [file_namec1, file_namec2, file_namec3, file_namec4, 
             file_namec5, file_namec6, file_namec7, file_namec8]
legend = [legend1, legend2, legend3, legend4, 
          legend5, legend6, legend7, legend8]

## figure directory
directory = '../figures2'

## read in results    
nfiles = len(file_name)
## variable demand
cost_unmet_demand = []
system_cost = []
demand = []
unmet_demand = []
## constant demand
cost_unmet_demand_c = []
system_cost_c = []
demand_c = []
unmet_demand_c = []

for i in range(nfiles):

    f_name = get_file_name(file_path + file_name[i], DATE, NEW_FILES)
    df = pd.read_csv(f_name)
    cost_unmet_demand.append(df['var cost unmet demand ($/kWh)'].values)
    system_cost.append(df['system cost ($/kW/h)'].values)
    demand.append(df['mean demand (kW)'].values)
    unmet_demand.append(df['dispatch unmet demand (kW)'].values)
    
    f_namec = get_file_name(file_path + file_namec[i], DATE, NEW_FILES)
    df_c = pd.read_csv(f_namec)
    cost_unmet_demand_c.append(df_c['var cost unmet demand ($/kWh)'].values)
    system_cost_c.append(df_c['system cost ($/kW/h)'].values)
    demand_c.append(df_c['mean demand (kW)'].values)
    unmet_demand_c.append(df_c['dispatch unmet demand (kW)'].values)

## calculations    
## reliability (fraction of demand met)
reliability = 1 - np.array(unmet_demand)/np.array(demand)
reliability_c = 1 - np.array(unmet_demand_c)/np.array(demand_c)

## economic damage from not meeting demand
loss_unmet_demand = np.array(cost_unmet_demand) * np.array(unmet_demand)
loss_unmet_demand_c = np.array(cost_unmet_demand_c) * np.array(unmet_demand_c)

## cost of electricity 
## (equivalent to LCOE, system cost minus cost of not meeting demand)
elec_cost = np.array(system_cost) - loss_unmet_demand   
elec_cost_c = np.array(system_cost_c) - loss_unmet_demand_c   
    
## plot results 
## line colors
colors = plt.cm.plasma(np.linspace(0,1,nfiles))

## FIGURE 2
fig2, ax = plt.subplots(2,2, figsize=(5.6,5.2), sharex=True, sharey=False)
plt.subplots_adjust(wspace=0.4)

## first panel: x-axis (reliability), y-axis (cost of unmet demand) both log scale
## base case
ax[0,0].loglog(100*(1-reliability[0,:]), cost_unmet_demand[0], 
          linestyle='--', linewidth=1, color='k')
## all other cases
for i in range(1,nfiles):
    ax[0,0].loglog(100*(1-reliability[i,:]), cost_unmet_demand[i], 
              linestyle='--', linewidth=1, color=colors[i-1])

## second panel: x-axis (reliability) log scale, y-axis (electricity cost) linear scale
## base case
ax[1,0].semilogx(100*(1-reliability[0,:]), elec_cost[0,:], 
            linestyle='--', linewidth=1, color='k')
## all other cases
for i in range(1,nfiles):
    ax[1,0].semilogx(100*(1-reliability[i,:]), elec_cost[i,:], 
                linestyle='--', linewidth=1, color=colors[i-1])
## first panel: x-axis (reliability), y-axis (cost of unmet demand) both log scale
## base case
ax[0,1].loglog(100*(1-reliability_c[0,:]), cost_unmet_demand_c[0], 
          linestyle='--', linewidth=1, color='k')
## all other cases
for i in range(1,nfiles):
    ax[0,1].loglog(100*(1-reliability_c[i,:]), cost_unmet_demand_c[i], 
              linestyle='--', linewidth=1, color=colors[i-1])

## second panel: x-axis (reliability) log scale, y-axis (electricity cost) linear scale
## base case
ax[1,1].semilogx(100*(1-reliability_c[0,:]), elec_cost_c[0,:], 
            linestyle='--', linewidth=1, color='k')
## all other cases
for i in range(1,nfiles):
    ax[1,1].semilogx(100*(1-reliability_c[i,:]), elec_cost_c[i,:], 
                linestyle='--', linewidth=1, color=colors[i-1])
    
### third panel: reliability vs system cost
### base case
#ax[2].semilogx(100*(1-reliability[0,:]), system_cost[0], 
#            linestyle='--', linewidth=1, color='k')
### all other cases
#for i in range(1,nfiles):
#    ax[2].semilogx(100*(1-reliability[i,:]), system_cost[i], 
#                linestyle='--', linewidth=1, color=colors[i-1])
#
### fourth panel: reliability vs economic losses
### base case
#ax[3].semilogx(100*(1-reliability[0,:]), loss_unmet_demand[0,:], 
#            linestyle='--', linewidth=1, color='k')
### all other cases
#for i in range(1,nfiles):
#    ax[3].semilogx(100*(1-reliability[i,:]), loss_unmet_demand[i,:], 
#                linestyle='--', linewidth=1, color=colors[i-1])

## plot settings   
ax[0,0].set_xlim(0.001,100)
ax[0,0].invert_xaxis()
xtick_pos = [100,10,1,0.1,0.01,0.001]    # 1 - reliability
ax[0,0].set_xticks(xtick_pos)
#for which in ['right', 'top']:
#        ax[0].spines[which].set_visible(False)
#        ax[1].spines[which].set_visible(False)

## set x-axis tick labels
xtick_labels = []
for x in xtick_pos:
    xtick_labels.append('%.6g' % (100 - x))    # reliability
ax[0,0].set_xticklabels(xtick_labels)
ax[0,0].set_ylim(0.01,1000)
ax[0,0].set_yticks(np.geomspace(0.01,1000,6))
ax[0,0].yaxis.set_major_formatter(FormatStrFormatter('%.6g'))
ax[0,0].minorticks_off()
ax[1,0].set_ylim(0, 0.40)
ax[1,0].set_yticks(np.arange(0,0.45,0.05)) 
ax[1,0].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax[1,0].minorticks_off()
ax[0,1].set_ylim(0.01,1000)
ax[0,1].set_yticks(np.geomspace(0.01,1000,6))
ax[0,1].yaxis.set_major_formatter(FormatStrFormatter('%.6g'))
ax[0,1].minorticks_off()
ax[1,1].set_ylim(0, 0.40)
ax[1,1].set_yticks(np.arange(0,0.45,0.05)) 
ax[1,1].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax[1,1].minorticks_off()

## axis labels 
xlabel = 'Reliability [% demand met]'
ylabel = 'Cost of Unmet Demand [$/kWh]'
ax[1,0].set_xlabel(xlabel, fontsize=10)
ax[1,0].xaxis.set_label_coords(1.3, -.15)
ax[0,0].set_ylabel(ylabel, fontsize=10)
ylabel = 'Cost of electricity [$/kWh]'
ax[1,0].set_ylabel(ylabel, fontsize=10)

## legend or plot text
#ax[0].legend(legend, frameon=False, loc='upper center', 
#          bbox_to_anchor=(0.5,-0.25), fontsize=9)

## constant demand
#ax[0].text(0.9,0.04,'natural gas + solar + wind', fontsize=6)
#ax[0].text(0.5,0.09,'NG with carbon price\n+ solar + wind', 
#  fontsize=6, color=colors[0], rotation=33)
#ax[0].text(5,0.2,'solar + wind + storage', 
#  fontsize=6, color=colors[1], rotation= 36)
#ax[0].text(0.01,44,'wind + \nstorage', 
#  fontsize=6, color=colors[2])
#ax[0].text(10,10,'solar + \nstorage', 
#  fontsize=6, color=colors[3])
#ax[0].annotate("",
#            xy=(0.38, 3.5), xycoords='data',
#            xytext=(3, 8), textcoords='data',
#            arrowprops=dict(arrowstyle="->",connectionstyle="angle3",
#            color=colors[3], lw=0.5))
#ax[0].text(10,50,'wind + solar', 
#  fontsize=6, color=colors[4])
#ax[0].annotate("",
#            xy=(0.25, 10), xycoords='data',
#            xytext=(1, 40), textcoords='data',
#            arrowprops=dict(arrowstyle="->",connectionstyle="angle3",
#            color=colors[4], lw=0.5))
#ax[0].text(40,500,'solar only', 
#  fontsize=6, color=colors[6])
#ax[0].text(0.1,150,'wind only', 
#  fontsize=6, color=colors[5], rotation=40)
#ax[1].text(0.9,0.01,'natural gas + solar + wind', fontsize=6)
#ax[1].text(0.0011,0.067,'NG with carbon price\n+ solar + wind', 
#  fontsize=6, color=colors[0], ha='right')
#ax[1].text(0.32,0.125,'solar + wind + storage', 
#  fontsize=6, color=colors[1], rotation=5)
#ax[1].text(0.01,0.173,'wind + \nstorage', 
#  fontsize=6, color=colors[2])
#ax[1].text(30,0.13,'solar + storage', 
#  fontsize=6, color=colors[3], rotation=35)
#ax[1].text(0.03,0.29,'wind + solar', 
#  fontsize=6, color=colors[4])
#ax[1].text(40,0.37,'solar only', 
#  fontsize=6, color=colors[6])
#ax[1].text(0.1,0.34,'wind only', 
#  fontsize=6, color=colors[5])

## variable demand
ax[0,0].text(9,0.015,'natural gas + \nsolar + wind', fontsize=6)
ax[0,0].text(0.2,0.09,'NG with carbon price\n    + solar + wind', 
  fontsize=6, color=colors[0])
ax[0,0].annotate("",
            xy=(0.04, 1.5), xycoords='data',
            xytext=(0.01, 0.25), textcoords='data',
            arrowprops=dict(arrowstyle="->",connectionstyle="angle3",
            color=colors[0], lw=0.5))
ax[0,0].text(5,0.26,'solar + wind + storage', 
  fontsize=6, color=colors[1], rotation= 32)
ax[0,0].text(10,10,'wind + \nstorage', 
  fontsize=6, color=colors[2])
ax[0,0].annotate("",
            xy=(0.9, 3.5), xycoords='data',
            xytext=(3, 8), textcoords='data',
            arrowprops=dict(arrowstyle="->",connectionstyle="angle3",
            color=colors[2], lw=0.5))
ax[0,0].text(0.01,44,'solar + \nstorage', 
  fontsize=6, color=colors[3])
ax[0,0].text(10,50,'wind + solar', 
  fontsize=6, color=colors[4])
ax[0,0].annotate("",
            xy=(0.25, 10), xycoords='data',
            xytext=(1, 40), textcoords='data',
            arrowprops=dict(arrowstyle="->",connectionstyle="angle3",
            color=colors[4], lw=0.5))
ax[0,0].text(35,500,'solar only', 
  fontsize=6, color=colors[6])
ax[0,0].text(0.15,150,'wind only', 
  fontsize=6, color=colors[5], rotation=40)
ax[1,0].text(0.9,0.044,'natural gas + solar + wind', fontsize=6)
ax[1,0].text(0.0011,0.07,'NG with carbon price\n+ solar + wind', 
  fontsize=6, color=colors[0], ha='right')
ax[1,0].text(0.32,0.132,'solar + wind + storage', 
  fontsize=6, color=colors[1], rotation=5)
ax[1,0].text(0.01,0.187,'wind + \nstorage', 
  fontsize=6, color=colors[2])
ax[1,0].text(1.2,0.21,'solar + storage', 
  fontsize=6, color=colors[3], rotation=25)
ax[1,0].text(0.03,0.3,'wind + solar', 
  fontsize=6, color=colors[4])
ax[1,0].text(37,0.37,'solar only', 
  fontsize=6, color=colors[6])
ax[1,0].text(0.35,0.34,'wind only', 
  fontsize=6, color=colors[5])
ax[0,0].annotate('A', (0.03,1.1), xycoords='axes fraction',
                       ha='left', va='top', weight='bold', fontsize='large')
ax[0,1].annotate('B', (0.03,1.1), xycoords='axes fraction',
                       ha='left', va='top', weight='bold', fontsize='large')
ax[1,0].annotate('C', (0.03,1.1), xycoords='axes fraction',
                       ha='left', va='top', weight='bold', fontsize='large')
ax[1,1].annotate('D', (0.03,1.1), xycoords='axes fraction',
                       ha='left', va='top', weight='bold', fontsize='large')
ax[0,0].annotate('Variable demand', (0.2,1.2), xycoords='axes fraction',
                       ha='left', va='top', fontsize='large')
ax[0,1].annotate('Constant demand', (0.2,1.2), xycoords='axes fraction',
                       ha='left', va='top', fontsize='large')

#plt.show()

## save figure 2
## constant demand
#fig2.savefig(directory + '/figure2-costs_v_reliability-constant_demand' + '.svg', 
#            dpi=600, bbox_inches='tight', pad_inches=0.2) 
## variable demand
#fig2.savefig(directory + '/figure2-costs_v_reliability-variable_demand' + '.svg', 
#            dpi=600, bbox_inches='tight', pad_inches=0.2) 
fig2.savefig(directory + '/figure2-costs_v_reliability-both_demand' + '.svg', 
            dpi=600, bbox_inches='tight', pad_inches=0.2)

## FIGURE 3
fig3, ax = plt.subplots(3,1, figsize=(4,10), sharex=True, sharey=False)

ax[0].semilogx(cost_unmet_demand[0], system_cost[0], 
            linestyle='--', linewidth=1, color='k')
ax[1].semilogx(cost_unmet_demand[0], elec_cost[0], 
            linestyle='--', linewidth=1, color='k')
# indices with unmet demand leading to 1 (= average demand)
x = np.array(unmet_demand[0])
idx = np.where(x < 1)[0]
# indices up to the point where reliability = 0
adder = 0 if NEW_FILES else 1
idx_new = np.append(idx,np.max(idx)+adder)  
# plot results up to reliability = 0 for case 1
ax[2].semilogx(np.array(cost_unmet_demand)[0,idx_new], loss_unmet_demand[0,idx_new], 
            linestyle='--', linewidth=1, color='k')

for i in range(1,nfiles):
    ax[0].semilogx(cost_unmet_demand[i], system_cost[i], 
                linestyle='--', linewidth=1, color=colors[i-1])
    ax[1].semilogx(cost_unmet_demand[i], elec_cost[i], 
      linestyle='--', linewidth=1, color=colors[i-1])
    # indices with unmet demand leading to 1 (= average demand)
    x = np.array(unmet_demand[i])
    idx = np.where(x < 1)[0]
    # indices up to the point where reliability = 0
    idx_new = np.append(idx,np.max(idx)+adder)
    # plot results up to zero reliability
    ax[2].semilogx(np.array(cost_unmet_demand)[i,idx_new], loss_unmet_demand[i,idx_new], 
                linestyle='--', linewidth=1, color=colors[i-1])

## plot settings

## axes
ax[0].set_xlim(0.01,1000)
ax[0].set_xticks(np.geomspace(0.01,1000,6))
ax[0].xaxis.set_major_formatter(FormatStrFormatter('%.6g'))
ax[0].set_ylim(0, 0.40)
ax[0].set_yticks(np.arange(0,0.45,0.05))
ax[0].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax[0].minorticks_off()
ax[1].set_ylim(0, 0.40)
ax[1].set_yticks(np.arange(0,0.45,0.05))
ax[1].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax[1].minorticks_off()
ax[2].set_ylim(0,0.14)
ax[2].yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax[2].minorticks_off()
ylabel0 = 'Total system cost [$/kWh]'
ax[0].set_ylabel(ylabel0, fontsize=10)
ylabel1 = 'Cost of electricity [$/kWh]'
ax[1].set_ylabel(ylabel1, fontsize=10)
xlabel = 'Cost of Unmet Demand [$/kWh]'
ylabel2 = 'Economic damage [$/kWh demand]'
ax[2].set_xlabel(xlabel, fontsize=10)
ax[2].set_ylabel(ylabel2, fontsize=10)

## legend or plot lables
ax[2].legend(legend, frameon=False, loc='upper center', 
          bbox_to_anchor=(0.5,-0.25), fontsize=9)

plt.show()

## save figure 3
## constant demand
#fig3.savefig(directory + '/figure3-costs_v_CUD-constant_demand' + '.png', 
#            dpi=600, bbox_inches='tight', pad_inches=0.2)
## variable demand
#fig3.savefig(directory + '/figure3-costs_v_CUD-variable_demand' + '.svg', 
#            dpi=600, bbox_inches='tight', pad_inches=0.2)


   
