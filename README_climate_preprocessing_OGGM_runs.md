# Workflows

## 1. flatten GFDL-ESM2M ESM climate datasets
`cd runs` 
run in terminal in OGGM cluster:
- `sbatch slurm_flatten_oversh_stab_monthly.slurm stab_T12`
    - exectutes python script:
        - `flatten_oversh_stab_monthly_files.py`
  

## 2. do global OGGM glacier projections run (with flattened files)
`cd runs` 
- executes python script:
    - `0_run_with_hydro_oversh_stab_per_rgi_reg.py`
        - uses internally `func_add.py`
- via: 
    ```
    sbatch --array=1-28 slurm_run_with_hydro.slurm 01
    sbatch --array=1-19 slurm_run_with_hydro.slurm 02
    sbatch --array=1-5 slurm_run_with_hydro.slurm 03
    sbatch --array=1-8 slurm_run_with_hydro.slurm 04
    sbatch --array=1-21 slurm_run_with_hydro.slurm 05
    sbatch --array=1-1 slurm_run_with_hydro.slurm 06
    sbatch --array=1-2 slurm_run_with_hydro.slurm 07
    sbatch --array=1-4 slurm_run_with_hydro.slurm 08
    sbatch --array=1-2 slurm_run_with_hydro.slurm 09
    sbatch --array=1-6 slurm_run_with_hydro.slurm 10
    sbatch --array=1-4 slurm_run_with_hydro.slurm 11
    sbatch --array=1-2 slurm_run_with_hydro.slurm 12
    sbatch --array=1-55 slurm_run_with_hydro.slurm 13
    sbatch --array=1-28 slurm_run_with_hydro.slurm 14
    sbatch --array=1-14 slurm_run_with_hydro.slurm 15
    sbatch --array=1-3 slurm_run_with_hydro.slurm 16
    sbatch --array=1-16 slurm_run_with_hydro.slurm 17
    sbatch --array=1-4 slurm_run_with_hydro.slurm 18
    sbatch --array=1-3 slurm_run_with_hydro.slurm 19
    ```
## 3. repeat global OGGM glacier projections under random climate of year 2399-2499 for 20000 additional years
- repeat what is done in Sect. 2, but set `run_steady_state=True` in `0_run_with_hydro_oversh_stab_per_rgi_reg.py`
    - uses internally `run_random_climate_prescribe_years` defined in  `func_add.py`


### TODO -> for final runs --> repeat everything using the `slurm_run_with_hydro_2500incl` files
    - because the other files only go until 2499 instead of 2500 accidentally 
    - todo -> set testing = False
    - rename old "output" folder ... to not overwrite it accidentally 
    

## 4. merge provide and rgi regions in separate files by extracting the most important variables
- `runs/1_merge_basins_provide_regions_oversh_stab.ipynb`
    - need to check if this is actually still used ...
    
    
## 5. 
- `analysis_notebooks/0_get_common_working_rgi_ids_extract_error_statistics.ipynb`
    - uses the RGI batch files `/home/www/lschuster/provide/gfdl-esm2m_oversh_stab_uni_bern/runs/output/RGI{rgi_reg_s}/run_hydro_w5e5_gcm_merged_from_2000_gfdl-esm2...` as input 
    - Create the common working RGI list and analyse amount of errors per region ... 
        - creates `working_rgis_for_oversh_stab_scenario_bc_1980_2019.csv`
        - creates `random_climate_run_20000years_working_rgis_for_oversh_stab_scenarios_1980_2019.csv`
    - extracts error statistics that are mentioned in the methods
    
- `analysis_notebooks/0_check_extract_global_regional_gcm_climate.ipynb`
    - creates these three csv files with climate estimates of GFDL-ESM2M, 
        - globally and per rgi-region (glacier-area weighted): `annual_glob_rgi_reg_basin_temp_precip_timeseries_oversh_stab.csv`
        - per provide region (glacier-area weighted): `annual_provide_reg_glacier_mask_temp_precip_timeseries_oversh_stab.csv`
        - per basin (glacier-area weighted) : `annual_basin_glacier_mask_temp_precip_timeseries_oversh_stab.csv`
    - all together: 
        - `annual_glob_glacier_rgi_reg_temp_precip_timeseries_oversh_stab.csv`
    - todo: 
        - remove those csv files/entries that are not needed, merge all files together, and always use the the merged dataset!
        
- `analysis_notebooks/0_global_gcm_climate_cmip6_cmip5_ipcc_ar6_def.ipynb
    - creates `Global_mean_temp_deviation....*.csv`
    - creates supplemental figures:
        - gcm_global_colors_by_temp_change*_ipcc_ar6_def.png

- `analysis_notebooks/0_failing_glaciers_find_reason.ipynb`
    - just checks for provide region P06 why so much glacier area is failing --> maybe remove or move into 
    `analysis_notebooks/0_get_common_working_rgi_ids_extract_error_statistics.ipynb`
    
  
## all additional analysis is done in `analysis_notebooks/schuster_et_al_phd_paper_2_overshoot_glaciers`
- notebooks are described in `analysis_notebooks/schuster_et_al_phd_paper_2_overshoot_glaciers/README.md`
