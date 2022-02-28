#!/usr/bin/python

import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import os
import pandas as pd
import scipy.stats
xr.set_options(keep_attrs=True)

alphabet = ['(a)','(b)','(c)','(d)','(e)','(f)','(g)','(h)','(i)']

monthnames = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']


# Define map plot properties
geoplotprop = {}
geoplotprop['TREFHT_trend'] = {'levels' : 10.*np.arange(-.2,.22,.02), 'cmap' : plt.cm.RdBu_r,'label':'Trend in 2m air temperature (K/decade)' }
geoplotprop['T200_trend'] = {'levels' : 10.*np.arange(-.1,.11,.01), 'cmap' : plt.cm.RdBu_r  ,'label':'Trend in 200m air temperature (K/decade)'}
geoplotprop['T500_trend'] = {'levels' : 10.*np.arange(-.1,.11,.01), 'cmap' : plt.cm.RdBu_r  ,'label':'Trend in 500m air temperature (K/decade)'}
geoplotprop['U_trend'] = {'levels' : 10.*np.arange(-.08,.08+.01,.01), 'cmap' : plt.cm.PRGn  ,'label':'Trend in surface U wind (m s$^{-1}$/decade)'}
geoplotprop['V_trend'] = {'levels' : 10.*np.arange(-.08,.08+.01,.01), 'cmap' : plt.cm.PRGn  ,'label':'Trend in surface V wind (m s$^{-1}$/decade)'}
geoplotprop['windspeed_trend'] = {'levels' : 10.*np.arange(-.04,.04+.005,.005), 'cmap' : plt.cm.PRGn  ,'label':'Trend in surface wind speed (m s$^{-1}$/decade)'}
geoplotprop['PS_trend'] = {'levels' : 10.*np.arange(-20,22,2), 'cmap' : plt.cm.BrBG,'label':'Trend in surface pressure (Pa/decade)'}
geoplotprop['Z200_trend'] = {'levels' : np.arange(-30,33,3), 'cmap' : plt.cm.PiYG,'label':'Trend in Z200 (m/decade)'}
geoplotprop['Z500_trend'] = {'levels' : np.arange(-20,22,2), 'cmap' : plt.cm.PiYG,'label':'Trend in Z500 (m/decade)'}


def set_line_prop (mynames):
    
    mylist = []
    for f in mynames:
        if 'LENSmean' in f:
            mylist.append({'label' : 'LENSmean', 'c' : 'tab:blue', 'linewidth' : 1.5, 'alpha' : 1.})

        elif 'LENS' in f:
            mylist.append({'label' : 'LENS', 'c' : 'tab:blue', 'linewidth' : .5, 'alpha' : .3})

        elif '60' in f or 'aNUDGEmean' in f:
            mylist.append({'label' : 'aNUDGE', 'c' : 'tab:red', 'linewidth' : 1.5, 'alpha' : 1.})

        elif 'ERA' in f or 'GIS'  in f or 'HadC' in f or 'HADI' in f or 'OBS' in f:
             mylist.append({'label' : 'OBS', 'c' : 'k', 'linewidth' : 1.5, 'alpha' : 1.})
 
    df = pd.DataFrame(mylist, index = mynames) 
    df = df.transpose()
    
    return df


def linregress(first_samples, second_samples, dim):
    slope, intercept, r_value, p_value, std_err = xr.apply_ufunc(_nanlinregress,
                       first_samples, second_samples,
                       input_core_dims  = [[dim], [dim]], 
                       output_core_dims = [[],[],[],[],[]],
                       vectorize=True)
        
    return slope, intercept, r_value, p_value, std_err

def _nanlinregress(x, y):
    '''Calls scipy linregress only on finite numbers of x and y'''
    finite = np.isfinite(x) & np.isfinite(y)
    if not finite.any():
        # empty arrays passed to linreg raise ValueError:
        # force returning an object with nans:
        return scipy.stats.linregress([np.nan], [np.nan])
    return scipy.stats.linregress(x[finite], y[finite])


def pearson(first_samples, second_samples, dim):
    pearson, pval = xr.apply_ufunc(_nanpearson,
                       first_samples, second_samples,
                       input_core_dims  = [[dim], [dim]], 
                       output_core_dims = [[],[]],
                       vectorize=True)
        
    return pearson, pval

def _nanpearson(x, y):
    '''Calls scipy pearsonr only on finite numbers of x and y'''
    finite = np.isfinite(x) & np.isfinite(y)
    if not finite.any():
        # empty arrays passed to linreg raise ValueError:
        # force returning an object with nans:
        return scipy.stats.pearsonr([np.nan], [np.nan])
    return scipy.stats.pearsonr(x[finite], y[finite])



def xr_reshape(A, dim, newdims, coords):
    """ Reshape DataArray A to convert its dimension dim into sub-dimensions given by
    newdims and the corresponding coords.
    Example: Ar = xr_reshape(A, 'time', ['year', 'month'], [(2017, 2018), np.arange(12)]) """

    # Create a pandas MultiIndex from these labels
    ind = pd.MultiIndex.from_product(coords, names=newdims)

    # Replace the time index in the DataArray by this new index,
    A1 = A.copy()

    A1.coords[dim] = ind

    # Convert multiindex to individual dims using DataArray.unstack().
    # This changes dimension order! The new dimensions are at the end.
    A1 = A1.unstack(dim)

    # Permute to restore dimensions
    i = A.dims.index(dim)
    dims = list(A1.dims)

    for d in newdims[::-1]:
        dims.insert(i, d)

    for d in newdims:
        _ = dims.pop(-1)


    return A1.transpose(*dims)
