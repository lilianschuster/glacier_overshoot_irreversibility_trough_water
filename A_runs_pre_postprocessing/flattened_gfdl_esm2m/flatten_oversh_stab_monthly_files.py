# updated script version for flattening gfdl-esm2m overshoot stabilisation scenarios from university of Bern 

from oggm import utils
import sys
import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

scenario = str(sys.argv[1])


path='/home/www/lschuster/provide/gfdl-esm2m_oversh_stab_uni_bern/data/additional_data/data_from_others/gfdl_esm2m'


ds_ref = xr.open_dataset(path + '/oversh_T20OS15/' + 'atmos_month_1861.nc')
ds_ref = ds_ref.rename({'lat': 'latitude'})
ds_ref = ds_ref.rename({'lon': 'longitude'})

ds_ref = ds_ref.isel(latitude=slice(1,-1))
max_lat = np.unique((ds_ref.latitude.values[1:]-ds_ref.latitude.values[:-1])/2)[0]
max_lon = np.unique(ds_ref.longitude.values[1:] - ds_ref.longitude.values[:-1])[0]/2
print(max_lat, max_lon)
ds_ref.coords['longitude'] = np.where(ds_ref.longitude.values < 0,
                                      ds_ref.longitude.values + 360,
                                      ds_ref.longitude.values)
ds_ref = ds_ref.sortby(ds_ref.longitude)
ds_ref.longitude.attrs['units'] = 'degrees_onlypositive'

# get the dataset where coordinates of glaciers are stored
frgi = utils.file_downloader('https://cluster.klima.uni-bremen.de/~oggm/rgi/rgi62_stats.h5')
#frgi = '/home/users/lschuster/glacierMIP/rgi62_stats.h5'
odf = pd.read_hdf(frgi, index_col=0)

nx, ny = ds_ref.dims['longitude'], ds_ref.dims['latitude']
# just make them into 0-> 360 scheme
cenlon_for_bins = np.where(odf['CenLon'] < 0,
                           odf['CenLon']+360, odf['CenLon'])

# Nearest neighbor lookup
lon_bins = np.linspace(ds_ref.longitude.data[0] - max_lon, ds_ref.longitude.data[-1] + max_lon, nx+1)
# !!! attention W5E5 sorted from 90 to -90 !!!!
lat_bins = np.linspace(ds_ref.latitude.data[0] - max_lat, ds_ref.latitude.data[-1] + max_lat, ny+1)
# before it was wrongly 
# lon_bins = np.linspace(0, 360, nx), lat_bins = np.linspace(90, -90, ny)
# which created a non-aligned bins, in addition there was one bin missing, creating a slightly 
# larger resolution which after adding up a lot got problematic... 
# at the end it resulted in 19 glaciers where the nearest grid point was not found


odf['lon_id'] = np.digitize(cenlon_for_bins, lon_bins)-1
odf['lat_id'] = np.digitize(odf['CenLat'], lat_bins)-1
odf['lon_val'] = ds_ref.longitude.data[odf.lon_id]
odf['lat_val'] = ds_ref.latitude.data[odf.lat_id]
# Use unique grid points as index and compute the area per location
odf['unique_id'] = ['{:03d}_{:03d}'.format(lon, lat) for (lon, lat) in zip(odf['lon_id'], odf['lat_id'])]
mdf = odf.drop_duplicates(subset='unique_id').set_index('unique_id')
mdf['Area'] = odf.groupby('unique_id').sum()['Area']
print('Total number of glaciers: {} and number of GCM gridpoints with glaciers in them: {}'.format(len(odf), len(mdf)))

# this is the mask that we need to remove all non-glacierized gridpoints
mask = np.full((ny, nx), np.NaN)
mask[mdf['lat_id'], mdf['lon_id']] = 1 
ds_ref['glacier_mask'] = (('latitude', 'longitude'), np.isfinite(mask))

# check the distance to the gridpoints-> it should never be larger than 
diff_lon = ds_ref.longitude.data[odf.lon_id] - odf.CenLon
# if the distance is 360 -> it is the same as 0,
diff_lon = np.where(np.abs(diff_lon - 360) < 170, diff_lon-360, diff_lon)
odf['ll_dist_to_point'] = ((diff_lon)**2 + (ds_ref.latitude.data[odf.lat_id] - odf.CenLat)**2)**0.5

assert odf['ll_dist_to_point'].max() < (max_lon**2 + max_lat**2)**0.5

# just select the glacier_mask variable:
ds_ref = ds_ref.drop_vars(['time_bnds','t_ref','precip']).drop_dims('time')


