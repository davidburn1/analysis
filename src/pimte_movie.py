"""
module load ffmpeg is needed
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib import animation


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

	q = 2 E / 1243.125 sin(th) # for reflectivity in units of 1/nm
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

    #E = E * 1.6E-19 
    #hbar = 6.62e-34 / (2.0 * np.pi)
    #c = 3.0e8
    """ convert scattering angles into Q """
    #qy = E/(hbar*c) * (np.sin(PHI) ) * 1e-9   
    #qx = E/(hbar*c) * (np.sin(TH) ) * 1e-9 
    qx = 2*E/1243 * (np.cos(TH_F)*np.cos(PHI) - np.cos(th_i))  
    qy = 2*E/1243 * (np.cos(TH_F)*np.sin(PHI))

    return [qy, qx]





directory = "/dls/i10/data/2019/mm21868-1/"


if (len(sys.argv) == 2):
	scanID = int(sys.argv[1])
else:
	print "enter the scan id"




f = h5py.File(directory + 'i10-%06d.nxs' % scanID,'r')
cth = f['entry1']['before_scan']['cth']['cth'][()]
energy = f['entry1']['before_scan']['pgm_energy']['pgm_energy'][()]

fields = f['entry1']['instrument']['field']['field'][:]
#print f['entry1']['instrument']['pimtetiff'].keys()
images = f['entry1']['instrument']['pimtetiff']['data_file']['file_name'][()]
f.close()






Writer = animation.writers['ffmpeg']
writer = Writer(fps=14, bitrate=1800)


X,Y = qgrid(energy, cth)


fig, ax = plt.subplots(1, 1, figsize=(6,4), facecolor='w')
ax.set_aspect('equal', 'box')
label = plt.text(0.99,0.99,"", ha='right', va='top', transform=ax.transAxes)

a = None

def animate(i):
	print '{0}\r'.format(i)
	global a
	if a is not None: a.remove()
	im = np.array(Image.open(images[i]))
	a = plt.pcolormesh(X,Y, im, cmap='gist_ncar_r', vmin=100, vmax=1000)
	label.set_text("%0.1f mT" % fields[i])



anim = animation.FuncAnimation(fig, animate, frames=range(len(fields)), blit=False, save_count=0)
anim.save(directory + '/processing/movie-%06d.mp4' % scanID)




#plt.xlim(300,-300)
#plt.ylim(300,-300)
#plt.show()

