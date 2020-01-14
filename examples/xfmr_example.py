import numpy as np
import matplotlib.pyplot as plt
from lmfit import Parameters
from David.analysis.xfmr import loadXFMRDelayScans2 as loadXFMRDelayScans, fitXFMR2 as fitXFMR

plt.rcParams.update({'font.size': 14, 'xtick.top': True, 'ytick.right': True, 'xtick.direction': 'in', 'ytick.direction': 'in'})

#%%

directory = "/dls/i10/data/2019/mm23338-1/data"









#%%
""" load the data """
data = {}
data['Fecp'] = {}

fields = np.array([5,10,13,14])
fields = np.append(fields, np.arange(15, 22.1, 0.2))
fields = np.append(fields, [23, 24, 25])
fields = np.append(fields, np.arange(26, 32.1, 0.2))
fields = np.append(fields, [33, 34, 35, 40])
delay = np.linspace(0, 500, 36)
scanIDs = np.arange(len(fields)) + 585516

data['Fecp'] = loadXFMRDelayScans(directory, fields, delay, scanIDs)

#%%
""" plot a colormap """

fig, ax = plt.subplots(1, 1, figsize=(6, 5), facecolor='w')
plt.pcolormesh(grp['field'], grp['delay'], grp['x'].T, cmap='RdYlBu_r', vmin=-5e-13, vmax=5e-13)
plt.title("Fe pc")
plt.colorbar()
plt.xlabel("Field (mT)")
plt.ylabel("Delay (ps)")
plt.show()

fig, ax = plt.subplots(1, 1, figsize=(6, 5), facecolor='w')
plt.pcolormesh(grp['field'], grp['delay'], grp['y'].T, cmap='RdYlBu_r', vmin=-1e-12, vmax=1e-12)
plt.title("Fe pc")
plt.colorbar()
plt.xlabel("Field (mT)")
plt.ylabel("Delay (ps)")
plt.show()


#%%
""" Fit the data  """

p=Parameters()
p.add('amp', vary=True, value=1e-13, min=1e-15, max=4e-13)
p.add('phase', vary=True, value=130.0, min=-100.0, max=150.0)
p.add('freq', vary=False, value=4)
p.add('offset', vary=True, value=0.0)

fitXFMR(data['Fecp'], p)



#%%
""" plot the fit """

fig, ax = plt.subplots(2, 1, figsize=(6, 10), facecolor='w', sharex=True)

grp = data['Fepc']
ax[0].errorbar(grp['field'], grp['amp'], yerr=grp['amp_stderr'], fmt='r', label="Fe")
ax[1].errorbar(grp['field'], grp['phase'], yerr=grp['phase_stderr'], fmt='r')

#ax[0].set_title("m7-0047 (10 $\AA$ Mn) 4 GHz")
ax[0].legend(fontsize=10, loc=1)
ax[1].set_xlabel("Field (mT)")
ax[0].set_ylabel("Amplitude (A)")
ax[1].set_ylabel("Phase (degrees)")
#plt.xlim(-200,200)

ax[0].set_ylim(0, 5e-13)
#ax[1].set_ylim(-180, 180)
plt.show()

