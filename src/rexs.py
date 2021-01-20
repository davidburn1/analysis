import numpy as np
import h5py
from PIL import Image

#from ascii_data import loadI10Data

#import matplotlib.pyplot as plt

def qgrid(E, cth, center_x=0, center_y=0):
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

    px = (np.arange(2048)-1024+(center_x))  #  pixels
    py = (np.arange(2048)-1024+(center_y)) #  pixels
    
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













def phaseDiagram_tiff2hdf_fieldScan(directory, temperatures, fields, scanIDs, bins=4):
    """
    convert a phase diagram script into a single hdf file
    Assume the cth and ctth angles stays constant
    Field scans at constant temperatures
    """

    grid = np.zeros((len(temperatures), len(fields), 2048//bins, 2048//bins))


    for i in range(len(scanIDs)):
        print(i, scanIDs[i], temperatures[i])
        f = h5py.File(directory + 'i10-%06d.nxs' % scanIDs[i],'r')  
        cth = f['entry1']['before_scan']['cth']['cth'][()]
        energy = f['entry1']['before_scan']['pgm_energy']['pgm_energy'][()]
        image_fns = f['entry1']['instrument']['pimtetiff']['data_file']['file_name'][()]
        #print image_fns
        f.close()
	    #data = loadI10Data(directory + 'i10-%06d.dat' % s)
	    #cth = 90 - float(data['metadata']['th'] )
	    #energy = float(data['metadata']['pgm_energy'])
	    #image_fns = [directory + "%06d-pimte-files/%05d.tif" % (s, int(x)) for x in data['path']]

	    
        QX,QY = qgrid(energy, cth, center_x=0, center_y=0)
        QX = QX.reshape(2048//bins, bins, 2048//bins, bins).mean(1).mean(2)
        QY = QY.reshape(2048//bins, bins, 2048//bins, bins).mean(1).mean(2)


        for j,fn in enumerate(image_fns):
            im = np.array(Image.open(fn))
            im = im.reshape(2048//bins, bins, 2048//bins, bins).mean(1).mean(2)
            grid[i,j,:,:] = im
            del im


            #plt.pcolormesh(QX,QY, grid[i,j,:,:], cmap='gist_ncar_r', vmin=250, vmax=3000)
            #plt.show()

	    

    return QX, QY, grid





def phaseDiagram_tiff2hdf_temperatureScan(directory, temperatures, fields, scanIDs, bins=4):
    """
    convert a phase diagram script into a single hdf file
    Assume the cth and ctth angles stays constant

    interpolate the id numbers for the temperature id and read the closest image to the regular grid temperature
    """

    grid = np.zeros((len(temperatures), len(fields), 2048//bins, 2048//bins))


    for i in range(len(scanIDs)):
        print(i, scanIDs[i], fields[i])
        f = h5py.File(directory + 'i10-%06d.nxs' % scanIDs[i], 'r')
        cth = f['entry1']['before_scan']['cth']['cth'][()]
        energy = f['entry1']['before_scan']['pgm_energy']['pgm_energy'][()]
        image_fns = f['entry1']['instrument']['pimtetiff']['data_file']['file_name'][()]
        temperatures_raw = f['entry1']['instrument']['temperature']['sample'][()]
        f.close()
        #data = loadI10Data(directory + 'i10-%06d.dat' % s)
        #cth = 90 - float(data['metadata']['th'] )
        #energy = float(data['metadata']['pgm_energy'])
        #image_fns = [directory + "%06d-pimte-files/%05d.tif" % (s, int(x)) for x in data['path']]
        #temperatures_raw = data['Channel1Temp']

	    
        QX,QY = qgrid(energy, cth, center_x=0, center_y=0)
        QX = QX.reshape(2048//bins, bins, 2048//bins, bins).mean(1).mean(2)
        QY = QY.reshape(2048//bins, bins, 2048//bins, bins).mean(1).mean(2)


        argsort = np.argsort(temperatures_raw)
        temperatures_raw = temperatures_raw[argsort]
        image_fns = np.array(image_fns)[argsort]

        # find the id of the image which has the closest temperature to the regular grid temperatures
        idmap =  np.interp(temperatures, temperatures_raw, np.arange(len(temperatures_raw)))
        idmap = np.round(idmap).astype(int)

        for j,fn in enumerate(idmap):
            #print j, fn
            im = np.array(Image.open(image_fns[fn]))
            im = im.reshape(2048//bins, bins, 2048//bins, bins).mean(1).mean(2)
            grid[j,i,:,:] = im
            del im

        
      
    return QX, QY, grid





