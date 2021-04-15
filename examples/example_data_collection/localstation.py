""" Energy calibration """
#run("0_IMPORTANT/newfescanidu.py")
run("0_IMPORTANT/newfescaniduRASOR.py")


run("beamline/poms/send_email.py")

""" run fast scan """
run("beamline/poms/scannables/flyingScan.py")
#from beamline.poms.scannables.flyingScan import fscan
#alias("fscan");


""" load SR current amplifiers  """
from David.scannables.sr570Scannable import sr570Scannable
reflGain = sr570Scannable("I", "SER1")
fluoGain = sr570Scannable("I", "SER2")

""" auto gain detectors """ 
from David.scannables.autoGainDetector import autoGainDetector
fluo  = autoGainDetector("fluo", macr18, fluoGain)
refl  = autoGainDetector("refl", macr17, reflGain)
reflf = autoGainDetector("refl", macr17, reflGain)
reflf.minCPS = 0

""" background M1 position correction check """
run("beamline/common/M1_Check.py")
start_m1_check()

""" I0 """
#from poms.scannables.fixedGainDetector import fixedGainDetector
#i0 = fixedGainDetector("i0", macr16, 1e7) #v/A

"""##########"""
"""   RASOR   """
"""##########"""

""" Temperature control """
##from David.scannables.rasor.rasorTemperatureScannable import rasorTemperatureScannable
#r#asorTemp = rasorTemperatureScannable("temperature")

""" hkl scannables """
#from David.scannables.rasor.lScannable import lScannable
#ll = lScannable( pgm_energy, tth, th)

""" eggcup magnet calibrated scannable """
#from David.scannables.rasor.eggcupMagnetsScannable import eggcupMagnetsScannable
#field = eggcupMagnetsScannable(emecy1, emecy2, [28.58, 9.06, 3.66]) # small magnets
#field = eggcupMagnetsScannable(emecy1, emecy2, [184.0, 7.97, 18.5]) # big magnets - Nov 2018
#meta_add(field)

#from David.scannables.rasor.kepcoScannable import kepcoScannable
#kepco = kepcoScannable(ui1ao2)


""" ccd offset motor scannables """
#from David.scannables.rasor.ccd import ccdOffsetScannable, px2chi, pimteShOpen, pimteShClose
#ctth = ccdOffsetScannable('ctth', tth, 90+0.44) #fixed offset on the detector arm - does not change
#cth = ccdOffsetScannable('cth', th, 180)
#meta_add(cth, ctth)

""" background tth motor check """
#from beamline.rasor import tthCheck, thCheck
#tthCheck.start_tth_check()
#thCheck.start_th_check()

""" Checkbeam """
checktopup_time.minimumThreshold=1
checktopup_time.secondsToWaitAfterBeamBackUp = 2
add_default(checkbeam)









"""##########"""
"""   POMS   """
"""##########"""
run("beamline/poms/functions.py")

""" vmag scannable """
from poms.scannables.vmagScannable import vmagScannable
vmag = vmagScannable('vmag', hostName='172.23.110.103', hostPort=4042)
meta_add(vmag)

""" Temperature control """
from poms.scannables.pomsTemperatureScannable import pomsTemperatureScannable
pomsTemp = pomsTemperatureScannable("temperature")
meta_add(pomsTemp)



"""##########"""
"""   CCD    """
"""##########"""

#pimteSum = DisplayEpicsPVClass('pimteSum', 'BL10I-EA-PIMTE-01:STAT:Total_RBV', 'counts', '%d')
#pixisSum = DisplayEpicsPVClass('pixisSum', 'BL10I-EA-PIXIS-01:STAT:Total_RBV', 'counts', '%d')

"""##########"""
""" Dynamics """
"""##########"""

""" Colby delay line scannable """
from poms.scannables.colbyDelayLineScannable import colbyDelayLineScannable
delay = colbyDelayLineScannable('delay', "172.23.110.129")
meta_add(delay)

""" XFMR detector """
#from beamline.poms.scannables.zurichXFMRDetector import socketDevice, zurichRangeScannable, zurichDetector
run("beamline/poms/scannables/zurichXFMRDetector.py")
zursoc = socketDevice(host='DIAMRD3079.dc.diamond.ac.uk', port=10000)
zurRange = zurichRangeScannable(zursoc)
xfmr = zurichDetector(zursoc)
meta_add(zurRange)




""" set rasor metadata """
#meta_add(pgm_energy, th, tth, chi, thp, ttp, eta, sx, sy, sz, dsu, dsd, th_off, tth_off, emecy1, emecy2, emecpitch,pinhx, pinhy)
meta_add(s4xsize, s4ysize,)
add_default(macr16)

""" poms metadata """
meta_add(user1_axis1, user1_axis2, user1_axis3)


""" change data save folder """
import os
from gda.jython import InterfaceProvider
cwd = InterfaceProvider.getPathConstructor().createFromDefaultProperty()
if (cwd.split("/")[-1] != "data"):
    setSubdirectory("data")


scan_processing_on()

print ""
print "finished running user localstation"

