## Overview over analysis and figure notebooks
In the following, we give an overview of the notebooks to analyse the data and to create the figures for the manuscript:

### 1. Idealised/Conceptual model notebooks

- [B_main_analysis_figure_creation/1_idealised_suppl_comparison.ipynb](B_main_analysis_figure_creation/1_idealised_suppl_comparison.ipynb)
    - all idealised experiment figures `Fig. 1, Supplementary Figs. 2, 3` are created here
    - postprocessed experiments (OGGM glacier directories) are saved in https://cluster.klima.uni-bremen.de/~lschuster/provide/gfdl-esm2m_oversh_stab_uni_bern/data/idealised_exps_preprocessing/, but can also be reproduced (takes longer) 
    

### 2. Volume ESM notebooks
  
- [B_main_analysis_figure_creation/2a_fig_2_suppl_prcp.ipynb](B_main_analysis_figure_creation/2a_fig_2_suppl_prcp.ipynb)
    - computes sea-level equivalent estimates (by taking OGGM's volume above-sea level estimate)
    - creates `Fig. 2` (+ variants of it ...)
    - creates `Supplementary Fig. 11` (with global precipitation evolution)
    - creates `Supplementary Fig. 5` (with individual RGI region projections for all overshoot scenarios)

- [B_main_analysis_figure_creation/2b_suppl_fig_steady_state_glacier_temp_irreversiblities.ipynb](B_main_analysis_figure_creation/2b_suppl_fig_steady_state_glacier_temp_irreversiblities.ipynb)
    - Assesses the influence of the temporal irreversibility -> using regional projections with random climate after the year 2500
    - creates `Supplementary Fig. 4` and additional regional analysis and figures not shown in the manuscript
    - also looks into single glacier behavior in RGI19
        

- [B_main_analysis_figure_creation/2c_fig_3_volume_clustering_map.ipynb](B_main_analysis_figure_creation/2c_fig_3_volume_clustering_map.ipynb) 
    - regional mass analysis by searching for clusters -> creates `Fig. 3`
    - also creates potential supplementary figure with clustering from mass estimates but showing the runoff evolution instead of the mass evolution
        - not used at the moment in the manuscript: `figures/additional_figures/2x_suppl_worldmap_cluster_runoff_rgi_reg_manual_chosen_3_clusters_show_tempFalse_v_8plots.png`
    - also does some additional analysis (most of it not used/mentioned in manuscript)
    
### 3. Runoff ESM notebooks 
 
- [B_main_analysis_figure_creation/3a_basin_stats.ipynb](B_main_analysis_figure_creation/3a_basin_stats.ipynb)  
    - does some basin statistic analysis mentioned in the manuscript 
    - creates `Supplementary Figs. 6-8` of all glaciated basins with analysis on annual runoff and precipitation 
    - creates `Supplementary Fig. 9` of selected dry glaciated basins with analysis on annual meltwater runoff
    - creates `Supplementary Fig. 10` with basin statistics of all 60 glaciated basins
    - creates `Supplementary Fig. 11` with three-month averaged precipitation seasonality of selected basins     
    - creates files to create later Fig. 4 (but we create Fig. 4 only in the next notebook)
 
 - [B_main_analysis_figure_creation/3b_fig_4.ipynb](B_main_analysis_figure_creation/3b_fig_4.ipynb) 
     - creates `Fig. 4`

- [B_main_analysis_figure_creation/3c_suppl_fig_runoff_RGIregions.ipynb](B_main_analysis_figure_creation/3c_suppl_fig_runoff_RGIregions.ipynb)
    - creates additional figure with RGI region aggregated glacier runoff and near-glacier precipitation (not used anymore because replaced by basin runoff figures)
    
- [B_main_analysis_figure_creation/3d_check_runoff_glacierized_area_overshoot.ipynb](B_main_analysis_figure_creation/3d_check_runoff_glacierized_area_overshoot.ipynb)
    - checks the issue of glacierised area temporal changes 
    - we shortly mention results in methods, but we do not use any figures from this notebook

### 4. Additional analysis that is just for supplements or for the discussion

- [B_main_analysis_figure_creation/4a_discussion_CMIP6_over_gcms.ipynb](B_main_analysis_figure_creation/4a_discussion_CMIP6_over_gcms.ipynb) 
    - creates `Supplementary Fig. 1` with global temperature changes of CMIP6 climate scenarios, which have temperature overshoots until 2300 and respective glacier model projections on three glacier models. We analyse glacier model projections as global aggregates and for three example regions.
        - uses data from Schuster et al., 2023: lilianschuster/glacier-model-projections-until2300: v0.1 Zenodo (https://doi.org/10.5281/zenodo.10059477)
  
- [B_main_analysis_figure_creation/4b_discussion_bias_correction_period_sensitivity_comparison_climate_models.ipynb](B_main_analysis_figure_creation/4b_discussion_bias_correction_period_sensitivity_comparison_climate_models.ipynb)
    - influence of the period options of the bias correction (1980-2019 vs 2000-2019) (numbers and Supplementary figure 13)
    - trial to quantitatively compare other overshoot climate models and scenarios (not used, not succesful)


## Notes
All files available at the OGGM cluster are defined in the code as e.g. `/home/www/lschuster/...` or `/home/www/fmaussion/...`. These files are accessible outside the OGGM cluster via https://cluster.klima.uni-bremen.de/~lschuster/ or https://cluster.klima.uni-bremen.de/~fmaussion/, respectively. 
