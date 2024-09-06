import seaborn as sns
import numpy as np
import pandas as pd
import geopandas as gpd

pal_colorblind = sns.color_palette("colorblind")
color_scenario = {'stab_T12': pal_colorblind[-3],
                 'stab_T15':pal_colorblind[0],
                  'oversh_T20OS15':pal_colorblind[-1],
                  'oversh_T25OS15':pal_colorblind[1],
                  'oversh_T30OS15':pal_colorblind[3],
                  'stab_T20':pal_colorblind[2],
                'stab_T25': pal_colorblind[5],
                 'stab_T30':pal_colorblind[4]}


color_scenario_all_oversh = {'stab_T12': color_scenario['stab_T12'],
 'stab_T15': color_scenario['stab_T15'],
 'stab_T30': color_scenario['stab_T30'],
'oversh_T20OS15': color_scenario['oversh_T20OS15'],
 'oversh_T25OS15': color_scenario['oversh_T25OS15'],
 'oversh_T30OS15': color_scenario['oversh_T30OS15']}


color_scenario_poster = {'stab_T12': color_scenario['stab_T12'],
 'stab_T15': color_scenario['stab_T15'],
 'stab_T30': color_scenario['stab_T30'],
 'oversh_T30OS15': color_scenario['oversh_T30OS15']}


label_scenario = {'stab_T12': '1.2°C Stabilisation',
 'oversh_T30OS15': '3.0$\\rightarrow$1.5°C Overshoot',
 'stab_T15': '1.5°C Stabilisation',
 'stab_T30': '3.0°C Stabilisation',
 'oversh_T20OS15': '2.0$\\rightarrow$1.5°C Overshoot',
 'oversh_T25OS15': '2.5$\\rightarrow$1.5°C Overshoot'}

scenario_ls = {'stab_T12': '-',
 'stab_T15': '-',
 'oversh_T30OS15': '--',
 'stab_T30': '-',
 'oversh_T20OS15': '--',
 'oversh_T25OS15': '--'}


d_reg_num_name = {}
d_reg_num_name['01'] = 'Alaska'
d_reg_num_name['02'] = 'W Canada & US' # Western Canada & USA
d_reg_num_name['03'] = 'Arctic Canada N'
d_reg_num_name['04'] = 'Arctic Canada S'
d_reg_num_name['05'] = 'Greenland Periphery' # maybe rather call it Greenland Periphery as in Rounce et al., 2023???
d_reg_num_name['06'] = 'Iceland'
d_reg_num_name['07'] = 'Svalbard & Jan Mayen'
d_reg_num_name['08'] = 'Scandinavia'
d_reg_num_name['09'] = 'Russian Arctic'
d_reg_num_name['10'] = 'North Asia'
d_reg_num_name['11'] = 'Central Europe'
d_reg_num_name['12'] = 'Caucasus & Middle East'
d_reg_num_name['13'] = 'Central Asia'
d_reg_num_name['14'] = 'South Asia W' #West
d_reg_num_name['15'] = 'South Asia E' # EAST
d_reg_num_name['16'] = 'Low Latitudes'
d_reg_num_name['17'] = 'Southern Andes'
d_reg_num_name['18'] = 'New Zealand'
d_reg_num_name['19'] = 'Subantarctic & Antarctic Islands' ## NEW name!!!

#### both functions are mainly used in notebook 3a_basin_stats.ipynb    
def find_largest_continuous_span(years):
    # function to correctly find the largest continuous span of years in a list
    max_span_start = years[0]
    max_span_end = years[0]
    current_span_start = years[0]
    current_span_end = years[0]

    for i in range(1, len(years)):
        if years[i] == current_span_end + 1:
            current_span_end = years[i]
        else:
            if (current_span_end - current_span_start) > (max_span_end - max_span_start):
                max_span_start = current_span_start
                max_span_end = current_span_end
            current_span_start = years[i]
            current_span_end = years[i]

        if (current_span_end - current_span_start) > (max_span_end - max_span_start):
            max_span_start = current_span_start
            max_span_end = current_span_end

    return (max_span_start, max_span_end)

