"""
file name: plot_elec_cost_vs_reliability.py
    plot cost of electricity against corresponding reliability 
    (= fraction of demand met) for all cases
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

file_name1 = '1-unmet_demand-cp0/1-unmet_demand-cp0_20190226_221554'
legend1 = 'wind + solar + storage + natural gas (base case)'

file_name2 = '2-unmet_demand-cp200/2-unmet_demand-cp200_20190227_020128'
legend2 = 'wind + solar + storage + natural gas @ \$200/t' + '$\mathregular{CO_2}$'

file_name3 = '3-unmet_demand-wind-solar-storage/3-unmet_demand-wind-solar-storage_20190227_101927'
legend3 = 'wind + solar + storage'

file_name4 = '4-unmet_demand-wind-storage/4-unmet_demand-wind-storage_20190227_000042'
legend4 = 'wind + storage'

file_name5 = '5-unmet_demand-solar-storage/5-unmet_demand-solar-storage_20190227_121954'
legend5 = 'solar + storage'

file_name6 = '6-unmet_demand-wind-solar/6-unmet_demand-wind-solar_20190226_223652'
legend6 = 'wind + solar'

file_name = [file_name1, file_name2, file_name3, 
             file_name4, file_name5, file_name6]
legend = [legend1, legend2, legend3, legend4, legend5, legend6]

directory = file_path + 'plots'
if not os.path.exists(directory):
    os.mkdir(directory)

#%% read results

# number of files
nfiles = len(file_name)

# results stored as lists
cost_unmet_demand = []
system_cost = []
demand = []
unmet_demand = []

for i in range(nfiles):
    # read data from .csv files as dataframes
        # reference: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html
    df = pd.read_csv(file_path + file_name[i] + '.csv')
    cost_unmet_demand.append(df['var cost unmet demand ($/kWh)'].values)
    system_cost.append(df['system cost ($/kW/h)'].values)
    demand.append(df['mean demand (kW)'].values)
    unmet_demand.append(df['dispatch unmet demand (kW)'].values)

#%% calculations
        
# reliability (fraction of demand met)
reliability = 1 - np.array(unmet_demand)/np.array(demand)

# economic damage from not meeting demand
loss_unmet_demand = np.array(cost_unmet_demand) * np.array(unmet_demand)

# cost of electricity 
# (equivalent to LCOE, system cost minus cost of not meeting demand)
elec_cost = np.array(system_cost) - loss_unmet_demand

#%% plot results

fig, ax = plt.subplots(1,1, figsize=(3,2.5), sharex=False, sharey=False)
plt.subplots_adjust(hspace=0.3)

# line colors
colors = plt.cm.plasma(np.linspace(0,1,nfiles))

#------------------------------------------------------------------------------
# x-axis (reliability) on logarithmic scale
# y-axis (electricity cost) on linear scale

# base case
ax.semilogx(100*(1-reliability[0,:]), elec_cost[0,:], 
            linestyle='-', linewidth=1.8, color='k')

# all other cases
for i in range(1,nfiles):
    ax.semilogx(100*(1-reliability[i,:]), elec_cost[i,:], 
                linestyle='--', linewidth=1, color=colors[i-1])

#------------------------------------------------------------------------------
# plot settings

# axes
ax.set_xlim(0.001,100)
ax.invert_xaxis()
xtick_pos = [100,10,1,0.1,0.01,0.001]    # 1 - reliability
ax.set_xticks(xtick_pos)
# set x-axis tick labels
xtick_labels = []
for x in xtick_pos:
    xtick_labels.append('%.6g' % (100 - x))    # reliability
ax.set_xticklabels(xtick_labels)
ax.set_ylim(0, np.max(elec_cost))
ax.set_yticks(np.arange(0,np.max(elec_cost)+0.05,0.05))
ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
ax.minorticks_off()

# axis labels and legend
xlabel = 'Reliability [% demand met]'
ylabel = 'Cost of electricity [$/kWh]'
ax.set_xlabel(xlabel, fontsize=10)
ax.set_ylabel(ylabel, fontsize=10)
ax.legend(legend, frameon=False, loc='upper center', 
          bbox_to_anchor=(0.5,-0.25), fontsize=9)

#------------------------------------------------------------------------------
# save plot

#fig.savefig(file_path + 'plots/' + '2b-elec cost vs. reliability' + '.png', 
#            dpi=600, bbox_inches='tight', pad_inches=0.2)
#fig.savefig(file_path + 'plots/' + '2b-elec cost vs. reliability' + '.svg', 
#            dpi=600, bbox_inches='tight', pad_inches=0.2)

plt.show()
