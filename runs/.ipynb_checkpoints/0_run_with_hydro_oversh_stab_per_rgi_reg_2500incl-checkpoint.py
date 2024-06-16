import os
import logging 
import sys

# Libs
import xarray as xr
import pandas as pd
import numpy as np
import geopandas as gpd
import matplotlib.pyplot as plt

# Locals
import oggm.cfg as cfg
from oggm import utils, workflow, tasks
# from oggm.shop import gcm_climate
import logging
# Module logger
log = logging.getLogger(__name__)
from oggm import entity_task

from func_add_2500incl import run_hydro_from_2000_ref_area_2000_hist_w5e5_w_overshot_stab_scenarios


# normally from oggm.shop.gcm_climate import process_cmip_data
# but the changes are not yet updated ...
from oggm.shop.gcm_climate import process_gcm_data, process_cmip_data

# will run the stabilisation scenario separately 
run_steady_state = False
only_stab = False
if only_stab:
    scenarios = ['stab_T12']
elif run_steady_state:
    scenarios = ['stab_T15','oversh_T30OS15']
else:
    scenarios = ['stab_T12',
                 'stab_T15',
                 'oversh_T20OS15',
                 'oversh_T25OS15',
                 'oversh_T30OS15',
                 'stab_T20',
                 'stab_T25',
                 'stab_T30']

###########
    
# Initialize OGGM and set up the default run parameters
cfg.initialize(logging_level='ERROR')
rgi_version = '62'

cfg.PARAMS['border'] = 160 # changed for OGGM v16

# I got a strange KeyError: 'dl_verify_data_cluster.klima.uni-bremen.de' (only for RGI reg 03 and  'gfdl-esm4' 'ssp370')
cfg.PARAMS['dl_verify'] = False 
cfg.PARAMS['continue_on_error'] = True
cfg.PARAMS['use_multiprocessing']=True
cfg.PARAMS['store_model_geometry'] = True
           
# Local working directory (where OGGM will write its output)
WORKING_DIR = os.environ.get('OGGM_WORKDIR', '')
if not WORKING_DIR:
    raise RuntimeError('Need a working dir')
utils.mkdir(WORKING_DIR)
cfg.PATHS['working_dir'] = WORKING_DIR

OUTPUT_DIR = os.environ.get('OGGM_OUTDIR', '')
if not OUTPUT_DIR:
    raise RuntimeError('Need an output dir')
utils.mkdir(OUTPUT_DIR)


rgi_reg = str(sys.argv[1])

OGGM_GLACIER_JOB = os.environ.get('OGGM_GLACIER_JOB', '')
test = False
if test:
    n_glacier=32
else:
    n_glacier = 1000
id0 = (int(OGGM_GLACIER_JOB)-1)*n_glacier
id1 = (int(OGGM_GLACIER_JOB))*n_glacier
print(id0,id1)


#if rgi_reg not in ['{:02d}'.format(r) for r in range(1, 20)]:
#    raise RuntimeError('Need an RGI Region')

# Module logger
log = logging.getLogger(__name__)
log.workflow(f'Starting run for RGI reg {rgi_reg}: glaciers [{id0}:{id1}]')    

# RGI glaciers
rgi_ids = gpd.read_file(utils.get_rgi_region_file(rgi_reg, version=rgi_version))
if rgi_reg == '05':
    log.workflow('Remove connectivity 2  glaciers')
    rgi_ids = rgi_ids.loc[(rgi_ids['Connect'] == 0) | (rgi_ids['Connect'] ==1)]
rgi_ids = rgi_ids[id0:id1]    


# Go - get the pre-processed glacier directories
# TODO -> need to change the preprocessed directory to that here when it is available ... 
base_url = 'https://cluster.klima.uni-bremen.de/~oggm/gdirs/oggm_v1.6/L3-L5_files/2023.3/elev_bands/W5E5_spinup/'
# old v2023.1 version: base_url = 'https://cluster.klima.uni-bremen.de/~oggm/gdirs/oggm_v1.6/L3-L5_files/2023.1/elev_bands/W5E5_spinup'
gdirs = workflow.init_glacier_directories(rgi_ids, from_prepro_level=5, prepro_border=160,
                                          prepro_base_url=base_url, prepro_rgi_version=rgi_version)

if run_steady_state:
    ALL_DIAGS = ['volume','area']
