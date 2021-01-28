

zursoc.query("daq.setDouble('/dev4206/demods/0/timeconstant', 4.01688583)")  # 20 mHz bandwidth
zursoc.query("daq.setDouble('/dev4206/demods/0/rate', 20)") # set data transfer rate 20 S/s

pos energy 778.2 #Co
for hh in dnp.arange(0, 50.1, 2):
    pos vmag(hh)
    ascan delay 0 600 55 xfmr 5 
