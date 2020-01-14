import h5py
import numpy as np
import matplotlib.pyplot as plt
from lmfit import minimize, Parameters, fit_report, Model


def loadXFMRDelayScans(directory, fields, delay, scanIDs):
	grid = np.zeros((len(fields), len(delay)))

	for i in range(len(fields)):
		f = h5py.File(directory+"/i10-%06d.nxs" % scanIDs[i], 'r')
		grp = f['entry1']['instrument']
		delay = grp['delay']['delay'][:]
		grid[i,:] = grp['zurich']['x'][:]  
		f.close()

	return grid

def loadXFMRDelayScans2(directory, fields, delay, scanIDs):
	# improved version which returns a dict
	data = {}
	data['field'] = fields
	data['delay'] = delay
	data['static'] = np.zeros((len(fields), len(delay)))
	data['x'] = np.zeros((len(fields), len(delay)))
	data['y'] = np.zeros((len(fields), len(delay)))

	for i in range(len(fields)):
		f = h5py.File(directory+"/i10-%06d.nxs" % scanIDs[i], 'r')
		grp = f['entry1']['instrument']
		#delay = grp['delay']['delay'][:]
		data['static'][i,:] = grp['zurich']['static'][:]
		data['x'][i,:] = grp['zurich']['x'][:]  
		data['y'][i,:] = grp['zurich']['y'][:]
		f.close()

	return data



def load_data(delays, fields, scanIDs):
    #loads a series of delay scans at different fields
    data = {}
    data['fields'] = fields
    data['delays'] = delays

    data['x_raw'] = np.empty((len(delays),len(fields)))
    data['y_raw'] = np.empty((len(delays),len(fields)))

    #print np.shape(data['x_raw'])

    for i,s in enumerate(scanIDs):
        f = h5py.File("../../../i10-%06d.nxs" % (s ) ,'r')
        #print f['entry1']['before_scan']['delay'].value
        grp = f['entry1']['instrument']
	if len(scanIDs) == len(fields):
		data['x_raw'][:,i]  = (grp['xfmr']['x'][:] ) /1.0e-12
		data['y_raw'][:,i]  = (grp['xfmr']['y'][:] ) /1.0e-12
	elif len(scanIDs) == len(delays):
		data['x_raw'][i,:]  = (grp['xfmr']['x'][:] ) /1.0e-12
		data['y_raw'][i,:]  = (grp['xfmr']['y'][:] ) /1.0e-12
	else:
		print "length of scanIDs must equal either length of delays or fields"
        f.close()

    return data


def process_lia(data, lia_off_x, lia_off_y, lia_phase, lia_off_re=0, lia_off_im=0):
    data['gridx'] = data['x_raw'] - lia_off_x
    data['gridy'] = data['y_raw'] - lia_off_y

    # find true real and imagnary lock-in contributions based on a lia_phase argand rotation
    th = np.radians(lia_phase)
    data['lia_re'] = data['gridx']*np.cos(th) + data['gridy']*np.sin(th)
    data['lia_im'] = -data['gridx']*np.sin(th) + data['gridy']*np.cos(th)

    data['lia_re'] = data['lia_re'] - lia_off_re
    data['lia_im'] = data['lia_im'] - lia_off_im

    #find phase and amplitude of the lia signal
    data['lia_ph'] = np.arctan2(data['lia_re'], data['lia_im'])
    data['lia_r'] = np.sqrt(data['lia_re']**2 + data['lia_im']**2)


    
    return data


def plot_lia(data):
    fig, ax = plt.subplots(1,4, figsize=(16, 6), facecolor='w', sharex=True, sharey=True)
    vmax = np.max([data['lia_re'], data['lia_im']])
    vmin = np.min([data['lia_re'], data['lia_im']])
    
    ax[0].pcolormesh(data['fields'], data['delays'], data['lia_re'], cmap='bwr', vmin=vmin, vmax=vmax)
    ax[1].pcolormesh(data['fields'], data['delays'], data['lia_im'], cmap='bwr', vmin=vmin, vmax=vmax)

    ax[2].pcolormesh(data['fields'], data['delays'], data['lia_r'], cmap='gist_ncar')
    ax[3].pcolormesh(data['fields'], data['delays'], data['lia_ph'], cmap='bwr', vmax=np.pi, vmin=-np.pi)
    
    ax[0].set_ylabel("Delay (ps)")
    ax[0].set_xlabel("Field (mT)")
    ax[1].set_xlabel("Field (mT)")
    ax[2].set_xlabel("Field (mT)")
    ax[3].set_xlabel("Field (mT)")
    
    ax[0].set_title("X'")
    ax[1].set_title("Y'")
    ax[2].set_title("Magnitude")
    ax[3].set_title("Phase")
    plt.show()


