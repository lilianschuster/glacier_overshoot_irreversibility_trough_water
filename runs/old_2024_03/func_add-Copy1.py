# Locals
import oggm.cfg as cfg
from oggm import utils, workflow, tasks
from oggm.shop import gcm_climate
import logging
# Module logger
log = logging.getLogger(__name__)
from oggm import entity_task

@entity_task(log)
def run_hydro_from_2000_ref_area_2000_hist_w5e5_w_overshot_stab_scenarios(gdir, 
                                                                          scenarios=['stab_T15',
                                                                                     'oversh_T20OS15',
                                                                                     'oversh_T25OS15',
                                                                                     'oversh_T30OS15',
                                                                                     'stab_T20',
                                                                                     'stab_T25',
                                                                                     'stab_T30']):
    '''
    Runs historical hydro climate from 2000 until 2020 using W5E5. 
    Finally the future projections from 2020 until 2500 for the scenarios are done. 
    The ref_area_yr is 2000. Here, the bias correction had been done once from 2000-2019 and
    once from 1980-2019
    
    '''
    tasks.run_with_hydro(gdir, run_task=tasks.run_from_climate_data,
                     climate_filename='climate_historical',
                     ys=2000, init_model_yr=2000,
                     store_monthly_hydro=True,
                     init_model_filesuffix='_spinup_historical',
                     ref_geometry_filesuffix='_spinup_historical',
                     ref_area_yr = 2000,
                     output_filesuffix='_historical_from_2000_run')
    
    for scenario in scenarios:
        rid = f'_gfdl-esm2m_{scenario}_endyr_2500_bc_2000_2019'
        tasks.run_with_hydro(gdir,
                 run_task=tasks.run_from_climate_data,
                             ys=2020, # this is important! Start from 2020 glacier
                             ye=2499,
                 # use gcm_data, not climate_historical
                 climate_filename='gcm_data',
                 # use the chosen scenario
                 climate_input_filesuffix=rid,
                 # we start from the previous run, 
                 init_model_filesuffix='_historical_from_2000_run',
                 ref_geometry_filesuffix='_historical_from_2000_run', 
                 ref_area_yr = 2000,
                 # recognize the run for later
                 output_filesuffix=f'_future_run{rid}',
                 # add monthly diagnostics
                 store_monthly_hydro=True);


        utils.merge_consecutive_run_outputs(gdir,
                                input_filesuffix_1='_historical_from_2000_run',
                                input_filesuffix_2=f'_future_run{rid}',
                                output_filesuffix=f'_merged_from_2000_run{rid}',
                                delete_input=False,
                               ) # we will delete that later
        
      
        rid = f'_gfdl-esm2m_{scenario}_endyr_2500_bc_1980_2019'
        tasks.run_with_hydro(gdir,
                 run_task=tasks.run_from_climate_data,
                             ys=2020, # this is important! Start from 2020 glacier
                             ye=2499,
                 # use gcm_data, not climate_historical
                 climate_filename='gcm_data',
                 # use the chosen scenario
                 climate_input_filesuffix=rid,
                 # we start from the previous run, 
                 init_model_filesuffix='_historical_from_2000_run',
                 ref_geometry_filesuffix='_historical_from_2000_run', 
                 ref_area_yr = 2000,
                 # recognize the run for later
                 output_filesuffix=f'_future_run{rid}',
                 # add monthly diagnostics
                 store_monthly_hydro=True);
        utils.merge_consecutive_run_outputs(gdir,
                                input_filesuffix_1='_historical_from_2000_run',
                                input_filesuffix_2=f'_future_run{rid}',
                                output_filesuffix=f'_merged_from_2000_run{rid}',
                                delete_input=False,
                               ) # we will delete that later