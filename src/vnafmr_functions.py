#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 00:02:44 2019

@author: chj24174
"""


import numpy as np
import matplotlib.pyplot as plt
import h5py
import matplotlib.cm as cm

from mpl_toolkits import mplot3d



def plotVNAFMR(scanID):
    fig, ax = plt.subplots(1, 1, figsize=(8,6), facecolor='w', sharex=True)
    
    f = h5py.File(directory+'/poms-vnafmr-%06d.hdf5' % scanID,'r')


    data = np.absolute(f['s12'][:]).T
    X,Y = np.meshgrid(f['field'][:], f['freq'][:] )
    plt.pcolormesh(X,Y,data, cmap='jet')#, vmax=0.0002, vmin=-0.0002)
    
    
    plt.colorbar()
    plt.xlabel("Field (mT)")
    plt.ylabel("Frequency (GHz)")
    plt.show()
    f.close()



def plotVNAFMRDiff(scanID):
    fig, ax = plt.subplots(1, 1, figsize=(8,6), facecolor='w', sharex=True)
    
    f = h5py.File(directory+'/poms-vnafmr-%06d.hdf5' % scanID,'r')
    
    #field = f['field'][:]
    #freq = f['freq'][:]

    data = np.absolute(f['s12'][:]).T
    data = np.diff(data, axis=1)
    X,Y = np.meshgrid(f['field'][:], f['freq'][:] )
    plt.pcolormesh(X,Y,data, cmap='jet', vmax=0.0002, vmin=-0.0002)
    
    
    plt.colorbar()
    plt.xlabel("Field (mT)")
    plt.ylabel("Frequency (GHz)")
    plt.show()
    f.close()
    
