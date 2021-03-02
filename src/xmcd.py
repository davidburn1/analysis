import h5py
import numpy as np
import pandas as pd



def correctEnergyShift(data):
	#differentiate
	#minimise the differential	
	#correct for the shift
	pass


def loadXMCDList(directory, scans):
	"""
	Take a list of scan numbers: scans,
	Normalise all data by I0,
	Interpolate energy onto a regular grid, 
	Average the scans in each list.
	"""
	data = {}
	data['m17'] = {}
	data['m18'] = {}
	data['raw'] = [None] * len(scans)
	

	mcsr17_grid = np.array([])
	mcsr18_grid = np.array([])
	for i, s in enumerate(scans):
		f = h5py.File(directory+"/i10-%06d.nxs" % (s) ,'r')
		grp = f['entry1']['instrument']

		energy = grp['energy']['demand'][:]
		energyRaw = grp['energy']['pgm_energy'][:]

		data['raw'][i] = {}
		data['raw'][i]['energy'] = grp['energy']['pgm_energy'][:] 
		data['raw'][i]['macr16'] = grp['mcs16']['data'][:]
		data['raw'][i]['macr17'] = grp['mcs17']['data'][:]
		data['raw'][i]['macr18'] = grp['mcs18']['data'][:]

		mcsr17  = grp['mcs17']['data'][:] / grp['mcs16']['data'][:]
		mcsr18  = grp['mcs18']['data'][:] / grp['mcs16']['data'][:]
		f.close()

		# interpolate the energy to get the signal on a regular energy grid
		mcsr17_grid = np.append(mcsr17_grid, np.interp(energy, energyRaw, mcsr17))
		mcsr18_grid = np.append(mcsr18_grid, np.interp(energy, energyRaw, mcsr18))


	# average over all of the scans in the list
	mcsr17_grid = mcsr17_grid.reshape(len(scans),len(energy))
	mcsr18_grid = mcsr18_grid.reshape(len(scans),len(energy))	
	data['m17'] = mcsr17_grid.mean(axis=0)
	data['m18'] = mcsr18_grid.mean(axis=0)

	data['energy'] = energy

	return data



# analyse collections of XMCD scans
def loadXMCD(directory, scansA, scansB):
	"""
	Take two lists of scan numbers, scansA and scansB. 
	Normalise all data by I0, interpolate energy onto a regular grid, average the scans in each list.
	"""
	dA = loadXMCDList(directory, scansA)
	dB = loadXMCDList(directory, scansB)

	data = {}
	data['raw_a'] = dA['raw']
	data['raw_b'] = dB['raw']
	data['energy'] = dA['energy']
	data['m17'] = {'a':dA['m17'], 'b':dB['m17']}
	data['m18'] = {'a':dA['m18'], 'b':dB['m18']}
	 

	# find the energies of the maximum and minimum differences
	for m in ['m17', 'm18']:
		minIndex = np.argmin(data[m]['a']-data[m]['b'])
		data[m]['min'] = data['energy'][minIndex]

		maxIndex = np.argmax(data[m]['a']-data[m]['b'])
		data[m]['max'] = data['energy'][maxIndex]

	return data


def saveXMCDdat(filename, data):
    d2 = {'energy':data['energy'], 'a':data['m17']['a'], 'b':data['m17']['b']}
    df = pd.DataFrame(d2)
    df.to_csv(filename, index=False)


# analyse collections of XMCD scans
def loadXMCDStepScans(directory, scansA, scansB):
    data = {}
    egyStrings = ["egy_g_idu_circ_pos_energy", "egy_g_idu_circ_neg_energy", "egy_g_idd_circ_pos_energy", "egy_g_idd_circ_neg_energy"]
    
    
    
    f = h5py.File(directory+"/i10-%06d.nxs" % (scansA) ,'r')
    grp = f['entry1']['instrument']
    for egyStr in egyStrings:
    	if egyStr in grp:
    		data['energy'] = grp[egyStr][egyStr][:]
            
    #refl = f['entry1']['instrument']['refl']['refl'][()]
    data['a'] = grp['refl']['refl'][()] / grp['macr16']['data'][:]
    f.close()
    
    
    f = h5py.File(directory+"/i10-%06d.nxs" % (scansB) ,'r')
    grp = f['entry1']['instrument']
    for egyStr in egyStrings:
    	if egyStr in grp:
    		data['energy'] = grp[egyStr][egyStr][:]
            
    #refl = f['entry1']['instrument']['refl']['refl'][()]
    data['b'] = grp['refl']['refl'][()] / grp['macr16']['data'][:]
    f.close()
    
    return data





""" MH based on flying scans of the field, repeated at both polarisations """
def loadMH(directory, s):
	# pc_dec, pc_inc, nc_dec, nc_inc
	data = {}
	data['pc'] = {}
	data['nc'] = {}

	data['pc']['inc'] = {}
	data['pc']['dec'] = {}
	data['nc']['inc'] = {}
	data['nc']['dec'] = {}

	f = h5py.File(directory+"/i10-%06d.nxs" % (s) ,'r')
	grp = f['entry1']['instrument']
	data['pc']['dec']['field'] = grp['field']['field'][()]
	data['pc']['dec']['drain'] = grp['drain']['drain'][()]
	data['pc']['dec']['fluo1'] = grp['fluo1']['fluo1'][()]
	data['pc']['dec']['fluo2'] = grp['fluo2']['fluo2'][()]
	f.close()

	f = h5py.File(directory+"/i10-%06d.nxs" % (s+1) ,'r')
	grp = f['entry1']['instrument']
	data['pc']['inc']['field'] = grp['field']['field'][()]
	data['pc']['inc']['drain'] = grp['drain']['drain'][()]
	data['pc']['inc']['fluo1'] = grp['fluo1']['fluo1'][()]
	data['pc']['inc']['fluo2'] = grp['fluo2']['fluo2'][()]
	f.close()

	f = h5py.File(directory+"/i10-%06d.nxs" % (s+2) ,'r')
	grp = f['entry1']['instrument']
	data['nc']['dec']['field'] = grp['field']['field'][()]
	data['nc']['dec']['drain'] = grp['drain']['drain'][()]
	data['nc']['dec']['fluo1'] = grp['fluo1']['fluo1'][()]
	data['nc']['dec']['fluo2'] = grp['fluo2']['fluo2'][()]
	f.close()

	f = h5py.File(directory+"/i10-%06d.nxs" % (s+3) ,'r')
	grp = f['entry1']['instrument']
	data['nc']['inc']['field'] = grp['field']['field'][()]
	data['nc']['inc']['drain'] = grp['drain']['drain'][()]
	data['nc']['inc']['fluo1'] = grp['fluo1']['fluo1'][()]
	data['nc']['inc']['fluo2'] = grp['fluo2']['fluo2'][()]
	f.close()

	return data








def loadXMLD(directory, scans):
	data = {}
	data['scans'] = []

	for s in scans:
		f = h5py.File(directory+"/i10-%06d.nxs" % (s) ,'r')
		grp = f['entry1']['instrument']
		energy = grp['egy_g_idu_lin_arbitrary_energy']['demand'][:]
		raw_energy = grp['egy_g_idu_lin_arbitrary_energy']['pgm_energy'][:]
		sig  = grp['mcsr17_g']['data'][:] / grp['mcsr16_g']['data'][:]
		f.close()

		sig = np.interp(energy, raw_energy, sig) # interpolate to get regular energy points
		data['scans'] = np.append(data['scans'], {'energy':energy, 'sig':sig})

	return data





