import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
import sys
import h5py




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



