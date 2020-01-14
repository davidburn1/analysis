

import numpy as np
import matplotlib.pyplot as plt
import h5py
import matplotlib.cm as cm
plt.rcParams.update({'font.size': 14, 'xtick.top': True, 'ytick.right': True, 'xtick.direction': 'in', 'ytick.direction': 'in'})

    
#%%
    

directory = "/dls/i10/data/2019/mm23338-1/data/data/data"


shift=1e-12

fields = [-200, -150] + range(-110, 111, 2) + [150, 200]
scanIDs = np.arange(len(fields)) + 581940

f, ax = plt.subplots(1, 1, figsize=(6, 15))

for i in range(len(fields)):
    f = h5py.File(directory+"/i10-%06d.nxs" % scanIDs[i], 'r')
    grp = f['entry1']['instrument']
    delay = grp['delay']['delay'][:]
    x1 = grp['zurich']['x'][:] 
    y1 = grp['zurich']['y'][:] 
    f.close()
    
    plt.plot(delay, x1+fields[i]*shift)


plt.xlabel("Delay (ps)")
plt.ylabel("XFMR")

plt.show()

