

xfmr.setTimeConstant(4.01688583)# 20 mHz bandwidth
xfmr.setDataRate(20) # 20 S/s

pos energy 778.2 #Co
for hh in dnp.arange(0, 50.1, 2):
    pos vmag(hh)
    ascan delay 0 600 55 xfmr 5 
