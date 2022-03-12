import numpy as np

import pyk2

x_from_file = np.loadtxt('./rcx.dump')

pyk2.pyk2_init()
pyk2.pyk2(x_particles=x_from_file)