def plot_lia_argand(data):
	plt.plot(data['lia_re'], data['lia_im'])
	plt.plot([0], [0], 'o')
	plt.xlabel("X'")
	plt.ylabel("Y'")
	plt.show()





def fitSin(data, phase=50, showPlot=False):
    
    def sinFunc(x, freq, amp, off, phase):
        return amp * np.sin(np.radians(x*freq*360/1000.0 + phase)) + off

    mod = Model(sinFunc)
    
    data['r'] = np.zeros(len(data['fields']))
    data['ph'] = np.zeros(len(data['fields']))
    
    params = mod.make_params(freq=2,amp=1, off=12, phase=phase)
    params['freq'].vary = False
    params['phase'].max = 360
    params['phase'].min = 0
    params['amp'].min = 0
    
    for i, d in enumerate(data['fields']):

        result = mod.fit(data['lia_r'][1:,i], params, x=data['delays'][1:]) # ignore the first bad point
        params = result.params
        out = result.params.valuesdict()
        data['r'][i] = out['amp']
        data['ph'][i] = out['phase']
        
	if showPlot:
		plt.plot(data['delays'],data['lia_r'][:,i])
		#plt.plot(data['delays'], result.init_fit, 'k--')
		plt.plot(data['delays'][1:], result.best_fit, 'r-')
		plt.show()

    return data



def fitXFMR(p, grid, delay, showPlots=False):

	def sin(x, amp, phase, freq, offset):
		return amp*np.sin(phase*2*np.pi/360.0 + ( x)/1000.0*freq*2*np.pi) + offset

	def fitSinData(x,y, params):
		#result = mod.fit(y, p, x=x, method='nelder')
		result = mod.fit(y, p, x=x)

		if showPlots:
			plt.plot(x, result.init_fit, 'k--')
			plt.plot(x, result.best_fit, 'r-')
			plt.plot(x, y, '.')
			plt.show()
		return result

	mod =  Model(sin)
	fitparams = []
	    

	for i in range(np.shape(grid)[0]):
	    fit = fitSinData(delay, grid[i,:], p)
            valuesdict = fit.params.valuesdict() 
            valuesdict['amp_stderr'] = fit.params['amp'].stderr
            valuesdict['phase_stderr'] = fit.params['phase'].stderr
	    fitparams.append( valuesdict )
	    p = fit.params
	    
	amp = [g['amp'] for  g in fitparams]
	phase = [g['phase'] for  g in fitparams]

	data = {}
	data['amp'] = np.array(amp)
	data['phase'] = np.array(phase)
        data['amp_stderr'] = np.array([g['amp_stderr'] for  g in fitparams])
        data['phase_stderr'] = np.array([g['phase_stderr'] for  g in fitparams])

	return data



def fitXFMR2(data, p, showPlots=False):

	def sin(x, amp, phase, freq, offset):
		return amp*np.sin(phase*2*np.pi/360.0 + ( x)/1000.0*freq*2*np.pi) + offset

	def fitSinData(x,y, params):
		#result = mod.fit(y, p, x=x, method='nelder')
		result = mod.fit(y, p, x=x)

		if showPlots:
			plt.plot(x, result.init_fit, 'k--')
			plt.plot(x, result.best_fit, 'r-')
			plt.plot(x, y, '.')
			plt.show()
		return result

	mod =  Model(sin)
	fitparams = []
	    

	for i in range(np.shape(data['x'])[0]):
	    fit = fitSinData(data['delay'], data['x'][i,:], p)
            valuesdict = fit.params.valuesdict() 
            valuesdict['amp_stderr'] = fit.params['amp'].stderr
            valuesdict['phase_stderr'] = fit.params['phase'].stderr
	    fitparams.append( valuesdict )
	    p = fit.params

	data['amp'] = np.array([g['amp'] for  g in fitparams])
	data['phase'] = np.array([g['phase'] for  g in fitparams])
        data['amp_stderr'] = np.array([g['amp_stderr'] for  g in fitparams])
        data['phase_stderr'] = np.array([g['phase_stderr'] for  g in fitparams])

	#return data





