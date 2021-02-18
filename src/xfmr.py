import h5py
import numpy as np
from lmfit import minimize, Parameters, fit_report, Model
import matplotlib.pyplot as plt



def loadXFMRDelayScans(directory, scanIDs):
    """  """
    data = {}

    # read the first file to get the length of the scan and the delay values
    f = h5py.File(directory+"/i10-%06d.nxs" % scanIDs[0], 'r')
    grp = f['entry1']['instrument']
    data['delay'] = grp['delay']['delay'][:]
    f.close()

    data['scanID'] = np.array(scanIDs)
    data['field'] = np.zeros((len(scanIDs)))
    data['x'] = np.zeros((len(data['field']), len(data['delay'])))
    data['y'] = np.zeros((len(data['field']), len(data['delay'])))
    data['static'] = np.zeros((len(data['field']), len(data['delay'])))

    # Loop through all the scans in the list
    for i in range(len(scanIDs)):
        f = h5py.File(directory+"/i10-%06d.nxs" % scanIDs[i], 'r')
        data['field'][i] =  f['entry1']['before_scan']['vmag']['field'][()]

        grp = f['entry1']['instrument']
        data['static'][i,:] = grp['zurich']['static'][:]
        data['x'][i,:] = grp['zurich']['x'][:]  
        data['y'][i,:] = grp['zurich']['y'][:]

        f.close()

    # sort the data by field value
    argsort = np.argsort(data['field'])
    data['scanID'] = data['scanID'][argsort]
    data['field'] = data['field'][argsort]
    data['static'] = data['static'][argsort,:]
    data['x'] = data['x'][argsort,:]
    data['y'] = data['y'][argsort,:]


    # show error if one of the files does not have the correct length

    return data




def fitXFMR(data, params, showPlots=False, ignoreStart=0):

    def sin(x, amp, phase, freq, offset):
        return amp*np.sin(phase*np.pi/180.0 + x/1000.0*freq*2*np.pi) + offset

    mod =  Model(sin)
    fitparams = []
        
    for i in range(len(data['field'])):
        x = data['delay'][ignoreStart:]
        y = data['x'][i,ignoreStart:]
        fit = mod.fit(y, params, x=x, method='nelder')
        fit = mod.fit(y, fit.params, x=x)

        if showPlots:
            plt.plot(x, fit.init_fit, 'k--')
            plt.plot(x, fit.best_fit, 'r-')
            plt.plot(x, y, '.')
            plt.title(data['scanID'][i])
            plt.show()

        valuesdict = fit.params.valuesdict() 
        valuesdict['amp_stderr'] = fit.params['amp'].stderr
        valuesdict['phase_stderr'] = fit.params['phase'].stderr
        fitparams.append( valuesdict )
        params = fit.params

    data['amp'] = np.array([g['amp'] for  g in fitparams])
    data['phase'] = np.array([g['phase'] for  g in fitparams])
    data['freq'] = np.array([g['freq'] for  g in fitparams])
    data['offset'] = np.array([g['offset'] for  g in fitparams])

    data['amp_stderr'] = np.array([g['amp_stderr'] for  g in fitparams])
    data['phase_stderr'] = np.array([g['phase_stderr'] for  g in fitparams])