for var in ['t_ref','precip']:
    print(var)
    with xr.open_mfdataset(path + f'/{scenario}/' + 'atmos_month_*.nc', engine='netcdf4') as ds:
        ds = ds[var].load()
    ds = ds.rename({'lat': 'latitude'}).rename({'lon': 'longitude'})

    ds.coords['longitude'] = np.where(ds.longitude.values < 0,
                                      ds.longitude.values + 360,
                                      ds.longitude.values)

    ds = ds.sortby(ds.longitude)
    ds.longitude.attrs['units'] = 'degrees_onlypositive'

    # as we use here only those gridpoints where glaciers are involved, need to put the mask on dsi as well!
    # dsi = ds_inv.where(ds_inv['glacier_mask'], drop = True)  # this makes out of in total 6483600 points only 116280 points!!!
    dsi = ds.isel(time=[0]).where(ds_ref['glacier_mask'], drop = True)
    # we do not want any dependency on latitude and longitude
    dsif = dsi.stack(points=('latitude', 'longitude')).reset_index(('points'))

    # drop the non-glacierized points
    dsifs = dsif.where(np.isfinite(dsi.stack(points=('latitude', 'longitude')).reset_index(('time', 'points'))), drop=True)
    # I have to drop the 'time_' dimension, to be equal to the era5_land example, because the invariant file should not have any time dependence !
    dsifs = dsifs.drop('time')
    dsifs = dsifs.drop('time_')


    ### test 
    lon, lat = (10.7584, 46.8003)
    c = (dsifs.longitude - lon)**2 + (dsifs.latitude - lat)**2
    surf_hef = dsifs.isel(points=c.argmin())
    np.testing.assert_allclose(surf_hef.longitude, lon, rtol=0.2)
    np.testing.assert_allclose(surf_hef.latitude, lat, rtol=0.2)

    # RGI60-19.00124
    lon,lat = (-70.8931 +360, -72.4474)
    c = (dsifs.longitude - lon)**2 + (dsifs.latitude - lat)**2
    surf_g = dsifs.isel(points=c.argmin())
    np.testing.assert_allclose(surf_g.longitude, lon, rtol=0.2)
    np.testing.assert_allclose(surf_g.latitude, lat, rtol=0.2)

    ####

    if scenario == 'oversh_T20OS15' and var =='t_ref':
        dsifs.to_netcdf(f'2023.2/gfdl-esm2m_{scenario}_glacier_invariant_flat.nc')

    for t in ds.time.values[:]:  # ds_merged_glaciers.time.values: .sel(time=slice('1901-04','2016-12'))
        # produce a temporary file for each month
        sel_l = ds.sel(time=[t])
        # don't do the dropping twice!!!!
        #sel = sel_l.where(ds_inv['glacier_mask'], drop = True)
        sel = sel_l.where(ds_ref['glacier_mask'])
        sel = sel.stack(points=('latitude', 'longitude')).reset_index(('time', 'points'))
        sel = sel.where(np.isfinite(sel), drop=True)
        sel.to_netcdf(f'2023.2/tmp/tmp_{scenario}_{var}_{t}.nc')
        #sel.to_netcdf(f'flat/tmp/tmp_{scenario}_{var}_{str(t[0])[:7]}.nc')

    
    for cent in [18,19,20,21,22,23,24]:
        with xr.open_mfdataset(f'2023.2/tmp/tmp_{scenario}_{var}_{cent}*.nc',
                                     concat_dim='time', combine='nested', engine ='netcdf4',
                               parallel = True).rename_vars({'time_':'time'}) as dso_all2: #use_cftime ...

            dso_all2.attrs['history'] = 'longitudes to 0 -> 360,  only glacier gridpoints chosen and flattened latitude/longitude --> points'
            dso_all2.attrs['info'] = f'gfdl-esm2m: {scenario}, University of Bern, data provided by Fabrice Lacroix' 
            dso_all2.attrs['postprocessing_date'] = str(np.datetime64('today','D'))
            dso_all2.attrs['postprocessing_scientist'] = 'lilian.schuster@uibk.ac.at'
            dso_all2.attrs['version'] = '2023.2'
            if var == 't_ref':
                var_n = 'tas'
            elif var == 'precip':
                var_n = 'pr'
            dso_all2 = dso_all2.rename_vars({var:var_n})
            dso_all2.to_netcdf(f'2023.2/tmp/gfdl-esm2m_{scenario}_{var_n}_global_monthly_flat_glaciers_{cent}.nc')
            
            
    dt = xr.open_mfdataset(f'2023.2/tmp/gfdl-esm2m_{scenario}_{var_n}_global_monthly_flat_glaciers_*.nc')
    dt = dt.rename({'latitude': 'lat'})
    dt = dt.rename({'longitude': 'lon'})
    # make sure that lat and lon are not time-dependent!!!
    assert np.all(dt.lat.std(dim='time').load() < 1e-10)
    assert np.all(dt.lon.std(dim='time').load() < 1e-10)
    # now remove the wrong time-dependence ...
    dt['lat'] = dt.lat.isel(time=0).reset_coords().lat
    dt['lon'] = dt.lon.isel(time=0).reset_coords().lon
    
    if var_n =='pr':
        assert dt.pr.attrs['units'] == 'kg/m2/s'
        # this is more consistent with the non-flattened files ...
        dt.pr.attrs['units'] = 'kg m-2 s-1'
    dt.to_netcdf(f'2023.2/gfdl-esm2m_{scenario}_{var_n}_global_monthly_flat_glaciers.nc')


    
    
