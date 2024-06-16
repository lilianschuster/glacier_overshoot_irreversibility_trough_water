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
label_scenario = {'stab_T12': 'Stabilisation 1.2°C',
                  'oversh_T20OS15':'Overshoot 2.0°C->1.5°C',
                  'oversh_T25OS15':'Overshoot 2.5°C->1.5°C',
                  'oversh_T30OS15':'Overshoot 3.0°C->1.5°C',
                  'stab_T15':'Stabilisation 1.5°C',
                  'stab_T20':'Stabilisation 2.0°C',
                  'stab_T25':'Stabilisation 2.5°C',
                  'stab_T30':'Stabilisation 3.0°C'}

color_scenario_poster = {'stab_T12': pal_colorblind[-3],
                      'stab_T15':pal_colorblind[0],
                  #'oversh_T20OS15':pal_colorblind[-1],
                  #'oversh_T25OS15':pal_colorblind[1],
                  'oversh_T30OS15':pal_colorblind[3],
                 'stab_T30':pal_colorblind[4]}


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
