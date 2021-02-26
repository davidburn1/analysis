import h5py
import numpy as np

def loadMH(directory, scanID, driftGradient=None):
    f = h5py.File(directory+"/i10-%06d.nxs" % scanID, 'r')
    grp = f['entry1']['instrument']
    signal = grp['refl']['refl'][:] / grp['macr16']['data'][:]
    field = grp['vmag']['field'][:]
    f.close()
    
    f = h5py.File(directory+"/i10-%06d.nxs" % (scanID+1), 'r')
    grp = f['entry1']['instrument']
    signal = np.append(signal, grp['refl']['refl'][:] / grp['macr16']['data'][:])
    field = np.append(field, grp['vmag']['field'][:])
    
    
    # subtract a gradient to take account of drift over time
    if (driftGradient is None):
        #automatically determine gradient from first and last point
        driftGradient = (signal[-1] - signal[0]) / len(signal)
    x = np.arange(len(signal))
    signal = signal - driftGradient*x
    
    
    # normalize
    signal = signal - np.mean(signal)
    signal = signal / np.max(signal)
    
    
    return {'field':field, 'sig':signal}
