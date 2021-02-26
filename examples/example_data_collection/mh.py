def MH():
    fields = dnp.arange(20, 5, -5).tolist()
    fields = fields + dnp.arange(5, -5, -0.1).tolist()
    fields = fields + dnp.arange(-5, -21, -5).tolist()
    pos vmag fields[0]; time.sleep(2)
    scan vmag tuple(dnp.array(fields)) refl 0.1
    scan vmag tuple(-dnp.array(fields)) refl 0.1
    pos vmag 0

pos pol pc

vmag.setAngle(35,90)
pos energy 707.3 #Fe
MH() 
pos energy 778.2 #Co
MH()
pos energy 852.2 #Ni
MH()
