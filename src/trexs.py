import numpy as np
import h5py
from PIL import Image



from rexs import qgrid


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
        image_fns = f['entry1']['instrument']['pixistiff']['data_file']['file_name'][()]
        #print image_fns
        f.close()
	    #data = loadI10Data(directory + 'i10-%06d.dat' % s)
	    #cth = 90 - float(data['metadata']['th'] )
	    #energy = float(data['metadata']['pgm_energy'])
	    #image_fns = [directory + "%06d-pimte-files/%05d.tif" % (s, int(x)) for x in data['path']]

	    
        QX,QY = qgrid(energy, 90, center_x=0, center_y=0)
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




