# Irreversible glacier change and trough water for centuries after overshooting the 1.5°C temperature target
Code to reproduce the glacier projections, figures and analysis of 
- Schuster et al. (in review): Irreversible glacier change and trough water for centuries after overshooting the 1.5°C temperature target, submitted to Nature Climate Change

If you use the code or the data, please cite the manuscript in review (LINK will be added soon) and the dataset/code on Zenodo. 

We projected global glacier mass and runoff from year 2000 to 2500 with the glacier model [OGGM v1.6.1](https://doi.org/10.5281/zenodo.8287580) ([Maussion et al., 2019](https://www.geosci-model-dev.net/12/909/2019/)) by appyling the climate from the [GFDL-ESM2M Earth Sytem Model (Lacroix et al., in review)](https://doi.org/10.22541/essoar.171588258.80079180/v1) from four stabilisation and three overshoot scenarios from year 2000 to 2500. We also projected glacier mass beyond 2500 (for additional 10000 years) by applying randomly the climate from the years 2399 to 2499 of the GFDL-ESM2M. 

The documentation of the code for the climate preprocessing, the OGGM projection runs and postprocessing is in [README_climate_preprocessing_OGGM_runs.md](README_climate_preprocessing_OGGM_runs.md). Some workflows and data for e.g. of the climate analysis of the individual regions or basins are only visible in the OGGM cluster folder which can be accessed under https://cluster.klima.uni-bremen.de/~lschuster/provide/gfdl-esm2m_oversh_stab_uni_bern/. The most important data is documented under [README_data.md](README_data.md) and available under [data/](data/).

In the following, we give an overview of the notebooks to analyse the data and to create the figures of the manuscript:

## Overview over analysis notebooks

### 1. Idealised/Conceptual model notebooks

- [B_main_analysis_figure_creation/1_idealised_suppl_comparison.ipynb](B_main_analysis_figure_creation/1_idealised_suppl_comparison.ipynb)
    - all idealised experiment figures `Fig. 1, Supplementary Fig. 2, 3` are created here
    - postprocessed experiments (OGGM glacier directories) are saved in https://cluster.klima.uni-bremen.de/~lschuster/provide/gfdl-esm2m_oversh_stab_uni_bern/data/idealised_exps_preprocessing/, but can also be reproduced (takes longer) 
    

### 2. Volume ESM notebooks
  
- [B_main_analysis_figure_creation/2a_fig_2_suppl_prcp.ipynb](B_main_analysis_figure_creation/2a_fig_2_suppl_prcp.ipynb)
    - creates `Fig. 2` (+ variants of it ...)
    - creates `Supplementary Fig. 11` (with global precipitation evolution)
    - creates `Supplementary Fig. 5` (with individual RGI region projections for all overshoot scenarios)

- [B_main_analysis_figure_creation/2b_suppl_fig_steady_state_glacier_temp_irreversiblities.ipynb](B_main_analysis_figure_creation/2b_suppl_fig_steady_state_glacier_temp_irreversiblities.ipynb)
    - Assesses the influence of the temporal irreversiblity -> using regional volume projections with random climate after year 2500 
    - creates `Supplementary Fig. 4` 
    -does additional analysis and figures not shown in the manuscript 
        

- [B_main_analysis_figure_creation/2c_fig_3_volume_clustering_map.ipynb](B_main_analysis_figure_creation/2c_fig_3_volume_clustering_map.ipynb) 
    - regional volume analysis by searching for clusters -> creates `Fig. 3`
    - also creates potential suppl. figure with clustering from volume estimates but showing the runoff evolution instead of volume evolution
        - not used at the moment in the manuscript: `figures/additional_figures/2x_suppl_worldmap_cluster_runoff_rgi_reg_manual_chosen_3_clusters_show_tempFalse_v_8plots.png`
    - also does some additional analysis (most of it not used/mentioned in manuscript)
    
### 3. Runoff ESM notebooks 
 
- [B_main_analysis_figure_creation/3a_basin_stats.ipynb](B_main_analysis_figure_creation/3a_basin_stats.ipynb)  
    - does some basin statistic analysis mentioned in the manuscript 
    - creates `Supplementary Fig. 6, 7`  of selected dry glaciated basins with analysis on annual and meltwater runoff
    - creates `Supplementary Fig. 8` with basin statistics of all 60 glaciated basins
    - creates `Supplementary Fig. 10` with three-month averaged precipitaion seasonality of selected basins     
    - creates files to later create Fig. 4 (but Fig. 4 is created in the next notebook)
 
 - [B_main_analysis_figure_creation/3b_fig_4.ipynb](B_main_analysis_figure_creation/3b_fig_4.ipynb) 
     - creates `Fig. 4`

- [B_main_analysis_figure_creation/3c_suppl_fig_runoff_RGIregions.ipynb](B_main_analysis_figure_creation/3c_suppl_fig_runoff_RGIregions.ipynb)
    - creates `Supplementary Fig. 9` with RGI region aggregated glacier runoff and near-glacier precipitation 
    
- [B_main_analysis_figure_creation/3d_check_runoff_glacierized_area_overshoot.ipynb](B_main_analysis_figure_creation/3d_check_runoff_glacierized_area_overshoot.ipynb)
    - checks the issue of glacierized area temporal changes 
    - results shortly mentioned in methods, but no figures from here are used

### Additional analysis that is just for supplements or more for the discussion... 

- [B_main_analysis_figure_creation/4a_discussion_CMIP6_over_gcms.ipynb](B_main_analysis_figure_creation/4a_discussion_CMIP6_over_gcms.ipynb) 
    - creates `Supplementary Fig. 1` with global temperature changes of CMIP6 climate screnarios with temperature overshoots until 2300 and respective glacier model projections on three glacier models. Glacier model projections are shown a global aggregates and for three exemple regions
        - uses data from lilianschuster/glacier-model-projections-until2300: v0.1 - https://doi.org/10.5281/zenodo.10059477
  
- [B_main_analysis_figure_creation/4b_discussion_bias_correction_period_sensitivity_comparison_climate_models.ipynb](B_main_analysis_figure_creation/4b_discussion_bias_correction_period_sensitivity_comparison_climate_models.ipynb)
    - for potential discussion : influence of bias correction time period options (1980-2019 vs 2000-2019), and with other overshoot climate models and scenarios
    - at the moment not anymore used for any main or suppl. figures as too complex analysis that tries to compare different overshoot GCMs/scenarios + bias correction approach
    
    
## Notes
All files that are available at the OGGM cluster are defined in the code as e.g. `/home/www/lschuster/...` or `/home/www/fmaussion/...`. These files can be accessed outside the OGGM cluster via: https://cluster.klima.uni-bremen.de/~lschuster/ or https://cluster.klima.uni-bremen.de/~fmaussion/, respectively. 

        
        

