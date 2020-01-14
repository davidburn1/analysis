import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
import sys
import h5py




	

def qgrid(E, cth):
    """
    Energy E in eV
    q in 1/AA
    cth = theta of sample

    Qx = E/(hbar*c) * (np.cos(th_f)*np.cos(phi) - np.cos(th_i)) * 1e-9 
    Qy = E/(hbar*c) * (np.cos(th_f)*np.sin(phi)) * 1e-9 
    Qz = E/(hbar*c) * (np.sin(th_f) + np.sin(th_i)) * 1e-9 
    """
    
    det_distance = 130e-3 # 130 mm for pimte
    px_size = 13.5e-6

    px = (np.arange(2048)-1024) + 0 #  pixels
    py = (np.arange(2048)-1024) + 0 #  pixels
    #PX, PY = np.meshgrid(px,py)
    
    """ scattering angles where the beam exits from the sample """
    phi = np.arctan2(px * px_size , det_distance) # scattering angle phi
    th  = np.arctan2(py * px_size , det_distance)
    
    PHI, TH = np.meshgrid(phi,th)
    


    th_i = np.radians(cth)
    TH_F = th_i + TH

    E = E * 1.6E-19 
    hbar = 6.62e-34 / (2.0 * np.pi)
    c = 3.0e8
    """ convert scattering angles into Q """
    #qy = E/(hbar*c) * (np.sin(PHI) ) * 1e-9   
    #qx = E/(hbar*c) * (np.sin(TH) ) * 1e-9 
    qx = E/(hbar*c) * (np.cos(TH_F)*np.cos(PHI) - np.cos(th_i)) * 1e-9 
    qy = E/(hbar*c) * (np.cos(TH_F)*np.sin(PHI)) * 1e-9 

    return [qy, qx]





directory = "/dls/i10/data/2019/mm21868-1/"


if (len(sys.argv) == 2):
	id1 = int(sys.argv[1])
	id2 = id1 + 1 
elif (len(sys.argv) == 3):
	id1 = int(sys.argv[1])
	id2 = int(sys.argv[2])
else:
	print "enter the scan numbers"

#f = h5py.File(directory + 'i10-%06d.nxs' % id1,'r')
#print f['entry1']['before_scan']['cth'].keys()
#f.close()

im1 = np.array(Image.open(directory+ "%06d-pimte-files/pimte-00000.tiff" % id1)) 
im2 = np.array(Image.open(directory+ "%06d-pimte-files/pimte-00000.tiff" % id2)) 
diff = (im1.astype(np.int16)-im2.astype(np.int16))
# wraps around to 65536 for -ve numbers


im = Image.fromarray(im1-im2)
im.save(directory + "/processing/%06d-%06d.tiff" % (id1, id2), "tiff")




#from matplotlib import cm
#diff = diff + np.min(diff)
#diff = diff / np.max(diff)

#cm_hot = cm.get_cmap('hot')

#im =  np.uint8(cm.gist_earth(diff)*255)
#print diff
#im = cm.hot(diff)
#im = np.uint8(im*255)

#print im

#print im
#cm_hot = cm.get_cmap('hot')
#diff = diff.convert('L')

#im = cm_hot(im)
#print im
#im = np.uint16(im)
##print im
#im = Image.fromarray(im)
#im.save(directory + "/processing/%06d-%06d_cmap.jpg" % (id1, id2), "jpeg")

zmax=200

#X,Y = np.meshgrid(np.arange(2048)-1024, np.arange(2048)-1024)

X,Y = qgrid(778.8, 30)

fig, ax = plt.subplots(1, 1)

# bwr, terrain
plt.pcolormesh(X,Y, diff, cmap="RdYlBu_r", vmax=zmax, vmin=-zmax)
plt.colorbar()
#ax.set_aspect('equal', 'box')

#plt.xlim(300,-300)
#plt.ylim(300,-300)
plt.show()

#print directory



