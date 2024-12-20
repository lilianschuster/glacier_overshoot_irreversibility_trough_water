# Preprocessing, glacier projection runs and postprocessing workflows

We projected global glacier changes under OGGM v1.6.1 with the GFDL-ESM2M Earth System Model from 2000 to 2500 under five stabilisation and three overshoot scenarios. We also made extended projections for an additional 10,000 years by applying a random climate from the years 2399 to 2499. 

In this document, we describe the scripts and notebooks for the climate data preprocessing, the OGGM runs, and the postprocessing workflows. 

We applied two bias correction options aggregated separately, but in the manuscript, only `_bc_1980_2019` is used. 
   - `_bc_1980_2019` (default approach, considered period for bias correction is 1980--2019)
   - `_bc_2000_2019` (considered period for bias correction is 2000--2019)

The raw data that is not in Zenodo is available under https://cluster.klima.uni-bremen.de/~lschuster/provide/gfdl-esm2m_oversh_stab_uni_bern/data/additional_data. All files and described folders are in https://cluster.klima.uni-bremen.de/~lschuster/provide/gfdl-esm2m_oversh_stab_uni_bern/. 

## 1. Flatten GFDL-ESM2M ESM climate datasets
creates GFDL-ESM2M climate data that are flattened (i.e., reducing the dimension from lon, lat to a merged lon_lat dimension and only selecting those grid points near glaciers). We do this to speed up the climate extraction during the OGGM runs. 

Run in the terminal in the OGGM cluster:
- e.g. `A_runs_pre_postprocessing/flattened_gfdl_esm2m/sbatch slurm_flatten_oversh_stab_monthly.slurm stab_T12`
    - The slurm files executes this python script:
        - `A_runs_pre_postprocessing/flattened_gfdl_esm2m/flatten_oversh_stab_monthly_files.py`
  

## 2. Global OGGM glacier projections runs (with flattened files)
- execute the following python script...
    - [A_runs_pre_postprocessing/00_run_with_hydro_oversh_stab_per_rgi_reg_2500incl.py](A_runs_pre_postprocessing/00_run_with_hydro_oversh_stab_per_rgi_reg_2500incl.py)
        - uses internally [A_runs_pre_postprocessing/00_func_add_2500incl.py](A_runs_pre_postprocessing/00_func_add_2500incl.py)
- via slurm in the cluster:
    ```
        sbatch --array=1-28 slurm_run_with_hydro_2500incl.slurm 01 'until 2500'
        sbatch --array=1-19 slurm_run_with_hydro_2500incl.slurm 02 'until 2500'
        sbatch --array=1-5 slurm_run_with_hydro_2500incl.slurm 03 'until 2500'
        sbatch --array=1-8 slurm_run_with_hydro_2500incl.slurm 04 'until 2500'
        sbatch --array=1-21 slurm_run_with_hydro_2500incl.slurm 05 'until 2500'
        sbatch --array=1-1 slurm_run_with_hydro_2500incl.slurm 06 'until 2500'
        sbatch --array=1-2 slurm_run_with_hydro_2500incl.slurm 07 'until 2500'
        sbatch --array=1-4 slurm_run_with_hydro_2500incl.slurm 08 'until 2500'
        sbatch --array=1-2 slurm_run_with_hydro_2500incl.slurm 09 'until 2500'
        sbatch --array=1-6 slurm_run_with_hydro_2500incl.slurm 10 'until 2500'
        sbatch --array=1-4 slurm_run_with_hydro_2500incl.slurm 11 'until 2500'
        sbatch --array=1-2 slurm_run_with_hydro_2500incl.slurm 12 'until 2500'
        sbatch --array=1-55 slurm_run_with_hydro_2500incl.slurm 13 'until 2500'
        sbatch --array=1-28 slurm_run_with_hydro_2500incl.slurm 14 'until 2500'
        sbatch --array=1-14 slurm_run_with_hydro_2500incl.slurm 15 'until 2500'
        sbatch --array=1-3 slurm_run_with_hydro_2500incl.slurm 16 'until 2500'
        sbatch --array=1-16 slurm_run_with_hydro_2500incl.slurm 17 'until 2500'
        sbatch --array=1-4 slurm_run_with_hydro_2500incl.slurm 18 'until 2500'
        sbatch --array=1-3 slurm_run_with_hydro_2500incl.slurm 19 'until 2500'
    ```
