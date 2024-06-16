# Locals
import oggm.cfg as cfg
from oggm import utils, workflow, tasks
from oggm.shop import gcm_climate
import logging
# Module logger
log = logging.getLogger(__name__)
from oggm import entity_task


from oggm import __version__
from oggm import entity_task
from oggm.exceptions import InvalidParamsError, InvalidWorkflowError
from oggm.core.massbalance import (MultipleFlowlineMassBalance,
                                   ConstantMassBalance,
                                   MonthlyTIModel,
                                   RandomMassBalance)
from oggm.core.centerlines import Centerline, line_order
from oggm.core.inversion import find_sia_flux_from_thickness
from oggm.core.flowline import flowline_model_run
# Constants
from oggm.cfg import SEC_IN_DAY, SEC_IN_YEAR
from oggm.cfg import G, GAUSSIAN_KERNEL
import pandas as pd
import numpy as np
import shapely.geometry as shpg
import xarray as xr
from scipy.linalg import solve_banded

# Optional libs
try:
    import salem
except ImportError:
    pass

# Builtins
import logging
import copy
from collections import OrderedDict
from functools import partial
from time import gmtime, strftime
import os
import shutil
import warnings

@entity_task(log)
def run_random_climate_prescribe_years(gdir, nyears=1000, y0=None, halfsize=15,
                       bias=0, seed=None, temperature_bias=None,
                       precipitation_factor=None,
                       store_monthly_step=False,
                       store_model_geometry=None,
                       store_fl_diagnostics=None,
                       mb_model_class=MonthlyTIModel,
                       climate_filename='climate_historical',
                       climate_input_filesuffix='',
                       output_filesuffix='', init_model_fls=None,
                       init_model_filesuffix=None,
                       init_model_yr=None,
                       zero_initial_glacier=False,
                       unique_samples=False, 
                                     prescribe_years=None,
                                     **kwargs):
    """Runs the random mass balance model for a given number of years.

    This will initialize a
    :py:class:`oggm.core.massbalance.MultipleFlowlineMassBalance`,
    and run a :py:func:`oggm.core.flowline.flowline_model_run`.

    Parameters
    ----------
    gdir : :py:class:`oggm.GlacierDirectory`
        the glacier directory to process
    nyears : int
        length of the simulation
    y0 : int
        central year of the random climate period. Has to be set!
    halfsize : int, optional
        the half-size of the time window (window size = 2 * halfsize + 1)
    bias : float
        bias of the mb model (offset to add to the MB). Default is zero.
    seed : int
        seed for the random generator. If you ignore this, the runs will be
        different each time. Setting it to a fixed seed across glaciers can
        be useful if you want to have the same climate years for all of them
    temperature_bias : float
        add a bias to the temperature timeseries (note that this is added
        to any bias that the calibration decided is needed)
    precipitation_factor: float
        multiply a factor to the precipitation time series (note that
        this factor is multiplied to any factor that was decided during
        calibration or by global parameters)
    store_monthly_step : bool
        whether to store the diagnostic data at a monthly time step or not
        (default is yearly)
    store_model_geometry : bool
        whether to store the full model geometry run file to disk or not.
        (new in OGGM v1.4.1: default is to follow
        cfg.PARAMS['store_model_geometry'])
    store_fl_diagnostics : bool
        whether to store the model flowline diagnostics to disk or not.
        (default is to follow cfg.PARAMS['store_fl_diagnostics'])
    mb_model_class : MassBalanceModel class
        The MassBalanceModel class to use inside the RandomMassBalance (default
        MonthlyTIModel)
    climate_filename : str
        name of the climate file, e.g. 'climate_historical' (default) or
        'gcm_data'
    climate_input_filesuffix: str
        filesuffix for the input climate file
    output_filesuffix : str
        this add a suffix to the output file (useful to avoid overwriting
        previous experiments)
    init_model_filesuffix : str
        if you want to start from a previous model run state. Can be
        combined with `init_model_yr`
    init_model_yr : int
        the year of the initial run you want to start from. The default
        is to take the last year of the simulation.
    init_model_fls : []
        list of flowlines to use to initialise the model (the default is the
        present_time_glacier file from the glacier directory)
    zero_initial_glacier : bool
        if true, the ice thickness is set to zero before the simulation
    unique_samples: bool
        if true, chosen random mass balance years will only be available once
        per random climate period-length
        if false, every model year will be chosen from the random climate
        period with the same probability
    kwargs : dict
        kwargs to pass to the FluxBasedModel instance
    """

    mb_model = MultipleFlowlineMassBalance(gdir,
                                           mb_model_class=partial(
                                               RandomMassBalance,
                                               mb_model_class=mb_model_class),
                                           y0=y0, halfsize=halfsize,
                                           bias=bias, seed=seed,
                                           filename=climate_filename,
                                           input_filesuffix=climate_input_filesuffix,
                                           unique_samples=unique_samples,
                                           prescribe_years=prescribe_years) ### THIS HAS CHANGED!!!

    if temperature_bias is not None:
        mb_model.temp_bias += temperature_bias
    if precipitation_factor is not None:
        mb_model.prcp_fac *= precipitation_factor

    return flowline_model_run(gdir, output_filesuffix=output_filesuffix,
                              mb_model=mb_model, ys=0, ye=nyears,
                              store_monthly_step=store_monthly_step,
                              store_model_geometry=store_model_geometry,
                              store_fl_diagnostics=store_fl_diagnostics,
                              init_model_filesuffix=init_model_filesuffix,
                              init_model_yr=init_model_yr,
                              init_model_fls=init_model_fls,
                              zero_initial_glacier=zero_initial_glacier,
                              **kwargs)

