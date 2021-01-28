def MH():
    fields = dnp.arange(20, 5, -5).tolist()
    fields = fields + dnp.arange(5, -5, -0.1).tolist()
    fields = fields + dnp.arange(-5, -20, -5).tolist()
    fields = tuple(fields)
    scan vmag fields refl 0.1
    scan vmag fields[::-1] refl 0.1
    pos vmag 0

pos pol pc

vmag.setAngle(35,90)
pos energy 707.3 #Fe
MH() 
pos energy 778.2 #Co
MH()
pos energy 852.2 #Ni
MH()