- raw OGGM output in 1000 glacier batches is saved as netCDF files in the folders RGIXX under https://cluster.klima.uni-bremen.de/~lschuster/provide/gfdl-esm2m_oversh_stab_uni_bern/A_runs_pre_postprocessing/output/
    - e.g in https://cluster.klima.uni-bremen.de/~lschuster/provide/gfdl-esm2m_oversh_stab_uni_bern/A_runs_pre_postprocessing/output/RGI03/run_hydro_w5e5_gcm_merged_from_2000_gfdl-esm2m_oversh_T20OS15_endyr_2500_bc_1980_2019_rgi03_0_1000.nc

## 3. Repeat global OGGM glacier projections under a random climate of the years 2399-2499 for 10000 additional years
- repeat what we did in Sect. 2, but run for 10000 years. For that execute the following python script again... 
    - [A_runs_pre_postprocessing/00_run_with_hydro_oversh_stab_per_rgi_reg_2500incl.py](A_runs_pre_postprocessing/00_run_with_hydro_oversh_stab_per_rgi_reg_2500incl.py)
        - uses among others internally `run_random_climate_prescribe_years` defined in  [A_runs_pre_postprocessing/00_func_add_2500incl.py](A_runs_pre_postprocessing/00_func_add_2500incl.py)

- via slurm in the cluster:
    ```
    sbatch --array=1-28 slurm_run_with_hydro_2500incl.slurm 01 'runs_steady_state'
    sbatch --array=1-19 slurm_run_with_hydro_2500incl.slurm 02 'runs_steady_state'
    sbatch --array=1-5 slurm_run_with_hydro_2500incl.slurm 03 'runs_steady_state' 
    sbatch --array=1-8 slurm_run_with_hydro_2500incl.slurm 04 'runs_steady_state'
    sbatch --array=1-21 slurm_run_with_hydro_2500incl.slurm 05 'runs_steady_state'
    sbatch --array=1-1 slurm_run_with_hydro_2500incl.slurm 06 'runs_steady_state'
    sbatch --array=1-2 slurm_run_with_hydro_2500incl.slurm 07 'runs_steady_state'
    sbatch --array=1-4 slurm_run_with_hydro_2500incl.slurm 08 'runs_steady_state'
    sbatch --array=1-2 slurm_run_with_hydro_2500incl.slurm 09 'runs_steady_state'
    sbatch --array=1-6 slurm_run_with_hydro_2500incl.slurm 10 'runs_steady_state'

    sbatch --array=1-4 slurm_run_with_hydro_2500incl.slurm 11 'runs_steady_state'
    sbatch --array=1-2 slurm_run_with_hydro_2500incl.slurm 12 'runs_steady_state'
    sbatch --array=1-55 slurm_run_with_hydro_2500incl.slurm 13 'runs_steady_state'

    sbatch --array=1-28 slurm_run_with_hydro_2500incl.slurm 14 'runs_steady_state'
    sbatch --array=1-14 slurm_run_with_hydro_2500incl.slurm 15 'runs_steady_state'
    sbatch --array=1-3 slurm_run_with_hydro_2500incl.slurm 16 'runs_steady_state'
    sbatch --array=1-16 slurm_run_with_hydro_2500incl.slurm 17 'runs_steady_state'
    sbatch --array=1-4 slurm_run_with_hydro_2500incl.slurm 18 'runs_steady_state'
    sbatch --array=1-3 slurm_run_with_hydro_2500incl.slurm 19 'runs_steady_state'
        ```
- raw OGGM output in 1000 glacier batches is saved in the folders RGIXX under https://cluster.klima.uni-bremen.de/~lschuster/provide/gfdl-esm2m_oversh_stab_uni_bern/A_runs_pre_postprocessing/output/
    - e.g. in https://cluster.klima.uni-bremen.de/~lschuster/provide/gfdl-esm2m_oversh_stab_uni_bern/A_runs_pre_postprocessing/output/RGI03/run_random_climate_from2500_using2400_2500_gfdl-esm2m_stab_T15_initial_oversh_T30OS15_bc_1980_2019_rgi03_0_1000.nc
    

