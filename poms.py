def loadSampleAlignmentData(scans):
    # Input a list of scans of user1_axis2 at different user1_axis1 positions
    # Returns a list of the refl intensity

    refl_out = np.array([])
    ax1_out = np.array([])
    ax2_out = np.array([])
    
    for i in range(len(scans)):
        f = h5py.File(directory+"/i10-%06d.nxs" % scans[i]  , 'r')
        refl_scan = f['entry1']['instrument']['refl']['refl'][:] 
        ax2_scan = f['entry1']['instrument']['user1_axis2']['user1_axis2'][:]
        ax1_scan = np.ones(len(refl)) * f['entry1']['before_scan']['user1_axis1']['user1_axis1'][()] 
        f.close()

        refl_out = np.append(refl_out, refl_scan)
        ax1_out = np.append(ax1_out, ax1_scan)
        ax2_out = np.append(ax2_out, ax2_scan)

    return ax1_out, ax2_out, refl_out