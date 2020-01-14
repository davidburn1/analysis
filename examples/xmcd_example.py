# -*- coding: utf-8 -*-
"""

"""

import matplotlib.pyplot as plt
import numpy as np
import h5py
from .. import loadXMCD


directory = "/dls/i10/data/2019/mm23338-1/data"

#%%


#Fe
data = loadXMCD(directory, [585444], [585445] )

fig, ax = plt.subplots(2, 1, figsize=(6, 6), facecolor='w', sharex=True)

ax[0].plot(data['energy'], data['m17']['a'], 'r')
ax[0].plot(data['energy'], data['m17']['b'], 'b')

ax[1].plot(data['energy'], data['m17']['b']-data['m17']['a'], 'k')

ax[1].set_xlabel("Energy (eV)")
ax[0].set_ylabel("XAS")
ax[1].set_ylabel("Difference")

plt.show()

print data['energy'][np.argmax(data['m17']['b']-data['m17']['a'])]

#%%


#Co
data = loadXMCD(directory, [585446], [585447] )

fig, ax = plt.subplots(2, 1, figsize=(6, 6), facecolor='w', sharex=True)

ax[0].plot(data['energy'], data['m17']['a'], 'r')
ax[0].plot(data['energy'], data['m17']['b'], 'b')

ax[1].plot(data['energy'], data['m17']['b']-data['m17']['a'], 'k')

ax[1].set_xlabel("Energy (eV)")
ax[0].set_ylabel("XAS")
ax[1].set_ylabel("Difference")

plt.show()

print data['energy'][np.argmax(data['m17']['b']-data['m17']['a'])]



#%%


#Ni
data = loadXMCD(directory, [585448], [585449] )

fig, ax = plt.subplots(2, 1, figsize=(6, 6), facecolor='w', sharex=True)

ax[0].plot(data['energy'], data['m17']['a'], 'r')
ax[0].plot(data['energy'], data['m17']['b'], 'b')

ax[1].plot(data['energy'], data['m17']['b']-data['m17']['a'], 'k')

ax[1].set_xlabel("Energy (eV)")
ax[0].set_ylabel("XAS")
ax[1].set_ylabel("Difference")

plt.show()

print data['energy'][np.argmax(data['m17']['b']-data['m17']['a'])]
