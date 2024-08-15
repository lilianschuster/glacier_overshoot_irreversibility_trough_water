# Main data documentation

## 1. Aggregated overshoot and stabilisation glacier projections with the glacier model OGGM

The bias correction period is in all main data files from 1980 to 2019, which is also the period we used in the manuscript.

### 1a. From 2000 to 2500 under the GFDL-ESM2M climate scenarios (two netCDF files)

   - `scenario`: we used eight scenarios from the GFDL-ESM2M
       - stab_T12, stab_T15, stab_T20, stab_T25, stab_T30 for 1.2, 1.5, 2.0, 2.5 and 3.0°C Stabilisation 
       - oversh_20OS15, oversh_20OS15, oversh_20OS15 for overshoots peaking at 2.0, 2.5 or 3.0°C and returning to 1.5°C
   - variables are the aggregated sums from individual glaciers for each RGI region or basin. To better compare scenarios, we only used those glaciers that work in all scenarios ("the common running glaciers"). 
   
**aggregated per RGI region (`rgi_reg`)**: netCDF file: `data/common_running_sum_all_rgi_reg_oversh_stab_2000_2500_bc_1980_2019.nc`
   - glacier variables:
       - `volume` (m3) and `area` (m2) are aggregated sums and valid for the first day of the year
       - `runoff` (kg yr-1): Annual glacier runoff: sum of annual melt and liquid precipitation on and off the glacier using a fixed-gauge with a glacier minimum reference area from the year 2000 
       - `melt_off_on` (kg yr-1): Annual meltwater components from glacier runoff: sum of meltwater on and off the glacier using a fixed-gauge with a glacier minimum reference area from the year 2000
   - used for Fig. 2-4 and supplementary figures
   
**aggregated per `basin`**: netCDF file: `data/common_running_sum_all_basins_oversh_stab_2000_2500_bc_1980_2019.nc`
   - variables:
       - same as regional file, but in addition monthly runoff (`runoff_monthly`) and meltwater components (`melt_off_on_monthly`), unit for both: kg month-1
   - `basin` indices defined as in the Global Runoff Data Centre dataset
   - used for Fig. 4 and supplementary figures


###  1b. For over >10000 years under extended GFDL-ESM2M climate scenarios (one netCDF file)

- `scenario`: two extended scenarios are used
    - `oversh_T30OS15_extended_w_2399-2499_stab_T15`: from the year 2000 to 2500, the 3.0->1.5°C Overshoot, then a random climate from 2399-2499 from the 1.5°C Stabilisation scenario
    - `stab_T15_extended_w_2399-2499_stab_T15`:  from the year 2000 to 2500, the 1.5°C Stabilisation, then a random climate from 2399-2499 from the 1.5°C Stabilisation scenario
- variables are the aggregated sums per RGI6 region for the common running glaciers of all scenarios until 2500 and of the common running glaciers of the two extended random climate scenario options over >10000 years

**aggregated per RGI region (`rgi_reg`)**: netCDF file: `data/common_running_sum_all_rgi_reg_extended_oversh_stab_over_10000years_1980_2019.nc`
   - variables: 
       - glacier `volume` (m3):  aggregated sum over glaciers and valid for the first day of the year   
   - used in Supplementary Fig. 4 and for analysis in the main text 

## 2. Global and regional extracted climate from the GFDL-ESM2M climate scenarios (one CSV file)

**aggregated globally, per RGI region or basin**: CSV file: `data/annual_glob_rgi_reg_basin_temp_precip_timeseries_oversh_stab.csv` 
- extracted annual time series of temperature, precipitation and other precipitation metrics from the GFDL-ESM2M with the following columns:
    - `year`: 1979 to 2499
    - `region`: 
        - `global`: global averages
        - `global_glacier`: global glacier-area weighted averages (by taking the gridpoints nearest to the glaciers)
        - `RGIXX_glacier`: regional glacier-area weighted averages for that specific RGI region XX
        - `basin_XXXX_glacier`: basin glacier-area weighted averages (indices XXXX as defined by the Global Runoff Data Centre GRDC)
    - `scenario`: one of the eight scenarios  (same naming conventions as in the netCDF glacier projection files)
    - `temp`: air temperature (unit: K)
    - `temp_21yr_avg`: same as `temp`; but using a centered 21-year rolling average (nan-values at beginning and end)
    - `precip`: total precipitation (unit: `kg m-2 yr-1`)
    - `precip_21yr_avg`: same as `temp`; but using a centered 21-year rolling average (nan-values at beginning and end)
    - `precip_3mdriest_avg_per_day`: three-month rolling precipitation average over the three months with the lowest precipitation (the chosen three months are selected once and do not change over time), only available for the basins. Here, precipitation data is extracted from the entire basin and not just the nearest glacier gridpoints (unit: kg m-2 day-1)
    - `precip_3mdriest_avg_per_day_51yr_avg`: same as `precip_3mdriest_avg_per_day`; but using a centered 51-year rolling average (nan-values at beginning and end)
- used in Fig. 2-4 and supplementary figures


## Additional data

In the notebooks, we extract some additional  "intermediate" summary data that we saved for later usage for a few figures or analyses. This "intermediate" data is available at https://cluster.klima.uni-bremen.de/~lschuster/provide/gfdl-esm2m_oversh_stab_uni_bern/data/additional_data/. 

We describe the scripts and notebooks for climate preprocessing, the OGGM runs, and postprocessing in [README_climate_preprocessing_OGGM_runs.md](README_climate_preprocessing_OGGM_runs.md) and those for figure creation in [README.md](README.md).

