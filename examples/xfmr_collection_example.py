

def xfmrScanUp8():
    sendEmail("starting xfmr scan 8 GHz")
    vmag.setAngle(0,0)
    pos vmag -500; time.sleep(5)
    
    fields = range(-200, -80, 5) + range(-80, 80, 20) + range(80, 200, 5) 
    for hh in fields:
        pos vmag(hh)
        ascan delay 0 250 25 xfmr 1