else:
    ALL_DIAGS = ['volume', 'volume_bsl', #'volume_bwl',
                 'area', 'length',  'calving', 'calving_rate',
                 'off_area', 'on_area', 'melt_off_glacier',
                 'melt_on_glacier', 'liq_prcp_off_glacier', 'liq_prcp_on_glacier',
                 'snowfall_off_glacier', 'snowfall_on_glacier', 'model_mb',
                 'residual_mb', 'snow_bucket']
# Add debug vars
cfg.PARAMS['store_diagnostic_variables'] = ALL_DIAGS

gdirs = workflow.init_glacier_directories(rgi_ids, from_prepro_level=5, prepro_border=160,
                                              prepro_base_url=base_url, prepro_rgi_version=rgi_version)


dir_path = 'https://cluster.klima.uni-bremen.de/~lschuster/provide/gfdl-esm2m_oversh_stab_uni_bern/flat/2023.2'

for scenario in scenarios:

    fp = f'{dir_path}/gfdl-esm2m_{scenario}_pr_global_monthly_flat_glaciers.nc'
    ft = f'{dir_path}/gfdl-esm2m_{scenario}_tas_global_monthly_flat_glaciers.nc'
    ft = utils.file_downloader(ft)
    fp = utils.file_downloader(fp)
    if not run_steady_state:
        rid = f'_gfdl-esm2m_{scenario}_endyr_2500_bc_2000_2019'
        workflow.execute_entity_task(process_cmip_data, gdirs, 
                                     filesuffix=rid,  # recognize the climate file for later
                                     fpath_temp=ft,  # temperature projections
                                     fpath_precip=fp,  # precip projections
                                     year_range=('2000', '2019'),
                                     y0=2000-10,y1=2501) # new this makes the processing a bit faster

    rid = f'_gfdl-esm2m_{scenario}_endyr_2500_bc_1980_2019'
    workflow.execute_entity_task(process_cmip_data, gdirs, 
                                 filesuffix=rid,  # recognize the climate file for later
                                 fpath_temp=ft,  # temperature projections
                                 fpath_precip=fp,  # precip projections
                                 year_range=('1980', '2019'),
                                 y0=1980-20,y1=2501,  # new this makes the processing a bit faster
                                 )
    
workflow.execute_entity_task(run_hydro_from_2000_ref_area_2000_hist_w5e5_w_overshot_stab_scenarios, gdirs, scenarios=scenarios, run_steady_state=run_steady_state)

# compile and store run output
eq_dir = os.path.join(OUTPUT_DIR, 'RGI' + rgi_reg)
utils.mkdir(eq_dir)
for scenario in scenarios:
    if not run_steady_state:
        rid = f'_gfdl-esm2m_{scenario}_endyr_2500_bc_2000_2019'
        utils.compile_run_output(gdirs, input_filesuffix=f'_merged_from_2000_run{rid}', 
                                path=os.path.join(eq_dir, f'run_hydro_w5e5_gcm_merged_from_2000{rid}_rgi{rgi_reg}_{id0}_{id1}.nc'))
    
        rid = f'_gfdl-esm2m_{scenario}_endyr_2500_bc_1980_2019'
        utils.compile_run_output(gdirs, input_filesuffix=f'_merged_from_2000_run{rid}', 
                                path=os.path.join(eq_dir, f'run_hydro_w5e5_gcm_merged_from_2000{rid}_rgi{rgi_reg}_{id0}_{id1}.nc'))
 
    elif run_steady_state:
        rid_output = f'_gfdl-esm2m_stab_T15_initial_{scenario}_bc_1980_2019'
        utils.compile_run_output(gdirs, input_filesuffix=f'_steady_state_random_run_2400_2500{rid_output}', 
                            path=os.path.join(eq_dir, f'run_random_climate_from2500_using2400_2500{rid_output}_rgi{rgi_reg}_{id0}_{id1}.nc'))

if run_steady_state:
    rid_output = f'_gfdl-esm2m_stab_T15_initial_zero_bc_1980_2019'
    utils.compile_run_output(gdirs, input_filesuffix=f'_steady_state_random_run_2400_2500{rid_output}', 
                            path=os.path.join(eq_dir, f'run_random_climate_from2500_using2400_2500{rid_output}_rgi{rgi_reg}_{id0}_{id1}.nc'))  
    
log.workflow('OGGM Done')