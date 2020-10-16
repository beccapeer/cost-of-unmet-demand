"""
file name: plot_system_cost_vs_VoLL.py
    plot total system cost as function of cost of unmet demand
    for all cases
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

#%% specify file path and file name

file_path = '../Output_Data/'

# variable demand
#file_name1 = '1-unmet_demand-cp0/1-unmet_demand-cp0_20200218_124557'
#legend1 = 'wind + solar + storage + natural gas'
#
#file_name2 = '2-unmet_demand-cp200/2-unmet_demand-cp200_20200216_134342'
#legend2 = 'wind + solar + storage + natural gas @ \$200/t' + '$\mathregular{CO_2}$'
#
#file_name3 = '3-unmet_demand-wind-solar-storage/3-unmet_demand-wind-solar-storage_20200216_144503'
#legend3 = 'wind + solar + storage'
#
#file_name4 = '4-unmet_demand-wind-storage/4-unmet_demand-wind-storage_20200216_154754'
#legend4 = 'wind + storage'
#
#file_name5 = '5-unmet_demand-solar-storage/5-unmet_demand-solar-storage_20200216_164608'
#legend5 = 'solar + storage'
#
#file_name6 = '6-unmet_demand-wind-solar/6-unmet_demand-wind-solar_20200216_165156'
#legend6 = 'wind + solar'
#
#file_name7 = '7-unmet_demand-solar-only/7-unmet_demand-solar-only_20200216_171908'
#legend7 = 'solar only'
#
#file_name8 = '8-unmet_demand-wind-only/8-unmet_demand-wind-only_20200216_172442'
#legend8 = 'wind only'

# constant demand
file_name1 = '1-unmet_demand_constant-cp0/1-unmet_demand-cp0_20200218_114235'
legend1 = 'wind + solar + storage + natural gas'

file_name2 = '2-unmet_demand_constant-cp200/2-unmet_demand-cp200_20200218_141812'
legend2 = 'wind + solar + storage + natural gas @ \$200/t' + '$\mathregular{CO_2}$'

file_name3 = '3-unmet_demand_constant-wind-solar-storage/3-unmet_demand_constant-wind-solar-storage_20200218_153457'
legend3 = 'wind + solar + storage'

file_name4 = '4-unmet_demand_constant-wind-storage/4-unmet_demand_constant-wind-storage_20200218_163438'
legend4 = 'wind + storage'

file_name5 = '5-unmet_demand_constant-solar-storage/5-unmet_demand_constant-solar-storage_20200218_175529'
legend5 = 'solar + storage'

file_name6 = '6-unmet_demand_constant-wind-solar/6-unmet_demand_constant-wind-solar_20200218_182400'
legend6 = 'wind + solar'

file_name7 = '7-unmet_demand_constant-solar-only/7-unmet_demand_constant-solar-only_20200218_183605'
legend7 = 'solar only'

file_name8 = '8-unmet_demand_constant-wind-only/8-unmet_demand_constant-wind-only_20200218_184040'
legend8 = 'wind only'

file_name = [file_name1, file_name2, file_name3, file_name4, 
             file_name5, file_name6, file_name7, file_name8]
legend = [legend1, legend2, legend3, legend4, 
          legend5, legend6, legend7, legend8]

directory = '../figures'
#if not os.path.exists(directory):
#    os.mkdir(directory)

#%% read results

# number of files
nfiles = len(file_name)

# results stored as lists
cost_unmet_demand = []
system_cost = []

for i in range(nfiles):
    # read data from .csv files as dataframes
        # reference: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html
    df = pd.read_csv(file_path + file_name[i] + '.csv')
    cost_unmet_demand.append(df['var cost unmet demand ($/kWh)'].values)
    system_cost.append(df['system cost ($/kW/h)'].values)
        
#%% plot results

fig, ax = plt.subplots(1,1, figsize=(3,2.5), sharex=True, sharey=False)

# line colors
colors = plt.cm.plasma(np.linspace(0,1,nfiles))

# base case
ax.semilogx(cost_unmet_demand[0], system_cost[0], 
            linestyle='--', linewidth=1, color='k')

# all other cases
for i in range(1,nfiles):
    ax.semilogx(cost_unmet_demand[i], system_cost[i], 
                linestyle='--', linewidth=1, color=colors[i-1])

#------------------------------------------------------------------------------
# plot settings

# axes
ax.set_xlim(0.01,1000)
ax.set_xticks(np.geomspace(0.01,1000,6))
ax.xaxis.set_major_formatter(FormatStrFormatter('%.6g'))
ax.set_ylim(0, 0.40)
ax.set_yticks(np.arange(0,0.45,0.05))
#ax.set_ylim(0, np.max(system_cost))
#ax.set_yticks(np.arange(0,np.max(system_cost)+0.05,0.05))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax.minorticks_off()

# axis labels and legend
xlabel = 'Cost of Unmet Demand [$/kWh]'
ylabel = 'Overall system cost [$/kWh]'
ax.set_xlabel(xlabel, fontsize=10)
ax.set_ylabel(ylabel, fontsize=10)
ax.legend(legend, frameon=False, loc='upper center', 
          bbox_to_anchor=(0.5,-0.25), fontsize=9)

#------------------------------------------------------------------------------
# save plot

#fig.savefig(file_path + 'plots/' + '3c-system cost vs. VoLL' + '.png', 
#            dpi=600, bbox_inches='tight', pad_inches=0.2)
#fig.savefig(file_path + 'plots/' + '3c-system cost vs. VoLL' + '.svg', 
#            dpi=600, bbox_inches='tight', pad_inches=0.2)

plt.show()
