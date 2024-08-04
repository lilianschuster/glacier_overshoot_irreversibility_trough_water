import seaborn as sns

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


import geopandas as gpd
pd_provide_reg_full_name = gpd.read_file('/home/www/lschuster/provide/provide_glacier_regions/provide_glacier_regions.shp')
pd_provide_reg_full_name.index = pd_provide_reg_full_name.provide_id
provide_reg_full_name_dict = dict(pd_provide_reg_full_name['full_name'])
provide_reg_full_name_dict['P06'] = 'East Asia'
provide_reg_full_name_dict['P05'] = 'Svalbard, Jan Mayen\nand Russian Arctic'
provide_reg_full_name_dict['P13'] = 'Subantarctic and\nAntarctic Islands'
provide_reg_full_name_dict['P09'] = 'High Mountain Asia' # need to rename that probably, but this is better than "Central Asia" as that is already the name for only RGI region 13
