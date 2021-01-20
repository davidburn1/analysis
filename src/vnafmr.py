#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 27 00:02:44 2019

@author: chj24174
"""


import numpy as np
import h5py


    
def averageVNAFMR(directory, scanIDs):
    grid = np.array([])
    for s in scanIDs:
        f = h5py.File(directory+'/poms-vnafmr-%06d.hdf5' % s,'r')
        field = f['field'][:]
        freq = f['freq'][:]

        data = np.absolute(f['s12'][:]).T #+  np.transpose(s21)
        data = np.diff(data, axis=1)
        grid = np.append(grid, data)
        f.close()
        
    Xd,Yd = np.meshgrid(field[:-1], freq)
    #print np.shape(grid)
    grid = np.reshape(grid, (len(field)-1, len(freq), len(scanIDs)), order='f')
    gridd = grid.mean(2)
    
    
    X,Y = np.meshgrid(field, freq)
    #print np.shape(grid)
    grid = np.concatenate((np.zeros(len(freq))[None,:], gridd), axis=0).cumsum(axis=0)
    

    gridd = np.concatenate((np.zeros(len(freq))[None,:], gridd), axis=0)
    #return X,Y,grid, Xd, Yd, gridd

    return {'freq':freq, 'field':field, 'grid':grid.T, 'gridd':gridd.T}
                     
                
