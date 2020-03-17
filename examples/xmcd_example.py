# -*- coding: utf-8 -*-
"""

"""

import matplotlib.pyplot as plt
import numpy as np


import sys
sys.path.append('../')

from xmcd import loadXMCD, plotXMCD


directory = "/dls/i10/data/2019/mm23338-1/data"

#%%


#Fe
data = loadXMCD(directory, [585444], [585445] )
plotXMCD(data['energy'], data['m17']['a'], data['m17']['b'])

print data['m17']['min']

#%%


#Co
data = loadXMCD(directory, [585446], [585447] )
plotXMCD(data['energy'], data['m17']['a'], data['m17']['b'])

print data['m17']['min']


#%%


#Ni
data = loadXMCD(directory, [585448], [585449] )
plotXMCD(data['energy'], data['m17']['a'], data['m17']['b'])

print data['m17']['min']