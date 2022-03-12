import numpy as np

import pyk2

x_test = np.loadtxt("./rcx.dump")
xp_test = np.loadtxt("./rcxp.dump")
y_test = np.loadtxt("./rcy.dump")
yp_test = np.loadtxt("./rcyp.dump")
s_test = np.loadtxt("./rcs.dump")
p_test = np.loadtxt("./rcp.dump")

pyk2.pyk2_init()
pyk2.pyk2(x_particles=x_test,
          xp_particles=xp_test,
          y_particles=y_test,
          yp_particles=yp_test,
          s_particles=s_test,
          p_particles=p_test)

x_ref = np.loadtxt('./rcx.dump_after_REF')

assert np.allclose(x_test, x_ref, rtol=1e6, atol=0)


