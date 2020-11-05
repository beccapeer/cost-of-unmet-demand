
BASE_CASE=input_unmet_demand_base_case.csv


# These are in the order of:
# - FIXED_COST_SOLAR,
# - FIXED_COST_WIND,
# - FIXED_COST_NATGAS,
# - FIXED_COST_STORAGE,
# Setting 1 --> -1 will turn off that tech
VARS="1,1,1,1,,"


# Changing the DEMAND_FILE will change the demand file
DEMAND_FILE="US_demand_unnormalized.csv"
CONSTANT_DEMAND="US_constant_demand_unnormalized.csv"

# Changing the CO2 pring
CO2_ZERO="CO2_PRICE,0"
CO2_200="CO2_PRICE,200"

# Use sed to find and replace text in the base case file to make exact copies of each
# file with only the precise alterations we want
# $ sed -i 's/old-text/new-text/g' base_case.csv


#CASE="1-input_unmet_demand-cp0"
#sed "s/UPDATE_GLOBAL_NAME/${CASE}/g" $BASE_CASE > $CASE.csv
#
#CASE="1-input_unmet_demand_constant-cp0"
#sed "s/UPDATE_GLOBAL_NAME/${CASE}/g; s/${DEMAND_FILE}/${CONSTANT_DEMAND}/g" $BASE_CASE > $CASE.csv
#
#
#
#
#CASE="2-input_unmet_demand-cp200"
#sed "s/UPDATE_GLOBAL_NAME/${CASE}/g; s/${CO2_ZERO}/${CO2_200}/g" $BASE_CASE > $CASE.csv
#
#CASE="2-input_unmet_demand_constant-cp200"
#sed "s/UPDATE_GLOBAL_NAME/${CASE}/g; s/${CO2_ZERO}/${CO2_200}/g; s/${DEMAND_FILE}/${CONSTANT_DEMAND}/g" $BASE_CASE > $CASE.csv
#
#
#
#
#CASE="3-input_unmet_demand-wind-solar-storage"
#sed "s/UPDATE_GLOBAL_NAME/${CASE}/g; s/${VARS}/1,1,-1,1,,/g" $BASE_CASE > $CASE.csv
#
#CASE="3-input_unmet_demand-constant-wind-solar-storage"
#sed "s/UPDATE_GLOBAL_NAME/${CASE}/g; s/${VARS}/1,1,-1,1,,/g; s/${DEMAND_FILE}/${CONSTANT_DEMAND}/g" $BASE_CASE > $CASE.csv
#
#
#
#
#CASE="4-input_unmet_demand-wind-storage"
#sed "s/UPDATE_GLOBAL_NAME/${CASE}/g; s/${VARS}/-1,1,-1,1,,/g" $BASE_CASE > $CASE.csv
#
#CASE="4-input_unmet_demand-constant-wind-storage"
#sed "s/UPDATE_GLOBAL_NAME/${CASE}/g; s/${VARS}/-1,1,-1,1,,/g; s/${DEMAND_FILE}/${CONSTANT_DEMAND}/g" $BASE_CASE > $CASE.csv
#
#
#
#
#CASE="5-input_unmet_demand-solar-storage"
#sed "s/UPDATE_GLOBAL_NAME/${CASE}/g; s/${VARS}/1,-1,-1,1,,/g" $BASE_CASE > $CASE.csv
#
#CASE="5-input_unmet_demand-constant-solar-storage"
#sed "s/UPDATE_GLOBAL_NAME/${CASE}/g; s/${VARS}/1,-1,-1,1,,/g; s/${DEMAND_FILE}/${CONSTANT_DEMAND}/g" $BASE_CASE > $CASE.csv
#
#
#
#
#CASE="6-input_unmet_demand-wind-solar"
#sed "s/UPDATE_GLOBAL_NAME/${CASE}/g; s/${VARS}/1,1,-1,-1,,/g" $BASE_CASE > $CASE.csv
#
#CASE="6-input_unmet_demand-constant-wind-solar"
#sed "s/UPDATE_GLOBAL_NAME/${CASE}/g; s/${VARS}/1,1,-1,-1,,/g; s/${DEMAND_FILE}/${CONSTANT_DEMAND}/g" $BASE_CASE > $CASE.csv
#
#
#
#
#CASE="7-input_unmet_demand-solar"
#sed "s/UPDATE_GLOBAL_NAME/${CASE}/g; s/${VARS}/1,-1,-1,-1,,/g" $BASE_CASE > $CASE.csv
#
#CASE="7-input_unmet_demand-constant-solar"
#sed "s/UPDATE_GLOBAL_NAME/${CASE}/g; s/${VARS}/1,-1,-1,-1,,/g; s/${DEMAND_FILE}/${CONSTANT_DEMAND}/g" $BASE_CASE > $CASE.csv
#
#
#
#
#CASE="8-input_unmet_demand-wind"
#sed "s/UPDATE_GLOBAL_NAME/${CASE}/g; s/${VARS}/-1,1,-1,-1,,/g" $BASE_CASE > $CASE.csv
#
#CASE="8-input_unmet_demand-constant-wind"
#sed "s/UPDATE_GLOBAL_NAME/${CASE}/g; s/${VARS}/-1,1,-1,-1,,/g; s/${DEMAND_FILE}/${CONSTANT_DEMAND}/g" $BASE_CASE > $CASE.csv

## wind+solar+storage varying storage costs to range from ~wind+solar system to wind+solar+cheap storage
#for SF in 100 10 1 0.1 0.01; do
#    CASE="9-input_unmet_demand-wind-solar-storage${SF}"
#    sed "s/UPDATE_GLOBAL_NAME/${CASE}/g; s/${VARS}/1,1,-1,${SF},,/g" $BASE_CASE > $CASE.csv
#done
#
## solar+storage varying storage costs to range from ~wind+solar system to wind+solar+cheap storage
#for SF in 100 10 1 0.1 0.01; do
#    CASE="10-input_unmet_demand-solar-storage${SF}"
#    sed "s/UPDATE_GLOBAL_NAME/${CASE}/g; s/${VARS}/1,-1,-1,${SF},,/g" $BASE_CASE > $CASE.csv
#done

## Test multiple years of data
for YEAR in 2016 2017 2018; do
    CASE="8-input_unmet_demand-wind_${YEAR}"
    sed "s/UPDATE_GLOBAL_NAME/${CASE}/g; s/${VARS}/-1,1,-1,-1,,/g; s/_YEAR,2018/_YEAR,${YEAR}/g" $BASE_CASE > $CASE.csv
done

