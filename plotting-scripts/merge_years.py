"""
    Create merged csv output file that takes values from SEM runs over multiple
    years and averages them.
    For example if we run wind only for 2016, 2017, and 2018 we will create a 
    merged file averaging all three system capacities for each price cap value
"""

import numpy as np
import pandas as pd
from glob import glob

years = [2016, 2017, 2018, 2019, 2020]

def get_output_files(f_base):

    #print(f_base+'*.csv')
    files = glob(f_base+'*.csv')
    #print(files)
    assert(len(files) == 1)
    return files[0]

def merge_files(scenario, f_names):

    for i, f in enumerate(f_names):
        print(i)
        if i == 0:
            master = pd.read_csv(f, index_col='case name')
            master = master.drop(columns=['problem status',])
            #print("Master")
            #print(master.head())
        else:
            df = pd.read_csv(f, index_col='case name')
            df = df.drop(columns=['problem status',])
            #print("New DF")
            #print(df.head())
            master = master + df
            #print("Updated Master")
            #print(master.head())

    master = master / float(len(f_names)) # float to make sure there's no Int rounding

    #print(master.head())
    print(master.shape)

    master.to_csv(f'../Output_Data/aggregates/{scenario}_2015-2020.csv')
    return master


scenarios = [
        "1-input_unmet_demand-constant-cp0",
        "1-input_unmet_demand-cp0",
        "2-input_unmet_demand-constant-cp200",
        "2-input_unmet_demand-cp200",
        "3-input_unmet_demand-constant-wind-solar-storage",
        "3-input_unmet_demand-wind-solar-storage",
        "4-input_unmet_demand-constant-wind-storage",
        "4-input_unmet_demand-wind-storage",
        "5-input_unmet_demand-constant-solar-storage",
        "5-input_unmet_demand-solar-storage",
        "6-input_unmet_demand-constant-wind-solar",
        "6-input_unmet_demand-wind-solar",
        "7-input_unmet_demand-constant-solar",
        "7-input_unmet_demand-solar",
        "8-input_unmet_demand-constant-wind",
        "8-input_unmet_demand-wind",
        ]

for storage in ["0.01", "0.1", "1", "10", "100"]:
    scenarios.append(f"10-input_unmet_demand-solar-storage{storage}")
    scenarios.append(f"9-input_unmet_demand-wind-solar-storage{storage}")
        

for scenario in scenarios:
    print(scenario)
    f_names = []
    base = f'../Output_Data/{scenario}_'
    start_year = 2015
    for year in years:
    
        yr_string = str(start_year)+'-'+str(year)
        f_try = base+yr_string+f'/{scenario}_'+yr_string+'_2020'
        f_names.append( get_output_files(f_try) )
        start_year = year   # for next iteration
    
    merge_files(scenario, f_names)