## 4. Merge PROVIDE and RGI regions in separate files by extracting the most important variables
- [A_runs_pre_postprocessing/0a_merge_basins_provide_regions_oversh_stab.ipynb](A_runs_pre_postprocessing/0a_merge_basins_provide_regions_oversh_stab.ipynb)
    - uses the raw data from Sect. 2,3 to get the glacier volume and area and to compute runoff and meltwater components on a monthly and annual basis
- creates merged data files in the following folders that are later further aggregated  (basically just used as temporary files)
    - https://cluster.klima.uni-bremen.de/~lschuster/provide/gfdl-esm2m_oversh_stab_uni_bern/A_runs_pre_postprocessing/output/rgi_reg
    - https://cluster.klima.uni-bremen.de/~lschuster/provide/gfdl-esm2m_oversh_stab_uni_bern/A_runs_pre_postprocessing/output/provide_reg
 
    
## 5. Find glaciers that do not fail in any of the scenarios
- [A_runs_pre_postprocessing/0b_get_common_working_rgi_ids_extract_error_statistics.ipynb](A_runs_pre_postprocessing/0b_get_common_working_rgi_ids_extract_error_statistics.ipynb)
    - extracts error statistics that we mention in the methods
    - uses the RGI batch files `A_runs_pre_postprocessing/output/RGIXX/run_hydro_w5e5_gcm_merged_from_2000_gfdl-esm2...` as input 
    - creates 
        - `data/additional_data/working_rgis_for_oversh_stab_scenario_bc_1980_2019.csv`
        - `data/additional_data/random_climate_run_10000years_working_rgis_for_oversh_stab_scenarios_1980_2019.csv`
        - and other similar files for the bias correction period 2000-2019 (`_bc_2000_2019`) 

## 6. Create volume/runoff/meltwater time-series for the aggregated characteristics of every region (RGI region, PROVIDE region or basin-wide) by always only selecting the common running glaciers 
- [A_runs_pre_postprocessing/0c_extract_summed_up_common_running_projections_files.ipynb](A_runs_pre_postprocessing/0c_extract_summed_up_common_running_projections_files.ipynb)
    - creates `data/common_running_sum_all_rgi_reg_oversh_stab_2000_2500_bc_1980_2019.nc`
    - creates `data/common_running_sum_all_basins_oversh_stab_2000_2500_bc_1980_2019.nc`
    - creates `data/common_running_sum_all_rgi_reg_extended_oversh_stab_over_10000years_1980_2019.nc`

## 7. Extract specific climate characteristics
- [A_runs_pre_postprocessing/0d_extract_RGIregion_basin_drymonths.ipynb](A_runs_pre_postprocessing/0d_extract_RGIregion_basin_drymonths.ipynb)
    - extracts basin  precipitation seasonality of three-month rolling average precipitation and driest months
    - creates `data/additional_data/basin_past_pr_seasonality_3m_roll_lastm.csv`
        - precipitation seasonality of three-month rolling average precipitation for each basin from 1990 to 2019
    - creates `data/additional_data/basin_driest_months.csv`
    
- [A_runs_pre_postprocessing/0e_check_extract_global_regional_gfdl-esm2m_climate.ipynb](A_runs_pre_postprocessing/0e_check_extract_global_regional_gfdl-esm2m_climate.ipynb)
    - extracts near-glacier area-weighted climate estimates of GFDL-ESM2M (globally and per RGI region or basin) 
        - it also uses statistics from the previous notebook about the driest months within a year ... 
        - saves these estimates under `data/annual_glob_rgi_reg_basin_temp_precip_timeseries_oversh_stab.csv`
        
## All additional analysis is done in [B_main_analysis_figure_creation](B_main_analysis_figure_creation)
- We describe the analysis and figure creation notebooks in [README.md](README.md), and the main data is further described in [README_data.md](README_data.md).
