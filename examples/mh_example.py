import numpy as np
import matplotlib.pyplot as plt
import h5py
import matplotlib.cm as cm
plt.rcParams.update({'font.size': 14, 'xtick.top': True, 'ytick.right': True, 'xtick.direction': 'in', 'ytick.direction': 'in'})

#%%%

        
directory = "/dls/i10/data/2019/mm23338-1/data"


    
#%%


def loadMH(scanID):
    f = h5py.File(directory+"/i10-%06d.nxs" % scanID, 'r')
    grp = f['entry1']['instrument']
    signal = grp['refl']['refl'][:] / grp['macr16']['data'][:]
    field = grp['vmag']['field'][:]
    f.close()
    
    f = h5py.File(directory+"/i10-%06d.nxs" % (scanID+1), 'r')
    grp = f['entry1']['instrument']
    signal = np.append(signal, grp['refl']['refl'][:] / grp['macr16']['data'][:])
    field = np.append(field, grp['vmag']['field'][:])
    
    signal = signal - np.mean(signal)
    signal = signal / np.max(signal)
    
    return {'field':field, 'sig':signal}

#%%
    
fig, ax = plt.subplots(1, 1, figsize=(10, 6), facecolor='w')


d = loadMH(585456)
plt.plot(d['field'], d['sig'], 'r', label='Co')
d = loadMH(585454)
plt.plot(d['field'], d['sig'], 'g', label='Fe')
d = loadMH(585458)
plt.plot(d['field'], d['sig'], 'b', label='Ni')

plt.legend()
plt.xlabel("Field (mT)")
plt.ylabel("Magnetisation")

plt.show()

