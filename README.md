# glacier_overshoot_irreversibility_trough_water
Code to reproduce the glacier projections, figure and analysis of 
- Schuster et al., (in preparation): TITLE, submitted to ... 

We projected global glacier mass and runoff from year 2000 to 2500 with the glacier model [OGGM v1.6.1](https://doi.org/10.5281/zenodo.8287580) ([Maussion et al., 2019](https://www.geosci-model-dev.net/12/909/2019/)) by appyling the climate from the [GFDL-ESM2M Earth Sytem Model (Lacroix et al., in review)](https://doi.org/10.22541/essoar.171588258.80079180/v1) from four stabilisation and three overshoot scenarios from year 2000 to 2500. We also projected glacier mass beyond 2500 (for additional 10000 years) by applying randomly the climate from the years 2399 to 2499 of the GFDL-ESM2M. The documentation of the code for the climate preprocessing, the OGGM projection runs and postprocessing is in [README_climate_preprocessing_OGGM_runs.md](README_climate_preprocessing_OGGM_runs.md).

In the following, we give an overview of the notebooks to analyse the data and to create the figures of the manuscript:

# Overview over analysis notebooks

## 1. Idealised/Conceptual model notebooks

- [main_analysis_figure_creation/1_idealised_suppl_comparison.ipynb](main_analysis_figure_creation/1_idealised_suppl_comparison.ipynb) XXX
    - all idealised experiment figures are created here 
        - creates `Fig. 1, Supplementary Fig. SXX`

         
## 2. Volume ESM notebooks
  
- [main_analysis_figure_creation/2a_fig_2_suppl_prcp.ipynb](main_analysis_figure_creation/2a_fig_2_suppl_prcp.ipynb) XXX
    - creates `Fig 2` (+ variants of it ...)
    - creates suppl. fig. with global prcp. evolution 
    - also creates suppl. figure with individual RGI regions for suppl. informations: 
        - suppl_2_rgi_reg_volume_changes_overshoot{a}_{bc}_portrait_4cols.pdf (+ variants...)

- [main_analysis_figure_creation/2b_suppl_fig_steady_state_glacier_temp_irreversiblities.ipynb](main_analysis_figure_creation/2b_suppl_fig_steady_state_glacier_temp_irreversiblities.ipynb) xxx 
    - Assess the influence of the temporal irreversiblity -> using regional volume projections with random climate after year 2500 
        - creates suppl. figures ... 4_only_global_reversibility .... (+ variants)
        - does additional analysis and figures not shown in the manuscript 
        

- [main_analysis_figure_creation/2c_fig_3_volume_clustering_map.ipynb](main_analysis_figure_creation/2c_fig_3_volume_clustering_map.ipynb)  xxxx
    - regional volume analysis by searching for clusters -> creates Fig. 3
    - also creates potential suppl. figure with clustering from volume estimates (FIg.3) but showing the runoff evolution instead of volume evolution
        - not used at the moment in the manuscript: ../figures/additional_figures/2x_suppl_worldmap_cluster_runoff_rgi_reg_manual_chosen_3_clusters_show_tempFalse_v_8plots.png
    - also does some additional analysis (most of it not used/mentioned in manuscript)
    - TODO --> compute internally the glacier-area weighted surface slope!!! (at the momment GMIP3 file used...)
    
## 3. Runoff ESM notebooks 
 
- [main_analysis_figure_creation/3a_basin_stats.ipynb](main_analysis_figure_creation/3a_basin_stats.ipynb)   xxxx 
    - does some basin statistic analysis mentioned in the manuscript 
    - creates suppl. figures of basin analysis (and annual and melt water runoff)
    - also creates suppl. plot with prcp seasonality    
    - creates files to later create Fig. 4 (but Fig. 4 is created in the next notebook)
 
 - [main_analysis_figure_creation/3b_fig4.ipynb](main_analysis_figure_creation/3b_fig4.ipynb)    xxxx
     - creates Fig. 4 

- [main_analysis_figure_creation/3c_suppl_fig_runoff_RGIregions.ipynb](main_analysis_figure_creation/3c_suppl_fig_runoff_RGIregions.ipynb)
    - creates suppl. figure with regional glacier runoff ... and precipitation 
    
- [main_analysis_figure_creation/3d_check_runoff_glacierized_area_overshoot.ipynb](main_analysis_figure_creation/3d_check_runoff_glacierized_area_overshoot.ipynb)
    - checks the issue of glacierized area temporal changes --> just important to mention in discussion somewhere.. 

## Additional analysis that is just for supplements or more for the discussion... 

- [main_analysis_figure_creation/4a_discussion_CMIP6_over_gcms.ipynb](main_analysis_figure_creation/4a_discussion_CMIP6_over_gcms.ipynb) 
    - notebook that shows the exemplarily different regional glacier responses for other existing CMIP6 overshoot scenarios until 2300
    - creates a supplementary figure 
    
- [main_analysis_figure_creation/4b_discussion_comparison_gcms.ipynb](main_analysis_figure_creation/4b_discussion_comparison_gcms.ipynb)
    - at the moment not anymore used for any main or suppl. figures as too complex analysis that tries to compare different overshoot GCMs/scenarios + bias correction approach
    - but maybe still good for some information to mention in main text?
    - creates figures like e.g. `../figures/4_discussion_gcm_gmodel_comparison.pdf`
    
    
## Notes
All files that are available at the OGGM cluster are defined in the code as e.g. `/home/www/lschuster/...` or `/home/www/fmaussion/...`. These files can be accessed outside the OGGM cluster via: https://cluster.klima.uni-bremen.de/~lschuster/ or https://cluster.klima.uni-bremen.de/~fmaussion/, respectively. 

        
        

