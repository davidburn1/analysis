import numpy as np
import h5py
from PIL import Image

import matplotlib.pyplot as plt

def qgrid(E, cth, center_x=1024, center_y=1024):
    """
    Energy E in eV
    returns q in 1/nm
    cth = theta of sample

    Qx = E/(hbar*c) * (np.cos(th_f)*np.cos(phi) - np.cos(th_i)) * 1e-9 
    Qy = E/(hbar*c) * (np.cos(th_f)*np.sin(phi)) * 1e-9 
    Qz = E/(hbar*c) * (np.sin(th_f) + np.sin(th_i)) * 1e-9 

	q = 2 E / 1243.125 sin(th) # for reflectivity in units of 1/nm
    """
    
    det_distance = 130e-3 # 130 mm for pimte
    px_size = 13.5e-6

    px = (np.arange(2048)-1024+(1024-center_x))  #  pixels
    py = (np.arange(2048)-1024+(1024-center_y)) #  pixels
    #PX, PY = np.meshgrid(px,py)
    
    """ scattering angles where the beam exits from the sample """
    phi = np.arctan2(px * px_size , det_distance) # scattering angle phi
    th  = np.arctan2(py * px_size , det_distance)
    
    PHI, TH = np.meshgrid(phi,th)
    


    th_i = np.radians(cth)
    TH_F = th_i + TH

    #E = E * 1.6E-19 
    #hbar = 6.62e-34 / (2.0 * np.pi)
    #c = 3.0e8
    """ convert scattering angles into Q """
    #qy = E/(hbar*c) * (np.sin(PHI) ) * 1e-9   
    #qx = E/(hbar*c) * (np.sin(TH) ) * 1e-9 
    qx = 2*E/1243 * (np.cos(TH_F)*np.cos(PHI) - np.cos(th_i))  
    qy = 2*E/1243 * (np.cos(TH_F)*np.sin(PHI))

    return [qy, qx]













def phaseDiagram_tiff2hdf_fieldScan(directory, temperatures, fields, scanIDs):
    """
    convert a phase diagram script into a single hdf file
    Assume the cth and ctth angles stays constant
    """

    bins = 4
    grid = np.zeros((len(temperatures), len(fields), 2048//bins, 2048//bins))


    for i,s in enumerate(scanIDs):
	    print i, s
	    f = h5py.File(directory + 'i10-%06d.nxs' % s,'r')
	    cth = f['entry1']['before_scan']['cth']['cth'][()]
	    energy = f['entry1']['before_scan']['pgm_energy']['pgm_energy'][()]
	    #ff = f['entry1']['instrument']['field']['field'][:]
	    image_fns = f['entry1']['instrument']['pimtetiff']['data_file']['file_name']#[()]
	    
	    QX,QY = qgrid(energy, cth)
	    QX = QX.reshape(2048//bins, bins, 2048//bins, bins).mean(1).mean(2)
	    QY = QY.reshape(2048//bins, bins, 2048//bins, bins).mean(1).mean(2)


	    for j,fn in enumerate(image_fns):
		    im = np.array(Image.open(fn))
		    im = im.reshape(2048//bins, bins, 2048//bins, bins).mean(1).mean(2)
		    grid[i,j,:,:] = im
		    del im


            plt.pcolormesh(QX,QY, grid[i,j,:,:], cmap='gist_ncar_r', vmin=250, vmax=3000)
            plt.show()

	    f.close()

    return QX, QY, grid





def phaseDiagram_tiff2hdf_temperatureScans(directory, temperatures, fields, scanIDs):
    """
    convert a phase diagram script into a single hdf file
    Assume the cth and ctth angles stays constant

    interpolate the id numbers for the temperature id and read the closest image to the regular grid temperature
    """

    bins = 4
    grid = np.zeros((len(temperatures), len(fields), 2048//bins, 2048//bins))


    for i,s in enumerate(scanIDs):
        print i, s
        f = h5py.File(directory + 'i10-%06d.nxs' % s,'r')
        cth = f['entry1']['before_scan']['cth']['cth'][()]
        energy = f['entry1']['before_scan']['pgm_energy']['pgm_energy'][()]
        #ff = f['entry1']['instrument']['field']['field'][:]
        image_fns = f['entry1']['instrument']['pimtetiff']['data_file']['file_name'][()]
        temperatures_raw = f['entry1']['instrument']['temperature']['sample'][()]
	    
        QX,QY = qgrid(energy, cth)
        QX = QX.reshape(2048//bins, bins, 2048//bins, bins).mean(1).mean(2)
        QY = QY.reshape(2048//bins, bins, 2048//bins, bins).mean(1).mean(2)


        argsort = np.argsort(temperatures_raw)
        temperatures_raw = temperatures_raw[argsort]
        image_fns = image_fns[argsort]

        idmap =  np.interp(temperatures, temperatures_raw, np.arange(len(temperatures_raw)))
        idmap = np.round(idmap).astype(int)

        for j,fn in enumerate(idmap):
            #print j, fn
            im = np.array(Image.open(image_fns[fn]))
            im = im.reshape(2048//bins, bins, 2048//bins, bins).mean(1).mean(2)
            grid[j,i,:,:] = im
            del im

        f.close()
      
    return QX, QY, grid