def get_basin_trough_water_stats(sel_stab, sel_oversh, 
                                 runoff_var = 'runoff_dry3m_rel_2000_2050_%'):

    # Find years of trough water and extract statistics
    # Definition: “Trough water” occurs if the 51- or 21-year average annual runoff from the 
    # “Overshoot 3.0°C -> 1.5°C” scenario is at least 5\% smaller than (i) in the “Stabilisation 1.5°C” scenario for 20 years 
    # and  (ii) than in the baseline period 
    # (initial steady state for the idealised experiments, 2000--2020 or 2000--2050 climate for the projections with the ESM).
    # --> the second condition just means it has to be smaller than or equal to 95% 
    
    # arguments: 
    # sel_stab, sel_oversh: (pd.DataFrame)
    #    Table with runoff_var of the stabilisation or overshoot scenario for a specific basin 
    # runoff_var: str
    #    one of the three runoff variables ('runoff_rel_2000_2050_%', 'melt_off_on_rel_2000_2050_%', 'runoff_dry3m_rel_2000_2050_%')
    #    can also be 21-year averaged

    # returns array with: 
    # - amount of trough water years (also if they are non-continuous)
    # - cumulative runoff difference during trough water years
    # - year where trough water is strongest (year w. largest difference)
    # - largest difference of Stabilisation minus Overshoot during trough water
    # - first year and last year of potential trough water (has to be checked for discontinuoties when plotted )
    

    sel_oversh.index = sel_oversh.time
    sel_stab.index = sel_stab.time
    condi_i = (sel_stab[runoff_var] - sel_oversh[runoff_var]) >= 5 #difference has to be larger thatn 5% 
    condi_ii = sel_oversh[runoff_var].dropna()<=95
    condi = condi_i & condi_ii
    
    yrs_trough = sel_stab.where(condi).dropna(how='all').index
    # check if largest continuos span with 5% difference is at least 20 years 
    if len(yrs_trough)>1:
        x0,x1 = find_largest_continuous_span(yrs_trough)
        condi_20_yrs = len(np.arange(x0,x1,+1))>=20
    else:
        condi_20_yrs = False
    
    if condi_20_yrs:
        #print(x0,x1)
        trough_water_years = len(yrs_trough)
        # difference stabilisation vs overshoot
        diff = (sel_stab.loc[yrs_trough][runoff_var] - sel_oversh.loc[yrs_trough][runoff_var])
        water_trough_min_yr = int(diff.idxmax())
        water_trough_max_diff = diff.max()
        # years of potential trough water
        yrs_trough_start_end = f'{yrs_trough[0]}_{yrs_trough[-1]}'
        runoff_diff_trough = diff.sum()
    else:
        trough_water_years = 0
        water_trough_min_yr = np.NaN
        water_trough_max_diff = np.NaN
        yrs_trough_start_end = np.NaN
        runoff_diff_trough = np.NaN

    return np.array([trough_water_years, runoff_diff_trough,
                     water_trough_min_yr, water_trough_max_diff, yrs_trough_start_end])

### this paragraph is not anymore used for main study
pd_provide_reg_full_name = gpd.read_file('/home/www/lschuster/provide/provide_glacier_regions/provide_glacier_regions.shp')
pd_provide_reg_full_name.index = pd_provide_reg_full_name.provide_id
provide_reg_full_name_dict = dict(pd_provide_reg_full_name['full_name'])
provide_reg_full_name_dict['P06'] = 'East Asia'
provide_reg_full_name_dict['P05'] = 'Svalbard, Jan Mayen\nand Russian Arctic'
provide_reg_full_name_dict['P13'] = 'Subantarctic and\nAntarctic Islands'
provide_reg_full_name_dict['P09'] = 'High Mountain Asia' # need to rename that probably, but this is better than "Central Asia" as that is already the name for only RGI region 13