@entity_task(log)
def run_hydro_from_2000_ref_area_2000_hist_w5e5_w_overshot_stab_scenarios(gdir, 
                                                                          scenarios=['stab_T15',
                                                                                     'oversh_T20OS15',
                                                                                     'oversh_T25OS15',
                                                                                     'oversh_T30OS15',
                                                                                     'stab_T20',
                                                                                     'stab_T25',
                                                                                     'stab_T30'],
                                                                         run_steady_state=False):
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
    if run_steady_state:
        store_monthly_hydro = False
        prescribe_years = pd.Series(data=np.tile(np.arange(2399,2500,1),200),
                                    index=np.arange(0,20200,1)) #np.tile(np.arange(2399,2500,1),200))
    else:
        store_monthly_hydro = True
        prescribe_years = False
    for scenario in scenarios:
        if not run_steady_state:
            rid = f'_gfdl-esm2m_{scenario}_endyr_2500_bc_2000_2019'
            tasks.run_with_hydro(gdir,
                     run_task=tasks.run_from_climate_data,
                                 ys=2020, # this is important! Start from 2020 glacier
                                 ye=2499, # ISSUE -> here I used as end year 2499, although I could actually have run it until 2500??? 
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
                 store_monthly_hydro=store_monthly_hydro);
        utils.merge_consecutive_run_outputs(gdir,
                                input_filesuffix_1='_historical_from_2000_run',
                                input_filesuffix_2=f'_future_run{rid}',
                                output_filesuffix=f'_merged_from_2000_run{rid}',
                                delete_input=False,
                               ) # we will delete that later
        if run_steady_state:
            rid_steady_state = f'_gfdl-esm2m_stab_T15_endyr_2500_bc_1980_2019'
            rid_output = f'_gfdl-esm2m_stab_T15_initial_{scenario}_bc_1980_2019'
            run_random_climate_prescribe_years(gdir, nyears=20200, # 101-year period repeat ... 
                                               y0=2449, halfsize=50,
                         init_model_yr=2499,
                           seed=42,
                           climate_filename='gcm_data',
                             # use the chosen scenario
                             climate_input_filesuffix=rid_steady_state,
                             # we start from the previous run, 
                             init_model_filesuffix=f'_future_run{rid}',
                            output_filesuffix=f'_steady_state_random_run_2399_2499{rid_output}',
                                          unique_samples=True, prescribe_years=prescribe_years)
    if run_steady_state:
        rid_steady_state = f'_gfdl-esm2m_stab_T15_endyr_2500_bc_1980_2019'
        rid_output = f'_gfdl-esm2m_stab_T15_initial_zero_bc_1980_2019'
        run_random_climate_prescribe_years(gdir, nyears=20200, # 101-year period repeat ... 
                                           y0=2449, halfsize=50,
                                         init_model_yr=2499,
                                           seed=42,
                                           climate_filename='gcm_data',
                                             # use the chosen scenario
                                             climate_input_filesuffix=rid_steady_state,
                                             # we start from ZERO!!!
                                            zero_initial_glacier=True,
                                            output_filesuffix=f'_steady_state_random_run_2399_2499{rid_output}',
                                                          unique_samples=True, prescribe_years=prescribe_years)
