# Main data documentation


## Glacier projections aggregated per RGI6 region from 2000 to 2500 with the glacier model OGGM under the GFDL-ESM2M climate scenarios
   - netcdf dataset: `data/common_running_sum_all_rgi_reg_oversh_stab_2000_2500_bc_1980_2019.nc`
   - glacier volume , area  runoff and melt_off_on (kg yr-1)
   - glacier volume (m3) and area (m2) are aggregated sums and valid for the first day of the year
   - `runoff`: Annual glacier runoff: sum of annual melt and liquid precipitation on and off the glacier using a fixed-gauge with a glacier minimum reference area from year 2000 (unit: kg yr-1)
   - `melt_off_on`: Annual meltwater components from glacier runoff: sum of meltwater on and off the glacier using a fixed-gauge with a glacier minimum reference area from year 2000 (unit: kg yr-1)
   - eight scenarios are used: 
       - stab_T12, stab_T15, stab_T20, stab_T25, stab_T30 for 1.2-3.0°C stabilisation 
       - oversh_20OS15, oversh_20OS15, oversh_20OS15 for overshoots peaking at 2, 2.5 or 3°C and returning to 1.5°C
    
    
.... todo .
                