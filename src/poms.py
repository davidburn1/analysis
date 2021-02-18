import numpy as np
import h5py
import matplotlib.pyplot as plt

def loadSampleAlignmentData(directory, scans):
    # Input a list of scans of user1_axis2 at different user1_axis1 positions
    # Returns a list of the refl intensity

    refl_out = np.array([])
    ax1_out = np.array([])
    ax2_out = np.array([])
    
    for i in range(len(scans)):
        f = h5py.File(directory+"/i10-%06d.nxs" % scans[i]  , 'r')
        refl_scan = f['entry1']['instrument']['refl']['refl'][:] 
        ax2_scan = f['entry1']['instrument']['user1_axis2']['user1_axis2'][:]
        ax1_scan = np.ones(len(refl_scan)) * f['entry1']['before_scan']['user1_axis1']['user1_axis1'][()] 
        f.close()

        refl_out = np.append(refl_out, refl_scan)
        ax1_out = np.append(ax1_out, ax1_scan)
        ax2_out = np.append(ax2_out, ax2_scan)

    return ax1_out, ax2_out, refl_out






def plotWaveguideAlignmentScans(directory, df):
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.5), facecolor='w', sharey=True)

    f = h5py.File(directory+"/i10-%06d.nxs" % df.a1ScanID, 'r')
    grp = f['entry1']['instrument']
    a1Energy = f['entry1']['before_scan']['pgm_energy']['pgm_energy'][()]
    refl = grp['refl']['refl'][:] #/ grp['macr16']['data'][:]
    axis = grp['user1_axis1']['user1_axis1'][()]
    f.close()
    a1MaxVal = np.max(refl)
    ax[0].plot(axis, refl)
    
    f = h5py.File(directory+"/i10-%06d.nxs" % df.a2ScanID, 'r')
    grp = f['entry1']['instrument']
    a2Energy = f['entry1']['before_scan']['pgm_energy']['pgm_energy'][()]
    refl = grp['refl']['refl'][:] #/ grp['macr16']['data'][:]
    axis = grp['user1_axis2']['user1_axis2'][()]
    f.close()
    a2MaxVal = np.max(refl)
    ax[1].plot(axis, refl)
    
    ax[0].axvline(df.a1Pos, color='r')
    ax[1].axvline(df.a2Pos, color='r')
    
    ax[0].text(0.95,0.95, "#%6d" % df.a1ScanID, ha="right", va="top", transform=ax[0].transAxes)
    ax[1].text(0.95,0.95, "#%6d" % df.a2ScanID, ha="right", va="top", transform=ax[1].transAxes)
    ax[0].text(0.95,0.85, "a1 = %2.2f" % df.a1Pos, ha="right", va="top", transform=ax[0].transAxes)
    ax[1].text(0.95,0.85, "a2 = %2.2f" % df.a2Pos, ha="right", va="top", transform=ax[1].transAxes)
    
    ax[0].text(0.05,0.95, "%2.2g A" % a1MaxVal, ha="left", va="top", transform=ax[0].transAxes)
    ax[1].text(0.05,0.95, "%2.2g A" % a2MaxVal, ha="left", va="top", transform=ax[1].transAxes)
    ax[0].text(0.05,0.85, "%4.1f eV" % a1Energy, ha="left", va="top", transform=ax[0].transAxes)
    ax[1].text(0.05,0.85, "%4.1f eV" % a2Energy, ha="left", va="top", transform=ax[1].transAxes)

        
    ax[0].set_xlabel("Axis 1 (mm)")
    ax[1].set_xlabel("Axis 2 (mm)")
    ax[0].set_ylabel("Intensity (A)")
    plt.subplots_adjust(hspace=0.1, wspace=0.1)
    
    plt.show()
