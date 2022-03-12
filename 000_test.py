import numpy as np

import pyk2

x_test = np.loadtxt('./rcx.dump')

pyk2.pyk2_init()
pyk2.pyk2(x_particles=x_test)

x_ref = np.loadtxt('./rcx.dump_after_REF')

assert np.allclose(x_test, x_ref, rtol=1e6, atol=0)


