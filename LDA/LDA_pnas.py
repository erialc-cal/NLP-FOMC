#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 15:35:24 2021

@author: Claire He
 Inspired by PNAS article

"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as mpl
#%%
#### Prepare speech document : 
file_path ='/Users/h2jw/Documents/GitHub/NLP-FOMC/update_version_7.csv'

df = pd.read_csv(file_path, low_memory=True)
    
#%% 

#### Extra cleaning    
  # Load in novelty, transience, resonance

example_NTR_path = 'novel_trans_reson.txt'

NTR_df = pd.read_table(example_NTR_path, sep=' ',
                       header=None, names=['Novelty', 'Transience', 'Resonance'])

#%%


def plot_quants_2Dhist(quants, NTR_df, ax, xbins, ybins, make_cbar=True,
                       cbar_axis=False, cbar_orientation='vertical', colorvmax=None):

    q0 = NTR_df[quants[0]]
    q1 = NTR_df[quants[1]]
    
    q0bins = xbins
    q1bins = ybins
    
    H, xedges, yedges = np.histogram2d(q0.as_matrix(),
                                       q1.as_matrix(),
                                       bins=[q0bins, q1bins])

    # H needs to be rotated and flipped
    H = np.rot90(H)
    H = np.flipud(H)

    # Mask zeros
    Hmasked = np.ma.masked_where(H==0,H) # Mask pixels with a value
    
    # Plot 2D histogram using pcolor
    if colorvmax:
        usemax = colorvmax
    else:
        usemax = H.max()
    pcolm = ax.pcolormesh(xedges,yedges,Hmasked, norm=mpl.colors.LogNorm(vmin=1, vmax=usemax))
    
    if make_cbar:
        if cbar_axis:
            cbar = fig.colorbar(pcolm, cax=cbar_axis, orientation=cbar_orientation)  
        else:
            cbar = fig.colorbar(pcolm, ax=ax, orientation=cbar_orientation)
        cbar.ax.set_ylabel('counts')
    
    ax.set_xlabel(quants[0])
    ax.set_ylabel(quants[1])
    
    if make_cbar:
        return H, cbar
    else:
        return H
