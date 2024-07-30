# Overview over analysis notebooks


## extract aggregated projection files or further climate datasets... 

- `0x_extract_RGIregion_basin_drymonths.ipynb`
    - creates `basin_past_pr_seasonality_3m_roll_lastm.csv`
    - creates `basin_driest_months.csv`
- `0_extract_summed_up_common_running_projections_files.ipynb`
    - Scripts to create volume/runoff/runoff component timeseries for the summed up characteristics of every provide regions /rgi /basin regions
        - creates `common_running_sum_all_provide_reg_oversh_stab_2000_2500.nc`
        - creates `common_running_sum_all_rgi_reg_oversh_stab_2000_2500.nc`
        - creates `common_running_sum_all_basins_oversh_stab_2000_2500.nc`

## 1. Idealised/Conceptual model notebooks

- `1_idealised_suppl_comparison.ipynb`
    - > all currently used idealised experiment figures are shown here
- externally on Lily's laptop as xkcd does not workk on cluster:
    - older variants (including those with xkcd) are on the laptop: 
    - Schreibtisch/PhD/phd_paper_2_overshoot_glaciers/idealised_conceptual_overshoot_reponse_v2024-06.ipynb
    
        
        
## volume ESM notebooks
  
- `2_fig_2_suppl_prcp.ipynb`
    - creates fig 2 (+ variants of it ...)
    - creates suppl. fig. with global prcp. evolution 
    - also creates suppl. figure with individual RGI regions for suppl. informations: 
        - 2_rgi_reg_volume_changes_overshoot{a}_{bc}_portrait_4cols.pdf (+ variants...)
- `2x_volume_timeseries_clustering_map_rgi_region_new.ipynb`
    - creates Fig. 3
    - also creates potential suppl. figure with clustering from volume estimates (FIg.3) but showing the runoff evolution instead of volume evolution
    - also does some additional analysis (some of it is old)
    
## runoff ESM notebooks 
- `3x_check_runoff_glacierized_area_overshoot.ipynb`
    - checks the issue of glacierized area temporal changes --> just important to mention in discussion somewhere.. 
   

- `3_basin_stats.ipynb`
    - does some basin statistic analysis mentioned in the manuscript 
    - creates suppl. figures of basin analysis (and annual and melt water runoff)
    - also creates suppl. plot with prcp seasonality    
    - creates files to later create Fig. 4 (but Fig. 4 is created in other notebook)
 
 - `3_fig4.ipynb`
     - creates Fig. 4 

- `4_runoff_RGIregions.ipynb`
    - creates suppl. figure with regional glacier runoff ... and precipitation 

## additional analysis that is maybe more for the discussion... 
- `4_steady_state_glacier_tipping_points`
    - Assess the influence of the temporal irreversiblity -> using regional volume projections with random climate after year 2500 
        - creates suppl. figures ... 4_only_global_reversibility .... (+ variants)
        - creates RGI19_crazy_tipping_point_glaciers... 
        
- `4_discussion_CMIP6_over_gcms.ipynb`
    - notebook that shows the exemplarily different regional glacier responses for other existing CMIP6 overshoot scenarios until 2300
    - creates a potential supplementary figure 
    
    
- `4_discussion_comparison_gcms.ipynb`
    - at the moment not anymore used for any main or suppl. figures as too complex analysis that tries to compare different overshoot GCMs/scenarios + bias correction approach
    - but maybe still good for some information to mention in main text?
    - creates figures like e.g. figures/4_discussion_gcm_gmodel_comparison.pdf
        
        
